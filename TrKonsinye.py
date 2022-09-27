from phBot import *
from time import localtime, strftime
from threading import Timer
import QtBind
import struct
import random
import json
import urllib.request
import os

pName = 'TrKonsinye'
pVersion = '1.0.0'
pUrl = 'https://raw.githubusercontent.com/TheMoB41/TrPlugins/main/TrKonsinye.py'

path = get_config_dir()[:-7]

gui = QtBind.init(__name__, pName)

PageIndex = 0
ItemCount = 0
Started = False


button1 = QtBind.createButton(gui, 'button_search', '    ARA    ', 500, 32)
lstItems = QtBind.createList(gui,10,62,580,200)
lblBuy = QtBind.createLabel(gui,'##OTO SATIN ALMA##\n    ##SEÇENEKLERİ##',600,10)
lblBuy = QtBind.createLabel(gui,'ITEM ADLARI :',600,40)
txtAddItem = QtBind.createLineEdit(gui,"",600,55,120,20)
lstBuyItems = QtBind.createList(gui,600,102,120,80)
button1 = QtBind.createButton(gui, 'button_add', '                EKLE               ', 600, 77)
button1 = QtBind.createButton(gui, 'button_remove', '               SİL              ', 600, 182)
lblBuy = QtBind.createLabel(gui,'MAX FİIYAT :',600,205)
txtMaxPrice = QtBind.createLineEdit(gui,"0",600,218,120,20)
lblBuy = QtBind.createLabel(gui,'MİN. ADET : ',600,238)
txtQuantity = QtBind.createLineEdit(gui,"0",600,253,120,20)
buttonStart = QtBind.createButton(gui, 'button_start', '               BAŞLAT               ', 600, 280)
lblClass = QtBind.createLabel(gui,'SINIF :',10,10)
ComboClass = QtBind.createCombobox(gui,10,32,150,22)
lblType = QtBind.createLabel(gui,'CİNS :',170,10)
ComboType = QtBind.createCombobox(gui,170,32,150,22)
lblDegree = QtBind.createLabel(gui,'DEGREE :',330,10)
ComboDegree = QtBind.createCombobox(gui,330,32,150,22)
def button_start():
	global Started, PageIndex, ItemCount
	if not Started:
		Started = True
		QtBind.setText(gui,buttonStart,'               DURDUR               ')
		EnterConsignmentNPC()
	elif Started:
		PageIndex = 0
		ItemCount = 0
		Started = False
		QtBind.setText(gui,buttonStart,'               BAŞLAT               ')
		ExitNPC()
def button_search():
	global Started
	QtBind.clear(gui,lstItems)
	Started = 'Search'
	EnterConsignmentNPC()
def button_add():
	item = QtBind.text(gui,txtAddItem)
	QtBind.append(gui,lstBuyItems,item)
	QtBind.setText(gui, txtAddItem,"")
	log('Plugin: ITEM EKLENDİ : [%s]' %item)
def button_remove():
	item = QtBind.text(gui,lstBuyItems)
	QtBind.remove(gui,lstBuyItems,item)
	log('Plugin: İTEM SİLİNDİ : [%s]' %item)
def LoadList(List):
	QtBind.clear(gui,ComboType)
	QtBind.clear(gui,ComboDegree)
	if List == 'All':
		for item in ItemList:
			QtBind.append(gui,ComboClass,item)
def LoadDegree():
	QtBind.clear(gui,ComboDegree)
	for i in range(1,16):
		QtBind.append(gui,ComboDegree,str(i))
SelectedClass = ''
SelectedType = ''
NeedsDegree = ['Attribute Stone','Element','Alchemic Stone','Socket Stone','Earring','Necklace','Ring','Garment','Armor','Protector','Blade','Bow','Shield','Spear','Sword','Glaive','Heavy Armor','Light Armor','Robe','Clearic Rod','Crossbow','Dagger','Dual Axe','Harp','One-handed Sword','Staff','Two-handed Sword','Warlock Rod','Fortress Weapon','Job Accessproes','Job Reinforcement','Job Armor','Job Weapons']
def event_loop():
	global SelectedClass, SelectedType
	if not Started:
		CurrentClass = QtBind.text(gui, ComboClass)
		CurrentType = QtBind.text(gui, ComboType)
		if SelectedClass != CurrentClass:
			QtBind.clear(gui,ComboType)
			QtBind.clear(gui,ComboDegree)
			SelectedClass = CurrentClass
			for item in ItemList[SelectedClass][0]:
				QtBind.append(gui,ComboType,item)
		if SelectedType != CurrentType:
			SelectedType = CurrentType
			if SelectedType in NeedsDegree:
				LoadDegree()
			else:
				QtBind.clear(gui,ComboDegree)
def RequestPage(Page):
	if Page == 0:
		p = b'\x01'
	if Page >= 1:
		p = b'\x03'
	p += struct.pack('B',Page)
	CurrentClass = QtBind.text(gui, ComboClass)
	CurrentType = QtBind.text(gui, ComboType)
	CurrentDegree = QtBind.text(gui, ComboDegree)
	if CurrentDegree == '':
		CurrentDegree = 0
	ItemIndex = ItemList[SelectedClass][0][CurrentType]
	p += struct.pack('<I',ItemIndex)
	p += struct.pack('<H',int(CurrentDegree))
	p += b'\x00'
	inject_joymax(0x750C,p,False)
def EnterConsignmentNPC():
	npcs = get_npcs()
	for key, npc in npcs.items():
		if npc['servername'].startswith('NPC_OPEN_MARKET'):
			log("Plugin: NPC GİRİŞİ YAPILIYOR.")
			p = struct.pack('<I', key)
			inject_joymax(0x7045,p, False)
			p += b'\x23'
			inject_joymax(0x7046,p, False)
			Timer(2.0,RequestPage(0)).start()
			return
	log('Plugin: KONSİNYE NPCSİ YAKININDA DEĞİLSİN !')

def ExitNPC():
	inject_joymax(0x7507,b'',False)
	npcs = get_npcs()
	for key, npc in npcs.items():
		if npc['servername'].startswith('NPC_OPEN_MARKET'):
			log("Plugin: NPCDEN ÇIKIŞ YAPILIYOR.")
			inject_joymax(0x704B, struct.pack('<I', key), False)
def BuyItem(CharName,ListingID,ItemID):
	p = struct.pack("H", int(len(CharName)))
	p += CharName.encode('ascii')
	p += struct.pack("<I", ListingID)
	p += struct.pack("<I", ItemID)
	inject_joymax(0x750A,p, False)
	Timer(3.0, ExitNPC, ()).start()
def handle_joymax(opcode,data):
	if opcode == 0xB50C:
		global PageIndex, ItemCount, Started
		if data[0] == 1 and Started or Started == 'Search':
			BuyItems = QtBind.getItems(gui,lstBuyItems)
			BuyQuantity = int(QtBind.text(gui, txtQuantity))
			BuyMaxPrice = int(QtBind.text(gui, txtMaxPrice))
			Index = 1
			NumberItemsOnPage = data[Index]
			Index += 1
			NumberOfPages = data[Index]
			Index += 1
			for i in range(NumberItemsOnPage):
				ListingID = struct.unpack_from('<I',data,Index)[0]
				Index += 4
				NameLength = struct.unpack_from('<H',data,Index)[0]
				Index += 2
				CharName = struct.unpack_from('<' + str(NameLength) + 's',data,Index)[0].decode('cp1252')
				Index += NameLength + 1
				ItemID = struct.unpack_from('<I',data,Index)[0]
				ItemName = get_item(ItemID)['name']
				Index += 4
				Quantity = int(struct.unpack_from('<I',data,Index)[0])
				Index += 4
				Price = int.from_bytes(struct.unpack_from('<8s',data,Index)[0], "little")
				Index += 8
				Index += 8
				ItemCount += 1
				if ItemName in BuyItems and Price <= BuyMaxPrice and Quantity >= BuyQuantity:
					log('Buying [%s][%s] from [%s] for [%s]' %(ItemName,Quantity,CharName,Price))
					BuyItem(CharName,ListingID,ItemID)
					PageIndex = 0
					ItemCount = 0
					Timer(10.0, EnterConsignmentNPC, ()).start()
					return
				itemdata = 'SATICI: [%s] ADET: [%s] FİYAT: [%s] ITEM :[%s]' %(CharName,Quantity,Price,ItemName)
				QtBind.append(gui,lstItems,itemdata)
			if PageIndex < NumberOfPages:
				PageIndex += 1
				Timer(1.0,RequestPage(PageIndex)).start()
			else:
				log("Plugin: TÜM İTEMLERİN KONTROLÜ TAMAMLANDI... TOPLAM İTEMLER : [%s]" %ItemCount)
				PageIndex = 0
				ItemCount = 0
				Timer(1.0, ExitNPC, ()).start()
				if Started != 'Search':
					Timer(20.0, EnterConsignmentNPC, ()).start()
				else:
					Started = False
	return True
ItemList = {
    "Alchemy": [
        {
            'Attribute Stone': 37,
            'Element': 35,
            'Elixir': 33,
            'Alchemic Stone': 36,
            'Alchemic Ingredient': 39,
            'Upgrade Ingredient': 63,
            'Socket Stone': 34
        }
    ],
    "Expendables": [
        {
            'Arrow': 46,
            'Pills': 43,
            'Enchancement': 45,
            'Recovery Potion': 42,
            'Return/Res.': 44
        }
    ],
    "Chinese Accessory": [
        {
            'Earring': 11,
            'Necklace': 10,
            'Ring': 12
        }
    ],
    "Chinese Armor": [
        {
            'Garment': 9,
            'Armor': 7,
            'Protector': 8
        }
    ],
    "Chinese Weapon": [
        {
            'Blade': 2,
            'Bow': 5,
            'Shield': 6,
            'Spear': 3,
            'Sword': 1,
            'Glaive': 4
        }
    ],
    "COS": [
        {
            'COS': 40,
            'COS Items': 41,
            'Fellow Items': 64
        }
    ],
    "Dress": [
        {
            'Avatar Dress': 30,
            'Additional Dress': 31,
            'Awakening Item': 32,
            'Triangluar Conflict': 29
        }
    ],
    "Others": [
        {
            'Transformation': 52,
            'Chatting': 55,
            'Others': 57,
            'Repair': 56,
            'Skill': 54,
            'Special Items': 53
        }
    ],
    "European Accessory": [
        {
            'Earring': 36,
            'Necklace': 26,
            'Ring': 28
        }
    ],
    "European Armor": [
        {
            'Heavy Armor': 23,
            'Light Armor': 24,
            'Robe': 25
        }
    ],
    "European Weapon": [
        {
            'Clearic Rod': 17,
            'Crossbow': 19,
            'Dagger': 20,
            'Dual Axe': 15,
            'Harp': 21,
            'Shield': 22,
            'One-handed Sword': 13,
            'Staff': 18,
            'Two-handed Sword': 14,
            'Warlock Rod': 16
        }
    ],
    "Event": [
        {
            'Event Items': 51
        }
    ],
    "Exchange": [
        {
            'Coin': 50
        }
    ],
    "Fortress War": [
        {
            'Fortress Item': 49,
            'Fortress Weapon': 48
        }
    ],
    "Guild": [
        {
            'Guild Items': 28
        }
    ],
    "Job Equipment": [
        {
            'Job Accessories': 60,
            'Job Reinforcement': 61,
            'Job Armor': 59,
            'Job Items': 62,
            'Job Weapons': 58
        }
    ]
}
LoadList('All')

log("Plugin: "+pName+" v"+pVersion+" BASARIYLA YUKLENDI.")
