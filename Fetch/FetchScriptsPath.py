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

import os

from autopkglib import Processor, ProcessorError

__all__ = ["FetchScriptsPath"]


class FetchScriptsPath(Processor):
    description = 'Returns path to a Scripts directoy in the directory this file is in.'
    input_variables = {
        "dirname": {
            'description': 'name of subdirectory in recipe folder.',
            'default': 'Scripts',
            'required': False,
        },
    }
    output_variables = {
        'dirpath': {
            'description': 'Full path to directory in this folder.',
        },
    }

    description = __doc__


    def scripts_directory(self, basepath, dirname):
        dirpath = os.path.join(basepath, dirname)
        if os.path.isdir(dirpath):
            return os.path.abspath(dirpath)
        return None


    def main(self):
        dirname = self.env.get('dirname', 'Scripts')
        basepath = os.path.dirname(os.path.abspath(__file__))
        self.env['dirpath'] = self.scripts_directory(basepath, dirname)
        self.output("Found Directory %s" % (self.env['dirpath']))


if __name__ == '__main__':
    processor = FetchScriptsPath()
    processor.execute_shell()
