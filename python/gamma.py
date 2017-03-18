#!/usr/bin/env python

# Copyright 2010 Thomas Troeger. All rights reserved.
# 
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met:
# 
#    1. Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
# 
#    2. Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in
#       the documentation and/or other materials provided with the
#       distribution.
# 
# THIS SOFTWARE IS PROVIDED BY Thomas Troeger ``AS IS'' AND ANY EXPRESS OR
# IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL Thomas Troeger OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF
# THE POSSIBILITY OF SUCH DAMAGE.

# Show effects of good and bad gamma pixel merge.
# @author Thomas Troeger.

import Image

# the default gamma value to use.
default_gamma=2.2

# ----------------------- pixel conversion functions ------------------------

def toLinear(pixel, gamma=default_gamma):
	"""
	Calculate linear value for pixel value.
	"""
	return ((float(pixel)/255)**float(gamma))*255

def toPixel(linear, gamma=default_gamma):
	"""
	Calculate pixel value from linear value.
	"""
	return ((float(linear)/255)**(1.0/float(gamma)))*255

# -------------------------- pixel merge functions --------------------------

def merge_good(pixel1, pixel2, gamma=default_gamma):
	"""
	Merge two pixel values correctly.
	"""
	linear1=toLinear(pixel1, gamma)
	linear2=toLinear(pixel2, gamma)
	return toPixel((linear1+linear2)/2, gamma)

def merge_bad(pixel1, pixel2, gamma=default_gamma):
	"""
	Erroneously merge two pixel values.
	"""
	return (float(pixel1)+float(pixel2))/2

def merge_diff(pixel1, pixel2, gamma=default_gamma):
	"""
	Get absolute value of difference of good and bad pixel
	merge.
	"""
	linear_good=(toLinear(pixel1, gamma)+toLinear(pixel2, gamma))/2
	linear_bad=toLinear(int(round((float(pixel1)+float(pixel2))/2)), gamma)
	linear_diff=abs(linear_good-linear_bad)
	return toPixel(linear_diff, gamma)

# ---------------------------- output functions -----------------------------

def create_image(f):
	"""
	Create image from merge function.
	"""
	# create image file.
	img=Image.new("RGB", (256, 256))
	# set image pixels.
	for px in range(0, 256):
		for py in range(0, 256):
			pv=int(round(f(px, py)))
			img.putpixel((px, py), (pv, pv, pv))
	# save image.
	img.save("gamma_%s.png" % (f.__name__))


# ---------------------------------- main -----------------------------------

# create image with good pixel combination.
create_image(merge_good)
# create image with bad pixel combination.
create_image(merge_bad)
# create image with difference of good and bad combination.
create_image(merge_diff)

