import socket
import os
import sys

# Create the client socket
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# For the different types of commands that occurs
def command(str):
    if str.split()[0] == 'CLOSE':
        print('Good Bye')
    elif str.split()[0] != 'RETR':
        print('Unknown command')
        print('Please try again')
    elif len(str.split()) == 1:
        print('Missing file name')
        print('Please try again')
    else:
        return str.split()[1]
    clientSocket.close()
    sys.exit(1)

def client(serverName, serverPort):
    # Connects the socket
    print('Waiting for connection...')
    try:
        clientSocket.connect((serverName, serverPort))
    except socket.error as e:
        print('Connection error occured')
        print('Please try again')
        clientSocket.close()
        sys.exit(1)

    # Asks user to enter command and copies the file to client folder
    print('You are now connected! Enter your commands now.')
    while True:
            userResponse = input('RFTCli> ')
            fileName = command(userResponse)
            clientSocket.send(fileName.encode())

            if clientSocket.recv(7).decode() == 'Contain':
                writeName = fileName
                if os.path.exists(writeName):
                    print('File already Exists')
                    continue
                with open (writeName, 'wb') as file:
                    while True:
                        data = clientSocket.recv(1024)
                        if not data:
                            break
                        file.write(data)
            else:
                print('File was not found')
                continue
            print('Received', fileName)
            clientSocket.close()

if __name__ == '__main__':
    try:
        serverName = input('Provide Server IP address: ')
        serverPort = int(input('Provide Port Number: '))
        client(serverName,serverPort)
    except ValueError:
        print('Server IP address or Port number entered incorrectly')
        print('Please try again')
        sys.exit(1)
