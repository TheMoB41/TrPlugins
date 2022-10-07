from phBot import *
import urllib.request
from threading import Timer
from datetime import datetime, timedelta
import datetime
import phBotChat
import QtBind
import struct
import random
import json
import os
import sqlite3
import signal
import subprocess

pName = 'TrController'
pVersion = '1.0.7'
pUrl = 'https://raw.githubusercontent.com/TheMoB41/TrPlugins/main/TrController.py'

# KURULUM
path = get_config_dir()[:-7]
StartBotAt = 0
CloseBotAt = 0
CheckStartTime = False
CheckCloseTime = False
SkipCommand = False
delay_counter = 0
BtnStart = False
Recording = False
RecordedPackets = []
ExecutedPackets = []
Index = 0
# KURESELLER
inGame = None
followActivated = False
followPlayer = ''
followDistance = 0
#GUI
gui = QtBind.init(__name__,pName)
lblxControl01 = QtBind.createLabel(gui,'TrController:\n * TheMoB TARAFINDAN DUZENLENMISTIR. \n * FEEDBACK SISTEMLI BIR YAZILIMDIR. \n * HATA VE ONERI BILDIRIMLERINIZI BANA ULASTIRABILIRSINIZ. \n\n * KOMUT DETAYLARI ICIN "TrINFO" PLUGININE GOZ ATABILIRSINIZ..',350,235)
tbxLeaders = QtBind.createLineEdit(gui,"",550,11,100,20)
lstLeaders = QtBind.createList(gui,550,32,140,48)
btnAddLeader = QtBind.createButton(gui,'btnAddLeader_clicked',"LIDER EKLE",655,10)
btnRemLeader = QtBind.createButton(gui,'btnRemLeader_clicked',"LIDER SIL",560,85)
LvlSaveName = QtBind.createLabel(gui,'CMD KAYIT İSMİ : ',10,13)
SaveName = QtBind.createLineEdit(gui,"",95,10,120,20)
RecordBtn = QtBind.createButton(gui, 'button_start', ' KAYIT BAŞLAT ', 220, 10)
Display = QtBind.createList(gui,20,50,280,180)
ShowCommandsBtn = QtBind.createButton(gui, 'button_ShowCmds', ' MEVCUT KAYITLI \n CMDLERİ GÖRÜNTÜLE ', 20, 240)
DeleteCommandsBtn = QtBind.createButton(gui, 'button_DelCmds', ' CMD SİL ', 145, 240)
ShowPacketsBtn = QtBind.createButton(gui, 'button_ShowPackets', ' PAKETLERİ GÖSTER ', 220, 240)
cbxShowPackets = QtBind.createCheckBox(gui, 'cbxAuto_clicked','PAKETLERİ GÖSTER ', 220, 265)
QtBind.createLabel(gui,'OTO TARGET : ',340,10)
QtBind.createList(gui,340,25,105,45)
cbxEnabled = QtBind.createCheckBox(gui,'cbxDoNothing','ETKİNLEŞTİR',345,30)
cbxDefensive = QtBind.createCheckBox(gui,'cbxDoNothing','DEFANSIF MOD',345,45)
QtBind.createLabel(gui,'GO MESAJ KOMUTLARI : ',345,120)
QtBind.createList(gui,345,140,170,70)
cbxGOAll = QtBind.createCheckBox(gui,"cbxGOAll_clicked","GO ALL MESAJ AKTİF ET !",350,145)
cbxGOParty = QtBind.createCheckBox(gui,"cbxGOParty_clicked","GO PARTY MESAJ AKTİF ET !",350,160)
cbxGOGuild = QtBind.createCheckBox(gui,"cbxGOGuild_clicked","GO GUILD MESAJ AKTİF ET !",350,175)
cbxGOUnion = QtBind.createCheckBox(gui,"cbxGOUnion_clicked","GO UNION MESAJ AKTİF ET !",350,190)
QtBind.createLabel(gui,'GOJOB MESAJ KOMUTLARI : ',525,120)
QtBind.createList(gui,525,140,190,70)
cbxGOJobAll = QtBind.createCheckBox(gui,"cbxGOJobAll_clicked","GOJOB ALL MESAJ AKTİF ET !",530,145)
cbxGOJobParty = QtBind.createCheckBox(gui,"cbxGOJobParty_clicked","GOJOB PARTY MESAJ AKTİF ET !",530,160)
cbxGOJobGuild = QtBind.createCheckBox(gui,"cbxGOJobGuild_clicked","GOJOB GUILD MESAJ AKTİF ET !",530,175)
cbxGOJobUnion = QtBind.createCheckBox(gui,"cbxGOJobUnion_clicked","GOJOB UNION MESAJ AKTİF ET !",530,190)
# ______________________________METHODLAR ______________________________ #
# TRController CONFIG YOLU
def getPath():
	return get_config_dir()+pName+"\\"
# KAYITLI CONFIG YOLU (JSON)
def getConfig():
	return getPath()+inGame['server'] + "_" + inGame['name'] + ".json"
# KARAKTER OYUNDAYSA KONTROL ET.
def isJoined():
	global inGame
	inGame = get_character_data()
	if not (inGame and "name" in inGame and inGame["name"]):
		inGame = None
	return inGame
# VARSAYILAN CONFIG AYARI YUKLEME
def loadDefaultConfig():
	QtBind.clear(gui,lstLeaders)
	QtBind.setChecked(gui, cbxEnabled, False)
	QtBind.setChecked(gui, cbxDefensive, False)
	QtBind.setChecked(gui, cbxGOAll, False)
	QtBind.setChecked(gui, cbxGOParty, False)
	QtBind.setChecked(gui, cbxGOGuild, False)
	QtBind.setChecked(gui, cbxGOUnion, False)
	QtBind.setChecked(gui, cbxGOJobAll, False)
	QtBind.setChecked(gui, cbxGOJobParty, False)
	QtBind.setChecked(gui, cbxGOJobGuild, False)
	QtBind.setChecked(gui, cbxGOJobUnion, False)
# ONCEKI KAYITLI TUM CONFIGLERI YUKLEME
def loadConfigs():
	loadDefaultConfig()
	if isJoined():
		if os.path.exists(getConfig()):
			data = {}
			with open(getConfig(),"r") as f:
				data = json.load(f)
			if "Leaders" in data:
				for nickname in data["Leaders"]:
					QtBind.append(gui,lstLeaders,nickname)
			if "Defensive" in data and data['Defensive']:
				QtBind.setChecked(gui, cbxDefensive, True)
			if "Target" in data and data['Target']:
				QtBind.setChecked(gui, cbxEnabled, True)
			if "GOMessageAll" in data:
				if data["GOMessageAll"] == "True":
					QtBind.setChecked(gui, cbxGOAll, True)
			if "GOMessageParty" in data:
				if data["GOMessageParty"] == "True":
					QtBind.setChecked(gui, cbxGOParty, True)
			if "GOMessageGuild" in data:
				if data["GOMessageGuild"] == "True":
					QtBind.setChecked(gui, cbxGOGuild, True)
			if "GOMessageUnion" in data:
				if data["GOMessageUnion"] == "True":
					QtBind.setChecked(gui, cbxGOUnion, True)
			if "GOJobMessageAll" in data:
				if data["GOJobMessageAll"] == "True":
					QtBind.setChecked(gui, cbxGOJobAll, True)
			if "GOJobMessageParty" in data:
				if data["GOJobMessageParty"] == "True":
					QtBind.setChecked(gui, cbxGOJobParty, True)
			if "GOJobMessageGuild" in data:
				if data["GOJobMessageGuild"] == "True":
					QtBind.setChecked(gui, cbxGOJobGuild, True)
			if "GOJobMessageUnion" in data:
				if data["GOJobMessageUnion"] == "True":
					QtBind.setChecked(gui, cbxGOJobUnion, True)
def cbxGOAll_clicked(checked):
	if inGame:
		# Init dictionary
		data = {}
		# Load config if exist
		if os.path.exists(getConfig()):
			with open(getConfig(), 'r') as f:
				data = json.load(f)
		# Add new leader
		if not "GOMessageAll" in data:
			data['GOMessageAll'] = []
		check = QtBind.isChecked(gui,cbxGOAll)
		data['GOMessageAll']=(str(check))
		with open(getConfig(),"w") as f:
			f.write(json.dumps(data, indent=4, sort_keys=True))
def cbxGOParty_clicked(checked):
	if inGame:
		# Init dictionary
		data = {}
		# Load config if exist
		if os.path.exists(getConfig()):
			with open(getConfig(), 'r') as f:
				data = json.load(f)
		# Add new leader
		if not "GOMessageParty" in data:
			data['GOMessageParty'] = []
		check = QtBind.isChecked(gui,cbxGOParty)
		data['GOMessageParty']=(str(check))
		with open(getConfig(),"w") as f:
			f.write(json.dumps(data, indent=4, sort_keys=True))
def cbxGOGuild_clicked(checked):
	if inGame:
		# Init dictionary
		data = {}
		# Load config if exist
		if os.path.exists(getConfig()):
			with open(getConfig(), 'r') as f:
				data = json.load(f)
		# Add new leader
		if not "GOMessageGuild" in data:
			data['GOMessageGuild'] = []
		check = QtBind.isChecked(gui,cbxGOGuild)
		data['GOMessageGuild']=(str(check))
		with open(getConfig(),"w") as f:
			f.write(json.dumps(data, indent=4, sort_keys=True))
def cbxGOUnion_clicked(checked):
	if inGame:
		# Init dictionary
		data = {}
		# Load config if exist
		if os.path.exists(getConfig()):
			with open(getConfig(), 'r') as f:
				data = json.load(f)
		# Add new leader
		if not "GOMessageUnion" in data:
			data['GOMessageUnion'] = []
		check = QtBind.isChecked(gui,cbxGOUnion)
		data['GOMessageUnion']=(str(check))
		with open(getConfig(),"w") as f:
			f.write(json.dumps(data, indent=4, sort_keys=True))
def cbxGOJobAll_clicked(checked):
	if inGame:
		# Init dictionary
		data = {}
		# Load config if exist
		if os.path.exists(getConfig()):
			with open(getConfig(), 'r') as f:
				data = json.load(f)
		# Add new leader
		if not "GOJobMessageAll" in data:
			data['GOJobMessageAll'] = []
		check = QtBind.isChecked(gui,cbxGOJobAll)
		data['GOJobMessageAll']=(str(check))
		with open(getConfig(),"w") as f:
			f.write(json.dumps(data, indent=4, sort_keys=True))
def cbxGOJobParty_clicked(checked):
	if inGame:
		# Init dictionary
		data = {}
		# Load config if exist
		if os.path.exists(getConfig()):
			with open(getConfig(), 'r') as f:
				data = json.load(f)
		# Add new leader
		if not "GOJobMessageParty" in data:
			data['GOJobMessageParty'] = []
		check = QtBind.isChecked(gui,cbxGOJobParty)
		data['GOJobMessageParty']=(str(check))
		with open(getConfig(),"w") as f:
			f.write(json.dumps(data, indent=4, sort_keys=True))
def cbxGOJobGuild_clicked(checked):
	if inGame:
		# Init dictionary
		data = {}
		# Load config if exist
		if os.path.exists(getConfig()):
			with open(getConfig(), 'r') as f:
				data = json.load(f)
		# Add new leader
		if not "GOJobMessageGuild" in data:
			data['GOJobMessageGuild'] = []
		check = QtBind.isChecked(gui,cbxGOJobGuild)
		data['GOJobMessageGuild']=(str(check))
		with open(getConfig(),"w") as f:
			f.write(json.dumps(data, indent=4, sort_keys=True))
def cbxGOJobUnion_clicked(checked):
	if inGame:
		# Init dictionary
		data = {}
		# Load config if exist
		if os.path.exists(getConfig()):
			with open(getConfig(), 'r') as f:
				data = json.load(f)
		# Add new leader
		if not "GOJobMessageUnion" in data:
			data['GOJobMessageUnion'] = []
		check = QtBind.isChecked(gui,cbxGOJobUnion)
		data['GOJobMessageUnion']=(str(check))
		with open(getConfig(),"w") as f:
			f.write(json.dumps(data, indent=4, sort_keys=True))
def ListContains(text,lst):
	text = text.lower()
	for i in range(len(lst)):
		if lst[i].lower() == text:
			return True
	return False
# LISTEYE LIDER EKLEME
def btnAddLeader_clicked():
	if inGame:
		player = QtBind.text(gui,tbxLeaders)
		# LISTEDE CHAR VARSA
		if player and not lstLeaders_exist(player):
			data = {}
			# CONFIG VARSA YUKLE
			if os.path.exists(getConfig()):
				with open(getConfig(), 'r') as f:
					data = json.load(f)
			# YENI LIDER EKLE
			if not "Leaders" in data:
				data['Leaders'] = []
			data['Leaders'].append(player)
			# CONFIGI YENIDEN YAPILANDIR
			with open(getConfig(),"w") as f:
				f.write(json.dumps(data, indent=4, sort_keys=True))
			QtBind.append(gui,lstLeaders,player)
			QtBind.setText(gui, tbxLeaders,"")
			log('Plugin: Lider eklendi.. ['+player+']')
# LISTEDEN LIDER SILME
def btnRemLeader_clicked():
	if inGame:
		selectedItem = QtBind.text(gui,lstLeaders)
		if selectedItem:
			if os.path.exists(getConfig()):
				data = {"Leaders":[]}
				with open(getConfig(), 'r') as f:
					data = json.load(f)
				try:
					# MEVCUT ISIM VARKEN EKLENEN AYNI ISMI SILME
					data["Leaders"].remove(selectedItem)
					with open(getConfig(),"w") as f:
						f.write(json.dumps(data, indent=4, sort_keys=True))
				except:
					pass # DOSYA YOKSA GORMEZDEN GEL
			QtBind.remove(gui,lstLeaders,selectedItem)
			log('Plugin: Lider Silindi.. ['+selectedItem+']')
# LIDER LISTESINDEYSE DEVAM ET
def lstLeaders_exist(nickname):
	nickname = nickname.lower()
	players = QtBind.getItems(gui,lstLeaders)
	for i in range(len(players)):
		if players[i].lower() == nickname:
			return True
	return False
# TELEPORT PAKETLERINI YUKLEME
def inject_teleport(source,destination):
	t = get_teleport_data(source, destination)
	if t:
		npcs = get_npcs()
		for key, npc in npcs.items():
			if npc['name'] == source or npc['servername'] == source:
				log("Plugin: TELEPORT SECILDI.. ["+source+"]")
				# TELEPORT BULUNDUGUNDA SECMEK ICIN.
				inject_joymax(0x7045, struct.pack('<I', key), False)
				# 2 SANIYE GECIKMELI TELEPORT BASLATICI
				Timer(2.0, inject_joymax, (0x705A,struct.pack('<IBI', key, 2, t[1]),False)).start()
				Timer(2.0, log, ("Plugin: TP : ["+destination+"]")).start()
				return
		log('Plugin: NPC BULUNAMADI. YANLIS NPC ADI VEYA SERVER ADI.')
	else:
		log('Plugin: TELEPORT DATA BULUNAMADI. YANLIS TELEPORT ADI VEYA SERVER ADI.')
# MESAJ GONDERMEK
def handleChatCommand(msg):
	# CESIT BELIRLEME
	args = msg.split(' ',1)
	# CESIT BULUNAMADIGINDA
	if len(args) != 2 or not args[0] or not args[1]:
		return
	# UYUMLU MESAJ BULUNDUGUNDA
	t = args[0].lower()
	if t == 'private' or t == 'note':
		# UYUMLU MESAJ BULUNAMADIGINDA
		argsExtra = args[1].split(' ',1)
		if len(argsExtra) != 2 or not argsExtra[0] or not argsExtra[1]:
			return
		args.pop(1)
		args += argsExtra
	# MESAJ CESIDINI KONTROL ET
	sent = False
	if t == "all":
		sent = phBotChat.All(args[1])
	elif t == "private":
		sent = phBotChat.Private(args[1],args[2])
	elif t == "party":
		sent = phBotChat.Party(args[1])
	elif t == "guild":
		sent = phBotChat.Guild(args[1])
	elif t == "union":
		sent = phBotChat.Union(args[1])
	elif t == "note":
		sent = phBotChat.Note(args[1],args[2])
	elif t == "stall":
		sent = phBotChat.Stall(args[1])
	elif t == "global":
		sent = phBotChat.Global(args[1])
	if sent:
		log('Plugin: MESAJ "'+t+'" GONDERILDI.')

# MAX RADIUSTA LOKASYON BELIRLEME
def randomMovement(radiusMax=10):
	# KARISIK POZIYON BELIRLEME
	pX = random.uniform(-radiusMax,radiusMax)
	pY = random.uniform(-radiusMax,radiusMax)
	# SECILEN POZISYONU BELIRLEME
	p = get_position()
	pX = pX + p["x"]
	pY = pY + p["y"]
	# YENI POZISYONU GITME
	move_to(pX,pY,p["z"])
	log("Plugin: POZISYON DEGISTIRILDI. (X:%.1f,Y:%.1f)"%(pX,pY))
# MESAFE KULLANARAK TAKIP BASLATMAK
def start_follow(player,distance):
	if party_player(player):
		global followActivated,followPlayer,followDistance
		followPlayer = player
		followDistance = distance
		followActivated = True
		return True
	return False
# PARTIDEYSE KOMUTLARI AL
def party_player(player):
	players = get_party()
	if players:
		for p in players:
			if players[p]['name'] == player:
				return True
	return False
# PARTY UYESINE RETURN
def near_party_player(player):
	players = get_party()
	if players:
		for p in players:
			if players[p]['name'] == player and players[p]['player_id'] > 0:
				return players[p]
	return None
# A-B NOKTALARI ARASINDA MESEFA HESAPLAMA
def GetDistance(ax,ay,bx,by):
	return ((bx-ax)**2 + (by-ay)**2)**0.5
# TAKIBI DURDUKMAK
def stop_follow():
	global followActivated,followPlayer,followDistance
	result = followActivated
	# stop
	followActivated = False
	followPlayer = ""
	followDistance = 0
	return result

# PET ACTIRMAK
def MountHorse():
	item = GetItemByExpression(lambda n,s: s.startswith('ITEM_COS_C_'),13)
	if item:
		UseItem(item)
		return True
	log('Plugin: ENVANTERDE AT BULUNAMADI.')
	return False
# SECILMIS CESITTEKI PETI ACTIRMAK
def MountPet(petType):
	if petType == 'pick':
		return False
	elif petType == 'horse':
		return MountHorse()
	# TUM ACILABILEN PETLER ICIN
	pets = get_pets()
	if pets:
		for uid,pet in pets.items():
			if pet['type'] == petType:
				p = b'\x01' # mount flag
				p += struct.pack('I',uid)
				inject_joymax(0x70CB,p, False)
				return True
	return False
# PET KAPATMAYI DENEMESI ICIN
def DismountPet(petType):
	petType = petType.lower()
	# ENVANTERDE PICK PET VARSA
	if petType == 'pick':
		return False
	# TUM ACILABILEN PETLER ICIN
	pets = get_pets()
	if pets:
		for uid,pet in pets.items():
			if pet['type'] == petType:
				p = b'\x00'
				p += struct.pack('I',uid)
				inject_joymax(0x70CB,p, False)
				return True
	return False
# SECILEN NPC IDLERI DATADA MEVCUTSA
def GetNPCUniqueID(name):
	NPCs = get_npcs()
	if NPCs:
		name = name.lower()
		for UniqueID, NPC in NPCs.items():
			NPCName = NPC['name'].lower()
			if name == NPCName:
				return UniqueID
	return 0
# ISIM VEYA SERVERDA ITEMI BULMAK
def GetItemByExpression(_lambda,start=0,end=0):
	inventory = get_inventory()
	items = inventory['items']
	if end == 0:
		end = inventory['size']
	for slot, item in enumerate(items):
		if start <= slot and slot <= end:
			if item:
				if _lambda(item['name'],item['servername']):
					item['slot'] = slot
					return item
	return None
# ENVANTER BOS SLOT VARSA
def GetEmptySlot():
	items = get_inventory()['items']
	# check the first empty
	for slot, item in enumerate(items):
		if slot >= 13:
			if not item:
				return slot
	return -1
# ENVANTER HAREKET ENJEKSIYONU
def Inject_InventoryMovement(movementType,slotInitial,slotFinal,logItemName,quantity=0):
	p = struct.pack('<B',movementType)
	p += struct.pack('<B',slotInitial)
	p += struct.pack('<B',slotFinal)
	p += struct.pack('<H',quantity)
	log('Plugin: Moving item "'+logItemName+'"...')
	inject_joymax(0x7034,p,False)
# ITEM GIYMEYI DENE
def EquipItem(item):
	itemData = get_item(item['model'])
	if itemData['tid1'] != 1:
		log('Plugin: '+item['name']+' cannot be equiped!')
		return
	t = itemData['tid2']
	if t == 1 or t == 2 or t == 3 or t == 9 or t == 10 or t == 11:
		t = itemData['tid3']
		# head
		if t == 1:
			Inject_InventoryMovement(0,item['slot'],0,item['name'])
		# shoulders
		elif t == 2:
			Inject_InventoryMovement(0,item['slot'],2,item['name'])
		# chest
		elif t == 3:
			Inject_InventoryMovement(0,item['slot'],1,item['name'])
		# pants
		elif t == 4:
			Inject_InventoryMovement(0,item['slot'],4,item['name'])
		# gloves
		elif t == 5:
			Inject_InventoryMovement(0,item['slot'],3,item['name'])
		# boots
		elif t == 6:
			Inject_InventoryMovement(0,item['slot'],5,item['name'])
	# shields
	elif t == 4:
		Inject_InventoryMovement(0,item['slot'],7,item['name'])
	# accesories ch/eu
	elif t == 5 or t == 12:
		t = itemData['tid3']
		# earring
		if t == 1:
			Inject_InventoryMovement(0,item['slot'],9,item['name'])
		# necklace
		elif t == 2:
			Inject_InventoryMovement(0,item['slot'],10,item['name'])
		# ring
		elif t == 3:
			# Check if second ring slot is empty
			if not GetItemByExpression(lambda s,n: True,11):
				Inject_InventoryMovement(0,item['slot'],12,item['name'])
			else:
				Inject_InventoryMovement(0,item['slot'],11,item['name'])
	# weapon ch/eu
	elif t == 6:
		Inject_InventoryMovement(0,item['slot'],6,item['name'])
	# job
	elif t == 7:
		Inject_InventoryMovement(0,item['slot'],8,item['name'])
	# avatar
	elif t == 13:
		t = itemData['tid3']
		# hat
		if t == 1:
			Inject_InventoryMovement(36,item['slot'],0,item['name'])
		# dress
		elif t == 2:
			Inject_InventoryMovement(36,item['slot'],1,item['name'])
		# accesory
		elif t == 3:
			Inject_InventoryMovement(36,item['slot'],2,item['name'])
		# flag
		elif t == 4:
			Inject_InventoryMovement(36,item['slot'],3,item['name'])
	# devil spirit
	elif t == 14:
		Inject_InventoryMovement(36,item['slot'],4,item['name'])
# ITEM CIKARTMAYI DENE
def UnequipItem(item):
	slot = GetEmptySlot()
	if slot != -1:
		Inject_InventoryMovement(0,item['slot'],slot,item['name'])
def UseItem(item):
	p = struct.pack('<B',item['slot'])
	loc = get_locale()
	tid = GetTIDFromItem(item['model'])
	if loc == 22: # vsro
		p += struct.pack('<H',tid)
	else:
		p += struct.pack('<I',tid)
	log('Plugin: ITEM KULLANILIYOR : "'+item['name']+'"...')
	inject_joymax(0x704C,p,True)
def GetTIDFromItem(itemId):
	conn = GetDatabaseConnection()
	c = conn.cursor()
	c.execute('SELECT cash_item, tid1, tid2, tid3 FROM items WHERE id=?',(itemId,))
	result = c.fetchone()
	result = result[0] + (3 * 4) + (result[1] * 32) + (result[2] * 128) + (result[3] * 2048)
	conn.close()
	return result
def GetDatabaseConnection():
	bot_path = os.getcwd()
	data = {}
	locale = get_locale()
	if locale == 22:
		with open(bot_path+"/vSRO.json","r") as f:
			data = json.load(f)
		server = character_data['server']
		for k in data:
			servers = data[k]['servers']
			if server in servers:
				for path in os.scandir(bot_path+"/Data"):
					if path.is_file() and path.name.endswith(".db3"):
						conn = sqlite3.connect(bot_path+"/Data/"+path.name)
						c = conn.cursor()
						c.execute('SELECT * FROM data WHERE k="path" AND v=?',(data[k]['path'],))
						if c.fetchone():
							return conn
						else:
							conn.close()
	# iSRO
	elif locale == 18:
		return sqlite3.connect(bot_path+"/Data/iSRO.db3")
	# TrSRO
	elif locale == 56:
		return sqlite3.connect(bot_path+"/Data/TRSRO.db3")
	return None
def getnickname(UniqueID):
	# Load all players from party
	players = get_party()

	# Checking if UID is mine
	if UniqueID == inGame['player_id']:
		return inGame['name']

	# Check the UID with all players
	if players:
		for key, player in players.items():
			if player['player_id'] == UniqueID:
				return player['name']
	return ""
def Inject_SelectTarget(targetUID):
	p = struct.pack('<I', targetUID)
	inject_joymax(0x7045, p, False)
# ______________________________ ETKINLIKLER ______________________________ #
# PLUGIN BAGLANTISI
def connected():
	global inGame
	inGame = None
# CHAR OYUNA BAGLANDIGINDA
def joined_game():
	loadConfigs()
def teleported():
	global inGame
	# update uid on teleported
	inGame = get_inGame()
# TUM MESAJ KANALLARINDA KONTROL EDILEBILIR DURUMDA
def handle_chat(t,player,msg):
	# UNION CHATI GORMESI ICIN GUILD ISMI SILME
	if t == 11:
		msg = msg.split(': ',1)[1]
	# KOMUTU VEREN LIDER LISTESINDE YA DA DC UZERINDE MI
	if player and lstLeaders_exist(player) or t == 100:
		# MESAJ KOMUTLARI
		if msg == "BASLAT":
			start_bot()
			log("Plugin: BOT BASLATILDI.")
		elif msg.startswith("GO"):
			msgData = msg[3:].split()
			data = bytearray()
			data.append(int(msgData[0], 16))
			data.append(int(msgData[1], 16))
			data.append(int(msgData[2], 16))
			data.append(int(msgData[3], 16))
			data.append(int(msgData[4], 16))
			data.append(int(msgData[5], 16))
			data.append(int(msgData[6], 16))
			data.append(int(msgData[7], 16))
			data.append(int(msgData[8], 16))
			inject_joymax(0x705A, data, False)
		elif msg.startswith("GJ"):
			msgData = msg[3:].split()
			data = bytearray()
			data.append(int(msgData[0], 16))
			data.append(int(msgData[1], 16))
			data.append(int(msgData[2], 16))
			data.append(int(msgData[3], 16))
			data.append(int(msgData[4], 16))
			data.append(int(msgData[5], 16))
			inject_joymax(0x705A, data, False)
		elif msg == "DURDUR":
			stop_bot()
			log("Plugin: BOT DURDURULDU")
		elif msg.startswith("TRACE"):
			# BOSLUK SILMEK ICIN
			msg = msg.rstrip()
			if msg == "TRACE":
				if start_trace(player):
					log("Plugin: TRACE BU KISIYE BASLATILDI : ["+player+"]")
			else:
				msg = msg[5:].split()[0]
				if start_trace(msg):
					log("Plugin: TRACE BASLATILDI. ["+msg+"]")
		elif msg == "NOTRACE":
			stop_trace()
			log("Plugin: TRACE DURDURULDU.")
		elif msg.startswith("KORKUR"):
			# BOSLUK SILMEK ICIN
			msg = msg.rstrip()
			if msg == "KORKUR":
				p = get_position()
				set_training_position(p['region'], p['x'], p['y'],p['z'])
				log("Plugin: MEVCUT POZISYON ATANDI. (X:%.1f,Y:%.1f)"%(p['x'],p['y']))
			else:
				try:
					# ARGUMENLERI KONTROL ET
					p = msg[6:].split()
					x = float(p[0])
					y = float(p[1])
					# SECILMEMISSE OTOMATIK KONTROL ET
					region = int(p[2]) if len(p) >= 3 else 0
					z = float(p[3]) if len(p) >= 4 else 0
					set_training_position(region,x,y,z)
					log("Plugin: BURAYA POZISYON ATANDI : (X:%.1f,Y:%.1f)"%(x,y))
				except:
					log("Plugin: YANLIS KOORDINAT !")
		elif msg == 'KORAL':
			# MEVCUT POZISYONU KONTROL ET
			pos = get_position()
			phBotChat.Private(player,'CHARIN POZİSYONU : (X:%.1f,Y:%.1f,Z:%1f,Region:%d)'%(pos['x'],pos['y'],pos['z'],pos['region']))
		elif msg.startswith("RANGE"):
			# BOSLUK SILMEK ICIN
			msg = msg.rstrip()
			if msg == "RANGE":
				radius = 35
				set_training_radius(radius)
				log("Plugin: RANGE DEGISTIRILDI : "+str(radius)+" m.")
			else:
				try:
					# RADIUS BELIRLEMEK ICIN
					radius = int(float(msg[9:].split()[0]))
					# PY HATASI ALMAMASI ICIN RADIUS LIMIT BELIRLEME
					radius = (radius if radius > 0 else radius*-1)
					set_training_radius(radius)
					log("Plugin: RADIUS DEGISTIRILDI.o "+str(radius)+" m.")
				except:
					log("Plugin: YANLIS RADIUS DEGERI !")
		elif msg.startswith('SCKUR'):
			msg = msg.rstrip()
			if msg == 'SCKUR':
				set_training_script('')
				log('Plugin: SCRIPT YOLU SIFIRLANDI')
			else:
				set_training_script(msg[9:])
				log('Plugin: SCRIPT YOLU DEGISTIRILDI.')
		elif msg.startswith('ALANKUR '):
			msg = msg[8:]
			if msg:
				if set_training_area(msg):
					log('Plugin: KASILMA ALANI DEGISTIRILDI : ['+msg+']')
				else:
					log('Plugin: KASILMA ALANI ['+msg+'] LISTEDE BULUNAMADI.')
		elif msg == "SIT":
			log("Plugin: OTUR/KALK")
			inject_joymax(0x704F,b'\x04',False)
		elif msg == "JUMP":
			log("Plugin: YATIR YEDIN IYI MI.")
			inject_joymax(0x3091,b'\x0c',False)
		elif msg.startswith("CAPE"):
			# BOSLUK SILMEK ICIN
			msg = msg.rstrip()
			if msg == "CAPE":
				log("Plugin: VARSAYILAN PVP MODU (Yellow)")
				inject_joymax(0x7516,b'\x05',False)
			else:
				# CAPE TIPLERINI BELIRLEMEK ICIN
				cape = msg[4:].split()[0].lower()
				if cape == "off":
					log("Plugin: PVP MODUNDAN CIKILIYOR.")
					inject_joymax(0x7516,b'\x00',False)
				elif cape == "red":
					log("Plugin: PVP MODUNA GECILIYOR. (Red)")
					inject_joymax(0x7516,b'\x01',False)
				elif cape == "gray":
					log("Plugin: PVP MODUNA GECILIYOR. (Gray)")
					inject_joymax(0x7516,b'\x02',False)
				elif cape == "blue":
					log("Plugin: PVP MODUNA GECILIYOR. (Blue)")
					inject_joymax(0x7516,b'\x03',False)
				elif cape == "white":
					log("Plugin: PVP MODUNA GECILIYOR. (White)")
					inject_joymax(0x7516,b'\x04',False)
				elif cape == "yellow":
					log("Plugin: PVP MODUNA GECILIYOR. (Yellow)")
					inject_joymax(0x7516,b'\x05',False)
				else:
					log("Plugin: YANLIS CAPE RENGI !")
		elif msg == "ZERK":
			log("Plugin: ZERK MODUNA GECILIYOR.")
			inject_joymax(0x70A7,b'\x01',False)
		elif msg == "RETURN":
			# OLU OLUP OLMADIGINI KONTROL ETTIRMEK
			character = get_character_data()
			if character['hp'] == 0:
				# OLUYSE
				log('Plugin:SEHRE DONULUYOR.')
				inject_joymax(0x3053,b'\x01',False)
			else:
				log('Plugin: RETURN SCROLL KULLANILIYOR.')
				# SISTEME GORE COK CHAR KULLANILDIGINDA CPU KULLANIMI ARTAR
				Timer(random.uniform(0.5,2),use_return_scroll).start()
		elif msg.startswith("TP"):
			# DEVAMI YOKSA RETURN ATAR
			msg = msg[3:]
			if not msg:
				return
			# FARKLI CHARLARDAN KOMUT ALABILMESI ICIN
			split = ',' if ',' in msg else ' '
			# ARGUMANLARI CIKARTMA
			source_dest = msg.split(split)
			# TP ESNASINDA 2 ISMINDE DOGRULUGUNU KONTROL ETME
			if len(source_dest) >= 2:
				inject_teleport(source_dest[0].strip(),source_dest[1].strip())
		elif msg.startswith("INJECT "):
			msgPacket = msg[7:].split()
			msgPacketLen = len(msgPacket)
			if msgPacketLen == 0:
				log("Plugin: ENJEKTE PAKETTE HATA !")
				return
			# PAKET KONTROLU
			opcode = int(msgPacket[0],16)
			data = bytearray()
			encrypted = False
			dataIndex = 1
			if msgPacketLen >= 2:
				enc = msgPacket[1].lower()
				if enc == 'true' or enc == 'false':
					encrypted = enc == "true"
					dataIndex +=1
			# PAKET DATA OLUSTURMA VE ENJEKTE ETMEK
			for i in range(dataIndex, msgPacketLen):
				data.append(int(msgPacket[i],16))
			inject_joymax(opcode,data,encrypted)
			log("Plugin: PAKET ENJEKTE EDILIYOR. \nOpcode: 0x"+'{:02X}'.format(opcode)+" - Encrypted: "+("Yes" if encrypted else "No")+"\nData: "+(' '.join('{:02X}'.format(int(msgPacket[x],16)) for x in range(dataIndex, msgPacketLen)) if len(data) else 'None'))
		elif msg.startswith("CHAT "):
			handleChatCommand(msg[5:])
		elif msg.startswith("DAGIL"):
			if msg == "DAGIL":
				randomMovement()
			else:
				try:
					radius = int(float(msg[6:].split()[0]))
					radius = (radius if radius > 0 else radius*-1)
					randomMovement(radius)
				except:
					log("Plugin: MAKSIMUM RADIUS YANLIS !")
		elif msg.startswith("FOLLOW"):
			# default values
			charName = player
			distance = 10
			if msg != "FOLLOW":
				# Check params
				msg = msg[6:].split()
				try:
					if len(msg) >= 1:
						charName = msg[0]
					if len(msg) >= 2:
						distance = float(msg[1])
				except:
					log("Plugin: TAKİP MESAFESİ YANLIŞ !")
					return
			# Start following
			if start_follow(charName, distance):
				log("Plugin: BU KİŞİ TAKİP EDİLİYOR : [" + charName + "] MESAFE : [" + str(distance) + "] ")
		elif msg == "NOFOLLOW":
			if stop_follow():
				log("Plugin: TAKİP DURDURULDU..")
		elif msg.startswith("PROFIL"):
			if msg == "PROFIL":
				if set_profile('Default'):
					log("Plugin: VARSAYILAN PROFIL KURULDU.")
			else:
				msg = msg[7:]
				if set_profile(msg):
					log("Plugin: "+msg+" ISIMLI PROFIL KURULDU.")
		elif msg == "DC":
			log("Plugin: BAGLANTI KESILIYOR.")
			disconnect()
		elif msg.startswith("MOUNT "):
			# VARSAYILAN DEGERLER
			pet = "horse"
			if msg != "MOUNT ":
				msg = msg[5:].split()
				if msg:
					pet = msg[0]
			# PET ACMAYI DENE
			if MountPet(pet):
				log("Plugin: PET ACILIYOR. ["+pet+"]")
		elif msg.startswith("DISMOUNT"):
			# VARSAYILAN DEGERLER
			pet = "horse"
			if msg != "DISMOUNT":
				msg = msg[8:].split()
				if msg:
					pet = msg[0]
			# PET KAPATMAYI DENE
			if DismountPet(pet):
				log("Plugin: PET KAPATILIYOR. ["+pet+"]")
		elif msg == "PTAYRIL":
			# PARTIDE MI KONTROL ET
			if get_party():
				# CIKMASI ICIN
				log("Plugin: PARTIDEN AYRILIYOR.")
				inject_joymax(0x7061,b'',False)
		elif msg.startswith("RECALL "):
			msg = msg[7:]
			if msg:
				npcUID = GetNPCUniqueID(msg)
				if npcUID > 0:
					log("Plugin: YENIDEN DOGMA NOKTASI AYARLANIYOR : \""+msg.title()+"\"...")
					inject_joymax(0x7059, struct.pack('I',npcUID), False)
		elif msg.startswith("GIY "):
			msg = msg[6:]
			if msg:
				item = GetItemByExpression(lambda n,s: msg in n or msg == s,13)
				if item:
					EquipItem(item)
		elif msg.startswith("CIKART "):
			msg = msg[8:]
			if msg:
				item = GetItemByExpression(lambda n,s: msg in n or msg == s,0,12)
				if item:
					UnequipItem(item)
		elif msg.startswith("REVERSE "):
			msg = msg[8:]
			if msg:
				msg = msg.split(' ',1)
				if msg[0] == 'RETURN':
					if reverse_return(0,''):
						log('Plugin: SON RETURN KULLANIM NOKTASINA REVERSE KULLANILIYOR')
				elif msg[0] == 'OLUM':
					if reverse_return(1,''):
						log('Plugin: SON OLUM NOKTASINA REVERSE KULLANILIYOR')
				elif msg[0] == 'PLAYER':
					if len(msg) >= 2:
						if reverse_return(2,msg[1]):
							log('Plugin: BU KISIYE REVERSE KULLANILIYOR : "'+msg[1]+'" location')
				elif msg[0] == 'ALAN':
					if len(msg) >= 2:
						if reverse_return(3,msg[1]):
							log('Plugin: BU ALANA REVERSE ATILIYOR : "'+msg[1]+'" location')
		elif msg.startswith("USE "):
			msg = msg[4:]
			if msg:
				item = GetItemByExpression(lambda n,s: msg in n or msg == s,13)
				if item:
					UseItem(item)
		if msg == "TARGETON":
			QtBind.setChecked(gui, cbxEnabled, True)
			log('Plugin: TARGET MODU ETKİNLEŞTİRİLDİ.')
		elif msg == "TARGETOFF":
			QtBind.setChecked(gui, cbxEnabled, False)
			log('Plugin: TARGET MODU KAPATILDI.')
		if msg == "DEFFON":
			QtBind.setChecked(gui, cbxDefensive, True)
			log('Plugin: DEFANS MODU ETKİNLEŞTİRİLDİ.')
		elif msg == "DEFFOFF":
			QtBind.setChecked(gui, cbxDefensive, False)
			log('Plugin: DEFANS MODU KAPATILDI.')
	# GAUCHE EGLENCE KOMUTLARI
		if msg == "WALK":
			log("Plugin: YURUME MODU AKTIF")
			inject_joymax( 0x704F,b'\x02',False)
		elif msg == "RUN":
			log("Plugin: KOSMA MODU AKTIF")
			inject_joymax( 0x704F,b'\x03',False)
		elif msg == "COME":
			log("Plugin: COME ON BABE")
			inject_joymax( 0x3091,b'\x02',False)
		elif msg == "MERHABA":
			log("Plugin: MERHABA CINIM ")
			inject_joymax( 0x3091,b'\x00',False)
		elif msg == "H11":
			log("Plugin: HOTAN FORTRESS 1>1")
			inject_joymax( 0x705A,b'\x02\x00\x00\x00\x02\x99\x00\x00\x00\x02\x00\x00\x00',False)
		elif msg == "H12":
			log("Plugin: HOTAN FORTRESS 1>2")
			inject_joymax( 0x705A,b'\x02\x00\x00\x00\x02\x9A\x00\x00\x00\x02\x00\x00\x00',False)
		elif msg == "H13":
			log("Plugin: HOTAN FORTRESS 1>3")
			inject_joymax( 0x705A,b'\x02\x00\x00\x00\x02\x9B\x00\x00\x00\x02\x00\x00\x00',False)
		elif msg == "H14":
			log("Plugin: HOTAN FORTRESS 1>4")
			inject_joymax( 0x705A,b'\x02\x00\x00\x00\x02\x9C\x00\x00\x00\x02\x00\x00\x00',False)
		elif msg == "H21":
			log("Plugin: HOTAN FORTRESS 2>1")
			inject_joymax( 0x705A,b'\x03\x00\x00\x00\x02\x99\x00\x00\x00\x03\x00\x00\x00',False)
		elif msg == "H22":
			log("Plugin: HOTAN FORTRESS 2>2")
			inject_joymax( 0x705A,b'\x03\x00\x00\x00\x02\x9A\x00\x00\x00\x03\x00\x00\x00',False)
		elif msg == "H23":
			log("Plugin: HOTAN FORTRESS 2>3")
			inject_joymax( 0x705A,b'\x03\x00\x00\x00\x02\x9B\x00\x00\x00\x03\x00\x00\x00',False)
		elif msg == "H24":
			log("Plugin: HOTAN FORTRESS 2>4")
			inject_joymax( 0x705A,b'\x03\x00\x00\x00\x02\x9C\x00\x00\x00\x03\x00\x00\x00',False)
		elif msg == "H31":
			log("Plugin: HOTAN FORTRESS 3>1")
			inject_joymax( 0x705A,b'\x04\x00\x00\x00\x02\x99\x00\x00\x00\x04\x00\x00\x00',False)
		elif msg == "H32":
			log("Plugin: HOTAN FORTRESS 3>2")
			inject_joymax( 0x705A,b'\x04\x00\x00\x00\x02\x9A\x00\x00\x00\x04\x00\x00\x00',False)
		elif msg == "H33":
			log("Plugin: HOTAN FORTRESS 3>3")
			inject_joymax( 0x705A,b'\x04\x00\x00\x00\x02\x9B\x00\x00\x00\x04\x00\x00\x00',False)
		elif msg == "H34":
			log("Plugin: HOTAN FORTRESS 3>4")
			inject_joymax( 0x705A,b'\x04\x00\x00\x00\x02\x9C\x00\x00\x00\x04\x00\x00\x00',False)
		elif msg == "J11":
			log("Plugin: JANGAN FORTRESS 1>1")
			inject_joymax( 0x705A,b'\x08\x00\x00\x00\x02\x31\x00\x00\x00',False)
		elif msg == "J12":
			log("Plugin: JANGAN FORTRESS 1>2")
			inject_joymax( 0x705A,b'\x08\x00\x00\x00\x02\x32\x00\x00\x00',False)
		elif msg == "J13":
			log("Plugin: JANGAN FORTRESS 1>3")
			inject_joymax( 0x705A,b'\x08\x00\x00\x00\x02\x33\x00\x00\x00',False)
		elif msg == "J21":
			log("Plugin: JANGAN FORTRESS 2>1")
			inject_joymax( 0x705A,b'\x09\x00\x00\x00\x02\x31\x00\x00\x00',False)
		elif msg == "J22":
			log("Plugin: JANGAN FORTRESS 2>2")
			inject_joymax( 0x705A,b'\x09\x00\x00\x00\x02\x32\x00\x00\x00',False)
		elif msg == "J23":
			log("Plugin: JANGAN FORTRESS 2>3")
			inject_joymax( 0x705A,b'\x09\x00\x00\x00\x02\x33\x00\x00\x00',False)
		elif msg == "J31":
			log("Plugin: JANGAN FORTRESS 3>1")
			inject_joymax( 0x705A,b'\x0A\x00\x00\x00\x02\x31\x00\x00\x00',False)
		elif msg == "J32":
			log("Plugin: JANGAN FORTRESS 3>2")
			inject_joymax( 0x705A,b'\x0A\x00\x00\x00\x02\x32\x00\x00\x00',False)
		elif msg == "J33":
			log("Plugin: JANGAN FORTRESS 3>3")
			inject_joymax( 0x705A,b'\x0A\x00\x00\x00\x02\x33\x00\x00\x00',False)
		elif msg == "HWT1":
			log("Plugin: HOLY WATER TEMPLE KAT: 1 GİRİŞİ..")
			inject_joymax( 0x705A,b'\x03\x00\x00\x00\x02\xA5\x00\x00\x00',False)
		elif msg == "HWT2":
			log("Plugin: HOLY WATER TEMPLE KAT: 2 GİRİŞİ..")
			inject_joymax( 0x705A,b'\x03\x00\x00\x00\x02\xA6\x00\x00\x00',False)
		elif msg == "HWT3":
			log("Plugin: HOLY WATER TEMPLE KAT: 3 GİRİŞİ..")
			inject_joymax( 0x705A,b'\x03\x00\x00\x00\x02\xA7\x00\x00\x00',False)
# YEDEK
def ResetSkip():
	global SkipCommand
	SkipCommand = False
def LeaveParty(args):
	if get_party():
		inject_joymax(0x7061, b'', False)
		log('Plugin: PTDEN AYRILIYOR..')
	return 0
# Notification,title,message..Bir windows bildirimi göster..(bot simge durumuna küçültülmelidir)
def Notification(args):
	if len(args) == 3:
		title = args[1]
		message = args[2]
		show_notification(title, message)
		return 0
	log('Plugin: YANLIS BILDIRIM KOMUTU..')
	return 0
# NotifyList,message..Listede bir bildirim oluşturun..
def NotifyList(args):
	if len(args) == 2:
		message = args[1]
		create_notification(message)
		return 0
	log('Plugin: YANLIS BILDIRIM KOMUTU..')
	return 0
# PlaySound,ding.wav...WAV DOSYASI PHBOT KLASÖRÜNÜN İÇİNDE OLMALIDIR.
def PlaySound(args):
	FileName = args[1]
	if os.path.exists(path + FileName):
		play_wav(path + FileName)
		log('Plugin: YÜRÜTÜLÜYOR.. [%s]' % FileName)
		return 0
	log('Plugin: SES DOSYASI [%s] BULUNAMADI..' % FileName)
	return 0
# ÖRNEK - SetScript,Mobs103.txt
# SCRİPT PHBOT KLASÖRÜNDE OLMALIDIR.
def SetScript(args):
	name = args[1]
	if os.path.exists(path + name):
		set_training_script(path + name)
		log('Plugin: SCRIPT DEGISTIRILIYOR.. [%s]' % name)
		return 0
	log('Plugin: SCRIPT: [%s] BULUNAMADI..' % name)
	return 0
# CloseBot..BOTU HEMEN KAPATIR
# CloseBot,in,5... 5 DAKIKA SONRA BOTU KAPATIR
# CloseBot,at,05:30..BILGISAYAR SAATINE GORE BOTU KAPATIR (24 SAAT FORMATI)
def CloseBot(args):
	global CloseBotAt, CheckCloseTime
	CheckCloseTime = True
	if len(args) == 1:
		Terminate()
		return 0
	type = args[1]
	time = args[2]
	if type == 'in':
		CloseBotAt = str(datetime.datetime.now() + timedelta(minutes=int(time)))[11:16]
		log('Plugin: BOT KAPATILIYOR. [%s]' % CloseBotAt)
	elif type == 'at':
		CloseBotAt = time
		log('Plugin: BOT KAPATILIYOR. [%s]' % CloseBotAt)
	return 0
def Terminate():
	log("Plugin: BOT KAPATILIYOR...")
# os.kill(os.getpid(),9)
# GoClientless.. CLIENTLESS MODUNA GECIR.
def GoClientless(args):
	pid = get_client()['pid']
	if pid:
		os.kill(pid, signal.SIGTERM)
		return 0
	log('Plugin: CLIENT ACIK DEGIL..!')
	return 0
# StartBot,in,5.. 5 DAKIKA SONRA BOTU BASLAT
# StartBot,at,05:30.. BILGISAYAR SAATINE GORE BOT BASLATILIR (24 SAAT FORMATI)
def StartBot(args):
	global StartBotAt, CheckStartTime, SkipCommand
	if SkipCommand:
		SkipCommand = False
		return 0
	stop_bot()
	type = args[1]
	time = args[2]
	CheckStartTime = True
	if type == 'in':
		StartBotAt = str(datetime.datetime.now() + timedelta(minutes=int(time)))[11:16]
		log('Plugin: BOT BASLATILIYOR [%s]' % StartBotAt)
	elif type == 'at':
		StartBotAt = time
		log('Plugin: BOT BASLATILIYOR [%s]' % StartBotAt)
	return 0
# StopStart..BOTU DURDURUP 1 SANIYE SONRA TEKRAR BAŞLATIR.
def StopStart(args):
	global SkipCommand
	if SkipCommand:
		SkipCommand = False
		return 0
	stop_bot()
	Timer(1.0, start_bot, ()).start()
	Timer(30.0, ResetSkip, ()).start()
	SkipCommand = True
	return 0
# StartTrace,player..NICKI YAZILI PLAYERA TRACE BASLATIR.
def StartTrace(args):
	global SkipCommand
	if SkipCommand:
		SkipCommand = False
		return 0
	elif len(args) == 2:
		stop_bot()
		player = args[1]
		if start_trace(player):
			log('Plugin: TRACE BAŞLATILIYOR : [%s]' % player)
			return 0
		else:
			log('Plugin: OYUNCU [%s] YANINDA DEĞİL, DEVAM EDİLİYOR..' % player)
			SkipCommand = True
			Timer(1.0, start_bot, ()).start()
			Timer(30.0, ResetSkip, ()).start()
			return 0
	log('Plugin: YANLIŞ YAZIM FORMATI.')
	return 0
# RemoveSkill,skillname... EĞER SKİLL AKTİFSE İPTAL ET..
def RemoveSkill(args):
	locale = get_locale()
	if locale == 18 or locale == 56:
		RemSkill = args[1]
		skills = get_active_skills()
		for ID, skill in skills.items():
			if skill['name'] == RemSkill:
				packet = b'\x01\x05'
				packet += struct.pack('<I', ID)
				packet += b'\x00'
				inject_joymax(0x7074, packet, False)
				log('Plugin: SKILL SILINIYOR. [%s]' % RemSkill)
				return 0
		log('Plugin: SKILL AKTİF DEĞİL..')
		return 0
	log('Plugin: Yalnızca iSRO veya TRSROda desteklenir ')
	return 0
# Drop,itemname... YAZILI ITEMIN ILK STACK'INI YERE ATAR..
def Drop(args):
	locale = get_locale()
	if locale == 18 or locale == 56:
		DropItem = args[1]
		items = get_inventory()['items']
		for slot, item in enumerate(items):
			if item:
				name = item['name']
				if name == DropItem:
					p = b'\x07'  # static stuff maybe
					p += struct.pack('B', slot)
					log('Plugin: ITEM YERE ATILIYOR. [%s][%s]' % (item['quantity'], name))
					inject_joymax(0x7034, p, True)
					return 0
		log(r'Plugin: YERE ATILACAK ITEM YOK')
		return 0
	log('Plugin: Yalnızca iSRO veya TRSROda desteklenir')
	return 0
# OpenphBot,commandlinearguments..SEÇILEBİLİR ARGÜMANLARLA YENİ BİR BOT AÇAR.
def OpenphBot(args):
	cmdargs = args[1]
	if os.path.exists(path + "phBot.exe"):
		subprocess.Popen(path + "phBot.exe " + cmdargs)
		log('Plugin: YENİ BOT AÇILIYOR..')
		return 0
	log('Plugin: BOT YOLU BULUNAMADI..')
	return 0
def event_loop():
	global delay_counter, CheckStartTime, SkipCommand, CheckCloseTime
	if CheckStartTime:
		delay_counter += 500
		if delay_counter >= 60000:
			delay_counter = 0
			CurrentTime = str(datetime.datetime.now())[11:16]
			if CurrentTime == StartBotAt:
				CheckStartTime = False
				SkipCommand = True
				log('Plugin: BOT BAŞLATILIYOR..')
				start_bot()
	elif CheckCloseTime:
		delay_counter += 500
		if delay_counter >= 60000:
			delay_counter = 0
			CurrentTime = str(datetime.datetime.now())[11:16]
			if CurrentTime == CloseBotAt:
				CheckCloseTime = False
				Terminate()
	if inGame and followActivated:
		player = near_party_player(followPlayer)
		# check if is near
		if not player:
			return
		# check distance to the player
		if followDistance > 0:
			p = get_position()
			playerDistance = round(GetDistance(p['x'],p['y'],player['x'],player['y']),2)
			# check if has to move
			if followDistance < playerDistance:
				# generate vector unit
				x_unit = (player['x'] - p['x']) / playerDistance
				y_unit = (player['y'] - p['y']) / playerDistance
				# distance to move
				movementDistance = playerDistance-followDistance
				log("Following "+followPlayer+"...")
				move_to(movementDistance * x_unit + p['x'],movementDistance * y_unit + p['y'],0)
		else:
			# Avoid negative numbers
			log("TAKİP EDİLİYOR : "+followPlayer+"...")
			move_to(player['x'],player['y'],0)

def button_start():
	global BtnStart, RecordedPackets
	if len(QtBind.text(gui, SaveName)) <= 0:
		log('Plugin: LÜTFEN ÖZEL KOMUT DOSYASI KOMUTU İÇİN BİR AD GİRİN')
		return
	if BtnStart == False:
		BtnStart = True
		QtBind.setText(gui, RecordBtn, ' KAYIT DURDURULUYOR.. ')
		log('Plugin: BAŞLATILDI.. LÜTFEN KAYDA BAŞLAMAK İÇİN NPCYİ SEÇİN.')
	elif BtnStart == True:
		log('Plugin: KAYIT TAMAMLANDI.')
		Name = QtBind.text(gui, SaveName)
		SaveNPCPackets(Name, RecordedPackets)
		BtnStart = False
		QtBind.setText(gui, RecordBtn, ' KAYIT BAŞLATILIYOR.. ')
		Recording = False
		RecordedPackets = []
		Timer(1.0, button_ShowCmds, ()).start()
def button_ShowCmds():
	QtBind.clear(gui, Display)
	data = {}
	if os.path.exists(path + "CustomNPC.json"):
		with open("CustomNPC.json", "r") as f:
			data = json.load(f)
			for name in data:
				QtBind.append(gui, Display, name)
	else:
		log('Plugin: ŞUANDA KAYITLI KOMUT YOK..')
def button_DelCmds():
	Name = QtBind.text(gui, Display)
	QtBind.clear(gui, Display)
	data = {}
	if Name:
		with open("CustomNPC.json", "r") as f:
			data = json.load(f)
			for name, value in list(data.items()):
				if name == Name:
					del data[name]
					with open("CustomNPC.json", "w") as f:
						f.write(json.dumps(data, indent=4))
						log('Plugin: KAYITLI KOMUT: [%s] SİLİNDİ..' % name)
						Timer(1.0, button_ShowCmds, ()).start()
						return
			else:
				log('Plugin: [%s] ADINDA KAYITLI KOMUT BULUNAMADI..' % Name)
				Timer(1.0, button_ShowCmds, ()).start()
def button_ShowPackets():
	Name = QtBind.text(gui, Display)
	QtBind.clear(gui, Display)
	data = {}
	if Name:
		with open("CustomNPC.json", "r") as f:
			data = json.load(f)
			for name in data:
				if name == Name:
					Packets = data[name]['Packets']
					for packet in Packets:
						QtBind.append(gui, Display, packet)
def GetPackets(Name):
	global ExecutedPackets
	data = {}
	with open("CustomNPC.json", "r") as f:
		data = json.load(f)
		for name in data:
			if name == Name:
				ExecutedPackets = data[name]['Packets']
def SaveNPCPackets(Name, Packets=[]):
	data = {}
	if os.path.exists(path + "CustomNPC.json"):
		with open("CustomNPC.json", "r") as f:
			data = json.load(f)
	else:
		data = {}
	data[Name] = {"Packets": Packets}
	with open("CustomNPC.json", "w") as f:
		f.write(json.dumps(data, indent=4))
	log("Plugin: KOMUT KAYDEDİLDİ..")
def CustomNPC(args):
	global SkipCommand
	if SkipCommand:
		SkipCommand = False
		return 0
	stop_bot()
	Name = args[1]
	GetPackets(Name)
	Timer(0.5, InjectPackets, ()).start()
	return 0
def InjectPackets():
	global Index, ExecutedPackets
	opcode = int(ExecutedPackets[Index].split(':')[0], 16)
	dataStr = ExecutedPackets[Index].split(':')[1].replace(' ', '')
	LendataStr = len(dataStr)
	data = bytearray()
	for i in range(0, int(LendataStr), 2):
		data.append(int(dataStr[i:i + 2], 16))
	inject_joymax(opcode, data, False)
	if QtBind.isChecked(gui, cbxShowPackets):
		log("Plugin: ENJEKTE EDILDI.. (Opcode) 0x" + '{:02X}'.format(opcode) + " (Data) " + (
			"None" if not data else ' '.join('{:02X}'.format(x) for x in data)))
	NumofPackets = len(ExecutedPackets) - 1
	if Index < NumofPackets:
		Index += 1
		Timer(2.0, InjectPackets, ()).start()
	elif Index == NumofPackets:
		global SkipCommand
		log('Plugin: KOMUT TAMAMLANDI..')
		Index = 0
		ExecutedPackets = []
		Timer(30.0, ResetSkip, ()).start()
		SkipCommand = True
		start_bot()
def handle_silkroad(opcode, data):
	global Recording, BtnStart, RecordedPackets
	if data == None:
		return True
	if BtnStart:
		if opcode == 0x7045:
			Recording = True
			log('Plugin: KAYIT BAŞLATILDI.')
			RecordedPackets.append("0x" + '{:02X}'.format(opcode) + ":" + ' '.join('{:02X}'.format(x) for x in data))
			if QtBind.isChecked(gui, cbxShowPackets):
				log("Plugin: KAYIT EDİLDİ.. (Opcode) 0x" + '{:02X}'.format(opcode) + " (Data) " + (
					"None" if not data else ' '.join('{:02X}'.format(x) for x in data)))
		if Recording == True:
			if opcode != 0x7045:
				RecordedPackets.append(
					"0x" + '{:02X}'.format(opcode) + ":" + ' '.join('{:02X}'.format(x) for x in data))
				if QtBind.isChecked(gui, cbxShowPackets):
					log("Plugin: KAYIT EDİLDİ.. (Opcode) 0x" + '{:02X}'.format(opcode) + " (Data) " + (
						"None" if not data else ' '.join('{:02X}'.format(x) for x in data)))
	if '{:02X}'.format(opcode) == "705A" and QtBind.isChecked(gui, cbxGOAll):
		phBotChat.All('GO ' + ' '.join('{:02X}'.format(x) for x in data))
		# log(str(opcode)+"Client: (Opcode) 0x" + '{:02X}'.format(opcode) + " (Data) "+ str(data))
		return True
	if '{:02X}'.format(opcode) == "705A" and QtBind.isChecked(gui, cbxGOParty):
		phBotChat.Party('GO ' + ' '.join('{:02X}'.format(x) for x in data))
		# log(str(opcode)+"Client: (Opcode) 0x" + '{:02X}'.format(opcode) + " (Data) "+ str(data))
		return True
	if '{:02X}'.format(opcode) == "705A" and QtBind.isChecked(gui, cbxGOGuild):
		phBotChat.Guild('GO ' + ' '.join('{:02X}'.format(x) for x in data))
		# log(str(opcode)+"Client: (Opcode) 0x" + '{:02X}'.format(opcode) + " (Data) "+ str(data))
		return True
	if '{:02X}'.format(opcode) == "705A" and QtBind.isChecked(gui, cbxGOUnion):
		phBotChat.Union('GO ' + ' '.join('{:02X}'.format(x) for x in data))
		# log(str(opcode)+"Client: (Opcode) 0x" + '{:02X}'.format(opcode) + " (Data) "+ str(data))
		return True
	if '{:02X}'.format(opcode) == "705A" and QtBind.isChecked(gui, cbxGOJobAll):
		phBotChat.All('GJ ' + ' '.join('{:02X}'.format(x) for x in data))
		# log(str(opcode)+"Client: (Opcode) 0x" + '{:02X}'.format(opcode) + " (Data) "+ str(data))
		return True
	if '{:02X}'.format(opcode) == "705A" and QtBind.isChecked(gui, cbxGOJobParty):
		phBotChat.Party('GJ ' + ' '.join('{:02X}'.format(x) for x in data))
		# log(str(opcode)+"Client: (Opcode) 0x" + '{:02X}'.format(opcode) + " (Data) "+ str(data))
		return True
	if '{:02X}'.format(opcode) == "705A" and QtBind.isChecked(gui, cbxGOJobGuild):
		phBotChat.Guild('GJ ' + ' '.join('{:02X}'.format(x) for x in data))
		# log(str(opcode)+"Client: (Opcode) 0x" + '{:02X}'.format(opcode) + " (Data) "+ str(data))
		return True
	if '{:02X}'.format(opcode) == "705A" and QtBind.isChecked(gui, cbxGOJobUnion):
		phBotChat.Union('GJ ' + ' '.join('{:02X}'.format(x) for x in data))
		# log(str(opcode)+"Client: (Opcode) 0x" + '{:02X}'.format(opcode) + " (Data) "+ str(data))
		return True
	return True

def handle_joymax(opcode, data):
	if opcode == 0xB070 and QtBind.isChecked(gui,cbxEnabled):
		if data[0] == 1:
			skillType = data[1]
			index = 7
			attackerUID = struct.unpack_from("<I",data,index)[0]
			index += 8
			locale = get_locale()
			if locale == 18 or locale == 56:
				index += 4
			targetUID = struct.unpack_from("<I",data,index)[0]
			if skillType == 2:
				nickname = getnickname(attackerUID)
				if nickname and ListContains(nickname,QtBind.getItems(gui,lstLeaders)):
					log("Plugin: DÜŞMAN BU KİŞİDEN HEDEF ALINIYOR : "+nickname)
					Inject_SelectTarget(targetUID)
				elif QtBind.isChecked(gui,cbxDefensive):
					nickname = getnickname(targetUID)
					if nickname and ListContains(nickname,QtBind.getItems(gui,lstLeaders)):
						log("Plugin: BU KİŞİYE SALDIRAN DÜŞMAN HEDEF ALINIYOR : "+nickname)
						Inject_SelectTarget(attackerUID)
	return True
# PLUGIN YUKLENIRSE
log("Plugin: "+pName+" v"+pVersion+" BASARIYLA YUKLENDI.")
if os.path.exists(getPath()):
	# CONFIG YUKLEME
	loadConfigs()
else:
	# CONFIG DOSYASI OLUSTURMA
	os.makedirs(getPath())
	log('Plugin: '+pName+' CONFIG KLASORU OLUSTURULDU.')
