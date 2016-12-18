import web
from handle import Handle

if __name__ == '__main__':
    urls = ('/wx', 'Handle')
    app = web.application(urls, globals())
    app.run()
