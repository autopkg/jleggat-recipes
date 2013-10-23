#!/usr/bin/env python
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

import re
from autopkglib import Processor, ProcessorError


__all__ = ["cpanmVersioner"]


class cpanmVersioner(Processor):
    description = "Extracts version of cpanm to be installed."
    input_variables = {
        "input_file_path": {
            "required": True,
            "description": "Path to cpanm file to check.",
        },
    }
    output_variables = {
        "version": {
            "description": "Version of cpanm.",
        },
    }

    description = __doc__


    def get_version(self, file_path):

        file_object = open(file_path)
        try:
            text = file_object.read()
        finally:
            file_object.close()

        m = re.search(r'our \$VERSION = "?([0-9\.]+)"?;', text)
        if not m:
            raise ProcessorError(
            "Couldn't find version in %s"
            % (file_path))

        return m.group(1)

    def main(self):
        input_file_path = self.env['input_file_path']
        self.env['version'] = self.get_version(input_file_path)
        self.output("Found version %s in file %s" % (self.env['version'], input_file_path))


if __name__ == '__main__':
    processor = cpanmVersioner()
    processor.execute_shell()
