#!/usr/bin/python
# coding=utf8
#
# Copyright (c) 2015 Johann A. Briffa
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
# MA 02110-1301, USA.

import argparse
import commands
import numpy as np
import matplotlib.pyplot as plt
import jbtiff

## main program

def main():
   # interpret user options
   parser = argparse.ArgumentParser()
   parser.add_argument("-i", "--input", required=True,
                     help="input image file to encode")
   parser.add_argument("-o", "--output", required=True,
                     help="output JPEG lossless raw data file")
   parser.add_argument("-S", "--slice", required=True, type=int,
                     help="first sensor image slice width")
   parser.add_argument("-C", "--components", required=True, type=int,
                     help="number of color components to create")
   parser.add_argument("-P", "--precision", required=True, type=int,
                     help="number of bits per sensor pixel")
   parser.add_argument("-d", "--display", action="store_true", default=False,
                     help="display encoded images")
   args = parser.parse_args()

   # See raw_decode.py for color components & slicing example

   # load sensor image
   I = jbtiff.pnm_file.read(open(args.input,'r'))
   assert len(I.shape) == 2 # must be a one-channel image
   (height,width) = I.shape

   # determine the number of slices and the width of each slice
   slices = (width + args.slice - 1) // args.slice
   slice_widths = [args.slice] * (slices-1) + [width - args.slice*(slices-1)]
   # first slice image
   a = np.zeros((height, width), dtype=np.dtype('>H'))
   for i, sw in enumerate(slice_widths):
      col_s = sum(slice_widths[0:i])
      col_e = col_s + sw
      a.flat[col_s*height:col_e*height] = I[:,col_s:col_e].flat

   # determine color components to create
   components = []
   for i in range(args.components):
      f = 'parts.%d' % (i+1)
      components.append(f)
   # next split color components
   for i, f in enumerate(components):
      # space for raw data for this color component
      b = np.zeros((height, width / args.components), dtype=np.dtype('>H'))
      # extract data from sliced color image
      b = a[:,i::args.components]
      # save to file
      b.tofile(f)
      # show user what we've done, as needed
      if args.display:
         plt.figure()
         plt.imshow(b, cmap=plt.cm.gray)
         plt.title('%s (linear)' % f)

   # convert raw data color components to lossless JPEG encoded file
   cmd = 'pvrg-jpeg -ih %d -iw %d -k 1 -p %d -s "%s"' % \
      (height, width / args.components, args.precision, args.output)
   for i, f in enumerate(components):
      cmd += ' -ci %d %s' % (i+1, f)
   st, out = commands.getstatusoutput(cmd)
   if st != 0:
      raise AssertionError('Error encoding JPEG file: %s' % out)

   # show user what we've done, as needed
   if args.display:
      plt.show()
   return

# main entry point
if __name__ == '__main__':
   main()
