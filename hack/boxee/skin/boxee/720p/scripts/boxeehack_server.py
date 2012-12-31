import socket
import common
import xbmc,time
import select
import urllib

def run_server():
    #Example of a simple tcp server using non-blocking sockets in a threaded script.
    # The combination of threaded script and non-blocking sockets ensures that
    # this script can be interrupted correctly when stopping the role (e.g. when
    # redeploying your project.) 

    #The server accepts only a single connection at time. It receives data until the
    # client either closes the connection or stops sending data for more than 2 seconds.
    # While receiving data it calculates the bit rate and outputs it on outputs[0].

    port = 2100

    #Create socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    #bind to our desired port (on any available address)
    try:
        server_socket.bind(('', port))
    except:
        return

    #set to non-blocking operation
    server_socket.setblocking(0)

    #main loop for the threaded script
    while 1:
        #listen for incoming connection requests
        server_socket.listen(1)
    
        #use select to determine when a connection is available
        server_rfds, server_wfds, server_xfds = select.select([server_socket], [], [], 2)
        if server_socket in server_rfds:
            #accept the connection
            connection, address = server_socket.accept()
        
            #make new connection non-blocking
            connection.setblocking(0)
        
            #loop receiving data and calculate bit rate
            start = time.time()
            bitrate = 0.0
            data_bits = 0.0
            conn_closed = 0
            while conn_closed == 0:
                #use select to wait for data on connection, timeout after 2 seconds
                conn_rfds, conn_wfds, conn_xfds = select.select([connection], [], [connection], 2)
            
                #break on error
                if connection in conn_xfds:
                    break
            
                #check for data received, calculate bit rate
                elif connection in conn_rfds:
                    data = connection.recv(1024)
                    if len(data) == 0:
                        break

                    #calculate average bit rate in Mbps
                    data_bits += len(data) * 8.0
                    timediff = time.time() - start
                    if timediff > 0.0:
                        bitrate = (data_bits/timediff)/1000000
            
                    data = "".join(data.split("GET /")).split(" HTTP/")[0]
                    data = urllib.unquote(data).decode("utf-8")
                    xbmc.executebuiltin(str("%s" % data).encode("ascii"))
                    connection.send("HTTP/1.1 200 OK\nContent-type: text/html\n\n%s" % data)
                    connection.close()
                    conn_closed = 1
            
                #break if we have a timeout condition
                else:
                    break
        
            #close the inbound connection
            if conn_closed == 0:
                connection.close()

    #close the server on exit
    server_socket.close()

if (__name__ == "__main__"):
    command = sys.argv[1]

    if command == "run_server": run_server()