# Copyright (c) 2015 The MITRE Corp.

# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation
# files (the "Software"), to deal in the Software without
# restriction, including without limitation the rights to use,
# copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following
# conditions:

# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
# OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.

__author__="jgibson"

import argparse
import coffeescript
import os.path

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Compile CoffeeScript files with the Python-CoffeeScript bridge.')
    parser.add_argument('-b', '--bare', default=False, action='store_true',
        help='Compile without the top-level function wrapper.')
    parser.add_argument('-o', '--output', default=None,
        help='The output directory for the compiled JavaScript, defaults to where the CoffeeScript lives.')
    parser.add_argument('-V', '--verbose', default=False, action='store_true',
        help='Whether or not to be noisy during compilation.')
    parser.add_argument('-c', '--compile', default=False, action='store_true',
        help='Ignored. Exists only for compatibility with the native CoffeeScript compiler.')
    parser.add_argument('filename', metavar='<CoffeeScript file>', nargs='+',
        help='CoffeeScript file to compile.')
    args = parser.parse_args()

    for filename in args.filename:
        if args.output:
            path_pair = os.path.split(filename)
            ext_pair = os.path.splitext(path_pair[1])
            coffee_file = ext_pair[0] + '.js' if ext_pair[1].lower() == '.coffee' else path_pair[1] + '.js'
            # The native CoffeeScript compiler appears to do the equivalent of os.path.normpath()
            coffee_path = os.path.normpath(os.path.join(args.output, coffee_file))
        else:
            ext_pair = os.path.splitext(filename)
            coffee_path = ext_pair[0] + '.js' if ext_pair[1].lower() == '.coffee' else filename + '.js'
        if args.verbose:
            print 'Compiling %s into %s' % (filename, coffee_path)
        out = coffeescript.compile_file(filename, bare=args.bare)
        with open(coffee_path, 'w') as fout:
            fout.write(out)
