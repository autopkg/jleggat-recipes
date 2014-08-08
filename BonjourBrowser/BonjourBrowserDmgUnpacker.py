#!/usr/bin/env python
#
# Copyright 2010 Per Olofsson
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

# emulate
# /usr/bin/hdiutil convert -quiet BonjourBrowser.dmg -format UDTO -o BonjourBrowser
# /usr/bin/hdiutil attach -nobrowse -noautoopen -mountpoint right_here BonjourBrowser.cdr

import os
import FoundationPlist
import tempfile
import shutil
import subprocess

from autopkglib import Processor, ProcessorError

__all__ = ["SLADmgUnpacker"]


class SLADmgUnpacker(PkgExtractor):
    description = "Mounts a dmg with sla and extracts the payload to pkgroot."
    input_variables = {
        "dmg_path": {
            "required": True,
            "description":
                "Path to a dmg for extraction.",
        },
    }
    output_variables = {
    }

    __doc__ = description

    def read_dmg_info(self, path):
        """Read Contents/Info.plist inside a bundle."""

        try:
            info = FoundationPlist.readPlist(
                os.path.join(path, "Contents", "Info.plist"))
        except FoundationPlist.FoundationPlistException as err:
            raise ProcessorError(err)
        return info

    def convert_to_cdr(self, src_dmg, out_cdr):
        '''Convert SLA protected dmg to dmg'''
        try:
            p = subprocess.Popen(("/usr/bin/hdiutil",
                                  "convert",
                                  "-plist",
                                  "-format",
                                  "UDTO",
                                  "-o",
                                  out_cdr,
                                  src_dmg),
                                  stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            (out, err) = p.communicate()
            info = FoundationPlist.readPlistFromString(out)
            cdr_path = info[0]
        except (OSError, IOError), err:
            raise ProcessorError(
                "Couldn't convert dmg file")
        return cdr_path

    def convert_to_dmg(self, src_cdr, out_dmg):
        '''Convert cdr to dmg'''
        try:
            p = subprocess.Popen(("/usr/bin/hdiutil",
                                  "convert",
                                  "-plist",
                                  "-format",
                                  "UDZO",
                                  "-o",
                                  out_dmg,
                                  src_cdr),
                                  stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            (out, err) = p.communicate()
            info = FoundationPlist.readPlistFromString(out)
            dmg_path = info[0]
        except (OSError, IOError), err:
            raise ProcessorError(
                "Couldn't convert cdr file")
        return dmg_path

    def verify_dmg(self, src_dmg):
        '''Check that dmg is good.'''
        try:
            p = subprocess.Popen(("/usr/bin/hdiutil",
                                  "verify",
                                  "-plist",
                                  src_dmg),
                                  stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            (out, err) = p.communicate()
            info = FoundationPlist.readPlistFromString(out)
        except (OSError, IOError), err:
            raise ProcessorError(
                "Couldn't verify dmg file")

    def main(self):
        # dmg to work with.
        dmg_path = self.env["dmg_path"]
        cache_dir = os.path.join(self.env["RECIPE_CACHE_DIR"], self.env["NAME"])
        # Create the directory if needed.
        if not os.path.exists(cache_dir):
            try:
                os.mkdir(cache_dir)
            except OSError as e:
                raise ProcessorError("Can't create %s: %s" % (path, e.strerror))

        # Wrap all other actions in a try/finally.
        try:
            temp_path = tempfile.mkdtemp(prefix="tmp", dir=cache_dir)
            # convert original dmg to cdr
            new_cdr = self.convert_to_cdr(dmg_path, temp_path)
            # convert cdr to dmg
            new_dmg = self.convert_to_cdr(cdr_path, temp_path)
            # convert cdr to dmg
            self.verify_dmg(new_dmg)
            # copy new_dmg overwritting the orignal.
            shutil.copy(new_dmg,dmg_path)
        except BaseException as e:
            raise ProcessorError(e)
        finally:
            # This removes the tmp directory and anything beneath it.
            shutil.rmtree(temp_path)

if __name__ == '__main__':
    processor = SLADmgUnpacker()
    processor.execute_shell()
