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

import os.path
import re
from autopkglib import Processor, ProcessorError


__all__ = ["MonitVersioner"]


class MonitVersioner(Processor):
    description = "Extracts version of Monit to be installed."
    input_variables = {
        "root_path": {
            "required": True,
            "description": "Path to root of unzipped Monit files.",
        },
        "file_name": {
            "required": False,
            "description":
                ("File to look for; defaults to CHANGES"),
        },
    }
    output_variables = {
        "version": {
            "description": "Version of Monit.",
        },
    }

    description = __doc__


    def get_version(self, dir, file):
        re_pattern = re.compile(r'Version (?P<version>[0-9\.]+)')
        file_path = os.path.join(dir, file)

        file_object = open(file_path)
        try:
            text = file_object.read()
        finally:
            file_object.close()

        m = re.search(r'^Version (?P<version>[0-9\.]+)$', text)
        if not m:
            raise ProcessorError(
            "Couldn't find version in %s"
            % (file_path))

        return m.group("version")

    def main(self):
        root_path = self.env['root_path']
        file_name = self.env.get("file_name", 'CHANGES')
        self.env['version'] = self.get_version(root_path, file_name)
        self.output("Found version %s in file %s" % (self.env['version'], root_path))


if __name__ == '__main__':
    processor = MonitVersioner()
    processor.execute_shell()
