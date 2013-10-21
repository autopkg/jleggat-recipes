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
import glob
from Foundation import NSData, NSPropertyListSerialization, NSPropertyListMutableContainers

from DmgMounter import DmgMounter
from autopkglib import Processor, ProcessorError


__all__ = ["AdobeShockwaveVersioner"]


class AdobeShockwaveVersioner(DmgMounter):
    description = "Extracts version of Shockwave installed from dmg."
    input_variables = {
        "dmg_path": {
            "required": True,
            "description": "Path to a dmg containing Shockwave installer.",
        },
    }
    output_variables = {
        "version": {
            "description": "Version of Shockwave.",
        },
    }

    __doc__ = description

    def find_pkg(self, path):
        """Find Shockwave pkg at path."""

        apps = glob.glob(os.path.join(path, "*.pkg"))
        if len(apps) == 0:
            raise ProcessorError("No pkg found in dmg")
        return apps[0]

    def read_pkg_info(self, path):
        """Read Contents/Info.plist inside a pkg."""

        plistpath = os.path.join(path, "Contents", "Info.plist")
        info, format, error = \
            NSPropertyListSerialization.propertyListFromData_mutabilityOption_format_errorDescription_(
                NSData.dataWithContentsOfFile_(plistpath),
                NSPropertyListMutableContainers,
                None,
                None
            )
        if error:
            raise ProcessorError("Can't read %s: %s" % (plistpath, error))

        return info

    def main(self):
        # Mount the image.
        mount_point = self.mount(self.env["dmg_path"])
        # Wrap all other actions in a try/finally so the image is always
        # unmounted.
        try:
            app_path = self.find_pkg(mount_point)
            info = self.read_pkg_info(app_path)
            self.env["app_name"] = os.path.basename(app_path)
            try:
                self.env["version"] = info["CFBundleShortVersionString"]
                self.output("Version: %s" % self.env["version"])
            except BaseException as e:
                raise ProcessorError(e)
        finally:
            self.unmount(self.env["dmg_path"])


if __name__ == '__main__':
    processor = AdobeShockwaveVersioner()
    processor.execute_shell()
