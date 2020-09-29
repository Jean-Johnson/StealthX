import threading
import socket
import optparse
import time
import sys
import http.server
import socketserver

knownports = [20, 21, 23, 25, 118, 137, 156, 8080, 4444, 80, 443]

up_ports = []
HOST = ""
interface = ""
count = 0
header = """███████╗████████╗███████╗ █████╗ ██╗  ████████╗██╗  ██╗██╗  ██╗
██╔════╝╚══██╔══╝██╔════╝██╔══██╗██║  ╚══██╔══╝██║  ██║╚██╗██╔╝
███████╗   ██║   █████╗  ███████║██║     ██║   ███████║ ╚███╔╝ 
╚════██║   ██║   ██╔══╝  ██╔══██║██║     ██║   ██╔══██║ ██╔██╗ 
███████║   ██║   ███████╗██║  ██║███████╗██║   ██║  ██║██╔╝ ██╗
╚══════╝   ╚═╝   ╚══════╝╚═╝  ╚═╝╚══════╝╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝
                                                               
"""
parser = optparse.OptionParser(
    header
    + "usage: python3 stealthX.py --host <host ip>\n-i <on/off>\n-f <filename.txt containing port numbers>"
)
parser.add_option("--host", action="store", type="string", dest="HOST")
parser.add_option("-i", action="store", type="string", dest="interface")
parser.add_option("-f", action="store", type="string", dest="fname")
(options, args) = parser.parse_args()
if options.HOST == None:
    print(parser.usage)
    sys.exit(0)


class settrap(threading.Thread):
    def __init__(self, PORT):
        threading.Thread.__init__(self)
        self.PORT = PORT

    def run(self):
        global count
        print("[+]Setting Trap in port ", self.PORT)
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            print("jean")
            try:
                s.bind((options.HOST, self.PORT))
            except:
                print("[!]Port ", self.PORT, " used by another process")
                return
            up_ports.append(self.PORT)
            s.listen(1)
            conn, addr = s.accept()
            with conn:
                count += 1
                print("[!]Intrustion detected on PORT >> ", self.PORT, " from ", addr)
        print("[+]Attack Count= ", count)
        s.close()
        page()
        print("[+]PORT ", self.PORT, " Closed for sometimes")
        time.sleep(40)
        self.run()


class web(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        print("[+]Creating the page")
        time.sleep(2)
        page()
        webPORT = 8000
        Handler = http.server.SimpleHTTPRequestHandler
        with socketserver.TCPServer(("", webPORT), Handler) as httpd:
            print("[+]Interface started on Port ", webPORT)
            httpd.serve_forever()


def page():
    f = open("index.html", "w")
    f.write(
        "<!DOCTYPE html>\n<html>\n<head><title>StealthX</title></head>\n<body>\n<center>\n<h1>StealthX</h1>\n"
    )
    f.write("<h1>Attack Count is " + str(count) + "</h1><br>\n")
    f.write("open ports are>><br>")
    for i in up_ports:
        f.write(str(i) + "<br>")
    f.write("</center>\n</body>\n</html>")
    f.close()


if __name__ == "__main__":
    t = []
    print(header)
    for i in knownports:
        pro = settrap(i)
        t.append(pro)
        pro.start()
    if options.interface == "on":
        pro = web()
        t.append(pro)
        pro.start()
    for td in t:
        td.join()
    print("[-]Exitting Stay Safe")
