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
      if(option!=0):
         user[pid]=conn

         while True:
            message=client_connection.recv(1024)
            print(message)
            for conn in user.values():
               conn.send(message)
           
      else:
          while True:
            message=client_connection.recv(1024)
            print(message)
            client_connection.send(message)
            if(message=="exit"):
               client_connection.close()
   
   except socket.error:
      print("----------------------------------\n")
      
   finally:
      print("--------------Bye bye!------------\n")
      client_connection.close()
            
      

if __name__=='__main__':
   
   
   PORT=int(sys.argv[1])
   try:
      if(sys.argv[2]=='-b'):
         listen_socket=open_server(PORT)
         manager=multiprocessing.Manager()
         user=manager.dict()
         
         while True:
            print("-b option is on")
            client_connection, client_address=listen_socket.accept()
            client_connection.send("on")
            process=multiprocessing.Process(target=connection, args=(client_connection,client_address,PORT,1,user))
            process.daemon=True
            process.start()


           
         for process in multiprocessing.active_children():
            process.terminate()
            process.join()
            print("-----------DONE------------") 
         
      else:
         print("sample : python echoserver 1234 -b")
   
   except:

      listen_socket=open_server(PORT)
      
      
      while True:
         
         client_connection, client_address=listen_socket.accept()
         client_connection.send("off")
         process=multiprocessing.Process(target=connection, args=(client_connection,client_address,PORT,0,0))
         process.daemon=True
         process.start()


        
      for process in multiprocessing.active_children():
         process.terminate()
         process.join()
         print("-----------DONE------------")   

   finally:
      listen_socket.close()
      
