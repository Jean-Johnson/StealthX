# StealthX
Sort of a Honeypot to slowdown hackers and to get the user informed about the attacks attacks. 
Can be used to prevent novice Hackers

USAGE:
python3 stealthX.py --host <your ip address> -i <on/off>
  --host= specify ur ip
  -i to trun on web interface
  
  eg: python3 stealthX.py --host 0.0.0.0
Feature:
1) Deploy fake ports
2) log the attackers info
3) closes the attacked port
4) very basic Web interface to monitor the attack...
  
StealthX is best suitable to implement in local network.
If you want to implement it in a remotly accessible server, then do port forwarding on the fake ports and 8000(for web interface)
