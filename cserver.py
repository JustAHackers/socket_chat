# coding:utf-8
import socket,random,json
from thread import *
newport = 2230 #random.randint(1025,2000)
s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.bind ((socket.gethostbyname(socket.gethostname()), newport))
print("Server Started At Port " + (str(newport)))
s.listen(100)

allowed = "abcdefghijklmnopqrstuvwxyz1234567890_"
con = []
nme = {}
namelist = []
restricted_uname = ["system","admin","sudo","public"]
#Send params: msg,from,is_private
#Receive params: msg,to

def tjs(msg,frm="public",is_private=False):
    return json.dumps({"msg":msg,"from":frm,"is_private":is_private})

def cfunc(c,sender):
    while True:
     try:
       data = c.recv(1024)
       if not data:
          c.close()
          namelist.remove(sender)
          con.remove(c)
          nme.pop(sender)
          for t in con:
              t.send(tjs(sender.capitalize()+" Has left,there are "+str(len(con))+" others people here","system",True))
          break
       jdata = json.loads(data)
       if jdata["to"] == "public": #If target is public
          av = list(con)
          av.remove(c)
          for t in av:
              try:
                 t.send(tjs(jdata["msg"],sender))
              except Exception as e:
                 print (e)
                 t.close()
          print ("[public]["+sender.capitalize()+"] : "+jdata["msg"])
       elif jdata["to"].lower() in namelist: #If target send in user list
          nme[jdata["to"].lower()].send(tjs(jdata["msg"],sender.capitalize(),True))
       elif jdata["to"].lower() == "system": #User send system command
          if jdata["msg"] == "!who":
             c.send(tjs(", ".join([i.capitalize() for i in namelist]),"system",True))
          else:
             c.send(tjs("Unknown command!","system",True))
       else:
          c.send(tjs("No user named "+jdata["to"],"system",True))
     except socket.error:
       c.close()
       namelist.remove(sender)
       con.remove(c)
       nme.pop(sender)

while 1:
  try:
    c,a = s.accept()
    unms = c.recv(32).lower()
    for i in unms:
        if i not in allowed:
           c.send(tjs("Only alphabetical allowed!","system",True))
           c.close()
           continue
    if unms not in namelist and unms not in restricted_uname:
       namelist.append(unms)
    else:
       c.send(tjs("Username Already Taken!","system",True))
       c.close()
       continue
    con.append(c)
    nme[unms] = c
    for v in con:
        v.send(tjs(unms.capitalize()+" Connected! There are "+str(len(nme))+" People here","system",True))
    print ("[system] : "+unms.capitalize()+" Connected! There are "+str(len(nme))+" People here")
    start_new_thread(cfunc,(c,unms))
  except Exception as e:
    s.close()
    print e
    print ("Malfunction,closing servers")
    break
