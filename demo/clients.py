from myserver import ms


class client(ms):
    def _func_map(self, data):
        if data == "ME!":
            return data, 1
        elif data[:5] == "Hello":
            return data, 0
        else:
            if self.get_server_addr()[1] == 7772:
                return "2 I'm "+self.get_server_addr()[0]+":"+str(self.get_server_addr()[1])+" ,call me Kiki", 1


if __name__ == "__main__":
    CLIENT_CLASS = 2
    SERVER_CLASS = 1
    TEST_CLASS = 0
    clist = [('localhost', 7771, CLIENT_CLASS), ('localhost', 7772, CLIENT_CLASS),
             ('localhost', 7773, CLIENT_CLASS), ('localhost', 7774, CLIENT_CLASS)]
    test_addr = ('localhost', 6666, TEST_CLASS)
    server_addr = ('localhost', 7770, SERVER_CLASS)

    clients = []
    for c in clist:
        clients.append(client(c[:2], [test_addr, server_addr]))
