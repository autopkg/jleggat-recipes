#!/usr/bin/env python

import re
import urllib2
from autopkglib import Processor, ProcessorError

__all__ = ["MunkiAdminURLProvider"]

BASE_URL = 'https://github.com'
INDEX_PAGE = 'hjuutilainen/munkiadmin/releases'
re_dmg = '[^"]+\.dmg'

class MunkiAdminURLProvider(Processor):
        '''Provides URL to the latest version.'''

        input_variables = {
			"base_url": {
				"required": False,
				"description": "Default is '%s." % BASE_URL,
			},
			"download_page": {
				"required": False,
				"description":
					"page to find download on, default  is '%s." % INDEX_PAGE,
			},
        }
        output_variables = {
			'url': {
				'description': 'First matched sub-pattern from input found on the fetched page'
			}
        }

        description = __doc__

        def get_url(self, base_url, download_page, re_url):
                index_url = "/".join((base_url, download_page))
                try:
                        f = urllib2.urlopen(index_url)
                        content = f.read()
                        f.close()
                except BaseException as e:
                        raise ProcessorError('Could not retrieve URL: %s' % index_url)

                re_pattern = re.compile(r'a[^>]* href="(?P<url>%s)"' % re_url)

                m = re_pattern.search(content)
                if not m:
                    raise ProcessorError(
                    "Couldn't find download URL in %s"
                    % (index_url))

                return "".join((base_url, m.group("url")))

        def main(self):
            self.env['url'] = self.get_url(BASE_URL, INDEX_PAGE, re_dmg)
            self.output('File URL %s' % self.env['url'])

if __name__ == '__main__':
        processor = MunkiAdminURLProvider()
        processor.execute_shell()