
import os
import numpy as np
import random

from sverchok.utils.math import inverse, inverse_square, inverse_cubic

def show_welcome():
    text = """
                       .|
                       | |
                       |'|            ._____
               ___    |  |            |.   |' .---"|
       _    .-'   '-. |  |     .--'|  ||   | _|    |
    .-'|  _.|  |    ||   '-__  |   |  |    ||      |
    |' | |.    |    ||       | |   |  |    ||      |
____|  '-'     '    ""       '-'   '-.'    '`      |_________________________
jgs~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

███    ███ ███████  ██████   █████        ██████   ██████  ██      ██ ███████ 
████  ████ ██      ██       ██   ██       ██   ██ ██    ██ ██      ██ ██      
██ ████ ██ █████   ██   ███ ███████ █████ ██████  ██    ██ ██      ██ ███████ 
██  ██  ██ ██      ██    ██ ██   ██       ██      ██    ██ ██      ██      ██ 
██      ██ ███████  ██████  ██   ██       ██       ██████  ███████ ██ ███████ 
                                                                               
"""
    can_paint = os.name in {'posix'}
    if can_paint == True: 
        for line in text.splitlines():
            line_color = random.randint(31,37)
            with_color = f"\033[1;{line_color}m{line}\033[0m" if can_paint else "{line}"
            print(with_color.format(line))
    else:
        print(text)
