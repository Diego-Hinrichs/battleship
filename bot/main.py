import socket

# https://docs.python.org/3/library/socket.html
# https://pythontic.com/modules/socket/recvfrom

localIP = "127.0.0.1"
localPort = 20002
bufferSize = 1024
msgFromServer = "Hello UDP Client"
bytesToSend = str.encode(msgFromServer)

# Crear socket
# Familia de direcciones con las cuales mi socket puede comunicarse (AF_INET -> IPv4)
# También esta (AF_INET6 -> IPv6) (AF_BLUETOOTH, AF_UNIX)
UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

# Vincular socket a la direccion. El socket no debe estar vinculado
UDPServerSocket.bind((localIP, localPort))
print("UDP server up and listening")

# Esperar por paquetes entrantes
while(True):
    # Lee bytes enviados por el socket, retorna tupla (mensaje, ipAddress)
    bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)
    message = bytesAddressPair[0] # mensaje recibido
    address = bytesAddressPair[1]
    
    temp = str(message.decode())
    print(temp)
    
    clientMsg = f"Message: {type(temp)}"
    #clientIP = f"Client IP Address: {address}"

    print(clientMsg)
    #print(clientIP)

    # Sending a reply to client
    UDPServerSocket.sendto(bytesToSend, address) # Envia respuesta al cliente
