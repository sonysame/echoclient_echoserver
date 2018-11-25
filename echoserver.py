import socket
import sys
import os
import multiprocessing
from pwn import *
import copy_reg
from multiprocessing.reduction import rebuild_socket, reduce_socket


copy_reg.pickle(socket.socket, reduce_socket, rebuild_socket)


def open_server(port):
   HOST, PORT='', port
   listen_socket=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
   listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
   listen_socket.bind((HOST, PORT))
   listen_socket.listen(1)

   print '(Server side PORT %s)'% PORT
   return listen_socket

def connection(conn, addr, port, option, user):

   client_connection=conn
   client_address=addr
   PORT=port
   pid=os.getpid()
   print("\n\nprocess id is %d"%pid)
   
   try:
      if(option==1):
         user.append(conn)
         length=len(user)
         while True:
            message=client_connection.recv(1024)
            print(message)
            if(message=="exit"):
               del user[length-1]
               break
            for conn in user:
               conn.send(message)
           
      else:
          while True:
            message=client_connection.recv(1024)
            print(message)
            client_connection.send(message)
            if(message=="exit"):
               break

   
   except socket.error:
      print("----------------------------------\n")
      sys.exit(1)
      
   finally:
      print("--------------Bye bye!------------\n")
      client_connection.close()
            
      

if __name__=='__main__':
   
   
   PORT=int(sys.argv[1])
  
   listen_socket=open_server(PORT)
   manager=multiprocessing.Manager()
   user=manager.list()
         
   while True:
        
         client_connection, client_address=listen_socket.accept()
         
         if(len(sys.argv)==3 and sys.argv[2]=='-b'):
            print("-b option is on")
            client_connection.send("on")
            process=multiprocessing.Process(target=connection, args=(client_connection,client_address,PORT,1,user))
            process.daemon=True
            process.start()
         
         elif(len(sys.argv)==2):
            client_connection.send("off")
            process=multiprocessing.Process(target=connection, args=(client_connection,client_address,PORT,0,0))
            process.daemon=True
            process.start()
      
         else:
            print("syntax : echoserver <port> [-b]")
            print("sample : echoserver 1234 -b")
            sys.exit(1)

   for process in multiprocessing.active_children():
      process.terminate()
      process.join()
      print("-----------DONE------------")

listen_socket.close()