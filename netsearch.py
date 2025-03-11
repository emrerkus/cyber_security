import scapy.all as scapy
import argparse
import nmap

def netsearch(target_ip):
	arp_request = scapy.ARP(pdst=target_ip)
	broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
	combined_packet = broadcast/arp_request
	
	answered_list = scapy.srp(combined_packet, timeout=1, verbose=False)[0]
	print("IP Addresses and MAC addresses")
	print("------------------------------")
	for element in answered_list:
		print(f"ip address: {element[1].psrc}  mac address: {element[1].hwsrc}")


def nmap_search(target_ip):
	nm = nmap.PortScanner()
	nm.scan(target_ip, "22-443")
	titles = list(nm[target_ip])
	for title in titles:
		print(f"{title}:")
		if type(nm[target_ip][title]) == list:
			subtitles = nm[target_ip][title][0].keys()
			for subtitle in subtitles:
				print(f"   {subtitle}: {nm[target_ip][title][0][subtitle]}")
		else:
			subtitles = nm[target_ip][title].keys()
			for subtitle in subtitles:
				print(f"   {subtitle}: {nm[target_ip][title][subtitle]}")

parser = argparse.ArgumentParser(description="Perform ARP scan to discover IP and MAC addresses on a network.")
parser.add_argument("-s", "--search", dest="search", required=False, help="Target IP or IP range(e.g., 192.168.1.1/24)")
parser.add_argument("-n", "--nmap", dest="nmap", required=False, help="Target IP(e.g., 192.168.1.10)")

args = parser.parse_args()

if args.search:
	netsearch(args.search)
elif args.nmap:
	nmap_search(args.nmap)
