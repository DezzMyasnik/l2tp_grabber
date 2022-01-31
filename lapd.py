from scapy.all import *
import init_db
import math
from datetime import datetime

import scapy
from scapy import all
from scapy.all import *
from scapy.arch import IFACES
from paging import proc_paging
import init_db
from logger import *
import IP_collect
# import PyX

a = " "



dd = defaultdict()
prio = defaultdict()
l2tp_ident = defaultdict()
adresses = {}


def process_sub_chan(sub_chan, vlan_id, pkt):
    pos = 0


def write_pcap(filebytes, name):
    wrpcap(name, filebytes, append=True)


def chank(input, n):
    chunks = [input[i:i + n] for i in range(0, len(input), n)]
    return chunks


__gsm0338_base_table = u"@£$¥èéùìòÇ\nØø\rÅåΔ_ΦΓΛΩΠΨΣΘΞ\x1bÆæßÉ !\"#¤%&'()*+,-./0123456789:;<=>?¡ABCDEFGHIJKLMNOPQRSTUVWXYZÄÖÑÜ§¿abcdefghijklmnopqrstuvwxyzäöñüà"
__gsm0338_extra_table = u"````````````````````^```````````````````{}`````\\````````````[~]`|````````````````````````````````````€``````````````````````````"


def __gsm0338Decode(text):
    result = []
    normal_table = True
    for i in text:
        if int(i) == 27:
            normal_table = False
        else:
            if normal_table:
                result += __gsm0338_base_table[int(i)]
            else:
                result += __gsm0338_extra_table[int(i)]
            normal_table = True

    return "".join(result)


def __unpack7bit(content, header_length=0, message_length=0):
    """Decode byte with Default Alphabet encoding ('7bit')
    Function logic inspired from https://github.com/pmarti/python-messaging/blob/master/messaging/utils.py#L173
    Keyword arguments:
      content -- (bytes) Content to decode as hexa
    return: (bytes) Decoded content
    """

    count = last = 0
    result = []
    try:
        for i in range(0, len(content), 2):
            byte = int(content[i:i + 2], 16)
            mask = 0x7F >> count
            out = ((byte & mask) << count) + last
            last = byte >> (7 - count)
            result.append(out)

            if len(result) >= 0xa0:
                break

            if count == 6:
                result.append(last)
                last = 0

            count = (count + 1) % 7

        result = ''.join(map(chr, result))
        return result
        # Convert GSM 7bit encodage (GSM03.38) into normal string
        # return __gsm0338Decode(result[:message_length].encode())
    except ValueError:
        return ''


def get_number(hex_number, type_number):
    number = ''
    res = chank(hex_number, 2)
    if type_number in [209, 208]:  # 0xd1 0xd0
        number = __unpack7bit(hex_number)
    elif type_number in [145, 161, 129, 128]:  # 0x91 0xa1 0x81 0x80
        for item in res:
            number = number + item[::-1].replace('f', '')
    elif type_number == 241:  # 0xf1
        number = __unpack7bit(hex_number)

    return number


def gets_bytes_of_sms(input):
    byte_str = ''
    res = chank(input, 2)
    for item in res:
        byte_str = byte_str + item[::-1]
    return bytes.fromhex(byte_str)


def get_time_of_sms(time_dump):
    res = chank(time_dump, 2)
    byte_str = ''
    for item in res:
        byte_str = byte_str + item[::-1]
    res = chank(byte_str, 2)
    date_t = datetime.strptime(f"{res[0]}/{res[1]}/{res[2]} {res[3]}:{res[4]}:{res[5]}", "%y/%m/%d %H:%M:%S")

    return date_t

def detect_sms_message(byte_flag):
    if byte_flag & 0x09 == 0x9:
        return True
    return  False



def method(pkt):
    # pkt.show()
    # print(pkt.payload.payload.payload)

      # True -работа по файлу False - работа по
    try:
        if file_dir_online in [1,2]:

            #if len(pkt) > 70:
            if len(pkt) > 70 and detect_sms_message(pkt.load[13]) and pkt.load[14] == 0x01:
                    proc_sms(pkt)
            elif pkt.load[4]==0xaa and pkt.load[5]==0x18:
                proc_paging(pkt)
        else:
            payload_lapd = pkt.payload.payload.payload
            IP_collect.ip_collect(payload_lapd.load)
            """
            if len(payload_lapd)>41  and payload_lapd.load[40]==0x04:
                paket = raw(payload_lapd.load[41:])
                if len(paket)>60 and detect_sms_message(paket[13]) and paket[14] == 0x01:
                    proc_sms(paket)
            """



    except BaseException as s:
        log.error(f"3:{datetime.now()}\t{s} \t ") #{raw(payload_lapd.load).hex()}
        # print(f'{s}')


def proc_sms(pkt):
    len_of_rp_number = int(raw(pkt.load[18:19]).hex(), 16)  # длина входящего номера
    type_of_rp_number = int(raw(pkt.load[19:20]).hex(), 16)  # тип входящего номера
    type_of_tp_number = int(raw(pkt.load[30:31]).hex(), 16)  # тип исходящего номера
    len_of_tp_number = int(math.ceil(int(raw(pkt.load[29:30]).hex(), 16) / 2))  # длина исходящего номера,
    # в пакете указывается в десятичных символах, в байтовом представленнии делиться на два

    rp_number = get_number(raw(pkt.load[20:20 + 6]).hex(), type_of_rp_number)  # входящий номер
    tp_number = get_number(raw(pkt.load[31:31 + len_of_tp_number]).hex(), type_of_tp_number)  # исходящий номер

    position_of_len = 31 + len_of_tp_number + 2 + 7
    detect_multipart_sms = int(raw(pkt.load[28:29]).hex(), 16)
    time_of_sms = get_time_of_sms(raw(pkt.load[(31 + len_of_tp_number + 2):(31 + len_of_tp_number + 2 + 7)]).hex())
    len_of_sms = int(raw(pkt.load[position_of_len:position_of_len + 1]).hex(), 16)  # длина смс сообщения
    position_of_text = position_of_len + 1
    if detect_multipart_sms == 4:
        multipart = ''
    elif detect_multipart_sms in [64, 68]:
        position_of_header = position_of_len + 1
        tp_user_data = {"user_data_header_len": int(raw(pkt.load[position_of_header:position_of_header + 1]).hex(), 16),
                        'iei': int(raw(pkt.load[position_of_header + 1:position_of_header + 2]).hex(), 16),
                        'lenght': int(raw(pkt.load[position_of_header + 2:position_of_header + 3]).hex(), 16),
                        'mess_id': int(raw(pkt.load[position_of_header + 3:position_of_header + 4]).hex(), 16),
                        'message_parts': int(raw(pkt.load[position_of_header + 4:position_of_header + 5]).hex(), 16),
                        'message_part_number': int(raw(pkt.load[position_of_header + 5:position_of_header + 6]).hex(),
                                                   16)
                        }

        position_of_text = position_of_header + tp_user_data['user_data_header_len'] + 1
        len_of_sms = len_of_sms - tp_user_data['user_data_header_len'] - 1
        multipart = f'{tp_user_data["message_part_number"]}/{tp_user_data["message_parts"]}'

    sms_text = pkt.load[position_of_text:position_of_text + len_of_sms].decode('utf-16be')

    # write_pcap(pkt, 'd:\Workflow\Aleppo\lapd.pcap')
    with init_db.db_session:
        # print(f"{time_of_sms}\t{tp_number}\t{rp_number}\t{sms_text}\t{multipart}")
        init_db.SMS_text(time_of_sms=time_of_sms,
                         From_phone_num=tp_number,
                         To_phone_num=rp_number,
                         sms_text=sms_text,
                         multipart=multipart)
        init_db.commit()
        log.info(f"{time_of_sms}\t{tp_number}\t{rp_number}\t{sms_text}\t{multipart}")


def lapd(packet):
    if packet[0] == 0x01 and packet[1] == 0x00:
        return True

    return False


def get_files_from_dir(path_name):
    path_f = []
    for d, dirs, files in os.walk(path_name):
        for f in files:
            path = os.path.join(d, f)  # формирование адреса
            path_f.append(path)  # добавление адреса в список
    return path_f


# iface =  IFACES.dev_from_index(25)
# pdir = "d:\\Workflow\\Aleppo\\syriantel_1"
# files = get_files_from_dir(pdir)
# sniff(offline=data, prn = method ,store=0)
# sniff(iface=iface,filter="host 192.168.1.201",prn = method)
# for item in files:
#    sniff(offline=item, prn = method ,store=0)
file_dir_online = 3
if __name__ == '__main__':
    log.debug(f'{scapy.all.show_interfaces()}')
    logconfig()


    if file_dir_online==1:
        #Блок для работы по файлу,
        data = "D:\Workflow\Aleppo\syriantel_1\syriatel_new_1_001.pcap"
        sniff(offline=data, prn = method ,store=0)

    elif file_dir_online==2:

        #Блок для работы по директории с файлами
        pdir = "d:\\Workflow\\Aleppo\\syriantel_1"
        files = get_files_from_dir(pdir)
        for item in files:
           sniff(offline=item, prn = method ,store=0)

    elif file_dir_online==3:
        # Блок для работы по сети
        iface = IFACES.dev_from_index(26) # Установить номер сетевой карты, с которой получаются данные.
                                      # информация выводиться на консоль при старте скрипта
        while True:
            try:
                log.debug('Start sms catcher on host 192.167.1.201 dport 8050')
                sniff(iface=iface, filter="host 192.167.1.201", prn=method, store=0)
            except Exception as ex:
                log.debug(f'1:{ex})')
