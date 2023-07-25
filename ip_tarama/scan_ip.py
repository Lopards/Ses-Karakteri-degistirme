import nmap

"""def get_mac_address(ip_address):
    nm = nmap.PortScanner()
    nm.scan(ip_address, arguments='-sn')
    hosts = nm.all_hosts()
    if len(hosts) > 0:
        host = hosts[0]
        if 'mac' in nm[host]['addresses']:
            mac_address = nm[host]['addresses']['mac']
            return mac_address

    return "Bilinmeyen"

scanner = nmap.PortScanner()
scanner.scan('192.168.1.0/24', arguments='-sn')
hosts = scanner.all_hosts()

print("Ağdaki tüm cihazların IP ve MAC adresleri:")
for host in hosts:
    if 'mac' in scanner[host]['addresses']:
        ip_address = scanner[host]['addresses']['ipv4']
        mac_address = get_mac_address(ip_address)
        print(ip_address, mac_address)

"""

def scan_ip():
    nm = nmap.PortScanner()
    nm.scan('192.168.1.0/24', arguments='-sn')
    hosts = nm.all_hosts()

    print("Ağdaki tüm cihazların IP ve MAC adresleri:")
    for host in hosts:
        if 'mac' in nm[host]['addresses']:
            ip_address = nm[host]['addresses']['ipv4']
            mac_address = nm[host]['addresses']['mac']
            print(ip_address, mac_address)

scan_ip()
