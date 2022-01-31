# import pcapy as p
from scapy.all import *
# import PyX
from scapy.layers.inet import IP, Ether
from scapy.layers.l2 import Dot1Q

a = " "

data = "d:/gfp_handler-078CDCB8_dump_.pcap"
# a = rdpcap(data)
# a[0].show()
# print(a[0].len)
# print(a[0].load.hex())
dd = defaultdict()
prio = defaultdict()
l2tp_ident = defaultdict()
adresses = {}


def proccess_chan(chan):
    sapi = chan[0] & 0x20 | chan[0] & 0x40 | chan[0] & 0x80
    tei = chan[0] & 0x02 | chan[0] & 0x04 | chan[0] & 0x08 | chan[0] & 0x10
    sapi = sapi >> 5
    tei = tei >> 1
    element_id = chan[0]
    a = chan[2] & 0x10
    b = chan[2] & 0x20
    c = chan[2] & 0x40
    d = chan[2] & 0x80
    seq_number = a | b | c | d
    # seq_number = chan[2] >> 4

    # res3 = chan[4] << 0x0f
    res3 = (chan[4] & 0x80)
    speech_or_data_indicator = (chan[3] & 0x02 | chan[3] & 0x01)
    dtxu = chan[2] & 0x80
    dtxd = chan[2] & 0x40

    if dtxu == 0x80:
        dtxu = 'isx'
    else:
        dtxu = None
    if dtxd == 0x40:
        dtxd = 'vx'
    else:
        dtxd = None

    ts_number = chan[2] >> 5

    res4 = chan[5] >> 4
    chan_id = chan[0] << 8
    # id_= chan_id | res2 | res3 | res4
    # return (chan[0:2].hex(), res)
    return element_id, sapi, tei, seq_number, res3, res4, speech_or_data_indicator, dtxd, dtxu, ts_number


def process_sub_chan(sub_chan, vlan_id, pkt):
    pos = 0
    # i=0
    while pos < len(sub_chan):
        sub_sub_chan = sub_chan[pos:sub_chan[pos + 1]]
        # sub_sub_chan = sub_chan[i*sub_chan[1]:i*sub_chan[1]+sub_chan[1]]
        if len(sub_sub_chan) > 2:
            element_id, api, tei, seq_number, res3, res4, speech_or_data_indicator, \
            dtxd, dtxu, ts_number = proccess_chan(sub_sub_chan)
            typee = sub_sub_chan[pos] >> 5
            # name = f"test/{vlan_id}{adress[0]}_{adress[1]}.bin"
            dd = pkt.payload.payload.payload
            # pp = dd.load[0:9]
            # pkt.show()
            f = raw(dd.load[0:12]) + raw(sub_sub_chan)
            p = Ether(src=pkt.src, dst=pkt.dst) / Dot1Q(prio=pkt.prio, id=pkt.id) / IP(proto=pkt.proto,
                                                                                       dst=pkt.payload.payload.src,
                                                                                       src=pkt.payload.payload.dst) / f
            if speech_or_data_indicator == 0:
                name2 = f'test4/{hex(element_id)}_' \
                        f'{ts_number}_{dtxd if dtxd else dtxu if dtxu else None}.pcap'
            else:
                name2 = f'test4/{speech_or_data_indicator}.pcap'
            write_pcap(p, name2)
            """
            if typee == 2:
                name2 = f"test2/tei_{tei}_{seq_number}_{res4}.pcap"
                write_pcap(p,name2)
            elif typee == 1:
                name2 = f"test2/tei_{sub_sub_chan[0]}.pcap"
                write_pcap(p, name2)
            """
        pos += sub_sub_chan[1]
        """""
        if vlan_id in adresses:
            if adress[0] in adresses[vlan_id]:
                    #Если двухбатовый адрес встречался
                if adress[1] in adresses[vlan_id][adress[0]]:
                        #Если подканал внтури канала встречался
                    adresses[vlan_id][adress[0]][adress[1]].append(sub_sub_chan)
                    name = f"test/{vlan_id}{adress[0]}_{adress[1]}.bin"
                    #write_to_file(sub_sub_chan, name)
                else:
                        #Если подканала в канале еще не было
                    adresses[vlan_id][adress[0]][adress[1]] = [sub_sub_chan]
                    name = f"test/{vlan_id}{adress[0]}_{adress[1]}.bin"
                    #write_to_file(sub_sub_chan, name)
            else:
                    #если двухбайтового адреса не встречалось
                adresses[vlan_id][adress[0]] = {adress[1] : [sub_sub_chan]}
                name = f"test/{vlan_id}{adress[0]}_{adress[1]}.bin"
                #write_to_file(sub_sub_chan, name)

        else:
            adresses[vlan_id] = {adress[0] : {adress[1] : [sub_sub_chan]}}
            name = f"test/{vlan_id}{adress[0]}_{adress[1]}.bin"
            #write_to_file(sub_sub_chan, name)
        """


def write_pcap(filebytes, name):
    wrpcap(name, filebytes, append=True)


def write_to_file(fileBytes, name):
    # fileBytes = bytearray(fileBytes)
    try:
        with open(name, 'rb+') as file:
            file.seek(0, 2)
            file.write(fileBytes)
    except FileNotFoundError as msg:
        with open(name, 'wb') as file_:
            file_.write(fileBytes)


def method(pkt):
    # print(pkt.payload.payload)
    try:
        if pkt.payload.proto == 115:
            b = pkt.payload.payload
            p = b.payload
            if len(p.load) > 12:
                d = p.load[12:]
                process_sub_chan(d, pkt.payload.prio, pkt)
    except AttributeError as s:
        pass
        # print(f'{s}')
    except IndexError as er:
        pass
        # print(f'ошибка индекса {er}')


sniff(offline=data, prn=method, store=0)

#
