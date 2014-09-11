#!/usr/bin/env python

import json
import urllib2
from autopkglib import Processor, ProcessorError, github

__all__ = ["GithubTagProvider"]

class GithubTagProvider(Processor):
        '''Provides the latest tag from GitHub.  If a tag is provided, it verifies it exists.'''

        input_variables = {
                'repo_owner': {
                    'description': ('The owner of the github repo to poll.  Examples:'
                        '"octokit", "autopkg".'),
                    'required': True,
                },
                'repo_name': {
                    'description': ('The name of the github repo to poll.  Examples:'
                        '"go-octokit", "autopkg-recipes".'),
                    'required': True,
                },
                "tag": {
                    "description": ("Which tag to download and install, Default is to"
                        "return the latest tag from github."),
                    'required': False,
                },
        }
        output_variables = {
                'url': {
                    'description': 'Url to Download',
                },
                "version": {
                    "description": "Software version.",
                },
        }

        description = __doc__

        def get_github_tag(self, endpoint, tag):
                gh_session = github.GitHubSession()
                (results, code) = gh_session.call_api(endpoint)
                if results == None or code == None:
                    log_err("A GitHub API error occurred!")
                    return -1

                for item in results:
                    if tag != 'latest' and tag != item['name']:
                        continue
                    else:
                        retrieve = item
                        break

                try:
                    return [retrieve['name'], retrieve['zipball_url']]
                except Exception:
                    raise ProcessorError("Couldn't find retrieve tag %s from data" % tag)

        def main(self):
            repo_owner = self.env['repo_owner']
            repo_name = self.env['repo_name']
            tag = self.env.get("tag", 'latest')
            endpoint = '/repos/%s/%s/tags' % (repo_owner, repo_name)

            version, url = self.get_github_tag(endpoint, tag)

            self.env["version"] = version
            self.output('Version %s' % self.env['version'])
            self.env['url'] = url
            self.output('File URL %s' % self.env['url'])

if __name__ == '__main__':
        processor = GithubTagProvider()
        processor.execute_shell()