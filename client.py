import socket
import threading
import tkinter as tk 
from tkinter import scrolledtext
from tkinter import messagebox

HOST = '127.0.0.1'
PORT = 1234 


DARK_GREY = '#121212'
MEDIUM_GREY = '#1F1B24'
OCEAN_BLUE = '#5F7ADB'
WHITE = "white"
FONT = ("Helvetica", 17)
BUTTON_FONT = ("Helvetica", 15)
SMALL_FONT = ("Helvetica", 13)


#creating client socket object. 
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#TK is the base class for tkinter module. it will create the GUI window. 
root = tk.Tk()
#Change width and height of tkinter window. 
root.geometry("600x600")
#Change title of the tkinter window. 
root.title("Real Time Chat Application")
#The window is not resizeable by weight/height. Window cannnot be resized by user.
root.resizable(False,False)

#Prevent frames from resizing. 
root.grid_rowconfigure(0, weight= 1)
root.grid_rowconfigure(1, weight= 4)
root.grid_rowconfigure(2, weight= 1)

# function to write messages to the scroll textbox. Add Client messages.
# First need to enable the config state of the messagebox. 
# tk.END means add messsage at the end. New messages after old messages.
# After message inserted, disable user adding any text into scrolltextbox directly again. 
def add_message(message):
    message_box.config(state=tk.NORMAL)
    message_box.insert(tk.END, message + '\n') 
    message_box.config(state=tk.DISABLED)

#function to connect to the server.
def connect(): 
     # connect to the server.
    try: 
        client.connect((HOST, PORT))
        print("Successfully connected to server")
        add_message("[SERVER]: Sucessfully connected to the server")
    except: 
         messagebox.showerror("Unable to connect to server, "f"Unable to connect to server {HOST} {PORT}")

     #Retrieve text from textbox to save as username. 
    username = username_textbox.get()
    if username != '': 
        client.sendall(username.encode())
    else: 
        messagebox.showerror("Invalid Username", "Username cannot be empty !")

    #Listen to any messages.  
    threading.Thread(target=listen_for_messages_from_server, args=(client, )).start() 

    #Disable client from clicking on join again
    username_textbox.config(state=tk.DISABLED)
    username_button.config(state=tk.DISABLED)

#function to send message.
def send_message():
    message = message_textbox.get()
    if message != '': 
        client.sendall(message.encode())
        #will clear out the textbox after client sends messsage. 
        message_textbox.delete(0, len(message))
    else: 
        messagebox.showerror("Empty Message", "Message cannot be empty !")

#Frames are like widgets in tkinter where we can divide the total area into smaller areas. Three frames will be created to seperate the window space. 
#Need to position the frame within the window. Use Grid method. 
top_frame = tk.Frame(root, width= 600, height= 100, bg= DARK_GREY) 
top_frame.grid(row= 0, column= 0, sticky=tk.NSEW)

middle_frame = tk.Frame(root, width= 600, height= 400, bg= MEDIUM_GREY) 
middle_frame.grid(row= 1, column= 0, sticky=tk.NSEW)

bottom_frame = tk.Frame(root, width= 600, height= 100, bg= DARK_GREY) 
bottom_frame.grid(row= 2, column= 0, sticky=tk.NSEW)

# widget for prompting client to enter username. 
username_label = tk.Label(top_frame, text="Enter Username:", font= FONT, bg= DARK_GREY, fg= WHITE)
username_label.pack(side=tk.LEFT, padx= 10)

# widget for textbox for client to enter their username.
username_textbox = tk.Entry(top_frame, font= FONT, bg = MEDIUM_GREY, fg= WHITE, width= 23)
username_textbox.pack(side=tk.LEFT)

#when user clicks on button join it will exceute the function connect.  
username_button = tk.Button(top_frame, text= "Join", font= FONT, bg= OCEAN_BLUE, fg= WHITE, command= connect) 
username_button.pack (side=tk.LEFT, padx= 15)

#widget for textbox to enter message. 
message_textbox = tk.Entry(bottom_frame, font= FONT, bg= MEDIUM_GREY, fg= WHITE, width=38)
message_textbox.pack (side=tk.LEFT, padx= 10)

# widget to send message. 
message_button = tk.Button(bottom_frame, text="Send", font=BUTTON_FONT, bg= OCEAN_BLUE, fg= WHITE, command= send_message)
message_button.pack (side=tk.LEFT, padx= 8)

#Contain text of messages. 
message_box = scrolledtext.ScrolledText(middle_frame, font= SMALL_FONT, bg= MEDIUM_GREY, fg= WHITE, width = 67, height = 26.5)
#Scroll textbox will be disabled to directly type into it. 
message_box.config(state=tk.DISABLED)
message_box.pack(side=tk.TOP)

#function to recieve messages and display to user. 
def listen_for_messages_from_server(client): 
    
    while 1: 

        message = client.recv(2048).decode('utf-8')
        if message != '':
            #message will be sent in this format username ~ Hey. 
            #Divide the message and convert into form (username, Hey) 
            username = message.split("~")[0]
            content = message.split('~')[1]

            add_message(f"[{username}] {content}")
        else: 
            messagebox.showerror("Error","Message recevied from client is empty")

def main(): 

    # Render the tkinter window 
    root.mainloop()


#Main function has all code to run server. Only will call main function if server.py run directly. Function is not exceuted automatically when when file code is imported as a module.  
if __name__ == '__main__':
    main()
    