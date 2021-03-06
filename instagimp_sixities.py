#!/usr/bin/env python
#
# -------------------------------------------------------------------------------------
#
# Copyright (c) 2017, Nils Schaetti <n.schaetti@gmail.com>
#
# This file is part of InstaGIMP.  InstaGIMP is free software: you can
# redistribute it and/or modify it under the terms of the GNU General Public
# License as published by the Free Software Foundation, version 3.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# this program; if not, write to the Free Software Foundation, Inc., 51
# Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#

from gimpfu import *
import math
import sys, os

def checkColor(color):
    if color > 255:
        return 255
    if color < 0:
        return 0
    return color

def cubicFunction(a, b, c, d, x):
    return a * math.pow(x - 128, 3) + b * math.pow(x - 128, 2) + c * (x - 128) + d

def instagimp_sixities(img, layer) :
    # Indicates that the process has started.
    gimp.progress_init("Applying Sixties filter to " + layer.name + "...")

    # Set up an undo group, so the operation will be undone in one step.
    pdb.gimp_image_undo_group_start(img)
    
    # Initialize value
    alpha = 1.175
    beta = -30
    
    # Distance max
    dmax = math.sqrt(math.pow(layer.width,2) + math.pow(layer.height,2))
    
    try:
        # Iterate over all the pixels and convert them to gray.
        for x in range(layer.width):
            # Update the progress bar.
            gimp.progress_update(float(x) / float(layer.width))

            for y in range(layer.height):
                # Distance
                dx = math.fabs(x - (layer.width/2.0))
                dy = math.fabs(x - (layer.height/2.0))
                distance = math.sqrt(math.pow(dx,2) + math.pow(dy,2))
                
                # Get the pixel and verify that is an RGB value.
                pixel = layer.get_pixel(x,y)
                
                # Colors
                r = alpha * pixel[0] + beta
                g = alpha * pixel[1] + beta
                b = alpha * pixel[2] + beta
                
                # Color average
                average = (r + g + b) / 3.0
                
                # Yellow
                r += 10
                g += 13
                
                # White center
                r += ((60.0 / dmax) * (dmax - distance))
                g += ((60.0 / dmax) * (dmax - distance))
                b += ((60.0 / dmax) * (dmax - distance))
                
                # Black outside
                r -= ((60.0 / dmax) * distance)
                g -= ((60.0 / dmax) * distance)
                b -= ((60.0 / dmax) * distance)
                
                # Redious
                reddize = cubicFunction(0, 0.00005, 0, 0.5, average) * 115
                r += (reddize / 2.0)
                
                # Check bounds
                r = checkColor(r);
                g = checkColor(g);
                b = checkColor(b);
                
                if(len(pixel) >= 3):
                    # Create a new tuple representing the new color.
                    newColor = (int(r),int(g),int(b)) + pixel[3:]
                    layer.set_pixel(x,y, newColor)
        
        # Update the layer.
        layer.update(0, 0, layer.width, layer.height)

    except Exception as err:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        gimp.message("Unexpected error at line " + str(exc_tb.tb_lineno) + " : " + str(err))
    
    # Close the undo group.
    pdb.gimp_image_undo_group_end(img)
    
    # End progress.
    pdb.gimp_progress_end()

register(
    "python_fu_instagimp_sixities",
    "Sixities",
    "60s style GIMP filter",
    "JFM",
    "Open source (BSD 3-clause license)",
    "2016",
    "<Image>/Filters/InstaGIMP/Sixities",
    "RGB, RGB*",
    [
        (PF_FLOAT, "alpha", "Alpha", 1.175),
        (PF_SLIDER, "beta", "Beta", -30, (-255, 255, 1)),
        (PF_SLIDER, "blackoutside", "Black intensity", 80, (0, 255, 1)),
        (PF_SLIDER, "whitecenter", "White intensity", 60, (0, 255, 1)),
        (PF_SLIDER, "redint", "Reddize", 50, (0, 255, 1))
    ],
    [],
    instagimp_sixities)

main()
