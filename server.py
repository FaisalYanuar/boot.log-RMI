import os
import pickle
import rpyc

class prosesAnalisaLog(rpyc.Service):
    def exposed_getTop10(self, filelist):
        sentence = {}
        load = pickle.loads(filelist)
#        for filename in os.listdir("filenya/."):
        for filename in load:
            print filename
            for line in open("filenya/"+filename).xreadlines():
                #print line

                #cek = line.split(": ")
                #cek = " ".join(cek[1:])
                #cek = cek.split("\n")[0]

                cek = line.split()
                cek = " ".join(cek[4:])
                #print line
                #print cek
                if (cek in sentence):
                    sentence[cek] = sentence[cek] + 1
                else:
                    sentence[cek] = 0


        #print sentence
        #print sentence.items()

        sort = sorted(sentence.items(), key=lambda x: x[1], reverse=True)
        sort = pickle.dumps(sort)
        return sort

# connecting to client
# send class to client
# load client from connecting function
from rpyc.utils.server import ThreadedServer
temp = ThreadedServer(prosesAnalisaLog, port = 5000)
temp.start()
