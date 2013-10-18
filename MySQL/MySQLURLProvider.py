#!/usr/bin/env python

import re
import urllib2
from autopkglib import Processor, ProcessorError

__all__ = ["MySQLURLProvider"]

URL = 'http://dev.mysql.com'
FILE_INDEX = 'downloads/mysql/%s.html'
re_one = '\/downloads\/mirror\.php\?id=\d+'
re_two = '\/get\/Downloads\/[^"]+'

class MySQLURLProvider(Processor):
        '''Provides URL to the latest updated version.'''

        input_variables = {
			'version': {
				'required': True,
				'description': 'The major version of mysql to update.  eg. "5.6"',
			},
			'url': {
				'description': "URL of page to scrape, Default is '%s'." % URL,
				'required': False,
			},
        }
        output_variables = {
			'url': {
				'description': 'First matched sub-pattern from input found on the fetched page'
			}
        }

        description = __doc__

        def get_url(self, base_url, download_page, re_url):
                url = "/".join((base_url, download_page))
                try:
                        f = urllib2.urlopen(url)
                        content = f.read()
                        f.close()
                except BaseException as e:
                        raise ProcessorError('Could not retrieve URL: %s' % url)

                re_pattern = re.compile(r'a[^>]* href="(?P<url>%s)"' % re_url)

                m = re_pattern.search(content)
                if not m:
                    raise ProcessorError(
                    "Couldn't find download URL in %s"
                    % (url))

                return "".join((base_url, m.group("url")))

        def main(self):
            first = FILE_INDEX % version
            dmg_url = self.get_url(URL, first, re_one)
            url_segments = urlparse(dmg_url)
            dmg_index = url_segments.path
            self.env['url'] = self.get_url(URL, dmg_index.lstrip("/"), re_two)
            self.output('File URL %s' % self.env['url'])

if __name__ == '__main__':
        processor = MySQLURLProvider()
        processor.execute_shell()