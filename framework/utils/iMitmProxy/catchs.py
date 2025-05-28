import mitmproxy.http
from mitmproxy import ctx
from project.conf.pingback.configure import g_conf


class Counter:
    def __init__(self):
        self.num = 0

    def request(self, flow: mitmproxy.http.HTTPFlow):
        self.num = self.num + 1
        ctx.log.info("We've seen %d flows" % self.num)
        # ctx.log.info("server host: %s" % flow.request.host)
        is_replace = g_conf.get('pingback', 'replace')
        if is_replace == 'yes':
            for r_key in g_conf.options('replace'):
                r_value = g_conf.get('replace', r_key)
                res, des = tuple(r_value.split('::'))
                if r_key == 'host'and flow.request.host == res:
                    flow.request.host = des


addons = [
    Counter()
]