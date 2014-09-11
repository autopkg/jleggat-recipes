#!/usr/bin/env python

import json
import urllib2
import re
from autopkglib import Processor, ProcessorError, github

__all__ = ["GithubReleaseProvider"]

class GithubReleaseProvider(Processor):
        '''Provides the latest release from GitHub.  If a release is provided, it verifies it exists.'''

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
                "release": {
                    "description": ("Which release to download and install, Default is to"
                        "return the latest release from github."),
                    'required': False,
                },
                "build": {
                    "description": ("Which build to download and install, Default is to"
                        "return the first build found from github feed."),
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

        def get_github_release(self, repo_owner, repo_name, release, build):
                endpoint = '/repos/%s/%s/releases' % (repo_owner, repo_name)
                gh_session = github.GitHubSession()
                (results, code) = gh_session.call_api(endpoint)
                if results == None or code == None:
                    log_err("A GitHub API error occurred!")
                    return -1

                for item in results:

                    if release and release != item['name']: continue

                    if build:
                        regex = re.compile('%s-%s-%s\.(tgz|tbz|zip|tar.*)' % (repo_name, item[tag_name], build))
                        for asset in item[assets]:
                            if not regex.match(asset[name]): continue

                            download_url = asset[browser_download_url]
                            break
                    else:
                        download_url = item[assets][0][browser_download_url]
                        break

                try:
                    return results[index]['name'], downloadurl
                except Exception:
                    raise ProcessorError("Couldn't find retrieve release %s from data" % release)

        def main(self):
            repo_owner = self.env['repo_owner']
            repo_name = self.env['repo_name']
            release = self.env.get("release", None)
            build = self.env.get("build", None)

            version, url = self.get_github_release(repo_owner, repo_name, release, build)

            self.env["version"] = version
            self.output('Version %s' % self.env['version'])
            self.env['url'] = url
            self.output('File URL %s' % self.env['url'])

if __name__ == '__main__':
        processor = GithubReleaseProvider()
        processor.execute_shell()