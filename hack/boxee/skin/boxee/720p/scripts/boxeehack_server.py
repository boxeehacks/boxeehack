import socket
import xbmc

_connector = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
try:
    _connector.bind ( ( "0.0.0.0", 2100 ) )
    _connector.listen ( 999 )
    _running = True

    while _running:
        channel, details = _connector.accept()

        if _running:
            channel.setblocking(1)
            recvData = channel.recv(2000)

            recvData = "".join(recvData.split("GET /")).split(" HTTP/")[0]
            xbmc.executebuiltin("%s" % recvData)
            channel.send("HTTP/1.1 200 OK\nContent-type: text/html\n\n%s" % recvData)

            channel.close()
except:
    pass