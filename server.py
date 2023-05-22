import socket
import threading

# any PORT can be choosen between 0 to 65535.
HOST = '127.0.0.1'
PORT = 1234 
LISTENER_LIMIT = 5
# List of all currently connected clients. 
active_clients = [] 

# Function for server to be listening to all messages from connected clients.
def listen_for_messages(client, username):

    while 1:
         #if recieves message and it is not empty, final message is created and it is sent to all clients. 
        message = client.recv(2048).decode('utf-8')
        if message != '':
            
            final_msg = username + '~' + message
            send_messages_to_all(final_msg)

        else:
            print(f"The message send from client {username} is empty")


# Function to send message to a single client.
def send_message_to_client(client, message):
    #Whenever sending message, it needs to be encoded. Contrast, when receiving messages, it will be decoded.
    client.sendall(message.encode())

# Function to send any new message to all the clients that are connected to this server.
def send_messages_to_all(message):
    # Go through each and every client that is connected. 
    for user in active_clients:
        # One by one send the message to clients connected. 
        send_message_to_client(user[1], message)

# Function to handle client.
def client_handler(client):
    
   # Server will listen for client messages that will contain the username. 
    while 1:
        # recv is called whenever listening for messages from client.
        # 2048 is max size of the message. 
        # All messages are sent in encoding and need to be decoded.
        username = client.recv(2048).decode('utf-8')
        if username != '':
             # add client to list of active_clients. 
            active_clients.append((username, client))
            prompt_message = "SERVER~" + f"{username} added to the chat"
            send_messages_to_all(prompt_message)
            break
        else:
            print("Client username is empty")
     # Creating a thread to perform function listen_for_messages. Keep listening to messages from client.
    threading.Thread(target=listen_for_messages, args=(client, username, )).start()

# Main function
def main():

    # creating socket class object. 
    # AF_INET: using only IPv4 addresses. 
    # SOCK_STREAM: using TCP packets for communication. 
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Creating a try catch block.
    try:
        # Provide the server with an address in the form of host IP and port.
        server.bind((HOST, PORT))
        print(f"Running the server on {HOST} {PORT}")
    except:
        print(f"Unable to bind to host {HOST} and port {PORT}")

    # Set server limit:  max amount of clients that can connect to server at the same time.
    server.listen(LISTENER_LIMIT)

    # This while loop will keep listening to client connections.
    while 1:
        # address [0] will print host of the client and address [1] will print the port of the client. 
        client, address = server.accept()
        print(f"Successfully connected to client {address[0]} {address[1]}")
        # Creating a thread to perform function client_handler. Argument client passed in form of a double. Every time a client is connected, a new thread will start. 
        threading.Thread(target=client_handler, args=(client, )).start()

#Main function has all code to run server. Only will call main function if server.py run directly. 
# Function is not exceuted automatically when when file code is imported as a module.  
if __name__ == '__main__':
    main()