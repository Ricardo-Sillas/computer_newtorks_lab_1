from socket import *
import sys

if len(sys.argv) <= 1:
    print('Usage : "python ProxyServer.py server_ip"\n[server_ip : It is the IP Address Of Proxy Server')
    sys.exit(2)

# The proxy server is listening at 8888
tcpSerSock = socket(AF_INET, SOCK_STREAM)
tcpSerSock.bind((sys.argv[1], 8888))
tcpSerSock.listen(100)

# Stores the URL and responses
cache = {}

while 1:
    # Start receiving data from the client
    print('Ready to serve...')

    # Accepted connection
    tcpCliSock, addr = tcpSerSock.accept()

    print('Received a connection from:', addr)

    message = tcpCliSock.recv(1024).decode()
    print(message)


    # Extract the filename from the given message
    separatedLine = message.split('\n', 1)
    data = separatedLine[0].split(" ", 1)
    file = data[1].split(" ", 1)

    request = file[0]
    newRequest = file[0][1:]

    print(request)
    print(newRequest)

    filetouse = f'www.{newRequest}'

    requestMessage = ("GET " + "http://" + filetouse + " HTTP/1.0\n\n").encode()

    try:
        # Check whether the file exist in the cache
        if requestMessage in cache:
            print("response found in cache")
            response = cache[requestMessage]
            newFile = tcpCliSock.makefile('wrb', 0)
            newFile.write(response)
        else:
            print("response not found in cache")
            newTcpCliSock = socket(AF_INET, SOCK_STREAM)
            newTcpCliSock.connect((filetouse.encode(), 80))

            # Send get request
            newTcpCliSock.send(requestMessage)

            # Read back response
            response = newTcpCliSock.recv(2048)

            newFile = tcpCliSock.makefile('wrb', 0)
            newFile.write(response)
            tcpCliSock.send(response)

            cache[requestMessage] = response

    # Error handling for file not found in cache, need to talk to origin server and get the file
    except error:
        tcpCliSock.send(("HTTP/1.0 404 sendErrorErrorError\r\n").encode())
        tcpCliSock.send(("Content-Type:text/html\r\n").encode())
        tcpCliSock.send(("\r\n").encode())

    # Close the client and the server sockets
    tcpCliSock.close()
tcpSerSock.close()