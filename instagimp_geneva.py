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

def instagimp_geneva(img, layer, alpha, beta, brownfusion, blackoutside) :
    # Indicates that the process has started.
    gimp.progress_init("Applying Chicago filter to " + layer.name + "...")

    # Set up an undo group, so the operation will be undone in one step.
    pdb.gimp_image_undo_group_start(img)
    
    # Initialize value
    alpha = 1.775
    beta = -40
    
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
                
                # Color average
                average = (r + g + b) / 3.0
                
                # Brown fusion
                r = average;
                g = average;
                b = average + brownfusion
                
                # Black outside
                r -= ((blackoutside / dmax) * distance)
                g -= ((blackoutside / dmax) * distance)
                b -= ((blackoutside / dmax) * distance)
                
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
    "python_fu_instagimp_geneva",
    "Geneva",
    "20s style GIMP filter",
    "JFM",
    "Open source (BSD 3-clause license)",
    "2013",
    "<Image>/Filters/InstaGIMP/Geneva",
    "RGB, RGB*",
    [
        (PF_FLOAT, "alpha", "Alpha", 1.775),
        (PF_SLIDER, "beta", "Beta", -40, (-255, 255, 1)),
        (PF_SLIDER, "brownfusion", "Brown fusion", 25, (0, 255, 1)),
        (PF_SLIDER, "blackoutside", "Black intensity", 100, (0, 255, 1))
    ],
    [],
    instagimp_geneva)

main()
