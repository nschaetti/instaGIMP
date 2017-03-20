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

def instagimp_andromeda(img, layer, alpha, beta, whitecenter, blackoutside, redint, greenint, bluize, greenoutside) :
    # Indicates that the process has started.
    gimp.progress_init("Applying Ghost filter to " + layer.name + "...")

    # Set up an undo group, so the operation will be undone in one step.
    pdb.gimp_image_undo_group_start(img)
    
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
                dy = math.fabs(y - (layer.height/2.0))
                distance = math.sqrt(math.pow(dx,2) + math.pow(dy,2))
                
                # Get the pixel and verify that is an RGB value.
                pixel = layer.get_pixel(x,y)
                
                # Colors
                r = alpha * pixel[0] + beta
                g = alpha * pixel[1] + beta
                b = alpha * pixel[2] + beta
                
                # White center
                r += ((whitecenter / dmax) * (dmax - distance))
                g += ((whitecenter / dmax) * (dmax - distance))
                b += ((whitecenter / dmax) * (dmax - distance))
                
                # Black outside
                r -= ((blackoutside / dmax) * distance)
                g -= ((blackoutside / dmax) * distance)
                b -= ((blackoutside / dmax) * distance)
                
                # Yellow
                r -= redint
                g += greenint
                
                # Blueize
                average = (r+g+b)/3.0
                bluize2 = cubicFunction(0, 0.00006, 0, 0, average) * bluize
                b += bluize2
                
                 # Green outside
                g += ((greenoutside / dmax) * distance)
                
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
    "python_fu_instagimp_andromeda",
    "Ghost",
    "Black and white style GIMP filter",
    "JFM",
    "Open source (BSD 3-clause license)",
    "2016",
    "<Image>/Filters/InstaGIMP/Andromeda",
    "RGB, RGB*",
    [
        (PF_FLOAT, "alpha", "Alpha", 1.475),
        (PF_SLIDER, "beta", "Beta", -20, (-255, 255, 1)),
        (PF_SLIDER, "whitecenter", "White intensity", 40, (0, 255, 1)),
        (PF_SLIDER, "blackoutside", "Black intensity", 80, (0, 255, 1)),
        (PF_SLIDER, "redint", "Red", 10, (0, 255, 1)),
        (PF_SLIDER, "greenint", "Green", 50, (0, 255, 1)),
        (PF_SLIDER, "bluize", "Blue intensity", 60, (0, 255, 1)),
        (PF_SLIDER, "greenoutside", "Green intensity", 50, (0, 255, 1))
    ],
    [],
    instagimp_andromeda)

main()
