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

def instagimp_chicago(img, layer, whiteoutside, sepiacolor, redshift) :
    # Indicates that the process has started.
    gimp.progress_init("Applying Chicago filter to " + layer.name + "...")

    # Set up an undo group, so the operation will be undone in one step.
    pdb.gimp_image_undo_group_start(img)
    
    # Distance max
    dmax = math.sqrt(math.pow(layer.width,2) + math.pow(layer.height,2))
    #gimp.message("Red sepia : " + str(float(sepiacolor[0])))

    # Iterate over all the pixels and convert them to gray.
    try:
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
                r = pixel[0]
                g = pixel[1]
                b = pixel[2]
                
                # Color average
                average = (r + g + b) / 3.0
                
                # Sepia
                r = redshift + ((float(sepiacolor[0]) / 255.0) * average)
                g = ((float(sepiacolor[1]) / 255.0) * average)
                b = ((float(sepiacolor[2]) / 255.0) * average)
                """r = redshift + ((214.0 / 255.0) * average)
                g = ((240.0 / 255.0) * average)
                b = ((201.0 / 255.0) * average)"""
                
                # White out side
                r += ((float(whiteoutside) / dmax) * distance)
                g += ((float(whiteoutside) / dmax) * distance)
                b += ((float(whiteoutside) / dmax) * distance)
                
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
    "python_fu_instagimp_chicago",
    "Chicago",
    "20s style GIMP filter",
    "JFM",
    "Open source (BSD 3-clause license)",
    "2013",
    "<Image>/Filters/InstaGIMP/Chicago",
    "RGB, RGB*",
    [
        (PF_SLIDER, "whiteoutside", "White intensity", 120, (0, 255, 1)),
        (PF_COLOR, "sepiacolor", "Color", (214.0/255, 240.0/255, 201.0/255)),
        (PF_SLIDER, "redshift", "Red shift", 34, (0, 255, 1))
    ],
    [],
    instagimp_chicago)

main()
