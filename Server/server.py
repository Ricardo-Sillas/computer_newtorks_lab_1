import socket
import sys

# Create the client socket
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def server(serverName,serverPort):
    # The proxy server is listening at serverPort
    serverSocket.bind((serverName, serverPort))
    serverSocket.listen(100)

    # Start receiving data from the client
    while True:
        print('Listening for connection at %i...' %serverPort)
        connectionSocket, client_addr = serverSocket.accept()
        print('Connection accepted from:', client_addr)
        data = connectionSocket.recv(1024).decode()
        print('Asking for file',data)

        # Looks to see if file exists and sends file if so
        try:
            file = open(data,'rb')
            print('Sending the file...')
            connectionSocket.send('Contain'.encode())
            data = file.read(1024)
            while data:
                connectionSocket.send(data)
                data = file.read(1024)
        except FileNotFoundError:
            connectionSocket.send('Doesn\'t contain'.encode())
            print('File was not found')
            connectionSocket.close()
            continue
        print('Transfer Complete!')
        connectionSocket.close()
        print('Connection closed. See you later!\n')

if __name__=='__main__':
    try:
        serverName = '127.0.0.1'
        serverPort = int(input('Listen at port #: '))
        server(serverName,serverPort)
    except ValueError:
        print('Port number entered incorrectly')
        print('Please try again')
        sys.exit(1)
