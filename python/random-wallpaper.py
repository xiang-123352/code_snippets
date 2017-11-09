#! /usr/bin/env python
#coding=utf-8

"""This script generates a random circle wallpaper
Range of values to get from can be adjusted below to create a more artistic wallpaper
based on colour theory"""
from random import randint

# Document size
WIDTH, HEIGHT = (1920, 1200)

circles = []
blurs = []

# Make x number of circles and blur filters
for id in range(20):
    # Get random values
    x_position = randint(0, 1920)
    y_position = randint(300, 900)
    
    radius = randint(20, 250)
    
    # The range can be limited to use more exact colours
    r_colour = randint(0, 255)
    g_colour = randint(0, 255)
    b_colour = randint(0, 255)
    colour = "#%x%x%x"%(r_colour, g_colour, b_colour)
    
    # I've used opacities between 20% and 80% to keep it more even
    opacity = "0.%s"%(randint(20, 80))
    # I have no idea what the range for this is but inkscape suggests between 0.001 and 250
    blur_amount = "%s.%s"%(randint(1, 25), randint(0, 100))
    
    # Append circle xml to a list
    circles.append("""<circle cx="%s" cy="%s" r="%s" style="stroke:black; stroke-width:2; fill:%s; opacity:%s; filter:url(#blur%s);" />"""%(x_position, y_position, radius, colour, opacity, id))
    # Append filter xml to another list
    blurs.append("""<filter id="blur%s" width="1.5" height="1.5">
<feGaussianBlur in="SourceGraphic" stdDeviation="%s"/>
</filter>"""%(id, blur_amount))

# Bring it all together
svg = """<?xml version="1.0" standalone="no"?>
<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">
<svg width="%s" height="%s" version="1.1" xmlns="http://www.w3.org/2000/svg">
<defs>
<linearGradient
       id="linearGradient">
  <stop
     id="stop1"
     style="stop-color:#08559d;stop-opacity:1"
     offset="0" />
  <stop
     id="stop2"
     style="stop-color:#741175;stop-opacity:1"
     offset="1" />
</linearGradient>
<radialGradient
    cx="733.01025"
    cy="526.61871"
    r="625.84656"
    fx="733.01025"
    fy="526.61871"
    id="gradient"
    xlink:href="#linearGradient"
    gradientUnits="userSpaceOnUse"
    gradientTransform="matrix(3.7820774,2.7550586e-8,0,2.1400777,-1812.3015,-527.00498)" />
%s
</defs>
<rect width="%s" height="%s" style="fill:url(#gradient)" />
%s
</svg>"""%(WIDTH, HEIGHT, "\n".join(blurs), WIDTH, HEIGHT, "\n".join(circles))

# Save the svg
wallpaper_file = open('drawing.svg', 'w')
print >> wallpaper_file, svg

