# IPSEC Tunnel Generator #

1. This script generates the needed config to get an IPSEC tunnel between two PAN firewalls

2. You need to fill out the required information in the JSON file

3. The naming structure for the output is as follows below:

For example, lets say NYC01 is the local site and NYC04 is the remote site:
 
Crypto Profile: NYC01-NYC04-IKE-Crypto
IKE GW: NYC01-NYC04-IPSec-Crypto
IPSEC Tunnel: NYC01-NYC04-IPSec-Tunnel
Zone: VPN-NYC04-NYC01




