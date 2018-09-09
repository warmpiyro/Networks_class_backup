import socket
import os
import shutil
#filename connection
def sendFile(con, fileName):
    if(os.path.isfile(fileName) ):
        f=open(fileName, "r+")
        shutil.copy2(fileName,"*" )
        con.sendall(f)
        f.close()
        print("DONE SENDING")
    else:
        print("Path to file does not exist")
        
#takes connection and fileName then
def makeFile(con,fileName):
    if('/' in fileName):
        print("contains /")
    else:
        print("Receiving '",fileName,"'...")
        filee=open(fileName,"ab+")
        recvFile(con,fileName,filee)

def  getFileName(con):
    return (con.recv(4096)).decode("utf-8")
#recvFile recievies and writes to a filee
def recvFile(con,fileName,filee):
    con.settimeout(5)
    try:
        data=b''
        dataa=b''
        while len(dataa)==len(data) or len(dataa)==4096:
            dataa = con.recv(4096)
            filee.write(dataa.decode('utf-8'))
            data=data+dataa;
    except socket.timeout:
        print(";; connection timed out; no server data recieved")
#sendName to connection
def sendName(con,fileName):
    con.sendall(fileName.encode("utf-8"))
