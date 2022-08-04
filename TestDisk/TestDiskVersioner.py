#!/usr/local/autopkg/python
#
# Copyright 2013 Jeremy Leggat, 2010 Per Olofsson
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import absolute_import

import os.path

from autopkglib import Processor, ProcessorError

__all__ = ["TestDiskVersioner"]


class TestDiskVersioner(Processor):
    description = "Extracts version of TestDisk to be installed."
    input_variables = {
        "root_path": {
            "required": True,
            "description": "Path to root of TestDisk souorce files.",
        },
    }
    output_variables = {
        "version": {
            "description": "Version of TestDisk.",
        },
    }

    description = __doc__

    def get_version(self, file):
        try:
            f = open(file)
            data = f.readline()
            v = data.partition(' ')[0]
            float(v)
            return v
        except (ValueError, TypeError):
            return False

    def main(self):
        root_path = self.env['root_path']
        file = 'VERSION'
        file_path = os.path.join(root_path, file)
        self.env['version'] = self.get_version(file_path)
        self.output("Found version %s in file %s" % (self.env['version'], file_path))


if __name__ == '__main__':
    processor = TestDiskVersioner()
    processor.execute_shell()
