import tornado.ioloop
import tornado.web
import tornadoredis
from tornadoredis import Client as Redis

from tornado import gen
import json
from autocomplete import Autocomplete

CONNECTION_POOL = tornadoredis.ConnectionPool(max_connections=500, wait_for_available=True)
auto = Autocomplete ("university")

class RankApp(tornado.web.Application):
    """docstring for RankApp"""
    def __init__(self, arg):
        super(RankApp, self).__init__()
        self.arg = arg


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world")

class SearchHandler(tornado.web.RequestHandler):

    @tornado.web.asynchronous
    @gen.engine
    def get(self):
        
        data = self.get_argument("data", "")
        results = auto.search_query (data)
        print results
        self.finish(json.dumps(results))

application = tornado.web.Application([
    (r"/", MainHandler),
    (r"/search", SearchHandler),
])

def setUp ():
    auto=Autocomplete("university")
    auto.del_index()
    with open("data", "r") as f:
        for num, line in enumerate(f,1):
            item = {"uid":num, "score":1000-num, "term": line}
            print item
            auto.add_item (item)
            

if __name__ == "__main__":

    setUp()

    port = 8888
    application.listen(port)
    print "listen on :", port
    tornado.ioloop.IOLoop.instance().start()