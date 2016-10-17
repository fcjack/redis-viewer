import tornado.ioloop
import tornado.web

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("static/dashboard/dashboard.html")


class DashboardController(tornado.web.RequestHandler):
    def get(self):
        self.write("Tela de Dashboard")

class SettingsContoller(tornado.web.RequestHandler):
    def get(self):
        self.write("Acesso a tela de configurações")


def make_app():
    return tornado.web.Application([
        (r"/redis-viewer", MainHandler),
        (r"/redis-viewer/", MainHandler),
        (r"/redis-viewer/dashboard", DashboardController),
        (r"/redis-viewer/settings", SettingsContoller)
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()