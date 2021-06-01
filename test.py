chan = [0x52,0x25,0x24,0x80,0x81,0x7a]

a = chan[2] & 0x10
b = chan[2] & 0x20
c = chan[2] & 0x40
d = chan[2] & 0x80

res =a|b|c|d
res_res = (chan[2] & 0x10) | (chan[2] & 0x20) | (chan[2] & 0x40) | (chan[2] & 0x80)
print (res, res_res)
res2 = chan[2] >> 4
res3 = chan[4] << 0x0f
res4 = chan[5] >> 4
chan_id = chan[0] << 8

id_= chan_id | res | res3 | res4
#print(id_)
