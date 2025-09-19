import socket
import select

IP = "0.0.0.0"
PORT = 4000

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server_socket.bind((IP, PORT))
server_socket.listen()
print("listening on port " + str(PORT))

sockets_list = [server_socket]
clients = {}


def receive_message(client_socket):
    try:
        message = client_socket.recv(1024)
        if not len(message):
            return False
        
        return message
    except Exception as e:
        print(e)
        return False
    
while True:
    read_sockets, _, exception_sockets = select.select(sockets_list, [], sockets_list)

    for notified_socket in read_sockets:
        if notified_socket == server_socket:
            client_socket, client_address = server_socket.accept()

            message = receive_message(client_socket)
            print(f"accepted new connection ")
            print(sockets_list)
            if message is False:
                continue

            sockets_list.append(client_socket)
            clients[client_socket] = client_socket

            
        else:
            message = receive_message(notified_socket)
            if message is False:
                print(f"closed connection")
                sockets_list.remove(notified_socket)
                del clients[notified_socket]
                continue
            
            print(message)
            #user = clients[notified_socket]
            
            for client_socket in clients:
                if client_socket != notified_socket:
                    client_socket.send(message)
    
    
    for notified_socket in exception_sockets:
        sockets_list.remove(notified_socket)
        del clients[notified_socket]
