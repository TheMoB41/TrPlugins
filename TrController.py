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
from re import search

pName = 'TrController'
pVersion = '2.0.0'
pUrl = 'https://raw.githubusercontent.com/TheMoB41/TrPlugins/main/TrController.py'

# KURULUM
path = get_config_dir()[:-7]
StartBotAt = 0
CloseBotAt = 0
CheckStartTime = False
CheckCloseTime = False
SkipCommand = False
delay_counter = 0
# KURESELLER
inGame = None
followActivated = False
followPlayer = ''
followDistance = 0
#GUI
gui = QtBind.init(__name__,pName)
x=10
y=10
tbxLeaders = QtBind.createLineEdit(gui,"",x+535,y+135,85,20)
lstLeaders = QtBind.createList(gui,x+535,y+20,85,110)
lblxControl012 = QtBind.createLabel(gui,'LİDER LİSTESİ',x+540,y)
btnAddLeader = QtBind.createButton(gui,'btnAddLeader_clicked',"   LIDER EKLE   ",x+540,y+160)
btnRemLeader = QtBind.createButton(gui,'btnRemLeader_clicked',"    LIDER SIL    ",x+455,y+70)
QtBind.createList(gui,x+260,y-5,170,150)
QtBind.createLabel(gui,'GÖNDERİLECEK CHAT\n             KANALI',x+290,y)
cbxAllChat = QtBind.createCheckBox(gui,"cbxAll_clicked","ALL CHAT",x+295,y+35)
cbxPartyChat = QtBind.createCheckBox(gui,"cbxParty_clicked","PARTY CHAT",x+295,y+50)
cbxGuildChat = QtBind.createCheckBox(gui,"cbxGuild_clicked","GUILD CHAT",x+295,y+65)
cbxUnionChat = QtBind.createCheckBox(gui,"cbxUnion_clicked","UNION CHAT",x+295,y+80)
cbxprivateChat = QtBind.createCheckBox(gui,"cbxprivate_clicked","PRIVATE CHAT",x+295,y+95)
tbxprivatechat = QtBind.createLineEdit(gui,"PLAYER",x+315,y+115,60,20)
btnkaydet = QtBind.createButton(gui,'btnkaydet_clicked',"       AYARLARI KAYDET      ",x+440,y+260)
btnvarsayilan = QtBind.createButton(gui,'btnvarsayilan_clicked',"   VARSAYILAN AYARLAR   ",x+440,y+280)
btnkomutlar = QtBind.createButton(gui,'btnkomutlar_clicked',"   CHAT KOMUTLARI   ",x+600,y+240)
btnsckomutlar = QtBind.createButton(gui,'btnsckomutlar_clicked'," SCRIPT KOMUTLARI ",x+600,y+260)
btnhakkinda = QtBind.createButton(gui,'btnhakkinda_clicked',"         HAKKINDA         ",x+600,y+280)
QtBind.createList(gui,5,5,80,275)
btnbotbaslat = QtBind.createButton(gui,'btnbotbaslat_clicked',"     BAŞLAT     ",x,y)
btnbotdurdur = QtBind.createButton(gui,'btnbotdurdur_clicked',"    DURDUR    ",x,y+25)
btntrace = QtBind.createButton(gui,'btntrace_clicked',"     TRACE     ",x,y+50)
btnnotrace = QtBind.createButton(gui,'btnnotrace_clicked',"   NOTRACE   ",x,y+75)
btnreturn= QtBind.createButton(gui,'btnreturn_clicked',"    RETURN     ",x,y+100)
btnfollow = QtBind.createButton(gui,'btnfollow_clicked',"    FOLLOW    ",x,y+125)
btnnofollow = QtBind.createButton(gui,'btnnofollow_clicked'," NOFOLLOW ",x,y+150)
btninfo= QtBind.createButton(gui,'btninfo_clicked',"       INFO      ",x,y+175)
btnkoral = QtBind.createButton(gui,'btnkoral_clicked',"     KORAL    	 ",x,y+200)
btndagil= QtBind.createButton(gui,'btndagil_clicked',"      DAGIL      ",x,y+225)
btndc= QtBind.createButton(gui,'btndc_clicked',"        DC        ",x,y+250)
QtBind.createList(gui,85,5,190,275)
btnprofil= QtBind.createButton(gui,'btnprofil_clicked',"     PROFIL     ",x+80,y)
tbxprofil = QtBind.createLineEdit(gui,"PROFIL ISMI",x+155,y-2,100,20)
btnrange = QtBind.createButton(gui,'btnrange_clicked',"     RANGE     ",x+80,y+25)
tbxrange = QtBind.createLineEdit(gui,"000035",x+155,y+23,100,20)
btntraceplayer = QtBind.createButton(gui,'btntraceplayer_clicked',"     TRACE     ",x+80,y+50)
tbxtraceplayer = QtBind.createLineEdit(gui,"PLAYER",x+155,y+48,100,20)
btnsckur= QtBind.createButton(gui,'btnsckur_clicked',"     SCKUR     ",x+80,y+75)
tbxsckur = QtBind.createLineEdit(gui,"DOSYA YOLU",x+155,y+73,100,20)
btnkorkur = QtBind.createButton(gui,'btnkorkur_clicked',"    KORKUR    ",x+80,y+100)
tbxkorkur = QtBind.createLineEdit(gui,"X,Y",x+155,y+98,100,20)
btnalankur= QtBind.createButton(gui,'btnalankur_clicked',"   ALANKUR   ",x+80,y+125)
tbxalankur = QtBind.createLineEdit(gui,"ALAN ADI",x+155,y+123,100,20)
btnrevalan= QtBind.createButton(gui,'btnrevalan_clicked',"  REVERSE ALAN   ",x+80,y+150)
tbxrevalan = QtBind.createLineEdit(gui,"ALAN ADI",x+175,y+148,80,20)
btnrevplayer= QtBind.createButton(gui,'btnrevplayer_clicked'," REVERSE PLAYER ",x+80,y+175)
tbxrevplayer = QtBind.createLineEdit(gui,"PLAYER",x+175,y+173,80,20)
btnrevreturn= QtBind.createButton(gui,'btnrevreturn_clicked',"  REVERSE RETURN  ",x+80,y+200)
btnrevolum= QtBind.createButton(gui,'btnrevolum_clicked'," REVERSE OLUM ",x+80,y+225)
QtBind.createList(gui,275,155,165,140)
lblbilgi = QtBind.createLabel(gui,'BULUNDUĞUN CHAR',x+305,y+165)
lblcharname = QtBind.createLabel(gui,'',x+330,y+185)
lblbilgii = QtBind.createLabel(gui,'LİDER LİSTESİNE',x+310,y+210)
btnliderekle= QtBind.createButton(gui,'btnliderekle_clicked',"      EKLE      ",x+320,y+230)
btnlidercikart= QtBind.createButton(gui,'btnlidercikart_clicked',"    ÇIKART    ",x+320,y+250)
QtBind.createList(gui,x-5,280,435,31)
btnchat = QtBind.createButton(gui,'btnchat_clicked',"         CHAT         ",x,y+280)
tbxchatcesit = QtBind.createLineEdit(gui,"CESIT",x+90,y+276,50,20)
tbxchatmesaj = QtBind.createLineEdit(gui,"MESAJ",x+145,y+276,275,20)
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
			if "PRIVATECHAT" in data:
				QtBind.setText(gui, tbxprivatechat, data["PRIVATECHAT"])
			if "PROFIL" in data:
				QtBind.setText(gui, tbxprofil, data["PROFIL"])
			if "SCKUR" in data:
				QtBind.setText(gui, tbxsckur, data["SCKUR"])
			if "ALANKUR" in data:
				QtBind.setText(gui, tbxalankur, data["ALANKUR"])
			if "REVALAN" in data:
				QtBind.setText(gui, tbxrevalan, data["REVALAN"])
			if "REVPLAYER" in data:
				QtBind.setText(gui, tbxrevplayer, data["REVPLAYER"])
			if "TRACEPL" in data:
				QtBind.setText(gui, tbxtraceplayer, data["TRACEPL"])
			if "KORKUR" in data:
				QtBind.setText(gui, tbxkorkur, data["KORKUR"])
			if "RANGE" in data:
				QtBind.setText(gui, tbxrange, data["RANGE"])
			if "CHATCESIT" in data:
				QtBind.setText(gui, tbxchatcesit, data["CHATCESIT"])
			if "CHATMESAJ" in data:
				QtBind.setText(gui, tbxchatmesaj, data["CHATMESAJ"])
def btnkaydet_clicked():
	if inGame:
		data = {}
		if os.path.exists(getConfig()):
			with open(getConfig(), 'r') as f:
				data = json.load(f)
			data["PRIVATECHAT"] = QtBind.text(gui, tbxprivatechat)
			data["PROFIL"] = QtBind.text(gui, tbxprofil)
			data["SCKUR"] = QtBind.text(gui, tbxsckur)
			data["ALANKUR"] = QtBind.text(gui, tbxalankur)
			data["REVALAN"] = QtBind.text(gui, tbxrevalan)
			data["REVPLAYER"] = QtBind.text(gui, tbxrevplayer)
			data["TRACEPL"] = QtBind.text(gui, tbxtraceplayer)
			data["KORKUR"] = QtBind.text(gui, tbxkorkur)
			data["RANGE"] = QtBind.text(gui, tbxrange)
			data["CHATCESIT"] = QtBind.text(gui, tbxchatcesit)
			data["CHATMESAJ"] = QtBind.text(gui, tbxchatmesaj)
		with open(getConfig(), "w") as f:
			f.write(json.dumps(data, indent=4, sort_keys=True))
		log('Plugin Buton: AYARLAR KAYIT EDİLDİ.. ')
def btnvarsayilan_clicked():
	if inGame:
		QtBind.setText(gui, tbxprivatechat, "PLAYER")
		QtBind.setText(gui, tbxprofil,"PROFIL ISMI")
		QtBind.setText(gui, tbxsckur,"DOSYA YOLU")
		QtBind.setText(gui, tbxalankur,"ALAN ADI")
		QtBind.setText(gui, tbxrevalan, "ALAN ADI")
		QtBind.setText(gui, tbxrevplayer, "PLAYER")
		QtBind.setText(gui, tbxtraceplayer, "PLAYER")
		QtBind.setText(gui, tbxkorkur, "X,Y")
		QtBind.setText(gui, tbxrange, "000035")
		QtBind.setText(gui, tbxchatcesit, "CESIT")
		QtBind.setText(gui, tbxchatmesaj, "MESAJ")
		Timer(1.0,varsayilan_ayarlar()).start()
def varsayilan_ayarlar():
	if inGame:
		data = {}
		if os.path.exists(getConfig()):
			with open(getConfig(), 'r') as f:
				data = json.load(f)
			data["PRIVATECHAT"] = QtBind.text(gui, tbxprivatechat)
			data["PROFIL"] = QtBind.text(gui, tbxprofil)
			data["SCKUR"] = QtBind.text(gui, tbxsckur)
			data["ALANKUR"] = QtBind.text(gui, tbxalankur)
			data["REVALAN"] = QtBind.text(gui, tbxrevalan)
			data["REVPLAYER"] = QtBind.text(gui, tbxrevplayer)
			data["TRACEPL"] = QtBind.text(gui, tbxtraceplayer)
			data["KORKUR"] = QtBind.text(gui, tbxkorkur)
			data["RANGE"] = QtBind.text(gui, tbxrange)
			data["CHATCESIT"] = QtBind.text(gui, tbxchatcesit)
			data["CHATMESAJ"] = QtBind.text(gui, tbxchatmesaj)
		with open(getConfig(), "w") as f:
			f.write(json.dumps(data, indent=4, sort_keys=True))
			log('Plugin Buton: VARSAYILAN AYARLAR KAYIT EDİLDİ.. ')
def btnhakkinda_clicked():
	log('\n\nTrController:\n * TheMoB TARAFINDAN DUZENLENMISTIR. \n * FEEDBACK SISTEMLI BIR YAZILIMDIR. \n * HATA VE ONERI BILDIRIMLERINIZI BANA ULASTIRABILIRSINIZ.')
def btnkomutlar_clicked():
	log('\n\nTrController:\n  # BU PLUGIN LIDER LISTESINE EKLENMIS CHARLARIN CHAT EKRANINDAN DIGER CHARLARA CESITLI ISLEMLER YAPTIRIR.\n   # DESTEK KOMUTLARI: \n- BAŞLAT : BOTU BASLAT.\n- DURDUR : BOTU DURDUR.\n- TRACE #OYUNCU : LIDERE YADA YAZDIGIN CHARA TRACE AT.\n- NOTRACE : TRACE DURDUR.\n- FOLLOW : OYUN TAKIP SISTEMI.\n- NOFOLLOW : OYUN TAKIP SISTEMI DURDURMA.\n- KORKUR #PosX? #PosY? #Range? #PosZ? : KOORDINAT KURMAK.\n- KORAL : CHARIN MEVCUT KOORDINATLARINI PM OLARAK ALMAK.\n- RANGE #Radius? : RANGE DEGISTIR.\n(VARSAYILAN 35, OZEL DEGER GIRMEK ICIN BASINA 0000 KOYULMALIDIR.\n- SCKUR #DOSYA YOLU : YAZDIGINIZ DOSYA YOLUNDAKI SCRIPTI TANIMLAR.\n- ALANKUR #ISIM : YAZILAN ISIMDEKI KASILMA ALANINI AKTIF EDER.\n- PROFIL #ISIM : YAZDIGINIZ ISIMDEKI PROFILI YUKLER.\n# REVERSE KOMUTLARI :\n- REVERSE RETURN : SON RETURN NOKTASINA REVERSE.\n- REVERSE OLUM : SON OLUM NOKTASINA REVERSE.\n- REVERSE ALAN #ALAN ADI : YAZDIGINIZ ALAN ADINA REVERSE.\n- REVERSE PLAYER #NICK : YAZDIGINIZ PT UYESINE REVERSE.\n- RETURN : RETURN SCROLL KULLAN.\n- DAGIL #RANGE : SECILEN RANGEDE HERHANGI KOORDINATA GIDER.\n- DC : OYUN BAGLANTISINI KESER.\n- CHAT #CESIT #MESAJ : MESAJ GONDER.\n- INFO: CHAR HAKKINDA BİLGİLERİ GÖNDERİR.')
def btnsckomutlar_clicked():
	log('\n\nTrController:\n# SCRIPTE EKLENEBILIR ÖZEL KOMUTLAR :\n- Notification,title,message : BİR WİNDOWS BİLDİRİMİ GÖSTER.\n(BOT SİMGE DURUMUNA KÜÇÜLTÜLMELİDİR.)\n- NotifyList,message : LİSTEDE BİR BİLDİRİM OLUŞTURUR.\n- PlaySound,ding.wav : WAV DOSYASI PHBOT KLASÖRÜNÜN İÇİNDE OLMALIDIR.\n- SetScript,Mobs103.txt : SCRİPT PHBOT KLASÖRÜNDE OLMALIDIR.\n- CloseBot : BOTU HEMEN KAPATIR.\n- CloseBot,in,5 : 5 DAKIKA SONRA BOTU KAPATIR.\n- CloseBot,at,05:30 : BILGISAYAR SAATINE GORE BOTU KAPATIR. (24 SAAT FORMATI)\n- GoClientless : CLIENTLESS MODUNA GECIR.\n- StartBot,in,5 : 5 DAKIKA SONRA BOTU BASLAT.\n- StartBot,at,05:30 : BILGISAYAR SAATINE GORE BOT BASLATILIR. (24 SAAT FORMATI)\n- StopStart : BOTU DURDURUP 1 SANIYE SONRA TEKRAR BAŞLATIR.\n- StartTrace,player : NICKI YAZILI PLAYERA TRACE BASLATIR.\n- OpenphBot,commandlinearguments : SEÇILEBİLİR ARGÜMANLARLA YENİ BİR BOT AÇAR.')
def btnbotbaslat_clicked():
	if QtBind.isChecked(gui,cbxAllChat):
		phBotChat.All('BASLAT')
		log('Plugin Buton: KOMUT ALL CHATE GÖNDERİLDİ.. ')
	if QtBind.isChecked(gui,cbxPartyChat):
		phBotChat.Party('BASLAT')
		log('Plugin Buton: KOMUT PARTY CHATE GÖNDERİLDİ.. ')
	if QtBind.isChecked(gui,cbxGuildChat):
		phBotChat.Guild('BASLAT')
		log('Plugin Buton: KOMUT GUILD CHATE  GÖNDERİLDİ.. ')
	if QtBind.isChecked(gui,cbxUnionChat):
		phBotChat.Union('BASLAT')
		log('Plugin Buton: KOMUT UNION CHATE GÖNDERİLDİ.. ')
	if QtBind.isChecked(gui,cbxprivateChat):
		toplayer = QtBind.text(gui, tbxprivatechat)
		phBotChat.Private(toplayer, "BASLAT")
		log('Plugin Buton: KOMUT ' +toplayer+' A GÖNDERİLDİ.. ')
def btnbotdurdur_clicked():
	if QtBind.isChecked(gui,cbxAllChat):
		phBotChat.All('DURDUR')
		log('Plugin Buton: KOMUT ALL CHATE GÖNDERİLDİ.. ')
	if QtBind.isChecked(gui,cbxPartyChat):
		phBotChat.Party('DURDUR')
		log('Plugin Buton: KOMUT PARTY CHATE GÖNDERİLDİ.. ')
	if QtBind.isChecked(gui,cbxGuildChat):
		phBotChat.Guild('DURDUR')
		log('Plugin Buton: KOMUT GUILD CHATE  GÖNDERİLDİ.. ')
	if QtBind.isChecked(gui,cbxUnionChat):
		phBotChat.Union('DURDUR')
		log('Plugin Buton: KOMUT UNION CHATE GÖNDERİLDİ.. ')
	if QtBind.isChecked(gui,cbxprivateChat):
		toplayer = QtBind.text(gui, tbxprivatechat)
		phBotChat.Private(toplayer, "DURDUR")
		log('Plugin Buton: KOMUT ' +toplayer+' A GÖNDERİLDİ.. ')
def btntrace_clicked():
	if QtBind.isChecked(gui,cbxAllChat):
		phBotChat.All('TRACE')
		log('Plugin Buton: KOMUT ALL CHATE GÖNDERİLDİ.. ')
	if QtBind.isChecked(gui,cbxPartyChat):
		phBotChat.Party('TRACE')
		log('Plugin Buton: KOMUT PARTY CHATE GÖNDERİLDİ.. ')
	if QtBind.isChecked(gui,cbxGuildChat):
		phBotChat.Guild('TRACE')
		log('Plugin Buton: KOMUT GUILD CHATE  GÖNDERİLDİ.. ')
	if QtBind.isChecked(gui,cbxUnionChat):
		phBotChat.Union('TRACE')
		log('Plugin Buton: KOMUT UNION CHATE GÖNDERİLDİ.. ')
	if QtBind.isChecked(gui,cbxprivateChat):
		toplayer = QtBind.text(gui, tbxprivatechat)
		phBotChat.Private(toplayer, "TRACE")
		log('Plugin Buton: KOMUT ' +toplayer+' A GÖNDERİLDİ.. ')
def btnnotrace_clicked():
	if QtBind.isChecked(gui,cbxAllChat):
		phBotChat.All('NOTRACE')
		log('Plugin Buton: KOMUT ALL CHATE GÖNDERİLDİ.. ')
	if QtBind.isChecked(gui,cbxPartyChat):
		phBotChat.Party('NOTRACE')
		log('Plugin Buton: KOMUT PARTY CHATE GÖNDERİLDİ.. ')
	if QtBind.isChecked(gui,cbxGuildChat):
		phBotChat.Guild('NOTRACE')
		log('Plugin Buton: KOMUT GUILD CHATE  GÖNDERİLDİ.. ')
	if QtBind.isChecked(gui,cbxUnionChat):
		phBotChat.Union('NOTRACE')
		log('Plugin Buton: KOMUT UNION CHATE GÖNDERİLDİ.. ')
	if QtBind.isChecked(gui,cbxprivateChat):
		toplayer = QtBind.text(gui, tbxprivatechat)
		phBotChat.Private(toplayer, "NOTRACE")
		log('Plugin Buton: KOMUT ' +toplayer+' A GÖNDERİLDİ.. ')
def btntraceplayer_clicked():
	NICK = QtBind.text(gui, tbxtraceplayer)
	if QtBind.isChecked(gui,cbxAllChat):
		phBotChat.All('TRACE '+NICK)
		log('Plugin Buton: KOMUT ALL CHATE GÖNDERİLDİ.. ')
	if QtBind.isChecked(gui,cbxPartyChat):
		phBotChat.Party('TRACE '+NICK)
		log('Plugin Buton: KOMUT PARTY CHATE GÖNDERİLDİ.. ')
	if QtBind.isChecked(gui,cbxGuildChat):
		phBotChat.Guild('TRACE '+NICK)
		log('Plugin Buton: KOMUT GUILD CHATE  GÖNDERİLDİ.. ')
	if QtBind.isChecked(gui,cbxUnionChat):
		phBotChat.Union('TRACE '+NICK)
		log('Plugin Buton: KOMUT UNION CHATE GÖNDERİLDİ.. ')
	if QtBind.isChecked(gui,cbxprivateChat):
		toplayer = QtBind.text(gui, tbxprivatechat)
		phBotChat.Private(toplayer, "TRACE "+NICK)
		log('Plugin Buton: KOMUT ' +toplayer+' A GÖNDERİLDİ.. ')
def btnfollow_clicked():
	if QtBind.isChecked(gui,cbxAllChat):
		log('Plugin Buton: BU KOMUT YALNIZCA PARTY CHATTE KULLANILABİLİR..')
	if QtBind.isChecked(gui,cbxPartyChat):
		phBotChat.Party('FOLLOW')
		log('Plugin Buton: KOMUT PARTY CHATE GÖNDERİLDİ.. ')
	if QtBind.isChecked(gui,cbxGuildChat):
		log('Plugin Buton: BU KOMUT YALNIZCA PARTY CHATTE KULLANILABİLİR..')
	if QtBind.isChecked(gui,cbxUnionChat):
		log('Plugin Buton: BU KOMUT YALNIZCA PARTY CHATTE KULLANILABİLİR..')
	if QtBind.isChecked(gui,cbxprivateChat):
		log('Plugin Buton: BU KOMUT YALNIZCA PARTY CHATTE KULLANILABİLİR..')
def btnnofollow_clicked():
	if QtBind.isChecked(gui,cbxAllChat):
		log('Plugin Buton: BU KOMUT YALNIZCA PARTY CHATTE KULLANILABİLİR..')
	if QtBind.isChecked(gui,cbxPartyChat):
		phBotChat.Party('NOFOLLOW')
		log('Plugin Buton: KOMUT PARTY CHATE GÖNDERİLDİ.. ')
	if QtBind.isChecked(gui,cbxGuildChat):
		log('Plugin Buton: BU KOMUT YALNIZCA PARTY CHATTE KULLANILABİLİR..')
	if QtBind.isChecked(gui,cbxUnionChat):
		log('Plugin Buton: BU KOMUT YALNIZCA PARTY CHATTE KULLANILABİLİR..')
	if QtBind.isChecked(gui,cbxprivateChat):
		log('Plugin Buton: BU KOMUT YALNIZCA PARTY CHATTE KULLANILABİLİR..')
def btnkorkur_clicked():
	XY = QtBind.text(gui, tbxkorkur)
	if QtBind.isChecked(gui,cbxAllChat):
		phBotChat.All('KORKUR '+XY)
		log('Plugin Buton: KOMUT ALL CHATE GÖNDERİLDİ.. ')
	if QtBind.isChecked(gui,cbxPartyChat):
		phBotChat.Party('KORKUR '+XY)
		log('Plugin Buton: KOMUT PARTY CHATE GÖNDERİLDİ.. ')
	if QtBind.isChecked(gui,cbxGuildChat):
		phBotChat.Guild('KORKUR '+XY)
		log('Plugin Buton: KOMUT GUILD CHATE  GÖNDERİLDİ.. ')
	if QtBind.isChecked(gui,cbxUnionChat):
		phBotChat.Union('KORKUR '+XY)
		log('Plugin Buton: KOMUT UNION CHATE GÖNDERİLDİ.. ')
	if QtBind.isChecked(gui,cbxprivateChat):
		toplayer = QtBind.text(gui, tbxprivatechat)
		phBotChat.Private(toplayer, "KORKUR "+XY)
		log('Plugin Buton: KOMUT ' +toplayer+' A GÖNDERİLDİ.. ')
def btnkoral_clicked():
	if QtBind.isChecked(gui,cbxAllChat):
		phBotChat.All('KORAL')
		log('Plugin Buton: KOMUT ALL CHATE GÖNDERİLDİ.. ')
	if QtBind.isChecked(gui,cbxPartyChat):
		phBotChat.Party('KORAL')
		log('Plugin Buton: KOMUT PARTY CHATE GÖNDERİLDİ.. ')
	if QtBind.isChecked(gui,cbxGuildChat):
		phBotChat.Guild('KORAL')
		log('Plugin Buton: KOMUT GUILD CHATE  GÖNDERİLDİ.. ')
	if QtBind.isChecked(gui,cbxUnionChat):
		phBotChat.Union('KORAL')
		log('Plugin Buton: KOMUT UNION CHATE GÖNDERİLDİ.. ')
	if QtBind.isChecked(gui,cbxprivateChat):
		toplayer = QtBind.text(gui, tbxprivatechat)
		phBotChat.Private(toplayer, "KORAL")
		log('Plugin Buton: KOMUT ' +toplayer+' A GÖNDERİLDİ.. ')
def btnrange_clicked():
	range = QtBind.text(gui, tbxrange)
	if QtBind.isChecked(gui,cbxAllChat):
		phBotChat.All('RANGE '+range)
		log('Plugin Buton: KOMUT ALL CHATE GÖNDERİLDİ.. ')
	if QtBind.isChecked(gui,cbxPartyChat):
		phBotChat.Party('RANGE '+range)
		log('Plugin Buton: KOMUT PARTY CHATE GÖNDERİLDİ.. ')
	if QtBind.isChecked(gui,cbxGuildChat):
		phBotChat.Guild('RANGE '+range)
		log('Plugin Buton: KOMUT GUILD CHATE  GÖNDERİLDİ.. ')
	if QtBind.isChecked(gui,cbxUnionChat):
		phBotChat.Union('RANGE '+range)
		log('Plugin Buton: KOMUT UNION CHATE GÖNDERİLDİ.. ')
	if QtBind.isChecked(gui,cbxprivateChat):
		toplayer = QtBind.text(gui, tbxprivatechat)
		phBotChat.Private(toplayer, "RANGE "+range)
		log('Plugin Buton: KOMUT ' +toplayer+' A GÖNDERİLDİ.. ')
def btnsckur_clicked():
	sckur = QtBind.text(gui, tbxsckur)
	if QtBind.isChecked(gui,cbxAllChat):
		phBotChat.All('SCKUR '+sckur)
		log('Plugin Buton: KOMUT ALL CHATE GÖNDERİLDİ.. ')
	if QtBind.isChecked(gui,cbxPartyChat):
		phBotChat.Party('SCKUR '+sckur)
		log('Plugin Buton: KOMUT PARTY CHATE GÖNDERİLDİ.. ')
	if QtBind.isChecked(gui,cbxGuildChat):
		phBotChat.Guild('SCKUR '+sckur)
		log('Plugin Buton: KOMUT GUILD CHATE  GÖNDERİLDİ.. ')
	if QtBind.isChecked(gui,cbxUnionChat):
		phBotChat.Union('SCKUR '+sckur)
		log('Plugin Buton: KOMUT UNION CHATE GÖNDERİLDİ.. ')
	if QtBind.isChecked(gui,cbxprivateChat):
		toplayer = QtBind.text(gui, tbxprivatechat)
		phBotChat.Private(toplayer, "SCKUR "+sckur)
		log('Plugin Buton: KOMUT ' +toplayer+' A GÖNDERİLDİ.. ')
def btnalankur_clicked():
	alankur = QtBind.text(gui, tbxalankur)
	if QtBind.isChecked(gui,cbxAllChat):
		phBotChat.All('ALANKUR '+alankur)
		log('Plugin Buton: KOMUT ALL CHATE GÖNDERİLDİ.. ')
	if QtBind.isChecked(gui,cbxPartyChat):
		phBotChat.Party('ALANKUR '+alankur)
		log('Plugin Buton: KOMUT PARTY CHATE GÖNDERİLDİ.. ')
	if QtBind.isChecked(gui,cbxGuildChat):
		phBotChat.Guild('ALANKUR '+alankur)
		log('Plugin Buton: KOMUT GUILD CHATE  GÖNDERİLDİ.. ')
	if QtBind.isChecked(gui,cbxUnionChat):
		phBotChat.Union('ALANKUR '+alankur)
		log('Plugin Buton: KOMUT UNION CHATE GÖNDERİLDİ.. ')
	if QtBind.isChecked(gui,cbxprivateChat):
		toplayer = QtBind.text(gui, tbxprivatechat)
		phBotChat.Private(toplayer, "ALANKUR "+alankur)
		log('Plugin Buton: KOMUT ' +toplayer+' A GÖNDERİLDİ.. ')
def btnprofil_clicked():
	profil = QtBind.text(gui, tbxprofil)
	if QtBind.isChecked(gui,cbxAllChat):
		phBotChat.All('PROFIL '+profil)
		log('Plugin Buton: KOMUT ALL CHATE GÖNDERİLDİ.. ')
	if QtBind.isChecked(gui,cbxPartyChat):
		phBotChat.Party('PROFIL '+profil)
		log('Plugin Buton: KOMUT PARTY CHATE GÖNDERİLDİ.. ')
	if QtBind.isChecked(gui,cbxGuildChat):
		phBotChat.Guild('PROFIL '+profil)
		log('Plugin Buton: KOMUT GUILD CHATE  GÖNDERİLDİ.. ')
	if QtBind.isChecked(gui,cbxUnionChat):
		phBotChat.Union('PROFIL '+profil)
		log('Plugin Buton: KOMUT UNION CHATE GÖNDERİLDİ.. ')
	if QtBind.isChecked(gui,cbxprivateChat):
		toplayer = QtBind.text(gui, tbxprivatechat)
		phBotChat.Private(toplayer, "PROFIL "+profil)
		log('Plugin Buton: KOMUT ' +toplayer+' A GÖNDERİLDİ.. ')
def btnrevreturn_clicked():
	if QtBind.isChecked(gui,cbxAllChat):
		phBotChat.All('REVERSE RETURN')
		log('Plugin Buton: KOMUT ALL CHATE GÖNDERİLDİ.. ')
	if QtBind.isChecked(gui,cbxPartyChat):
		phBotChat.Party('REVERSE RETURN')
		log('Plugin Buton: KOMUT PARTY CHATE GÖNDERİLDİ.. ')
	if QtBind.isChecked(gui,cbxGuildChat):
		phBotChat.Guild('REVERSE RETURN')
		log('Plugin Buton: KOMUT GUILD CHATE  GÖNDERİLDİ.. ')
	if QtBind.isChecked(gui,cbxUnionChat):
		phBotChat.Union('REVERSE RETURN')
		log('Plugin Buton: KOMUT UNION CHATE GÖNDERİLDİ.. ')
	if QtBind.isChecked(gui,cbxprivateChat):
		toplayer = QtBind.text(gui, tbxprivatechat)
		phBotChat.Private(toplayer, "REVERSE RETURN")
		log('Plugin Buton: KOMUT ' +toplayer+' A GÖNDERİLDİ.. ')
def btnrevolum_clicked():
	if QtBind.isChecked(gui,cbxAllChat):
		phBotChat.All('REVERSE OLUM')
		log('Plugin Buton: KOMUT ALL CHATE GÖNDERİLDİ.. ')
	if QtBind.isChecked(gui,cbxPartyChat):
		phBotChat.Party('REVERSE OLUM')
		log('Plugin Buton: KOMUT PARTY CHATE GÖNDERİLDİ.. ')
	if QtBind.isChecked(gui,cbxGuildChat):
		phBotChat.Guild('REVERSE OLUM')
		log('Plugin Buton: KOMUT GUILD CHATE  GÖNDERİLDİ.. ')
	if QtBind.isChecked(gui,cbxUnionChat):
		phBotChat.Union('REVERSE OLUM')
		log('Plugin Buton: KOMUT UNION CHATE GÖNDERİLDİ.. ')
	if QtBind.isChecked(gui,cbxprivateChat):
		toplayer = QtBind.text(gui, tbxprivatechat)
		phBotChat.Private(toplayer, "REVERSE OLUM")
		log('Plugin Buton: KOMUT ' +toplayer+' A GÖNDERİLDİ.. ')
def btnrevalan_clicked():
	alan = QtBind.text(gui, tbxrevalan)
	if QtBind.isChecked(gui,cbxAllChat):
		phBotChat.All('REVERSE ALAN '+alan)
		log('Plugin Buton: KOMUT ALL CHATE GÖNDERİLDİ.. ')
	if QtBind.isChecked(gui,cbxPartyChat):
		phBotChat.Party('REVERSE ALAN '+alan)
		log('Plugin Buton: KOMUT PARTY CHATE GÖNDERİLDİ.. ')
	if QtBind.isChecked(gui,cbxGuildChat):
		phBotChat.Guild('REVERSE ALAN '+alan)
		log('Plugin Buton: KOMUT GUILD CHATE  GÖNDERİLDİ.. ')
	if QtBind.isChecked(gui,cbxUnionChat):
		phBotChat.Union('REVERSE ALAN '+alan)
		log('Plugin Buton: KOMUT UNION CHATE GÖNDERİLDİ.. ')
	if QtBind.isChecked(gui,cbxprivateChat):
		toplayer = QtBind.text(gui, tbxprivatechat)
		phBotChat.Private(toplayer, "REVERSE ALAN "+alan)
		log('Plugin Buton: KOMUT ' +toplayer+' A GÖNDERİLDİ.. ')
def btnrevplayer_clicked():
	revplayer = QtBind.text(gui, tbxrevplayer)
	if QtBind.isChecked(gui,cbxAllChat):
		phBotChat.All('REVERSE PLAYER '+revplayer)
		log('Plugin Buton: KOMUT ALL CHATE GÖNDERİLDİ.. ')
	if QtBind.isChecked(gui,cbxPartyChat):
		phBotChat.Party('REVERSE PLAYER '+revplayer)
		log('Plugin Buton: KOMUT PARTY CHATE GÖNDERİLDİ.. ')
	if QtBind.isChecked(gui,cbxGuildChat):
		phBotChat.Guild('REVERSE PLAYER '+revplayer)
		log('Plugin Buton: KOMUT GUILD CHATE  GÖNDERİLDİ.. ')
	if QtBind.isChecked(gui,cbxUnionChat):
		phBotChat.Union('REVERSE PLAYER '+revplayer)
		log('Plugin Buton: KOMUT UNION CHATE GÖNDERİLDİ.. ')
	if QtBind.isChecked(gui,cbxprivateChat):
		toplayer = QtBind.text(gui, tbxprivatechat)
		phBotChat.Private(toplayer, "REVERSE PLAYER "+revplayer)
		log('Plugin Buton: KOMUT ' +toplayer+' A GÖNDERİLDİ.. ')
def btnreturn_clicked():
	if QtBind.isChecked(gui,cbxAllChat):
		phBotChat.All('RETURN')
		log('Plugin Buton: KOMUT ALL CHATE GÖNDERİLDİ.. ')
	if QtBind.isChecked(gui,cbxPartyChat):
		phBotChat.Party('RETURN')
		log('Plugin Buton: KOMUT PARTY CHATE GÖNDERİLDİ.. ')
	if QtBind.isChecked(gui,cbxGuildChat):
		phBotChat.Guild('RETURN')
		log('Plugin Buton: KOMUT GUILD CHATE  GÖNDERİLDİ.. ')
	if QtBind.isChecked(gui,cbxUnionChat):
		phBotChat.Union('RETURN')
		log('Plugin Buton: KOMUT UNION CHATE GÖNDERİLDİ.. ')
	if QtBind.isChecked(gui,cbxprivateChat):
		toplayer = QtBind.text(gui, tbxprivatechat)
		phBotChat.Private(toplayer, "RETURN")
		log('Plugin Buton: KOMUT ' +toplayer+' A GÖNDERİLDİ.. ')
def btndagil_clicked():
	if QtBind.isChecked(gui,cbxAllChat):
		phBotChat.All('DAGIL')
		log('Plugin Buton: KOMUT ALL CHATE GÖNDERİLDİ.. ')
	if QtBind.isChecked(gui,cbxPartyChat):
		phBotChat.Party('DAGIL')
		log('Plugin Buton: KOMUT PARTY CHATE GÖNDERİLDİ.. ')
	if QtBind.isChecked(gui,cbxGuildChat):
		phBotChat.Guild('DAGIL')
		log('Plugin Buton: KOMUT GUILD CHATE  GÖNDERİLDİ.. ')
	if QtBind.isChecked(gui,cbxUnionChat):
		phBotChat.Union('DAGIL')
		log('Plugin Buton: KOMUT UNION CHATE GÖNDERİLDİ.. ')
	if QtBind.isChecked(gui,cbxprivateChat):
		toplayer = QtBind.text(gui, tbxprivatechat)
		phBotChat.Private(toplayer, "DAGIL")
		log('Plugin Buton: KOMUT ' +toplayer+' A GÖNDERİLDİ.. ')
def btndc_clicked():
	if QtBind.isChecked(gui,cbxAllChat):
		phBotChat.All('DC')
		log('Plugin Buton: KOMUT ALL CHATE GÖNDERİLDİ.. ')
	if QtBind.isChecked(gui,cbxPartyChat):
		phBotChat.Party('DC')
		log('Plugin Buton: KOMUT PARTY CHATE GÖNDERİLDİ.. ')
	if QtBind.isChecked(gui,cbxGuildChat):
		phBotChat.Guild('DC')
		log('Plugin Buton: KOMUT GUILD CHATE  GÖNDERİLDİ.. ')
	if QtBind.isChecked(gui,cbxUnionChat):
		phBotChat.Union('DC')
		log('Plugin Buton: KOMUT UNION CHATE GÖNDERİLDİ.. ')
	if QtBind.isChecked(gui,cbxprivateChat):
		toplayer = QtBind.text(gui, tbxprivatechat)
		phBotChat.Private(toplayer, "DC")
		log('Plugin Buton: KOMUT ' +toplayer+' A GÖNDERİLDİ.. ')
def btninfo_clicked():
	if QtBind.isChecked(gui,cbxAllChat):
		phBotChat.All('INFO')
		log('Plugin Buton: KOMUT ALL CHATE GÖNDERİLDİ.. ')
	if QtBind.isChecked(gui,cbxPartyChat):
		phBotChat.Party('INFO')
		log('Plugin Buton: KOMUT PARTY CHATE GÖNDERİLDİ.. ')
	if QtBind.isChecked(gui,cbxGuildChat):
		phBotChat.Guild('INFO')
		log('Plugin Buton: KOMUT GUILD CHATE  GÖNDERİLDİ.. ')
	if QtBind.isChecked(gui,cbxUnionChat):
		phBotChat.Union('INFO')
		log('Plugin Buton: KOMUT UNION CHATE GÖNDERİLDİ.. ')
	if QtBind.isChecked(gui,cbxprivateChat):
		toplayer = QtBind.text(gui, tbxprivatechat)
		phBotChat.Private(toplayer, "INFO")
		log('Plugin Buton: KOMUT ' +toplayer+' A GÖNDERİLDİ.. ')
def btnchat_clicked():
	cesit = QtBind.text(gui, tbxchatcesit)
	mesaj = QtBind.text(gui, tbxchatmesaj)
	if QtBind.isChecked(gui,cbxAllChat):
		phBotChat.All('CHAT '+cesit+' '+mesaj)
		log('Plugin Buton: KOMUT ALL CHATE GÖNDERİLDİ.. ')
	if QtBind.isChecked(gui,cbxPartyChat):
		phBotChat.Party('CHAT '+cesit+' '+mesaj)
		log('Plugin Buton: KOMUT PARTY CHATE GÖNDERİLDİ.. ')
	if QtBind.isChecked(gui,cbxGuildChat):
		phBotChat.Guild('CHAT '+cesit+' '+mesaj)
		log('Plugin Buton: KOMUT GUILD CHATE  GÖNDERİLDİ.. ')
	if QtBind.isChecked(gui,cbxUnionChat):
		phBotChat.Union('CHAT '+cesit+' '+mesaj)
		log('Plugin Buton: KOMUT UNION CHATE GÖNDERİLDİ.. ')
	if QtBind.isChecked(gui,cbxprivateChat):
		toplayer = QtBind.text(gui, tbxprivatechat)
		phBotChat.Private(toplayer,'CHAT '+cesit+' '+mesaj)
		log('Plugin Buton: KOMUT ' +toplayer+' A GÖNDERİLDİ.. ')
def ListContains(text,lst):
	text = text.lower()
	for i in range(len(lst)):
		if lst[i].lower() == text:
			return True
	return False
def btnliderekle_clicked():
	if inGame:
		player = QtBind.text(gui, lblcharname)
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
			with open(getConfig(), "w") as f:
				f.write(json.dumps(data, indent=4, sort_keys=True))
			QtBind.append(gui, lstLeaders, player)
			log('Plugin: Lider eklendi.. [' + player + ']')
def btnlidercikart_clicked():
	if inGame:
		selectedItem = QtBind.text(gui, lblcharname)
		if selectedItem:
			if os.path.exists(getConfig()):
				data = {"Leaders": []}
				with open(getConfig(), 'r') as f:
					data = json.load(f)
				try:
					# MEVCUT ISIM VARKEN EKLENEN AYNI ISMI SILME
					data["Leaders"].remove(selectedItem)
					with open(getConfig(), "w") as f:
						f.write(json.dumps(data, indent=4, sort_keys=True))
				except:
					pass  # DOSYA YOKSA GORMEZDEN GEL
			QtBind.remove(gui, lstLeaders, selectedItem)
			log('Plugin: Lider Silindi.. [' + selectedItem + ']')
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
		elif msg == "RETURN":
				# SISTEME GORE COK CHAR KULLANILDIGINDA CPU KULLANIMI ARTAR
				Timer(random.uniform(0.5,2),use_return_scroll).start()
				log('Plugin: RETURN SCROLL KULLANILIYOR.')
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
		elif msg == "INFO":
			char_data = get_character_data()
			currentHp = (char_data['hp'] / char_data['hp_max']) * 100
			currentExp = (char_data['current_exp'] / char_data['max_exp']) * 100
			currentJobExp = (char_data['job_current_exp'] / char_data['job_max_exp']) * 100
			level = char_data['level']
			gold = char_data['gold']
			skillpoint = char_data['sp']
			jobname = char_data['job_name']
			guildname = char_data['guild']
			message = "HP: {:0.2f}, EXP: {:0.2f}, Level: {}, Job Exp: {:0.2f}, Gold: {:,}, SP: {}, Job Nick: {}, Guild: {}".format(currentHp, currentExp,
																								  level, currentJobExp,
																								  gold,skillpoint,jobname,guildname)
			phBotChat.Private(player, message)
def ResetSkip():
	global SkipCommand
	SkipCommand = False
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
	if inGame:
		isim = get_character_data()['name']
		QtBind.setText(gui, lblcharname, isim)
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
# PLUGIN YUKLENIRSE
log("Plugin: "+pName+" v"+pVersion+" BASARIYLA YUKLENDI.")
if os.path.exists(getPath()):
	# CONFIG YUKLEME
	loadConfigs()
else:
	# CONFIG DOSYASI OLUSTURMA
	os.makedirs(getPath())
	log('Plugin: '+pName+' CONFIG KLASORU OLUSTURULDU.')
