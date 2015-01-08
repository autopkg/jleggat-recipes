#!/usr/bin/env python

import re
from autopkglib import Processor, ProcessorError

__all__ = ["FetchVersionParser"]

class FetchVersionParser(Processor):
        '''Provides URL to the latest version.'''

        input_variables = {
			"version": {
				"required": True,
				"description": "version string to parse.",
			},
        }
        output_variables = {
                'version': {
                        'description': 'The corrected version'
                }
        }

        description = __doc__

        def parse_version(self, v_string):
            version = re.sub(r'\([^)]*\)', '', v_string)
            return version.strip()

        def main(self):
            version = self.env['version']
            self.env['version'] = self.parse_version(version)
            self.output('Version: %s' % self.env['version'])

if __name__ == '__main__':
        processor = FetchVersionParser()
        processor.execute_shell()