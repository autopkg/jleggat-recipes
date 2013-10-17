#!/usr/bin/env python

import re
import urllib2
from autopkglib import Processor, ProcessorError

__all__ = ["ScrapedTextURLProvider"]

URL = "http://www.pgadmin.org/download/macosx.php"
re_url = '[^"]+\/osx\/'
re_dmg = '[^"]+\.dmg)'

class ScrapedTextURLProvider(Processor):
        '''Provides URL to the latest version.'''

        input_variables = {
                'url': {
                        'description': "URL of page to scrape, Default is '%s'." % BASE_URL,
                        'required': false,
                },
        }
        output_variables = {
                'url': {
                        'description': 'First matched sub-pattern from input found on the fetched page'
                }
        }

        description = __doc__

        def get_url(self, url, re_url):
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

                return m.group("url")

        def main(self):
            download_url = self.get_url(URL, re_url)
            self.env['url'] = self.get_url(download_url, re_dmg)
            self.output('File URL %s' % self.env['url'])

if __name__ == '__main__':
        processor = ScrapedTextURLProvider()
        processor.execute_shell()