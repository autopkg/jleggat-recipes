#!/usr/bin/env python

import re
import urllib2
from autopkglib import Processor, ProcessorError

__all__ = ["EasyFindURLProvider"]

URL = "http://www.devontechnologies.com/download/products.html"
re_url = '[^"]+EasyFind\.app\.zip'

class EasyFindURLProvider(Processor):
        '''Provides URL to the latest version.'''

        input_variables = {
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
            self.env['url'] = self.get_url(URL, re_url)
            self.output('File URL %s' % self.env['url'])

if __name__ == '__main__':
        processor = EasyFindURLProvider()
        processor.execute_shell()