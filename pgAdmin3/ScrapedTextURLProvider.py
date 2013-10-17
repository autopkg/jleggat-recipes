#!/usr/bin/env python

import re
import urllib2

from autopkglib import Processor, ProcessorError

__all__ = ["ScrapedTextURLProvider"]

class ScrapedTextURLProvider(Processor):
        '''Provides URL to the latest version.'''

        input_variables = {
                're_url': {
                        'description': 'Regular expression (Python) to match URL against page.',
                        'required': True,
                },
                'url': {
                        'description': 'URL of page to scrape',
                        'required': True,
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
                    "Couldn't finddownload URL in %s"
                    % (url))

                return m.group("url")

        def main(self):
                re_url = re.compile(self.env['re_url'])
                self.env['url'] = self.get_url(self.env['url'], re_url)
                self.output('File URL %s' % self.env['url'])

if __name__ == '__main__':
        processor = ScrapedTextURLProvider()
        processor.execute_shell()