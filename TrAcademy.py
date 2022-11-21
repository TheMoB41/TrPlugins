from phBot import *
import QtBind
from threading import Timer
from datetime import datetime
from datetime import timedelta
import struct
import random
import json
import os
import subprocess

pName = 'TrAcademy'
pVersion = '1.0.3'
pUrl = 'https://raw.githubusercontent.com/TheMoB41/TrSro-Plugins/main/TrAcademy'

# User settings
SIRA_VARSAYILAN_NUMARA = 100 # If Custom Nickname is set like "Jelly", it will try to create "Jelly100","Jelly101", ...
BILDIRIM_SES_YOLU = 'c:\\Windows\\Media\\Speech On.wav'
# ______________________________ YUKLEMELER ______________________________ #
# EVRENSEL
isCreatingCharacter = False
isDeletingCharacter = False
CreatingNickname = ""
isRestarted = False
# KULLANICI ARAYUZU
gui = QtBind.init(__name__,pName)
cbxEnabled = QtBind.createCheckBox(gui,'cbxDoNothing','AKTIF ET',6,9)
# PROFILLER
_x = 350
_y = 10
lblProfil = QtBind.createLabel(gui,"CONFIG PROFIL ISMI :",_x-10,_y)
tbxProfil = QtBind.createLineEdit(gui,"",_x+102,_y-3,110,19)
btnKaydet = QtBind.createButton(gui,'btnKaydet_clicked',"  KAYDET  ",_x+102+110+3,_y-5)
btnYukle = QtBind.createButton(gui,'btnYukle_clicked',"  YUKLE  ",_x+102+110+3+75,_y-5)
# TEMEL CONFIG
_x = 6
_y = 40
cbxCharSec = QtBind.createCheckBox(gui,'cbxDoNothing','SEC ( 1-40 LVL ARASI )',_x,_y-1)
cbxAkademideCharSec = QtBind.createCheckBox(gui,'cbxDoNothing','SEC ( EGER 40-50 LVL ARASI CHAR AKADEMIDEYSE )',_x+200,_y-1)
_y+=20
cbxCharKur = QtBind.createCheckBox(gui,'cbxDoNothing','OLUSTUR ( SECILECEK CHAR YOKSA )',_x,_y-1)
_y+=20
cbxCharSil = QtBind.createCheckBox(gui,'cbxDoNothing','SIL ( EGER 40-50 LVL ARASINDAYSA )',_x,_y-1)
# DETAYLI CONFIG
_x = 518
_y = 40
lblNick = QtBind.createLabel(gui,"NICK :",_x-5,_y)
tbxNick = QtBind.createLineEdit(gui,"",_x+94,_y-3,102,19)
_y+=20
lblSira = QtBind.createLabel(gui,"BASLANGIC SAYISI :",_x-5,_y)
tbxSira = QtBind.createLineEdit(gui,"",_x+95,_y-3,101,19)
_y+=20
lblIrk = QtBind.createLabel(gui,"IRK :",_x-5,_y)
cmbxIrk = QtBind.createCombobox(gui,_x+95,_y-3,102,19)
QtBind.append(gui,cmbxIrk,"CH")
QtBind.append(gui,cmbxIrk,"EU")
# DIGER AKSIYONLAR
_y = 130
_x = 6
lblCharlarDolu = QtBind.createLabel(gui,"ASAGIDAKI AKSIYONLAR YENI CHAR ACMAK MUMKUN OLMADIGINDA DEVREYE ALINIR :",_x,_y)
_y+=20
lblCMD = QtBind.createLabel(gui,"SISTEM KOMUTLARINI CALISTIR (CMD) :",_x+10,_y)
tbxCMD = QtBind.createLineEdit(gui,"",215,_y-3,205,19)
_y+=20
cbxCikis = QtBind.createCheckBox(gui,'cbxDoNothing','BOTU KAPAT',_x+9,_y)
_y+=20
cbxBildirimler_Full = QtBind.createCheckBox(gui,'cbxDoNothing','PHBOT BILDIRIMLERINDE GOSTER',_x+9,_y)
_y+=20
cbxSes_Full = QtBind.createCheckBox(gui,'cbxDoNothing','SES CAL.  DOSYA YOLU : ',_x+9,_y)
tbxSes_Full = QtBind.createLineEdit(gui,'',155,_y-1,240,19)
_y+=20
cbxLog_Full = QtBind.createCheckBox(gui,'cbxDoNothing','LOG DOSYASI OLUSTUR',_x+9,_y)
# ______________________________ METHODLAR ______________________________ #
# KLASOR YOLUNDAN DEVAM ET
def getPath():
	return get_config_dir()+pName+"\\"
# CHAR CONFIG YOLUNDAN DEVAM ET
def getConfig(name):
	if not name:
		name = pName;
	return getPath()+name+".json"
# VARSAYILAN CONFIGLERI YUKLE
def loadDefaultConfig():
	# Clear data
	QtBind.setText(gui,tbxProfil,"")
	QtBind.setChecked(gui,cbxEnabled,False)
	QtBind.setChecked(gui,cbxCharSec,True)
	QtBind.setChecked(gui,cbxCharKur,True)
	QtBind.setChecked(gui,cbxCharSil,True)
	QtBind.setChecked(gui,cbxAkademideCharSec,False)
	QtBind.setText(gui,tbxNick,"")
	QtBind.setText(gui,tbxSira,str(SIRA_VARSAYILAN_NUMARA))
	QtBind.setText(gui,cmbxIrk,"CH")
	QtBind.setText(gui,tbxCMD,"")
	QtBind.setChecked(gui,cbxBildirimler_Full,False)
	QtBind.setChecked(gui,cbxSes_Full,False)
	QtBind.setText(gui,tbxSes_Full,BILDIRIM_SES_YOLU)
	QtBind.setChecked(gui,cbxLog_Full,False)
	QtBind.setChecked(gui,cbxCikis,False)
# KAYITLI CONFIGLERI YUKLE
def loadConfigs(fileName=""):
	# CONFIG RESETLE
	loadDefaultConfig()
	# YUKLEMEK ICIN KAYITLI CONFIGLERI KONTROL ET
	if os.path.exists(getConfig(fileName)):
		data = {}
		with open(getConfig(fileName),"r") as f:
			data = json.load(f)
		# TUM DATAYI YUKLE
		QtBind.setText(gui,tbxProfil,fileName)
		if "AKTIF ET" in data and data['AKTIF ET']:
			QtBind.setChecked(gui,cbxEnabled,True)
		if "CharSec" in data and not data['CharSec']:
			QtBind.setChecked(gui,cbxCharSec,False)
		if "CharKur" in data and not data['CharKur']:
			QtBind.setChecked(gui,cbxCharKur,False)
		if "CharSil" in data and not data['CharSil']:
			QtBind.setChecked(gui,cbxCharSil,False)
		if "AkademideCharSec" in data and data['AkademideCharSec']:
			QtBind.setChecked(gui,cbxAkademideCharSec,True)
		if "Nick" in data:
			QtBind.setText(gui,tbxNick,data["Nick"])
		if "SIRA" in data and data["SIRA"]:
			QtBind.setText(gui,tbxSira,data["SIRA"])
		if "IRK" in data:
			QtBind.setText(gui,cmbxIrk,data["IRK"])
		if "CMD" in data:
			QtBind.setText(gui,tbxCMD,data["CMD"])
		if "BILDIRIMFULL" in data and data['BILDIRIMFULL']:
			QtBind.setChecked(gui,cbxBildirimler_Full,True)
		if "SESFULL" in data and data['SESFULL']:
			QtBind.setChecked(gui,cbxBildirimler_Full,True)
		if "SESFULLYOLU" in data and data["SESFULLYOLU"]:
			QtBind.setText(gui,tbxSes_Full,data["SESFULLYOLU"])
		if "LOGFULL" in data and data['LOGFULL']:
			QtBind.setChecked(gui,cbxLog_Full,True)
		if "CIKIS" in data and data['CIKIS']:
			QtBind.setChecked(gui,cbxCikis,True)
		return True
	return False
# OPSIYONEL AYARLARI KAYDET
def saveConfigs(fileName=""):
	data = {}
	# TUM DATAYI KAYDET
	data["AKTIF ET"] = QtBind.isChecked(gui,cbxEnabled)
	data["CharSec"] = QtBind.isChecked(gui,cbxCharSec)
	data["CharKur"] = QtBind.isChecked(gui,cbxCharKur)
	data["CharSil"] = QtBind.isChecked(gui,cbxCharSil)
	data["AkademideCharSec"] = QtBind.isChecked(gui,cbxAkademideCharSec)
	data["Nick"] = QtBind.text(gui,tbxNick)
	sequence = QtBind.text(gui,tbxSira)
	if sequence.isnumeric():
		data["SIRA"] = sequence
	else:
		data["SIRA"] = str(SIRA_VARSAYILAN_NUMARA)
		QtBind.setText(gui,tbxSira,data["SIRA"])
	data["IRK"] = QtBind.text(gui,cmbxIrk)
	data["CMD"] = QtBind.text(gui,tbxCMD)
	data["BILDIRIMFULL"] = QtBind.isChecked(gui,cbxBildirimler_Full)
	data["SESFULL"] = QtBind.isChecked(gui,cbxSes_Full)
	data["SESFULLYOLU"] = QtBind.text(gui,tbxSes_Full)
	data["LOGFULL"] = QtBind.isChecked(gui,cbxLog_Full)
	data["CIKIS"] = QtBind.isChecked(gui,cbxCikis)
	# YENIDEN YAZMA
	with open(getConfig(fileName),"w") as f:
		f.write(json.dumps(data,indent=4,sort_keys=True))
# BUTON ETKINLIGI
def btnKaydet_clicked():
	# CONFIG ISMINI KONTROL ET
	strConfigName = QtBind.text(gui,tbxProfil)
	saveConfigs(strConfigName)
	if strConfigName:
		log('Plugin: Profil : ['+strConfigName+'] CONFIG KAYDEDILDI.')
	else:
		log("Plugin: CONFIG KAYDEDILDI.")
# BUTON ETKINLIGI
def btnYukle_clicked():
	# Check the config name
	strConfigName = QtBind.text(gui,tbxProfil)
	if loadConfigs(strConfigName):
		if strConfigName:
			log("Plugin: Profil : ["+strConfigName+"] CONFIG YUKLENDI.")
		else:
			log("Plugin: CONFIG YUKLENDI.")
	elif strConfigName:
		log("Plugin: Profil : ["+strConfigName+"] BULUNAMADI.")
# CHAR OLUSTURMA
def CreateCharacter():
	# SINIF SECIMI
	race = QtBind.text(gui,cmbxIrk)
	if race != 'EU':
		race = 'CH'
		model = get_monster_string('CHAR_CH_MAN_ADVENTURER')
		chest = get_item_string('ITEM_CH_M_HEAVY_01_BA_A_DEF')
		legs = get_item_string('ITEM_CH_M_HEAVY_01_LA_A_DEF')
		shoes = get_item_string('ITEM_CH_M_HEAVY_01_FA_A_DEF')
		weapon = get_item_string('ITEM_CH_SWORD_01_A_DEF')
	else:
		race = 'EU'
		model = get_monster_string('CHAR_EU_MAN_NOBLE')
		chest = get_item_string('ITEM_EU_M_HEAVY_01_BA_A_DEF')
		legs = get_item_string('ITEM_EU_M_HEAVY_01_LA_A_DEF')
		shoes = get_item_string('ITEM_EU_M_HEAVY_01_FA_A_DEF')
		weapon = get_item_string('ITEM_EU_SWORD_01_A_DEF')
	if not model or not chest or not legs or not shoes or not weapon:
		log('Plugin: HATA,SUNUCUDA ITEM KODLARI DEGISTIRILMIS.')
		return
	global isCreatingCharacter
	isCreatingCharacter = True
	log('Plugin: CHAR OLUSTURULUYOR ['+CreatingNickname+'] ('+race+')')
	p = b'\x01'
	p += struct.pack('<H', len(CreatingNickname))
	p += CreatingNickname.encode('ascii')
	p += struct.pack('<I', model['model'])
	p += struct.pack('<B', 0)
	p += struct.pack('<I', chest['model'])
	p += struct.pack('<I', legs['model'])
	p += struct.pack('<I', shoes['model'])
	p += struct.pack('<I', weapon['model'])
	# CHAR OLUSTURMAYI DENEME
	inject_joymax(0x7007,p, False)
	# CHAR LISTESI ICIN 2.5SN BEKLEME
	Timer(2.5,Inject_RequestCharacterList).start()
# PAKET ENJEKSIYON
def Inject_RequestCharacterList():
	inject_joymax(0x7007,b'\x02',False)
# PAKET ENJEKSIYON
def Inject_DeleteCharacter(charName):
	p = b'\x03'
	p += struct.pack('<H', len(charName))
	p += charName.encode('ascii')
	inject_joymax(0x7007,p, False)
# PAKET ENJEKSIYON
def Inject_CheckName(charName):
	p = b'\x04'
	p += struct.pack('<H', len(charName))
	p += charName.encode('ascii')
	inject_joymax(0x7007,p, False)
# RANDOM CHAR ISMI OLUSTURMA (MALE)
def GetRandomNick():
	# 12 HARFLI ISIM EKLEME
	names = ["Aegon","Aerys","Aemon","Aeron","Alliser","Areo","Bran","Bronn","Benjen","Brynden","Beric","Balon","Bowen","Craster","Davos","Daario","Doran","Darrik","Dyron","Eddard","Edric","Euron","Edmure","Gendry","Gilly","Gregor","GreyWorm","Hoster","Jon","Jaime","Jorah","Joffrey","Jeor","Jaqen","Jojen","Janos","Kevan","Khal","Lancel","Loras","Maekar","Mace","Mance","Nestor","Oberyn","Petyr","Podrick","Quentyn","Robert","Robb","Ramsay","Roose","Rickon","Rickard","Rhaegar","Renly","Rodrik","Randyll","Samwell","Sandor","Stannis","Stefon","Tywin","Tyrion","Theon","Tormund","Trystane","Tommen","Val","Varys","Viserys","Victarion","Vimar","Walder","Wyman","Yoren","Yohn","Zane"]
	name = names[random.randint(0,len(names)-1)]
	# DC ICIN YUKLEME YAPMAK
	if len(name) < 12:
		maxWidth = 12-len(name)
		if maxWidth > 4 :
			maxWidth = 4
		numbers = pow(10,maxWidth)-1
		name = str(name)+(str(random.randint(0,numbers))).zfill(maxWidth)
	return name
# KAYITLI CHAR SIRASINI GORUP 1 SAYI UZERINI OLUSTURMAK VEYA DATA KAYITLI DEGILSE 1 DEN BASLATMAK
def GetSequence():	
	sequence = QtBind.text(gui,tbxSira)
	# GECERLI DEGERI KONTROL ETMEK
	if sequence.isnumeric():
		sequence = int(sequence)
	else:
		sequence = SIRA_VARSAYILAN_NUMARA
	QtBind.setText(gui,tbxSira,str(sequence+1))
	saveConfigs(QtBind.text(gui,tbxProfil))
	return sequence
# ISIM UZUNLUGUNU VE SAYISINI KONTROL EDIP DEVAM ETMEK
def GetNickSequence(nickname):
	seq = str(GetSequence())
	nick = nickname+seq
	nickLength = len(nick)
	if nickLength > 12: # MAX KARAKTER SAYISI
		nickLength -= 12
		nick = nickname[:-nickLength]+seq
	return nick
# ISIM VARSA KONTROL ETMEK
def createNickname():
	global CreatingNickname
	customName = QtBind.text(gui,tbxNick) 
	if customName:
		CreatingNickname = GetNickSequence(customName)
	else:
		CreatingNickname = GetRandomNick()
	log("Plugin: NICK KONTROL EDILIYOR ["+CreatingNickname+"]")
	Inject_CheckName(CreatingNickname)
# BOTU SONLANDIRMAK
def KillBot():
	log("Plugin: BOT KAPATILIYOR..")
	# Suicide :(
	os.kill(os.getpid(),9)
# BUNUNLA AYNI KOMUT SATIRI ARGUMANLARINA SAHIP BIR BOT CALISTIR
def RestartBotWithCommandLine():
	# YALNIZCA BIR KEZ YURUTULEBILECEGINI GOSTEREN BAYRAK
	global isRestarted
	if isRestarted:
		return
	isRestarted = True
	# MEVCUT BOTTAN YOLU VE ARGUMANLARI ALIN
	cmd = ' '.join(get_command_line_args())
	# KILITLENMEYI ONLEMEK ICIN ARKA PLANDA CALISTIR
	subprocess.Popen(cmd)
	## BOTU KAPATMAK ICIN ZAMANLAYICI BASLATMA
	log("Plugin: BOT 5 SANIYE ICINDE KAPATILIYOR..")
	Timer(5.0,KillBot).start()
# ______________________________ ETKINLIKLER ______________________________ #
def handle_joymax(opcode,data):
	# SERVER_CHARACTER_SELECTION_RESPONSE
	if opcode == 0xB007 and QtBind.isChecked(gui,cbxEnabled):
		# PAKET AYRIŞTIRAMAYI FİLTRELE
		locale = get_locale()
		try:
			global isCreatingCharacter, isDeletingCharacter
			index = 0
			action = data[index]
			index+=1
			success = data[index]
			index+=1
			if action == 1:
				if isCreatingCharacter:
					isCreatingCharacter = False
					if success == 1:
						log("Plugin: CHAR BASARIYLA KURULDU..")
					else:
						log("Plugin: CHAR KURULAMADI.")
			elif action == 3:
				if isDeletingCharacter:
					isDeletingCharacter = False
					if success == 1:
						log("Plugin: CHAR BASARIYLA SILINDI..")
					else:
						log("Plugin: CHAR SILINEMEDI.")
			elif action == 4:
				if isCreatingCharacter:
					if success == 1:
						log("Plugin: NICK KULLANILABILIR..")
						CreateCharacter()
					else:
						log("Plugin: NICK KULLANILIYOR..")
						Timer(1.0,createNickname).start()
			elif action == 2:
				if success == 1:
					# ANA SUREC
					charList = []
					# SECIM EKRANINDAKI TUM CHARLARI KONTROL ET
					nChars = data[index]
					index+=1
					log("Plugin: TrAcademy CHAR LISTESI: "+ ("None" if not nChars else ""))
					for i in range(nChars):
						character = {}
						character['model_id'] = struct.unpack_from('<I',data,index)[0]
						index+=4
						# ReadAscii() / ushort (2) + string (length)
						charLength = struct.unpack_from('<H',data,index)[0]
						index+=2
						character['name'] = struct.unpack_from('<' + str(charLength) + 's',data,index)[0].decode('cp1252')
						index+= charLength
						
						# 18 = iSRO / 54 = jSRO / 56 = TRSRO
						if locale == 18 or locale == 54 or locale == 56:
							index+=2+struct.unpack_from('<H',data,index)[0]
						index+=1
						character['level'] = data[index]
						index+=1
						index+=8
						index+=2
						index+=2
						index+=2
						if locale == 18 or locale == 54 or locale == 56:
							index+=4
						index+=4
						index+=4
						if locale == 18 or locale == 54 or locale == 56:
							index+=2
						character['is_deleting'] = data[index]
						index+=1
						if locale == 18 or locale == 54 or locale == 56:
							index+=4
						if character['is_deleting']:
							minutesLeft = struct.unpack_from('<I',data,index)[0]
							character['deleted_at'] = datetime.now() + timedelta(minutes=minutesLeft)
							index+=4
						index+=1 #
						if data[index]:
							index+=1
							strLength = struct.unpack_from('<H', data, index)[0]
							index+=(2 + strLength)
						else:
							index+=1
						character['academy_type'] = data[index]
						index+=1
						forCount = data[index]
						index+=1
						for j in range(forCount):
							index+=4
							index+=1
						forCount = data[index]
						index+=1
						for j in range(forCount):
							index+=4
							index+=1
						# ONCEKI KARAKTER HAKKINDA BILGI GOSTER
						charList.append(character)
						log(str(i+1)+") "+character['name']+" (Lv."+str(character['level'])+")"+(" [* "+character['deleted_at'].strftime('%H:%M %d/%m/%Y')+"]" if character['is_deleting'] else ""))
					if locale == 18 or locale == 54 or locale == 56:
						index+=1
					try:
						if i == (nChars-1):
							data[index]
							log("Plugin: PAKET AYRISTIRMA HATASI..")
					except:
						try:
							data[index-1]
							# Smooth parsing
						except:
							log("Plugin: PAKET AYRISTIRMA HATASI..")
					# DUZGUN AYRISTIRMA
					try:
						OnCharacterList(charList)
					except Exception as innerEx:
						log("Plugin: "+str(innerEx))
		except Exception as ex:
			log("Plugin: AYRISTIRMA HATASI. ["+str(ex)+"] - "+pName+" BU SERVERDA KULLANILAMAZ..")
			log("DESTEK ICIN ILETISIME GECINIZ..")
			log("Data [" + ("None" if not data else ' '.join('{:02X}'.format(x) for x in data))+"] Locale ["+str(locale)+"]")
	return True
def OnCharacterList(CharList):
	for character in CharList:
		if not character['is_deleting']:
			charName = character['name']
			charLevel = character['level']
			charAcademyType = character['academy_type']

			if charLevel >= 40 and charLevel <= 50 and charAcademyType != 0:
				# Check setting
				if QtBind.isChecked(gui,cbxAkademideCharSec):
					log("Plugin: CHAR SECILIYOR : ["+charName+"] (AKADEMIDE..)")
					select_character(charName)
					return
			if charLevel >= 40 and charLevel <= 50:
				if QtBind.isChecked(gui,cbxCharSil):
					global isDeletingCharacter
					isDeletingCharacter = True
					log("Plugin: CHAR SİLİNİYOR : ["+charName+"] (40-50 LVL ARASI..)")
					Inject_DeleteCharacter(charName)
					Timer(3.0,Inject_RequestCharacterList).start()
					return
			if charLevel < 40:
				if QtBind.isChecked(gui,cbxCharSec):
					log("Plugin: CHAR SECILIYOR : ["+charName+"] (1-40LVL ARASI..)")
					select_character(charName)
					return
				#CHAR LİMİTİ
	if len(CharList) < 1:
		if QtBind.isChecked(gui,cbxCharKur):
			global isCreatingCharacter
			isCreatingCharacter = True
			Timer(3.0,createNickname).start()
	else:
		errMessage = "Plugin: YENI CHAR ACMAK ICIN ID'DE YETERLI ALAN YOK.."
		log(errMessage)
		cmd = QtBind.text(gui,tbxCMD)
		if cmd:
			log("Plugin: KOMUTU UYGULAMA DENENIYOR.. ["+cmd+"]")
			subprocess.Popen(cmd)
		if QtBind.isChecked(gui,cbxBildirimler_Full):
			show_notification(pName+' v'+pVersion,errMessage)
		if QtBind.isChecked(gui,cbxSes_Full):
			try:
				path = QtBind.text(gui,tbxSes_Full)
				play_wav(path if path else BILDIRIM_SES_YOLU)
			except:
				pass
		if QtBind.isChecked(gui,cbxLog_Full):
			from datetime import datetime
			logText = datetime.now().strftime('%m/%d/%Y - %H:%M:%S')+': '+errMessage
			profileName = QtBind.text(gui,tbxProfil)
			logText += '\nPROFİL KULLANILIYOR: '+ (profileName if profileName else 'None')
			with open(getPath()+'_log.txt','a') as f:
				f.write(logText)
		if QtBind.isChecked(gui,cbxCikis):
			log("Plugin: BOT 5 SANIYE ICINDE KAPATILIYOR.")
			Timer(5.0,KillBot).start()
# PLUGIN YUKLENME MESAJI
log('Plugin: '+pName+' v'+pVersion+' BASARIYLA YUKLENDI.')
if os.path.exists(getPath()):
	useDefaultConfig = True
	bot_args = get_command_line_args()
	if bot_args:
		for i in range(len(bot_args)):
			param = bot_args[i].lower()
			if param.startswith('-xTrAcademy-config='):
				configName = param[17:]
				if loadConfigs(configName):
					log("Plugin: "+pName+" PROFIL : ["+configName+"] KOMUT ILE YUKLENDI.")
					useDefaultConfig = False
				else:
					log("Plugin: "+pName+" PROFIL : ["+configName+"] BULUNAMADI.")
				break
	if useDefaultConfig:
		loadConfigs()
else:
	loadDefaultConfig()
	os.makedirs(getPath())
	log('Plugin: "'+pName+'" CONFIG KLASORU OLUSTURULDU..')
