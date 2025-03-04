B1;2cimport struct
import sys
import socket
from socket import * 
import os
import re
import base64 #was trying to make the png work 
from random import * #transaction id randomization
import binascii #making hex object
import datetime # time day WHEN
import time # for Query time
import functions # functions for parsing the messages 
UDPORT=53
DNSIPS="";
HOSTS="";
TYPES="";
addrecords='0000291000000000000000' # was at the end of dig querrys some times     

def setSend(argv,con):
    if(argv[1].rstrip()=="-t"):  #need flag
        if(typeToInt( argv[2].rstrip() )>0 ): # gotta be real type 
            TYPES= argv[2].rstrip();
            if(argv[3].rstrip()=="--tcp"): #checks for --tcp
                tcp=True;
                DNSIPS=argv[4].rstrip() 
                HOSTS=argv[5].rstrip()
                hey=makeQ(argv,  DNSIPS, HOSTS, TYPES)
                #print(bytes.fromhex(hey))
                #print("TCP sending...To","DNS:",DNSIPS," ",UDPORT,":port")
                msg=bytes.fromhex(hey)
                msg = (len(msg)).to_bytes(2, byteorder='big') + msg
                con.settimeout(3)
                data=''
                try:#if failes to connect
                    con.connect((DNSIPS, UDPORT))
                    try:
                        con.sendall(msg )
                        start_time=time.time()
                        try:
                            data=b''
                            dataa=b''
                            while len(dataa)==len(data) or len(dataa)==4096:
                                dataa = con.recv(4096)
                                data=data+dataa;
                            clock=time.time()-start_time;
                            #print("REC:",data)
                            #print(list(data))
                            #print(data.hex())
                            proccesBytes( clock ,DNSIPS, HOSTS, TYPES, data, tcp)
                        except timeout:
                            print(";; connection timed out; no server data recieved")
                    except  timeout:
                        print(";; failed to send try UDP ")
                except  timeout  :
                    print(";; server could not be reached try UDP ")   
                con.close() 
                return data 
            else:
                tcp=False;
                DNSIPS = (argv[3]).rstrip()
                HOSTS=argv[4].rstrip()
                hey=makeQ(argv,  DNSIPS, HOSTS, TYPES)
                #print("UDP sending...To","DNS:",DNSIPS," ",UDPORT,":port")
                #print("MESSAGE:",bytes.fromhex(hey))
                #g=  b'\xde\xad\x01\x00\x00\x01\x00\x00\x00\x00\x00\x00\x06google\x03com\x00\x00\xff\x00\x01'
                #print (g,":RIGHT FORMAT")
                con.settimeout(10)
                #con.sendto(bytes.fromhex(hey), (DNSIPS, UDPORT))
                #start_time = time.time()
                try:
                    con.sendto(bytes.fromhex(hey), (DNSIPS, UDPORT))
                    #con.sendto(g, (DNSIPS, UDPORT))
                    start_time = time.time()
                    data , adr= con.recvfrom(6500)
                    clock=time.time()-start_time;
                except timeout:
                    print(";; connection timed out; no servers could be reached")
                    return ''
                #print ("REC:",data)
                #print(list(data))
                #print(data.hex())
                proccesBytes(clock,DNSIPS, HOSTS, TYPES, data, tcp)
                return data
                
        else:
            print ("Bad Type Sorry! try ANY FORMAT= python3 dns_client.py -t TYPE_ARGUMENT [--tcp] DNSIP HOSTNAME ");
    else:
        print("no -t FORMAT= python3 dns_client.py -t TYPE_ARGUMENT [--tcp] DNSIP HOSTNAME  ");
        
def proccesBytes(clock,  DNSIPS, HOSTS, TYPES, data,tcp):
    hexDat=data.hex()
    size=len(data)-2
    if(tcp):
        hexDat=hexDat[4:] # tcp has size in front
    else:
        size+=2
    #print(hexDat[0], hexDat[1],hexDat[2],hexDat[3])
    
    #idd=intm(hexDat[0])*(16**3)+intm(hexDat[1])*(16**2)+intm(hexDat[2])*(16**1)+intm(hexDat[3])*(1)
    print(";; Got answer: " )
    #array with int for ans rr auth rr and add rr
    ArrArrArr=header(hexDat);
          # answer rr   authority rr + question
    total=ArrArrArr[0]+ArrArrArr[1]
    #start=24-25
    print()
    print(";; QUESTION SECTION: ")
    endLoc=question(hexDat)
    print(" ")
    print(";; ANSWER SECTION: ")
    functions.rest(endLoc,hexDat, total)
    print("\n ")
    clock=clock*1000
    clock='%.2f' % clock
    print(";; Query time: ",clock," msec" )
    print(";; SERVER: ",DNSIPS,"#",UDPORT,"(",DNSIPS,")")
    now = datetime.datetime.now()
    print(";; WHEN: ",now.strftime("%a %b %H:%M:%S EDT %Y")  )
    print(";; MSG SIZE  rcvd: ",size)
    return 0

def question(d):
    locationNull=doubleZero(d,24)
    ln=locationNull
    print(";",dehex(24,d).decode("utf-8"),"\t\t\t","IN\t",intToType( intm(d[ln+4])*16+intm(d[ln+5]) ) )
    #skips the 8+2 bits to get to name section
    return ln+8+2
    

    
    #returns value of string of hex chars
def addHex(d,where,bytes):
    if(bytes<1):
        return intm(d[where])
    else:
        return intm(d[where])*16**bytes+addHex(d,where+1,bytes-1)
    #returns value of string of hex chars                                                                                                                     
  #finds next location of 00 in hex string  
def doubleZero(d,location):
    if(intm(d[location])==0 and intm(d[location+1])==0):
        return location
    else:
        return doubleZero(d,location+1)
def header(d):
   # print(d)
    opt=optC( intm(d[4])% 8+int(intm(d[5])/8) )
    rc=rcC(intm(d[8]))
    #print("d[0:4]",d[0:4])
    #print("d[4:8]",d[4:8])
    x=0
    idd=intm(d[x])*(16**3)+intm(d[x+1])*(16**2)+intm(d[x+2])*(16**1)+intm(d[x+3])*(1)
    x=8 #4 is the flags
    que=intm(d[x])*(16**3)+intm(d[x+1])*(16**2)+intm(d[x+2])*(16**1)+intm(d[x+3])*(1)
    x=12
    ans=intm(d[x])*(16**3)+intm(d[x+1])*(16**2)+intm(d[x+2])*(16**1)+intm(d[x+3])*(1)
    x=16
    auth=intm(d[x])*(16**3)+intm(d[x+1])*(16**2)+intm(d[x+2])*(16**1)+intm(d[x+3])*(1)
    x=20
    add=intm(d[x])*(16**3)+intm(d[x+1])*(16**2)+intm(d[x+2])*(16**1)+intm(d[x+3])*(1)
    print(";; ->>HEADER<<- opcode: ",opt," status: ",rc,", ID:",idd)
    print(";; flags:",flags(d),"; QUERY: ",que ,", ANSWER:",ans,", AUTHORITY:",auth,", ADDITIONAL:",add )
    return [ans, auth, add]

# makes flag string
def flags(d):
    flags=" "
    if(intm(d[5])&4>0):
        flags+="aa "
    if(intm(d[5])&2>0):
        flags+="tr "
    if(intm(d[5])&1>0):
        flags+="rd"
    if(intm(d[6])&8>0):
        flags+="ra"
 #deHexiflify recursive
def dehex(start,d):
    if(intm(d[start])==12):
        j=intm(d[start+1])*(16**2)+intm(d[start+2])*(16**1)+intm(d[start+3])*(1)
        return dehex(j*2,d)
    count=intm(d[start])+intm(d[start+1])
    if(count>0):
        return bytearray.fromhex(d[start:(start+(count+1)*2)])+b'.'+dehex(start+count*2+2,d)
    else:
        return b''
        
def makeQ(argv,DNSIPS, HOSTS, TYPES):
     #print(DNSIPS," ",HOSTS, " " ,TYPES)
     #transactionAsHex....standar query flags... question1,ARR0, ARR0,ADDRR1, 
     # all Standard for dig checked on wire shark    
     #hostToHex()
     all=tranId()+'01'+'20'+'00'+'01'+'000000000001'+hostToHex(HOSTS)+'00'+'{:04x}'.format(typeToInt(TYPES),'x')
     """    class:in +addition records code     """
     all=all+'0001'+addrecords
     #print(all)
     return all
#for rCode
def rcC(nu):
        return {
         0: "NOERROR",
         1: "FORMATERROR",
         2: "SERVERFAILURE",
         3: "NAMEERROR",
         4: "NOTIMPLEMENTED",
         5: "REFUSED",
         6: "YXDOMAIN",
         7: "YXRRSET",
         8: "NXRRSET",
         9: "NOTAUTH",
         10: "NOTZONE"
    }.get(nu, "NOERROR")
    
#optc find opt string
def optC(numb):
    if(numb==0):
        return "QUERY"
    elif(numb==1):
        return "IQUERY"
    elif(numb==2):
        return "STATUS"
    elif(numb==3):
        return "RESERVED"
    elif(numb==4):
        return "NOTIFY"
    else:
        return "QUERY"
#IP TO HEX CONVERSION
def ipToHex(d):
    #print (d.split('.'))
    t=d.split('.')
    return '0'+str(len(t[0]))+sInt2h(t[0]) +'0'+str(len(t[1]))+sInt2h(t[1])+'0'+str(len(t[2]))+sInt2h(t[2])+'0'+str(len(t[3]))+sInt2h(t[3])
            
def hostToHex(h):
    #print (h.split('.'))
    t=h.split('.')
    at=h.find('.')
    if(at>0):    
        return '0'+str(len(t[0]))+s2h(t[0])+hostToHex(h[at+1:])
    else:
        return  '0'+str(len(t[0]))+s2h(t[0])
#prints argv

def printArgv(argv):
    x=1;
    print("; <<>> UdIg 0.1-P.S.118 <<>> " , end='' )
    for args in argv:
        print (args.rstrip()," " , end='' )
        x=x+1;
    print()
    #dig always prints this 
    print("; (1 server found)")
    print(";; global options: +cmd")

#check if someting --tcp is in argv
def argvCheck(argv, chk ):
    for args in argv:
        if chk  in args:
            return True
    return False

#checks if something in argv mMAY BE OBSOLEETE
def typeToVal( argv):
    for args in argv:
        if chk  in args:
            return True
    return False

#gets the int value from type!
def intToType(t):
            return {
         1: "A",
         2: "NS",
         5: "CNAME",
         6: "SOA",
         11: "WKS",
         12: "PTR",
         13: "HINFO",
         14: "MINFO",
         15: "MX",
         16: "TXT",
         255: "ANY"
    }.get(t, "ANY")
    
def typeToInt(t):
    if(t=="A"):
        return 1
    elif(t=="NS"):
        return 2
    elif(t=="CNAME"):
        return 5
    elif(t=="SOA"):
        return 6
    elif(t=="WKS"):
        return 11
    elif(t=="PTR"):
        return 12
    elif(t=="HINFO"):
        return 13
    elif(t=="MINFO"):
        return 14
    elif(t=="MX"):
        return 15
    elif(t=="TXT"):
        return 16
    elif(t=="ANY"):
        return 255
    else:
        return 0

# makes transaction id
def tranId():
    id= randint(0, 65535)  ;
    return '{:04x}'.format(id);

#string int 2 hex 
def sInt2h(s):
    if(len(s)>1):
        return format(ord(s[0]))+sInt2h(s[1:])
    else:
        return format(ord(s))    
    #string 2 hex recursive through
def s2h(s):
    if(len(s)>0):
        b=s[0]
        return   format(ord(b),'x')+ s2h(s[1:])
    else:
        return ''

def intm(st):
    if(st=='a'):
        return 10
    elif(st=='b'):
        return 11
    elif(st=='c'):
        return 12
    elif(st=='d'):
        return 13
    elif(st=='e'):
        return 14
    elif(st=='f'):
        return 15
    else:
        try:
            j=int( float(st) )
            return int(j)
        except TypeError:
            return -1

def firstcon(con):
    data = con.recv(65535)
    hexDat=data.hex()
    print("SIZE:",hexDat[0], hexDat[1],hexDat[2],hexDat[3])
    size= intm(hexDat[0])*(16**3)+intm(hexDat[1])*(16**2)+intm(hexDat[2])*(16**1)+intm(hexDat[3])*(1)
    if(len(data)<size):
       print("FCON:",data)
       return secCon(con, size,data)
    else:
        return data

def secCon(con,size, data):
    print(len(data))
    while len(data) < size:
        packet = con.recv(size - len(data))
        print("PACKET",packet)
        print("SIZE:",len(packet+data))
        if not packet:
            return None
        data += packet
    return data
    
