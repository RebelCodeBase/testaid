class Testpass(object):

    def __init__(self, host):
        self.host = host

    def testpass(self, path):
        return self.host.ansible('debug',
                                 'msg="{{ lookup(\'passwordstore\', \
                                 \'' + path + '\') }}"')['msg']
