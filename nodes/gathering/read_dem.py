import os
from pathlib import Path
import numpy as np

import bpy
from bpy.props import BoolProperty
from sverchok.node_tree import SverchCustomTreeNode
from sverchok.data_structure import updateNode

# Optional backends (pure-Python or lightweight native)
try:
    from megapolis.dependencies import tifffile as tiff
except Exception:
    tiff = None

try:
    from megapolis.dependencies import pyvips as pyvips
except Exception:
    pyvips = None

import PIL as PILpkg
from PIL import Image


# ---------------------------
# Utilities
# ---------------------------

def _faces_from_wh(width: int, height: int):
    faces = []
    for r in range(height - 1):
        base = r * width
        next_row = (r + 1) * width
        for c in range(width - 1):
            v0 = base + c
            v1 = base + c + 1
            v2 = next_row + c + 1
            v3 = next_row + c
            faces.append([v0, v1, v2, v3])
    return faces


def _affine_from_geotiff_tags(tags):
    """
    Build 2D affine transform from GeoTIFF tags.
    Returns (Axx, Axy, Ax0, Ayx, Ayy, Ay0) such that:
        X = Ax0 + Axx * col + Axy * row
        Y = Ay0 + Ayx * col + Ayy * row
    Priority:
      1) ModelTransformationTag (34264) 4x4
      2) ModelTiepoint (33922) + ModelPixelScale (33550)
      3) None -> pixel coords
    """
    mt = tags.get(34264) or tags.get('ModelTransformationTag') or tags.get('ModelTransformation')
    if mt is not None:
        M = np.array(mt, dtype=float).reshape(4, 4)
        Axx, Axy, Ax0 = M[0, 0], M[0, 1], M[0, 3]
        Ayx, Ayy, Ay0 = M[1, 0], M[1, 1], M[1, 3]
        return Axx, Axy, Ax0, Ayx, Ayy, Ay0

    mps = tags.get(33550) or tags.get('ModelPixelScaleTag') or tags.get('ModelPixelScale')
    mtp = tags.get(33922) or tags.get('ModelTiepointTag') or tags.get('ModelTiepoint')
    if mps is not None and mtp is not None:
        sx, sy = float(mps[0]), float(mps[1])
        tp = np.array(mtp, dtype=float)
        if tp.size >= 6:
            i0, j0, k0, X0, Y0, Z0 = tp[:6]
            # Common north-up convention: Y decreases with row
            Ax0 = X0 - sx * j0
            Ay0 = Y0 + sy * i0
            Axx, Axy = sx, 0.0
            Ayx, Ayy = 0.0, -sy
            return Axx, Axy, Ax0, Ayx, Ayy, Ay0

    # pixel coords fallback
    return 1.0, 0.0, 0.0, 0.0, -1.0, 0.0


def _read_geotiff_tifffile(path: str):
    with tiff.TiffFile(path) as tf:
        page = tf.pages[0]
        arr = page.asarray()
        if arr.ndim > 2:
            arr = arr.squeeze()
        arr = arr.astype('float64')
        h, w = arr.shape
        tags = {}
        for ti in page.tags.values():
            tags[ti.name] = ti.value
            code = getattr(ti, 'code', None)
            if code is not None:
                tags[code] = ti.value
        A = _affine_from_geotiff_tags(tags)
        return arr, w, h, A, tags


def _read_geotiff_pyvips(path: str):
    img = pyvips.Image.new_from_file(path, access='sequential')
    w, h = img.width, img.height
    if img.bands > 1:
        img = img.extract_band(0)
    arr = np.ndarray(buffer=img.write_to_memory(), dtype=np.float32, shape=[h, w]).astype('float64')
    tags = {}
    for k in ("tiff-modeltiepoint", "tiff-modelpixelscale", "tiff-modeltransformation"):
        try:
            tags[k] = img.get(k)
        except Exception:
            pass
    if "tiff-modelpixelscale" in tags:
        tags[33550] = list(map(float, tags["tiff-modelpixelscale"]))
    if "tiff-modeltiepoint" in tags:
        tags[33922] = list(map(float, tags["tiff-modeltiepoint"]))
    if "tiff-modeltransformation" in tags:
        tags[34264] = list(map(float, tags["tiff-modeltransformation"]))
    A = _affine_from_geotiff_tags(tags)
    return arr, w, h, A, tags


def _read_geotiff_pillow(path: str):
    if Image is None:
        raise RuntimeError("Pillow not available")
    im = Image.open(path).convert('F')
    arr = np.array(im, dtype='float64')
    h, w = arr.shape
    # no geotags—pixel coords with Y down (flip sign to keep Y up)
    A = (1.0, 0.0, 0.0, 0.0, -1.0, 0.0)
    tags = {}
    return arr, w, h, A, tags


def _read_geotiff(path: str):
    if tiff is not None:
        try:
            return _read_geotiff_tifffile(path)
        except Exception:
            pass
    if pyvips is not None:
        try:
            return _read_geotiff_pyvips(path)
        except Exception:
            pass
    return _read_geotiff_pillow(path)


def _read_esri_ascii(path: str):
    """
    ESRI ASCII Grid (.asc/.txt). Header example:
      ncols         1201
      nrows         1201
      xllcorner     500000
      yllcorner     4100000
      cellsize      30
      NODATA_value  -9999
    or center variants: xllcenter/yllcenter
    Returns (arr, width, height, affine6, nodata)
    """
    header_keys = {"ncols", "nrows", "xllcorner", "yllcorner", "xllcenter", "yllcenter",
                   "cellsize", "NODATA_value", "nodata_value"}
    meta = {}
    data_start = 0
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        lines = f.readlines()

    # parse header
    for i, line in enumerate(lines[:20]):  # header is usually first ~6 lines
        parts = line.strip().split()
        if not parts:
            continue
        key = parts[0].lower()
        if key in {k.lower() for k in header_keys} and len(parts) >= 2:
            try:
                meta[key] = float(parts[1]) if key != "ncols" and key != "nrows" else int(float(parts[1]))
            except Exception:
                pass
        # detect end of header when a line starts with a number list
        if key not in {k.lower() for k in header_keys}:
            # likely first data line
            data_start = i
            break

    ncols = int(meta.get("ncols"))
    nrows = int(meta.get("nrows"))
    cellsize = float(meta.get("cellsize"))
    nodata = meta.get("nodata_value")
    if nodata is None:
        nodata = meta.get("NODATA_value")
    if nodata is None:
        nodata = np.nan
    else:
        nodata = float(nodata)

    # origin (corner vs center)
    if "xllcorner" in meta and "yllcorner" in meta:
        x0 = float(meta["xllcorner"])
        y0 = float(meta["yllcorner"])
        # data rows go top→bottom in file? ESRI ASCII typically lists rows from top to bottom (north->south).
        # We'll read and flip so row 0 is north/top.
        # Affine with Y decreasing per row to keep "Y up" in world coords:
        Axx, Axy, Ax0 = cellsize, 0.0, x0
        Ayx, Ayy, Ay0 = 0.0, -cellsize, y0 + nrows * cellsize
    else:
        # center-based origin
        x0 = float(meta["xllcenter"])
        y0 = float(meta["yllcenter"])
        Ax0 = x0 - 0.5 * cellsize
        Ay0 = y0 + (nrows - 0.5) * cellsize
        Axx, Axy = cellsize, 0.0
        Ayx, Ayy = 0.0, -cellsize

    # read data
    data_lines = lines[data_start:]
    # robust parse: split and accumulate until we have nrows*ncols values
    values = []
    for ln in data_lines:
        vals = ln.strip().split()
        if not vals:
            continue
        values.extend(vals)
        if len(values) >= nrows * ncols:
            break
    arr = np.array(values[: nrows * ncols], dtype=np.float64).reshape(nrows, ncols)
    # ESRI ASCII typically top row is north; our affine uses decreasing Y per row already
    return arr, ncols, nrows, (Axx, Axy, Ax0, Ayx, Ayy, Ay0), nodata


def _read_npy(path: str):
    arr = np.load(path).astype('float64')
    if arr.ndim != 2:
        # try to squeeze band/extra dims
        arr = np.squeeze(arr)
        if arr.ndim != 2:
            raise RuntimeError("NPY must be 2D for DEM")
    h, w = arr.shape
    # pixel coords, Y up (negative per row)
    A = (1.0, 0.0, 0.0, 0.0, -1.0, float(h - 1))
    return arr, w, h, A, np.nan


def _read_npz(path: str):
    z = np.load(path)
    # try common keys
    for key in ("dem", "elevation", "z", "arr", "band1"):
        if key in z.files:
            arr = z[key]
            break
    else:
        # first array
        arr = z[z.files[0]]
    arr = np.array(arr, dtype='float64')
    if arr.ndim != 2:
        arr = np.squeeze(arr)
        if arr.ndim != 2:
            raise RuntimeError("NPZ array must be 2D for DEM")
    h, w = arr.shape
    A = (1.0, 0.0, 0.0, 0.0, -1.0, float(h - 1))
    return arr, w, h, A, np.nan


def _read_any(path: str):
    ext = Path(path).suffix.lower()
    if ext in (".tif", ".tiff"):
        return _read_geotiff(path)
    if ext in (".asc", ".txt", ".grd"):
        return _read_esri_ascii(path)
    if ext == ".npy":
        return _read_npy(path)
    if ext == ".npz":
        return _read_npz(path)
    # last-chance: try GeoTIFF readers anyway
    return _read_geotiff(path)


def _mask_faces_for_nodata(Z, faces, nodata):
    """Drop faces that touch any NODATA vertex, return filtered faces and a vertex mask."""
    if np.isnan(nodata):
        bad = np.isnan(Z)
    else:
        bad = (Z == nodata)
    h, w = Z.shape
    bad_flat = bad.reshape(-1)
    keep = []
    for f in faces:
        if not (bad_flat[f[0]] or bad_flat[f[1]] or bad_flat[f[2]] or bad_flat[f[3]]):
            keep.append(f)
    return keep


# ---------------------------
# Sverchok Node
# ---------------------------

class SvMegapolisReadDem(SverchCustomTreeNode, bpy.types.Node):
    """
    Triggers: Read DEM (GeoTIFF / ESRI ASCII / NPY / NPZ)
    Tooltip: Read a DEM without GDAL/Rasterio; builds XYZ vertices in map/pixel units and quad faces.
    """
    bl_idname = 'SvMegapolisReadDem'
    bl_label = 'Read DEM (GeoTIFF/ASC/NPY/NPZ)'
    bl_icon = 'MESH_DATA'
    sv_dependencies = {'tifffile'}  # optionally 'pyvips', 'Pillow'

    zero_min: BoolProperty(
        name="Zero min Z",
        description="Subtract minimum elevation so the lowest point is Z=0",
        default=False,
        update=lambda s,c: updateNode(s,c)
    )

    drop_nodata_faces: BoolProperty(
        name="Drop NODATA faces",
        description="Remove faces touching NODATA values (keeps mesh clean on edges)",
        default=True,
        update=lambda s,c: updateNode(s,c)
    )

    def sv_init(self, context):
        self.inputs.new('SvFilePathSocket', "Path")
        self.outputs.new('SvVerticesSocket', "Vertices")
        self.outputs.new('SvStringsSocket', "Faces")
        self.outputs.new('SvStringsSocket', "DEM data")

    def draw_buttons(self, context, layout):
        layout.prop(self, "zero_min")
        layout.prop(self, "drop_nodata_faces")

    def process(self):
        if not self.inputs["Path"].is_linked:
            return
        path = str(self.inputs["Path"].sv_get(deepcopy=False)[0][0])
        if not path or not Path(path).exists():
            return

        try:
            Z, width, height, (Axx, Axy, Ax0, Ayx, Ayy, Ay0), nodata = _read_any(path)
        except Exception as e:
            # emit empty on error
            self.outputs["Vertices"].sv_set([[]])
            self.outputs["Faces"].sv_set([[]])
            self.outputs["DEM data"].sv_set([[]])
            return

        Z = Z.astype('float64', copy=False)

        # optional zeroing
        if self.zero_min:
            finite_mask = np.isfinite(Z)
            if finite_mask.any():
                mn = np.nanmin(Z[finite_mask])
                Z = Z - mn

        # build coords via affine
        cols, rows = np.meshgrid(np.arange(width, dtype=np.float64),
                                 np.arange(height, dtype=np.float64))
        X = Ax0 + Axx * cols + Axy * rows
        Y = Ay0 + Ayx * cols + Ayy * rows

        xyz = np.stack([X, Y, Z], axis=-1).reshape(-1, 3).tolist()
        faces = _faces_from_wh(width, height)

        # Drop faces touching nodata if requested
        if self.drop_nodata_faces:
            faces = _mask_faces_for_nodata(Z, faces, nodata)

        self.outputs["Vertices"].sv_set([xyz])
        self.outputs["Faces"].sv_set([faces])
        self.outputs["DEM data"].sv_set(Z.tolist())


def register():
    bpy.utils.register_class(SvMegapolisReadDem)

def unregister():
    bpy.utils.unregister_class(SvMegapolisReadDem)

