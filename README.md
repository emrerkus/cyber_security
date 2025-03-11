# netsearch.py

netsearch.py ile yerel ağınızdaki IP adreslerini ve ilgili MAC adreslerini görebilir ve dilerseniz istediğiniz IP adresinin detaylı bilgilerine (eğer varsa) ulaşabilirsiniz.
Kullanımı aşağıdaki gibi:
> python netsearch.py -s <ip_aralığı (192.168.1.1/24 gibi)>

ya da,

> python netsearch.py -n <incelemek_istediğiniz_ip>

# arp_poisoning.py

arp poisoning ile ağ arasında ortaya geçebilir ve wireshark gibi ağ trafiği izleme tool'ları ile ağ trafiğini izleyebilirsiniz.
Kullanımı aşağıdaki gibi:
> python arp_poisoning.py -t <hedef_ip> -g <modem_ip>
