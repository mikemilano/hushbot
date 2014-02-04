from twisted.web.server import Site
from twisted.web.resource import Resource
from twisted.internet import reactor
import json


class WebService(Resource):
    def __init__(self, path):
        Resource.__init__(self)
        self.q = None
        self.path = path

    def render(self, request):
        if 'q' not in request.args:
            return json.dumps({'status': 0, 'message': 'invalid query', 'data': {}})

        self.q = request.args['q'][0]

        if self.q == 'players':
            return json.dumps({'status': 1, 'data': {}})

        else:
            return json.dumps({'status': 0, 'path': self.path, 'data': {}})


class WebServer(Resource):
    def getChild(self, path, request):
        return WebService(path)


if __name__ == '__main__':
    resource = WebServer()
    factory = Site(resource)
    reactor.listenTCP(8080, factory)
    reactor.run()