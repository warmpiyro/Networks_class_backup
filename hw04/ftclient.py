import socket
import _thread
import sys
import os
import ftp

# id== get id  iddone== done and remove host:port= send host port back
connection= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#connection.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
connection.bind(("0.0.0.0",47644)) #47645 is the server
#connection.listen(10)
print("command to connect:", socket.getfqdn() , connection.getsockname())
print(connection,":::connection")
serverName=sys.argv[2]; middle=':';
serverH,middle,serverP= serverName.partition(middle)
print(  serverName.partition(middle) )
serverH=serverName.partition(middle)[0] 
serverP= serverName.partition(middle)[2]
print(serverH, serverP)

typeC=sys.argv[3]

def recc(c, addr):
    fileName="temp.txt"
    dat=c.recv(4096)
    fileName=(dat).decode("utf-8")
    print(fileName)
    if( os.path.exists(fileName) ):
        print("Already file!")
        print("Transfer Failed")
    else:
        print("Receiving '",fileName,"'...")
        ftp.makeFile(c,fileName)
        print("Transfer complete!")

def start(serverH,serverP,connection):
    middle=":"
    print(typeC,"TYPE")
    if(typeC in ' --send '):
        print("IN SEND")
        ID=sys.argv[4]
        clientH,middle,clientP=ID.partition(middle)
        iddd=ID.partition(middle)[0]
        iddd=socket.gethostbyname (iddd)
        iddd+=":"
        iddd+=ID.partition(middle)[2]
        print("iddd",iddd)
        print("Asking '",serverName,"about ",ID ,"...")
        idd='vcf3:47644'
        #connect to server
        print("attempting to connect...",serverH,int(serverP) )
        print("host:",socket.getfqdn(serverH) )        
        connection.connect( (serverH,int(serverP)) )
        connection.sendall(iddd.encode('utf-8'))
        idd=connection.recv(256)
        connection.close()
        con=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #con.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        con.bind(("0.0.0.0",47645)) #47645 is the server                                                                                
        #con.listen(1)
        one=str((ID.partition(middle))[0])
        two=int(ID.partition(middle)[2])
        print( str(ID.partition(middle)[0]) , int(ID.partition(middle)[2]) )
        con.connect((one,two))
        print("idd:",idd.decode('utf-8'))
        if(True):
            print("Found client at '",socket.gethostbyname_ex(clientH),middle,clientP,"'..." )
            fileName1=sys.argv[5]
            if( os.path.isfile(fileName1) ):
                if("/" in fileName1):
                    ftemp=fileName1.split("/")
                    print(ftemp[len(ftemp)-1], len(ftemp))
                    fileName2=ftemp[len(ftemp)-1]
                    print(fileName2)
                else:
                    fileName2=fileName1
                print("Sending '",fileName2,"'...")
                ftp.sendName(con,fileName2)
                ftp.sendFile(con,fileName1)
            else:
                print("file not found!")           
        elif('no' in idd.decode('utf-8') ):
           print("client not connected")
            
    elif(typeC in " --receive  --recieve "):
        print("IN RECEIVE")
        print("Asking '",serverName,"' about an identification number...")
        print("Asking '" ,serverH+":"+serverP,"' about an identification number...")
        idd="vcf3:47644"
    #get ID from server is own name...
        if('.'not in serverH):
            serverHH=socket.gethostbyname(serverH)
        print(serverH,":serverHost  serverPort:",serverP)        
        connection.connect((serverH, int(serverP)))
        connection.sendall( ("id").encode("utf-8"))
        idd=(connection.recv(4096)).decode("utf-8")
        print("Issued '",idd,"' for identification...")
        connection.close()
        con=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        con.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        con.bind(("0.0.0.0",47644)) #47645 is the server 
        con.listen(1)
        print(connection)
        print(con)
        while True :
            c, addr = con.accept()
            
            _thread.start_new_thread(recc,(c,addr) ) 
        c.close()
        connection.close()

start(serverH,serverP,connection)
#_thread.start_new_thread(start,("nothing","something"))
#connection.close()
