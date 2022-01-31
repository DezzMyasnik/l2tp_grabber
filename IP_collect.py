
from scapy.all import *
from scapy.layers.http import HTTPRequest, HTTPResponse
from scapy.layers.inet import IP,Ether

def search_ip(paket):
    try:
        for i,item in enumerate(paket):
            if item == 0x45:
                return i
    except BaseException as ex:
        print(f"4:{ex}")


def ip_collect(payload):
    try:
        pos = search_ip(payload)
        if pos:
            if pos == 32:
                if payload[0]==0x00:
                    ip_packet = IP(raw(payload[pos:]))
                    if ip_packet.proto==132:

                        pkt = Ether(ip_packet.payload)
                        pkt2 = IP(pkt.payload)
                        write_pcap(pkt2, f'test\ip_sctp.pcap')
            else:
                ip_packet = IP(raw(payload[pos:]))
        #ip_packet.show()
                if len(ip_packet) == ip_packet.len:
                    #if ip_packet.sport != 443:
                    #    write_pcap(ip_packet, f'test\ip_{ip_packet.proto}.pcap')
                    if ip_packet.sport==80:
                        ip_packet.show()
                        if ip_packet.haslayer(HTTPResponse):
                            url = ip_packet[HTTPResponse].Host.decode() + ip_packet[HTTPResponse].Path.decode()
                            # get the requester's IP Address
                            ip = ip_packet[IP].src
                            # get the request method
                            method = packet[HTTPResponse].Method.decode()
                            print(f"\n {ip} Requested {url} with {method}")

        else:
            write_pcap(payload, f'test\ip_other.pcap')
    except BaseException as ex:
        pass
        #print(f"5:{ex} {ip_packet} {payload.hex()}")
    #print(ip_packet.dst)
    #if not os.path.exists(f'test\{ip_packet.dst}'):
    #    os.makedirs(f'test\{ip_packet.dst}')
    """
    if ip_packet.proto==6:
        if ip_packet.payload.sport==80:
            if not os.path.exists(f'test\http'):
                os.makedirs(f'test\http')

            write_pcap(ip_packet,f'test\http\{ip_packet.src}-{ip_packet.dst}.pcap')
    """
    #write_pcap(ip_packet,f'test\ip.pcap')

def write_pcap(filebytes, name):
    wrpcap(name, filebytes, append=True)