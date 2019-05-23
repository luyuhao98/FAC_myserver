import time
import threading
from myserver import ms


class server(ms):
    def __init__(self, server_addr, target_addr, target_num):
        super().__init__(server_addr, target_addr)
        self.target_num = target_num
        self.me_counter = 0
        self.me_mutex = threading.Lock()

    def me_handler(self, response, group_num):
        while self.me_counter < self.target_num:
            pass
        self.me_counter = 0
        self.group_send(group_num, response)

    def _func_map(self, data):
        if data == "ME!":
            if self.me_counter == 0:
                threading.Thread(target=self.me_handler,
                                 args=("You are the only one", 0)).start()
            self.me_mutex.acquire()
            self.me_counter = self.me_counter+1
            # print("me_counter: ",self.me_counter)
            self.me_mutex.release()
            return None

        data = data.split(' ')  # 2 I'm localhost:7772 ,call me Kiki
        try:
            group = int(data[0])
            if group == 2:
                raw_addr = data[2].split(':')
                addr_host, addr_port = raw_addr[0], int(raw_addr[1])
                nickname = data[-1]
                response_info = "Hello "+nickname+"!"
                self.send((addr_host, addr_port), response_info)
        except:
            print("I Got Shit on my ASS...zzzzzzz(sleep for 5 seconds)")
            time.sleep(5)
            print("I wake up")
            return "Server Wake UP", 0


if __name__ == "__main__":
    CLIENT_CLASS = 2
    SERVER_CLASS = 1
    TEST_CLASS = 0
    clist = [('localhost', 7771, CLIENT_CLASS), ('localhost', 7772, CLIENT_CLASS),
             ('localhost', 7773, CLIENT_CLASS), ('localhost', 7774, CLIENT_CLASS)]
    test_addr = ('localhost', 6666, TEST_CLASS)
    server_addr = ('localhost', 7770)
    s = server(server_addr, clist, len(clist))
    s.connect(test_addr)
