import threading 
import socket
import optparse
import time
import sys
knownports=[23,22,8080,4444]
HOST=""
count=0
header="""███████╗████████╗███████╗ █████╗ ██╗  ████████╗██╗  ██╗██╗  ██╗
██╔════╝╚══██╔══╝██╔════╝██╔══██╗██║  ╚══██╔══╝██║  ██║╚██╗██╔╝
███████╗   ██║   █████╗  ███████║██║     ██║   ███████║ ╚███╔╝ 
╚════██║   ██║   ██╔══╝  ██╔══██║██║     ██║   ██╔══██║ ██╔██╗ 
███████║   ██║   ███████╗██║  ██║███████╗██║   ██║  ██║██╔╝ ██╗
╚══════╝   ╚═╝   ╚══════╝╚═╝  ╚═╝╚══════╝╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝
                                                               
"""
parser=optparse.OptionParser(header+"usage: %prog --host <host ip>\n--level <number btw 1 to 5>")
parser.add_option("--host",action="store",type="string",dest="HOST")
parser.add_option("--level",action="store",type="int",dest="level")
(options,args)=parser.parse_args()
if(options.HOST == None):
	print(parser.usage)
	sys.exit(0)
class  settrap(threading.Thread):
	def __init__ (self,PORT):
		threading.Thread.__init__(self)
		self.PORT=PORT
	def run(self):
		global count
		print("[+]Setting Trap for port ", self.PORT)
		with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as s:
			s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
			s.bind((HOST,self.PORT))
			s.listen(1)
			conn, addr=s.accept()
			with conn:
				count+=1
				print("[!]Intrustion detected on PORT >> ",self.PORT," from ",addr)
		print("[+]Attack Count= ",count)
		s.close()
		print("[+]PORT ",self.PORT," Closed for sometimes")
		time.sleep(40)
		self.run()
if __name__ == "__main__":
	t=[]
	print(header)
	for i in knownports:
		pro=settrap(i)
		t.append(pro)
		pro.start()
	for td in t:
		td.join()
	print("[-]Exitting Stay Safe")
