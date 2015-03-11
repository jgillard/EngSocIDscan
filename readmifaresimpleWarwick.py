import os
import rfidiot
from time import sleep

card_present = False
while card_present is False:
    try:
        card = rfidiot.card
        card_present = True
    except:
        sleep(0.1)
        pass


if not card.select():
    card.waitfortag('')

# set options
block = 004
goodkey = 'A0A1A2A3A4A5'
goodkeytype = 'AA'

card.login(block, goodkeytype, goodkey)

if card.readMIFAREblock(block):
    IDstring = card.ReadablePrint(card.ToBinary(card.MIFAREdata))
    print IDstring
    IDnumber = IDstring[0:7]
    print(IDnumber)
