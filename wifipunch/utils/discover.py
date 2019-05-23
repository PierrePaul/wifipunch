#!/usr/bin/env python

import sys
import argparse
from datetime import datetime
from scapy.all import srp,Ether,ARP
import socket


def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("10.255.255.255", 80))
    local_ip = s.getsockname()[0]
    s.close()
    return local_ip


def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--target", dest="target",
                        help="Target IP/IP Range")
    options = parser.parse_args()
    return options


def scan(ip=None):
    if ip is None:
        ip = "192.168.2.0/24"
    arp_request = ARP(pdst=ip)
    broadcast = Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast/arp_request
    answered_list = srp(arp_request_broadcast, timeout=1, verbose=False)[0]
    clients_list = []
    for element in answered_list:
        client_dict = {"ip": element[1].psrc, "mac": element[1].hwsrc}
        clients_list.append(client_dict)
    return clients_list


def print_result(results_list):
        print("IP\t\t\tMAC Address")
        print("----------------------------------------------------")
        for client in results_list:
            print(client["ip"] + "\t\t" + client["mac"])


if __name__ == "__main__":
    options = get_arguments()
    if options.target is None:
        local_ip = get_local_ip()
        ip_range = local_ip[0:local_ip.rfind('.')] + '.0/24'
        scan_result = scan(ip_range)
    else:
        scan_result = scan(options.target)

    print_result(scan_result)
