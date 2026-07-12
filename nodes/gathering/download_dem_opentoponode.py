import os, threading, webbrowser
import bpy
from bpy.props import StringProperty, FloatProperty, EnumProperty
from bpy.types import Operator
from sverchok.node_tree import SverchCustomTreeNode
from sverchok.data_structure import updateNode, SvStringsSocket, SvListSocket
from sverchok.utils.sv_logging import sv_logger

try:
    import requests
except ImportError:
    from megapolis.dependencies import requests  # fallback

# ---------------------------------------------------------------------------
# HTML page for bbox selection (written on demand into mega-polis/web/)
# ---------------------------------------------------------------------------

LEAFLET_HTML = """<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8"/>
<title>Mega-Polis BBox Picker</title>
<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"/>
<link rel="stylesheet" href="https://unpkg.com/leaflet-draw@1.0.4/dist/leaflet.draw.css"/>
<style>
  html, body, #map { height:100%; margin:0; padding:0; }
  .bar { position:absolute; top:10px; left:10px; background:#fff; padding:8px 10px;
         border-radius:8px; box-shadow:0 2px 8px rgba(0,0,0,.15); font:14px system-ui,sans-serif; }
  .bar input { width:360px; }
  .bar button { margin-left:6px; }
</style>
</head>
<body>
<div class="bar">
  <strong>BBox (W,S,E,N):</strong>
  <input id="bbox" value="" readonly />
  <button id="copyBtn">Copy</button>
  <span id="msg" style="margin-left:8px;color:#333;"></span>
</div>
<div id="map"></div>
<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
<script src="https://unpkg.com/leaflet-draw@1.0.4/dist/leaflet.draw.js"></script>
<script>
var map = L.map('map').setView([0,0], 2);
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',{maxZoom:19}).addTo(map);

var drawn = new L.FeatureGroup();
map.addLayer(drawn);

var drawCtl = new L.Control.Draw({
  draw: { polygon:false, polyline:false, circle:false, circlemarker:false, marker:false, rectangle:true },
  edit: { featureGroup: drawn }
});
map.addControl(drawCtl);

function update(layer){
  var b = layer.getBounds();
  var val=[b.getWest(),b.getSouth(),b.getEast(),b.getNorth()].map(x=>x.toFixed(6)).join(",");
  document.getElementById('bbox').value=val;
}
map.on(L.Draw.Event.CREATED, e=>{
  drawn.clearLayers(); drawn.addLayer(e.layer); update(e.layer);
});
map.on('draw:edited', e=>{
  e.layers.eachLayer(layer=>update(layer));
});

document.getElementById('copyBtn').onclick=function(){
  var inp=document.getElementById('bbox'); inp.select(); document.execCommand('copy');
  document.getElementById('msg').textContent="Copied!";
  setTimeout(()=>{document.getElementById('msg').textContent="";},1200);
};
</script>
</body>
</html>
"""

def ensure_html():
    base = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))  # mega-polis root
    web_dir = os.path.join(base, "web")
    os.makedirs(web_dir, exist_ok=True)
    html_path = os.path.join(web_dir, "bbox_picker.html")
    if not os.path.exists(html_path):
        with open(html_path,"w",encoding="utf-8") as f: f.write(LEAFLET_HTML)
    return html_path

# ---------------------------------------------------------------------------
# Operators
# ---------------------------------------------------------------------------

class MP_OT_OpenBBox(Operator):
    bl_idname = "mp.open_bbox"
    bl_label = "Open BBox Picker"
    def execute(self, context):
        html=ensure_html()
        threading.Thread(target=lambda: webbrowser.open('file://'+html),daemon=True).start()
        self.report({'INFO'},"Opened BBox picker in browser")
        return {'FINISHED'}

class MP_OT_PasteBBox(Operator):
    bl_idname = "mp.paste_bbox"
    bl_label = "Paste BBox"
    node_path:StringProperty()
    def execute(self, context):
        clip = context.window_manager.clipboard.strip()
        parts = clip.split(',')
        if len(parts)!=4: return {'CANCELLED'}
        try: W,S,E,N = map(float,parts)
        except: return {'CANCELLED'}
        node = eval(self.node_path)
        node.west, node.south, node.east, node.north = W,S,E,N
        updateNode(node, context)
        return {'FINISHED'}

class MP_OT_DownloadDEM(Operator):
    bl_idname = "mp.download_dem"
    bl_label = "Download DEM"
    node_path:StringProperty()
    def execute(self, context):
        node=eval(self.node_path)
        url=(f"https://portal.opentopography.org/API/globaldem?"
             f"demtype={node.dataset}&south={node.south}&north={node.north}"
             f"&west={node.west}&east={node.east}&outputFormat=GTiff&API_Key={node.api_key}")
        try:
            r=requests.get(url,stream=True); r.raise_for_status()
            out=os.path.join(bpy.app.tempdir,"megapolis_dem.tif")
            with open(out,"wb") as f:
                for chunk in r.iter_content(8192): f.write(chunk)
            node.output_path=out
            updateNode(node, context)
            self.report({'INFO'},"DEM downloaded: "+out)
        except Exception as e:
            sv_logger.error("DEM download failed: %s",e)
            return {'CANCELLED'}
        return {'FINISHED'}

# ---------------------------------------------------------------------------
# Node
# ---------------------------------------------------------------------------

DEM_TYPES=[
    ('SRTMGL3','SRTMGL3 90m',''),
    ('SRTMGL1','SRTMGL1 30m',''),
    ('AW3D30','AW3D30 30m',''),
    ('NASADEM','NASADEM 30m',''),
    ('COP30','Copernicus 30m',''),
    ('COP90','Copernicus 90m',''),
]

class SvMegapolisOpenTopoNode(SverchCustomTreeNode, bpy.types.Node):
    bl_idname = 'SvMegapolisOpenTopoNode'
    bl_label = 'OpenTopography DEM'
    bl_icon = 'RNDCURVE'
    sv_category = 'Mega-Polis/Gathering'

    api_key:StringProperty(name="API Key",default="")
    dataset:EnumProperty(name="Dataset",items=DEM_TYPES,default='SRTMGL1')
    west:FloatProperty(name="West",default=-106)
    south:FloatProperty(name="South",default=39)
    east:FloatProperty(name="East",default=-105)
    north:FloatProperty(name="North",default=40)
    output_path:StringProperty(name="Out Path",default="")

    def sv_init(self, context):
        self.outputs.new(SvStringsSocket.bl_idname, "DEM Path")
        self.outputs.new(SvListSocket.bl_idname, "BBox")

    def draw_buttons(self, context, layout):
        layout.prop(self,"api_key")
        layout.prop(self,"dataset")
        layout.operator("mp.open_bbox")
        op=layout.operator("mp.paste_bbox"); op.node_path="self"
        op2=layout.operator("mp.download_dem"); op2.node_path="self"

    def process(self):
        if self.outputs['DEM Path'].is_linked:
            self.outputs['DEM Path'].sv_set([self.output_path])
        if self.outputs['BBox'].is_linked:
            self.outputs['BBox'].sv_set([[self.west,self.south,self.east,self.north]])

def register():
    bpy.utils.register_class(MP_OT_OpenBBox)
    bpy.utils.register_class(MP_OT_PasteBBox)
    bpy.utils.register_class(MP_OT_DownloadDEM)
    bpy.utils.register_class(SvMegapolisOpenTopoNode)

def unregister():
    bpy.utils.unregister_class(SvMegapolisOpenTopoNode)
    bpy.utils.unregister_class(MP_OT_DownloadDEM)
    bpy.utils.unregister_class(MP_OT_PasteBBox)
    bpy.utils.unregister_class(MP_OT_OpenBBox)

