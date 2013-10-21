#!/usr/bin/env python
#
# Copyright 2013 Greg Neagle
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


import os
import glob
import FoundationPlist
from autopkglib import Processor, ProcessorError
import json

__all__ = ["AdobeShockwavePlayerMungeInfo"]


class AdobeShockwavePlayerMungeInfo(Processor):
    """Finds the root MacVim-foo-bar folder from the expanded MacVim tbz archive"""
    input_variables = {
        "munki_info": {
            "required": False,
            "description": "The pkginfo property list.",
        },
    }
    output_variables = {
        "pkg_info": {
            "description": "Dictionary of pkginfo keys to copy to import into Munki.",
        },
    }
    description = __doc__

    def munge_plist(self, info):
        """Takes Munki info plist, strips quotes from version and returns as dictionary"""
        # Get pkginfo from output plist.
        print info
        pkginfo = FoundationPlist.readPlistFromString(info)
        print json.dumps(pkginfo, indent=1)
        print pkginfo[version]

        pkginfo[version] = pkginfo[version].strip('"\'')
        return pkginfo

    def main(self):
        # Get current version
        munki_info = self.env["munki_info"]
        self.env["pkg_info"] = self.munge_plist(munki_info)
        self.output("Found %s" % self.env["pkg_info"])


if __name__ == "__main__":
    processor = AdobeShockwavePlayerMungeInfo()
    processor.execute_shell()
