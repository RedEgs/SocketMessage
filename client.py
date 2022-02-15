from readline import insert_text
import socket
import threading
from tkinter import *
from tkinter import ttk
import time

# Window Settings 
root = Tk()
root.geometry("250x320")
root.title("Chatroom")

# Variable definiton
IpVar = StringVar()
NickVar = StringVar()
PortVar = IntVar()
MessageVar = StringVar()
PrintVar = StringVar()

global NICKNAME

# Title Definition
title = ttk.Label(root, text = 'Chatroom', font=('calibre',15, 'bold')).pack(pady=5)

# Connect Function Definition
def connect():
    
    # Globablising NICKNAME
    global NICKNAME
    
    # Getting values of the IP, Port and Nickname
    ip=IpVar.get()
    port=PortVar.get()
    NICKNAME=NickVar.get()
    
    # Globalising Client
    global CLIENT
    
    # Connecting to the server
    CLIENT = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    CLIENT.connect((ip, port))
    
    # Starting the receive thread
    receive_thread.start()
   
# Send Function         
def send():
    
    # Defining MESSAGE
    MESSAGE = MessageVar.get()  
    
    # The Send Message loop or function
    while True:
        MESSAGE = '{}: {}'.format(NICKNAME, MESSAGE)
        CLIENT.send(MESSAGE.encode('ascii'))
        break

# IP Definitions
iplabel = ttk.Label(root, text = 'IP: ', font=('calibre',10, 'bold')).pack()    
ip_entry = ttk.Entry(root,textvariable = IpVar, font=('calibre',10,'normal')).pack()

# Port Definitions
portlabel = ttk.Label(root, text = 'Port: ', font=('calibre',10, 'bold')).pack()
port_entry = ttk.Entry(root,textvariable = PortVar, font=('calibre',10,'normal')).pack() 

# Nickname Definitions
nicklabel = ttk.Label(root, text = 'Username: ', font=('calibre',10, 'bold')).pack()
nick_entry = ttk.Entry(root,textvariable = NickVar, font=('calibre',10,'normal')).pack() 

# Submit Button
submit_btn = ttk.Button(root,text = 'Connect', command = connect).pack(pady=10)


# Message Definitions
messagelabel = ttk.Label(root, text = 'Message: ', font=('calibre',10, 'bold')).pack()
message = ttk.Entry(root,textvariable = MessageVar, font=('calibre',10,'normal')).pack() 

# Submit Button Definition
submit_btn2= ttk.Button(root,text = 'Send', command = send).pack(pady=10)

# Text label for print statements
textlabel = ttk.Label(root, textvariable = PrintVar, font=('calibre',15, 'bold')).pack()




## Receive Function
def receive():   
    while True:
        try:
            # Receive Message From Server
            # If 'NICK' Send Nickname
            text = CLIENT.recv(1024).decode('ascii')
            if text == 'NICK':
                CLIENT.send(NICKNAME.encode('ascii'))
            else:
                PrintVar.set(text)
                
        except:
            # Close Connection When Error
            print("An error occured!")
            CLIENT.close()
            break



    

        
# Starting Threads For Listening And Writing
receive_thread = threading.Thread(target=receive)


## End Of Program
root.mainloop()