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

import sys
import argparse
import jbtiff

## main program

def main():
   # interpret user options
   parser = argparse.ArgumentParser()
   parser.add_argument("-i", "--input", required=True,
                     help="input raw file to process")
   parser.add_argument("-o", "--output", required=True,
                     help="output processed raw file")
   parser.add_argument("-d", "--display", action="store_true", default=False,
                     help="print read data")
   args = parser.parse_args()

   # read input file
   tiff = jbtiff.tiff_file(open(args.input, 'r'))
   # print data as needed
   if args.display:
      tiff.display(sys.stdout)
   # write output file
   tiff.write(open(args.output, 'w'))
   return

# main entry point
if __name__ == '__main__':
   main()
