#אלוהים גדול#
import socket
import _thread
import sys
import os
import re
import base64
idList=[''];
connection= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connection.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
connection.bind(("0.0.0.0",47645))
connection.listen(10)

print("command to connect:", socket.getfqdn() , connection.getsockname())
print(connection)
print("host:",socket.gethostbyname_ex( socket.getfqdn() ))
def addRec(client, adress):
    print("client",client,adress)
    data =client.recv(47645);
    data=data.decode('utf-8')
    print(data)
    if(data=="id"):
        cs=client.getsockname()
        cs=str(cs[0])+":"+str(cs[1])
        print(cs)
        idList.append(cs)
        idd=cs.encode('utf-8')
        client.send(idd)
        client.close()
    elif(data=="iddone"):
        cs=client+":"
        cs=cs+"47644"
        if(cs in idList):
            idList.remove(cs)
        else:
            print(cs,":can't remove")
        client.close();
    elif(':' in data):
        print(data)
        print(idList)
        if(data in idList):
            data.encode("utf-8")
            client.send(data)
            #client.close()
             #client.send(kk);
             #data =client.recv(47645);
        else:
            client.send(("no").encode("utf-8"))
            #client.close()
            print(data," :not recieving currently")    
        client.close()

while True:
    client, adress = connection.accept();
    print(client,adress)
    _thread.start_new_thread(addRec,(client,adress))
connection.close()
