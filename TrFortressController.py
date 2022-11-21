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

pName = 'TrFortressController'
pVersion = '1.0.0'
pUrl = 'https://raw.githubusercontent.com/TheMoB41/TrPlugins/main/TrFortressController.py'

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
lblxControl01 = QtBind.createLabel(gui,'TrFortressController:\n * TheMoB TARAFINDAN DUZENLENMISTIR. \n * FEEDBACK SISTEMLI BIR YAZILIMDIR. \n * HATA VE ONERI BILDIRIMLERINIZI BANA ULASTIRABILIRSINIZ.',380,250)
lblxControl02 = QtBind.createLabel(gui,' # KOMUTLAR :\n\n- BAŞLAT :BOTU BASLAT.\n- DURDUR :BOTU DURDUR.\n- TRACE #OYUNCU :LIDERE YADA YAZDIGIN CHARA TRACE AT.\n- NOTRACE :TRACE DURDUR.\n- FOLLOW :OYUN TAKIP SISTEMI.\n- NOFOLLOW :OYUN TAKIP SISTEMI DURDURMA.\n- ZERK :ZERK HAZIRSA KULLAN.\n- PTAYRIL :PTDEN AYRIL.\n- TARGETON :TARGET MODUNU ETKİNLEŞTİRİR.\n- TARGETOFF :TARGET MODUNU KAPATIR.\n- DEFFON :DEFANS MODUNU ETKİNLEŞTİRİR.\n- DEFFOFF :DEFANS MODUNU KAPATIR.',5,50)
tbxLeaders = QtBind.createLineEdit(gui,"",350,11,100,20)
lstLeaders = QtBind.createList(gui,350,32,176,48)
btnAddLeader = QtBind.createButton(gui,'btnAddLeader_clicked',"LIDER EKLE",455,10)
btnRemLeader = QtBind.createButton(gui,'btnRemLeader_clicked',"LIDER SIL",360,85)
QtBind.createLabel(gui,'OTO TARGET : ',615,10)
QtBind.createList(gui,615,25,105,45)
cbxEnabled = QtBind.createCheckBox(gui,'cbxDoNothing','ETKİNLEŞTİR',620,30)
cbxDefensive = QtBind.createCheckBox(gui,'cbxDoNothing','DEFANSIF MOD',620,50)
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
		elif msg == "PTAYRIL":
			# PARTIDE MI KONTROL ET
			if get_party():
				# CIKMASI ICIN
				log("Plugin: PARTIDEN AYRILIYOR.")
				inject_joymax(0x7061,b'',False)
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
