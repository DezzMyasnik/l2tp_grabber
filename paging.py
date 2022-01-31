from scapy.all import *


def chank(input, n):
    chunks = [input[i:i + n] for i in range(0, len(input), n)]
    number = ''
    for item in chunks:
        number = number + item[::-1].replace('f', '')
    return number

def get_packet_layers(packet):
    counter = 0
    while True:
        layer = packet.getlayer(counter)
        if layer is None:
            break

        yield layer
        counter += 1

dict_of_ms_id_types = {1: 'IMSI',
                       2: 'unk2',
                       3: 'unn3',
                       4: 'TMSI'}

def proc_sub_paging(num_block, packet):
    try:
        list_of_paging = packet.split(sep = b'\x00\x0c',maxsplit=num_block)
        for pag_info in list_of_paging:
            if len(pag_info)>0:
                len_of_payload = int(pag_info[0])
                type_of_ms_id = pag_info[1]&0x01 | pag_info[1]&0x02 | pag_info[1]&0x04
                ms_id = pag_info[2:2 + len_of_payload - 1]

                if pag_info[1] & 0x08 == 8:
                    identiti_dig = (pag_info[1]&0x10 | pag_info[1]&0x20 | pag_info[1]&0x40 | pag_info[1]&0x80)>>4

                    res = chank(ms_id.hex(),2)
                    ms_id = f'{identiti_dig}{res}'
                else:
                    ms_id = f'{ms_id.hex()}'
                ss = pag_info.hex()
                ttt = pag_info[1+len_of_payload]
                paging_group = pag_info[1 + len_of_payload] & 0x01 | \
                           pag_info[1 + len_of_payload] & 0x02 | \
                           pag_info[1 + len_of_payload] & 0x04  | \
                           pag_info[1 + len_of_payload] & 0x08  | \
                           pag_info[1 + len_of_payload] & 0x10  | \
                           pag_info[1 + len_of_payload] & 0x20  | \
                           pag_info[1 + len_of_payload] & 0x40

                print(f"{dict_of_ms_id_types[type_of_ms_id]} \t {ms_id} \t {paging_group}")
    except BaseException as ex:
        print(ex)


def proc_paging(packet):
    SPARE = (packet.load[6] & 0x80 | packet.load[6] & 0x40 | packet.load[6] & 0x20 | packet.load[6] & 0x10)>>4
    paging_msg_num = packet.load[6] &  0x1 | packet.load[6] &  0x2 | packet.load[6] &  0x4 | packet.load[6] &  0x8
    paging_load = raw(packet.load[7:])
    proc_sub_paging(paging_msg_num, paging_load)

    #print(paging_msg_num)