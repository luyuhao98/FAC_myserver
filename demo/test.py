from myserver import ms


class test(ms):
    def _func_map(self, data):
        print("Test: ", data)


if __name__ == "__main__":
    CLIENT_CLASS = 2
    SERVER_CLASS = 1
    TEST_CLASS = 0
    clist = [('localhost', 7771, CLIENT_CLASS), ('localhost', 7772, CLIENT_CLASS),
             ('localhost', 7773, CLIENT_CLASS), ('localhost', 7774, CLIENT_CLASS)]
    test_addr = ('localhost', 6666, TEST_CLASS)
    server_addr = ('localhost', 7770, SERVER_CLASS)

    t = test(test_addr[:2], clist)
    t.connect(server_addr)

    t.group_send(2, "ME!")
    t.group_send(1, "Sleep Spell")
    t.group_send(2, "It's your time, 7772")
