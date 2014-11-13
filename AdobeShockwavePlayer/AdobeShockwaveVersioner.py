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
from xml.etree import ElementTree

from autopkglib import Processor, ProcessorError


__all__ = ["AdobeShockwaveVersioner"]


class AdobeShockwaveVersioner(Processor):
    description = "Extracts version of Shockwave installed from dmg."
    input_variables = {
        "input_file_path": {
            "required": True,
            "description": "Path to a Distribution xml file from the Shockwave installer pkg.",
        },
        "xml_node_tag": {
            "required": False,
            "description":
                ("Tag to sort which xml node to use; defaults to "
                './/pkg-ref'),
        },
        "xml_version_attrib": {
            "required": False,
            "description":
                ("Which xml attrib to use; defaults to "
                "version"),
        },
    }
    output_variables = {
        "version": {
            "description": "Version of Shockwave.",
        },
    }

    description = __doc__


    def get_version(self, file,):
        # Open the xml file and parse it.
        try:
            with open(file, 'r') as f:
                tree = ElementTree.parse(f)
            # find the first matching element and return.
            for node in tree.findall('.//pkg-ref[@version]'):
                v = node.attrib.get('version')

            for node in tree.findall(".//bundle-version/*[@id='com.adobe.director.shockwave.bundle']"):
                bundleshortv = node.attrib.get('CFBundleShortVersionString')
                bundlev = node.attrib.get('CFBundleVersion')
                bundlep = node.attrib.get('path')

            return v.strip('"|\''), bundleshortv.strip('"|\''), bundlev.strip('"|\''), bundlep
        except BaseException as e:
            raise ProcessorError('Could not retrieve Version from %s' % file)

    def main(self):
        input_file_path = self.env['input_file_path']
        self.env['version'], self.env['bundleshortversion'], self.env['bundleversion'], self.env['bundlepath'] = self.get_version(input_file_path)
        self.output("Found version \"%s\" in file \"%s\"" % (self.env['version'], input_file_path))

if __name__ == '__main__':
    processor = AdobeShockwaveVersioner()
    processor.execute_shell()
