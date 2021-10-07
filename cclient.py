import socket,threading,requests,os,json,re
os.system("clear")
port = 2230
unms = raw_input("Name : ")


R = "\x1b[1;31m"
G = "\x1b[1;32m"
Y = "\x1b[1;33m"
B = "\x1b[1;34m"
P = "\x1b[1;35m"
C = "\x1b[1;36m"
W = "\x1b[1;37m"


def tjs(msg,to="public"):
    return json.dumps({"msg":msg,"to":to})

class client:
  s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
  try:
    s.connect (("127.0.0.1", port))
    print port
    s.send(unms)
  except socket.error:
    exit("Server Error")


  def sendmsg(self):
    while True:
      ab = raw_input(B)
      if ab.startswith("!"):
         if ab.startswith("!msg "):
            fo = re.search("!msg (.*?) (.*)",ab)
            to,msg = fo.group(1),fo.group(2)
            self.s.send(tjs(msg,to))
            continue
         else:
            self.s.send(tjs(ab,"system"))
            continue
      self.s.send(tjs(ab))

  def __init__(self):
    iThread = threading.Thread(target=self.sendmsg)
    iThread.daemon = True
    iThread.start()
    while True:
      data = self.s.recv(1024)
      if not data:
         print ("Server Error")
         exit()
      jdata = json.loads(data)
      print (W+"[{}][{}] : {}".format(R+jdata["from"]+W if jdata["from"] == "system" else P+jdata["from"]+W,Y+"PUBLIC"+W if not jdata["is_private"] else G+"PRIVATE"+W,C+jdata["msg"]+W))

client = client()
client.sendmsg()
