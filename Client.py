import rpyc
import os
import threading
import time
import pickle


class Client:
    def __init__(self, host, port):
        self.conn = rpyc.connect(host, port, config = {'allow_public_attrs':True})
        self.host = host
        self.port = port


class Main:

    def __init__(self):
        self.file_list = os.listdir("filenya/.")
        self.list1 = self.file_list[((len(self.file_list)/2)-1):]
        self.list2 = self.file_list[:(len(self.file_list)/2)]
        self.node_list = []
        self.threads = []
        self.elapsed_time = 0
        self.hasil1 = {}
        self.hasil2 = {}

    def worker1(self, node, list):
        list = pickle.dumps(list)
        load = node.conn.root.getTop10(list)
        load = pickle.loads(load)
        self.hasil1 = load
        #self.hasil1 = dict((x, y) for x, y in load)

    def worker2(self, node, list):
        list = pickle.dumps(list)
        load = node.conn.root.getTop10(list)
        load = pickle.loads(load)
        self.hasil2 = dict((x, y) for x, y in load)

    def gabungHasil(self):
        for freq in self.hasil1:
            if freq[0] in self.hasil2:
                self.hasil2[freq[0]] = self.hasil2[freq[0]] + freq[1]
            else:
                self.hasil2[freq[0]] = freq[1]

        self.hasil2 = sorted(self.hasil2.items(), key=lambda x: x[1], reverse=True)

    def run(self):
        # Connect to server
        self.node_list.append(Client('192.168.236.1', 5000))
        self.node_list.append(Client('192.168.236.53', 5000))

        start_time = time.time()

        t = threading.Thread(target=self.worker1, args=(self.node_list[0], self.list1))
        self.threads.append(t)
        t.start()

        g = threading.Thread(target=self.worker2, args=(self.node_list[1], self.list2))
        self.threads.append(g)
        g.start()

        for thread in self.threads:
            thread.join()

        self.gabungHasil()

        i = 0
        while i < 10:
            print self.hasil2[i]
            i = i + 1


        #print self.hasil1
        #print self.hasil2

        #print self.list1
        #print self.list2

        self.elapsed_time = time.time() - start_time

        print self.elapsed_time

if __name__ == "__main__":

    main = Main()
    main.run()
