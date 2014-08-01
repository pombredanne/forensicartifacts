import json
import webapp2
import sys

import artifact
import github_fetch

from google.appengine.api import memcache


class MainPage(webapp2.RequestHandler):

  def get(self):
    graph = memcache.get("artifact_graph")
    if not graph:
      # Try to get a fresh version
      github_fetch.GitHubFetch().GetArtifacts()

      # Load whatever we have from the datastore
      graph = artifact.ArtifactGraph()
      graph.LoadGraphFromDataStore()
      memcache.add("artifact_graph", graph)

    self.response.write(graph.GetJSONDictOfDicts())


application = webapp2.WSGIApplication([
    ("/", MainPage),
    ("/githubfetch", github_fetch.GitHubFetch),
], debug=True)
