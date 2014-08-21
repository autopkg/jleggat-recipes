#!/usr/bin/env python

import datetime
import re
from xml.dom.minidom import parse, parseString
import urllib2

from autopkglib import Processor, ProcessorError

__all__ = ["SourceForgeURLProvider"]

FILE_INDEX_URL = 'http://sourceforge.net/projects/%s/rss'

class SourceForgeURLProvider(Processor):
	'''Provides URL to the latest file that matches a pattern for a particular SourceForge project.'''

	input_variables = {
		'project_name': {
			'required': True,
			'description': 'Name of the SourceForge project',
			},
		'match_pattern': {
			'required': False,
			'description': 'Regex pattern to match file name, defaults to ".*", match all.',
			},
	}
	output_variables = {
		'url': {
			'description': 'URL to the latest SourceForge project download'
		}
	}

	description = __doc__

	def get_latest_file_url(self, proj_id, pattern):
		flisturl = FILE_INDEX_URL % proj_id

		try:
			f = urllib2.urlopen(flisturl)
			rss = f.read()
			f.close()
		except BaseException as e:
			raise ProcessorError('Could not retrieve RSS feed %s' % flisturl)

		re_file = re.compile(pattern, re.I)

		rss_parse = parseString(rss)

		items = []

		for i in  rss_parse.getElementsByTagName('item'):
			title = i.getElementsByTagName('title')[0].firstChild.nodeValue
			pubDate = i.getElementsByTagName('pubDate')[0].firstChild.nodeValue
			link = i.getElementsByTagName('link')[0].firstChild.nodeValue

			pubDatetime = datetime.datetime.strptime(pubDate, '%a, %d %b %Y %H:%M:%S UT')

			if re_file.search(title):
				items.append((pubDatetime, link),)

		items.sort(key=lambda r: r[0])

		if len(items) < 1:
			raise ProcessorError('No matched files')

		return items[-1][1]

	def get_sf_file_url(self, file_url):

		try:
			request = urllib2.Request(file_url)
			response = urllib2.urlopen(request)
			dl_url = response.geturl()
		except BaseException as e:
			raise ProcessorError('Could not retrieve Download URL from %s' % file_url)

		return dl_url

	def main(self):
		proj_id  = self.env['project_name']
		file_pat = self.env.get("match_pattern", '.*')

		file_url = self.get_latest_file_url(proj_id, file_pat)
		self.env['url'] = self.get_sf_file_url(file_url)
		self.output('File URL %s' % self.env['url'])

if __name__ == '__main__':
	processor = SourceForgeURLProvider()
	processor.execute_shell()