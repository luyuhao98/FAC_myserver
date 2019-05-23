import time
import threading
import socket
from abc import ABCMeta, abstractmethod

__author__ = 'LU,Yuhao'


class myserver(metaclass=ABCMeta):

    def __init__(self, server_addr, target_addr=None):

        self.__BUF_SIZE = 4096
        self.__con_mutex = threading.Lock()
        self.__tmutex = threading.Lock()
        self.__acc_mutex = threading.Lock()
        self.__tsocks = {}
        self.__connected = {}
        # self.__accepted = []
        self.__groups = {}

        threading.Thread(target=self.__server_thread,
                         args=(server_addr,)).start()
        if target_addr:
            if type(target_addr) == tuple:
                self.connect(target_addr)
            elif type(target_addr) == list:
                self.group_connect(target_addr)
            else:
                print("Invalid init argument: target_addr")

    def __server_thread(self, server_addr):

        assert len(
            server_addr) == 2, 'Invalid address format! Correct one:(host_ip,port)'
        assert type(
            server_addr[0]) == str, 'Invalid address format! Correct one:(host_ip,port)'
        assert type(
            server_addr[1]) == int, 'Invalid address format! Correct one:(host_ip,port)'

        self.__server_addr = server_addr
        self.__ssock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__ssock.setsockopt(
            socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
        self.__ssock.setsockopt(
            socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.__ssock.bind(self.__server_addr)

        self.__ssock.listen(20)
        while True:
            conn, addr = self.__ssock.accept()
            # self.__acc_mutex.acquire()
            # self.__accepted.append(addr)
            # self.__acc_mutex.release()
            threading.Thread(target=self.__parse,
                             args=(conn, addr,)).start()

    def __parse(self, conn, addr):
        while True:
            data = conn.recv(self.__BUF_SIZE)
            if data:
                data = data.decode()
                data = data.strip().split('\n')
                for msg in data:
                    threading.Thread(target=self.__rec_handle,
                                     args=(msg,)).start()
            else:
                print("Connect ", addr, "is dead")
                # self.__acc_mutex.acquire()
                # self.__accepted.remove(addr)
                # self.__acc_mutex.release()
                break

    def __rec_handle(self, msg):
        response = self._func_map(msg)
        if response:
            assert len(
                response) == 2, 'return of _func_map : response_info, group_num'
            assert type(
                response[0]) == str, 'response_info should be str'
            assert type(response[1]) == int, 'group_num should be int'
            response_info, group_num = response
            self.group_send(group_num, response_info)

    @abstractmethod
    def _func_map(self, msg):
        pass
        # print(data)
        # return "Server"+data, 0
        # return "Welcome to "+str(self.server_port)

    def group_connect(self, target_addrs):
        assert type(
            target_addrs) == list, 'Argument target_addrs should be a list'
        for addr in target_addrs:
            self.connect(addr)

    def connect(self, addr):
        assert len(
            addr) == 3, 'Invalid address format! Correct one:(host_ip,port,group_num)'
        assert type(
            addr[0]) == str, 'host_ip should be a str'

        assert type(
            addr[1]) == int, 'port should be an int'

        assert type(
            addr[2]) == int, 'group_num should be an int'

        if addr[:2] in list(self.__connected.keys()):
            if self.__connected[addr[:2]]:
                print("Has already connected to address: ", addr[:2])
            else:
                print("Connection Request to address: ",
                      addr[:2], " has already been sent. Please wait.")
            return

        self.__tmutex.acquire()
        self.__tsocks[addr[:2]] = socket.socket(
            socket.AF_INET, socket.SOCK_STREAM)
        self.__tsocks[addr[:2]].setsockopt(
            socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
        self.__tsocks[addr[:2]].setsockopt(
            socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.__tmutex.release()

        self.__con_mutex.acquire()
        self.__groups[addr[:2]] = addr[2]
        addr = addr[:2]
        self.__connected[addr] = False
        self.__con_mutex.release()

        threading.Thread(target=self.__connect_thread, args=(addr,)).start()

    def __connect_thread(self, addr):
        while not self.__connected[addr]:
            try:
                self.__tsocks[addr].connect(addr)
                self.__con_mutex.acquire()
                self.__connected[addr] = True
                self.__con_mutex.release()
                print("Succeed to connect to addr: ", addr)
                threading.Thread(
                    target=self.__parse, args=(self.__tsocks[addr], addr)).start()

            except Exception:
                pass

    # def __connect_sock_recv(self, taddr):
        # while True:
            # conn = self.__tsocks[taddr]
            # threading.Thread(target=self.__parse,
                             # args=(conn, taddr,)).start()

    def group_send(self, group_num, data):
        ifnull = 1
        for addr in self.__groups:
            if self.__groups[addr] == group_num:
                ifnull = 0
                threading.Thread(target=self.send,
                                 args=(addr, data)).start()
        if ifnull:
            print("Group ", group_num, " does not exist")

    def send(self, taddr, data):
        if taddr not in list(self.__connected.keys()):
            print('No connection to address ', taddr, ' .Please connect first')
            return
        while not self.__connected[taddr]:
            print("Waiting for the connection to Target Server: ", taddr)
            time.sleep(1)
            pass

        data = data+"\n"
        data = data.encode()

        self.__tsocks[taddr].sendall(data)
        print("Succeed to send msg to Target Server: ", taddr)

    def get_conn(self, addr):
        return self.__connected[addr]

    def get_group_num(self, addr):
        return self.__groups[addr]

    def get_target_addrs(self):
        return list(self.__connected.keys())

    # def get_accepted_addrs(self):
        # return self.__accepted

    def get_server_addr(self):
        return self.__server_addr


if __name__ == '__main__':
    s = myserver(('localhost', 7770), ('localhost', 6666, 0))
