#!/usr/bin/env python

import re
import urllib2
from xml.dom import minidom
from autopkglib import Processor, ProcessorError

__all__ = ["PADVersionProvider"]

class PADVersionProvider(Processor):
        '''Provides URL to the latest version.'''

        input_variables = {
                'url': {
                        'description': "URL of page to scrape.",
                        'required': True,
                },
        }
        output_variables = {
                'version': {
                        'description': 'First version information found on the fetched page'
                }
        }

        description = __doc__

        def get_pad_version(self, url):
                try:
                    dom = minidom.parse(urllib2.urlopen(url))
                    prog = dom.getElementsByTagName("Program_Info")[0]
                    version = prog.getElementsByTagName("Program_Version")[0]
                except BaseException as e:
                    raise ProcessorError('Could not retrieve URL: %s' % url)

                return version.childNodes[0].data

        def main(self):
			url  = self.env['url']
			version = self.get_pad_version(url)

			self.env["version"] = version.lstrip('v')
			self.output('Version %s' % self.env['version'])

if __name__ == '__main__':
        processor = PADVersionProvider()
        processor.execute_shell()