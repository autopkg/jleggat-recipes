#!/usr/bin/env python

import json
import urllib2
from autopkglib import Processor, ProcessorError, github

__all__ = ["GithubTagProvider"]

class GithubTagProvider(Processor):
        '''Provides the latest tag from GitHub.  If a tag is provided, it verifies it exists.'''

        input_variables = {
                'repo_name': {
                    'description': ('The github repo to poll as :owner/:repo.  Examples:'
                        '"octokit/go-octokit", "autopkg/autopkg".'),
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

                if tag == 'latest':
                    index = 0
                else:
                    index = [i for i,x in enumerate(results) if item.get('name') == tag]

                try:
                    return results[index]['name']
                except Exception:
                    raise ProcessorError("Couldn't find retrieve tag %s from data" % tag)

        def main(self):
            repo_name = self.env['repo_name']
            tag = self.env.get("tag", 'latest')
            endpoint = '/repos/%s/tags' % repo_name

            version = self.get_github_tag(endpoint, tag)

            self.env["version"] = version.lstrip('v')
            self.output('Version %s' % self.env['version'])

if __name__ == '__main__':
        processor = GithubTagProvider()
        processor.execute_shell()