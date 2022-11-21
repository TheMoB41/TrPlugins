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
pVersion = '1.2.0'
pUrl = 'https://raw.githubusercontent.com/TheMoB41/TrPlugins/main/TrController.py'

COMMANDS_CODES = {
	'ZERKPOT': ['ZERKPOT'],
	'STRSC': ['STRSC'],
	'INTSC': ['INTSC'],
	'MPSC': ['MPSC'],
	'HPSC': ['HPSC'],
	'DAMAGESC': ['DAMAGESC'],
	'RESSC': ['RESSC'],
	'TGSC': ['TGSC'],
	'DAMAGEABSSC': ['DAMAGEABSSC'],
	'DAMAGEINCSC': ['DAMAGEINCSC']
}
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
#GUI2
gui_ = QtBind.init(__name__,pName+"( BUTON )")
x=10
y=10
QtBind.createLabel(gui_,'GÖNDERİLECEK CHAT\n          KANALI : ',x+605,y+165)
QtBind.createList(gui_,x+615,y+195,95,105)
cbxAllChat = QtBind.createCheckBox(gui_,"cbxAll_clicked","ALL CHAT",x+620,y+200)
cbxPartyChat = QtBind.createCheckBox(gui_,"cbxParty_clicked","PARTY CHAT",x+620,y+215)
cbxGuildChat = QtBind.createCheckBox(gui_,"cbxGuild_clicked","GUILD CHAT",x+620,y+230)
cbxUnionChat = QtBind.createCheckBox(gui_,"cbxUnion_clicked","UNION CHAT",x+620,y+245)
cbxprivateChat = QtBind.createCheckBox(gui_,"cbxprivate_clicked","PRIVATE CHAT",x+620,y+260)
tbxprivatechat = QtBind.createLineEdit(gui_,"PLAYER",x+640,y+275,60,20)
btnkaydet = QtBind.createButton(gui_,'btnkaydet_clicked'," DEGISIKLIKLERI KAYDET ",x+480,y+210)
QtBind.createList(gui_,5,5,110,305)
btnbotbaslat = QtBind.createButton(gui_,'btnbotbaslat_clicked',"     BAŞLAT     ",x,y)
btnbotdurdur = QtBind.createButton(gui_,'btnbotdurdur_clicked',"    DURDUR    ",x,y+25)
btntrace = QtBind.createButton(gui_,'btntrace_clicked',"     TRACE     ",x,y+50)
btnnotrace = QtBind.createButton(gui_,'btnnotrace_clicked',"   NOTRACE   ",x,y+75)
btnreturn= QtBind.createButton(gui_,'btnreturn_clicked',"    RETURN     ",x,y+100)
btnfollow = QtBind.createButton(gui_,'btnfollow_clicked',"    FOLLOW    ",x,y+125)
btnnofollow = QtBind.createButton(gui_,'btnnofollow_clicked'," NOFOLLOW ",x,y+150)
btnzerk= QtBind.createButton(gui_,'btnzerk_clicked',"       ZERK       ",x,y+175)
btnkoral = QtBind.createButton(gui_,'btnkoral_clicked',"     KORAL    	 ",x,y+200)
btndagil= QtBind.createButton(gui_,'btndagil_clicked',"      DAGIL      ",x,y+225)
btnrevreturn= QtBind.createButton(gui_,'btnrevreturn_clicked',"  REVERSE RETURN  ",x,y+250)
btnrevolum= QtBind.createButton(gui_,'btnrevolum_clicked'," REVERSE OLUM ",x,y+275)
QtBind.createList(gui_,115,5,200,305)
btnprofil= QtBind.createButton(gui_,'btnprofil_clicked',"     PROFIL     ",x+110,y)
tbxprofil = QtBind.createLineEdit(gui_,"PROFIL ISMI",x+185,y-2,100,20)
btninject= QtBind.createButton(gui_,'btninject_clicked',"     INJECT     ",x+110,y+25)
tbxinject = QtBind.createLineEdit(gui_,"OPCODE+DATA",x+185,y+23,100,20)
btnrecall= QtBind.createButton(gui_,'btnrecall_clicked',"     RECALL     ",x+110,y+50)
tbxrecall = QtBind.createLineEdit(gui_,"TOWN ISMI",x+185,y+48,100,20)
btnsckur= QtBind.createButton(gui_,'btnsckur_clicked',"     SCKUR     ",x+110,y+75)
tbxsckur = QtBind.createLineEdit(gui_,"DOSYA YOLU",x+185,y+73,100,20)
btnalankur= QtBind.createButton(gui_,'btnalankur_clicked',"   ALANKUR   ",x+110,y+100)
tbxalankur = QtBind.createLineEdit(gui_,"ALAN ADI",x+185,y+98,100,20)
btnrevalan= QtBind.createButton(gui_,'btnrevalan_clicked',"  REVERSE ALAN   ",x+110,y+125)
tbxrevalan = QtBind.createLineEdit(gui_,"ALAN ADI",x+205,y+123,80,20)
btnrevplayer= QtBind.createButton(gui_,'btnrevplayer_clicked'," REVERSE PLAYER ",x+110,y+150)
tbxrevplayer = QtBind.createLineEdit(gui_,"PLAYER",x+205,y+148,80,20)
btngiy= QtBind.createButton(gui_,'btngiy_clicked',"        GİY        ",x+110,y+175)
tbxgiy = QtBind.createLineEdit(gui_,"ITEM ADI",x+185,y+173,100,20)
btncikart= QtBind.createButton(gui_,'btncikart_clicked',"     CIKART     ",x+110,y+200)
tbxcikart = QtBind.createLineEdit(gui_,"ITEM ADI",x+185,y+198,100,20)
btntraceplayer = QtBind.createButton(gui_,'btntraceplayer_clicked',"     TRACE     ",x+110,y+225)
tbxtraceplayer = QtBind.createLineEdit(gui_,"PLAYER",x+185,y+223,100,20)
btnkorkur = QtBind.createButton(gui_,'btnkorkur_clicked',"    KORKUR    ",x+110,y+250)
tbxkorkur = QtBind.createLineEdit(gui_,"X,Y",x+185,y+248,100,20)
btnrange = QtBind.createButton(gui_,'btnrange_clicked',"     RANGE     ",x+110,y+275)
tbxrange = QtBind.createLineEdit(gui_,"000035",x+185,y+273,100,20)
QtBind.createList(gui_,315,5,80,305)
btnstrsc = QtBind.createButton(gui_,'btnstrsc_clicked',"      STRSC     ",x+310,y)
btndc= QtBind.createButton(gui_,'btndc_clicked',"        DC        ",x+310,y+25)
btnptayril= QtBind.createButton(gui_,'btnptayril_clicked',"    PTAYRIL    ",x+310,y+50)
btnintsc = QtBind.createButton(gui_,'btnintsc_clicked',"      INTSC     ",x+310,y+75)
btninfo= QtBind.createButton(gui_,'btninfo_clicked',"       INFO      ",x+310,y+100)
btntargeton= QtBind.createButton(gui_,'btntargeton_clicked',"  TARGETON  ",x+310,y+125)
btntargetoff= QtBind.createButton(gui_,'btntargetoff_clicked'," TARGETOFF ",x+310,y+150)
btndeffon= QtBind.createButton(gui_,'btndeffon_clicked',"    DEFFON    ",x+310,y+175)
btndeffoff= QtBind.createButton(gui_,'btndeffoff_clicked',"   DEFFOFF   ",x+310,y+200)
btnhwt= QtBind.createButton(gui_,'btnhwt_clicked',"      HWT1     ",x+310,y+225)
btnhwtt= QtBind.createButton(gui_,'btnhwtt_clicked',"      HWT2     ",x+310,y+250)
btnhwttt= QtBind.createButton(gui_,'btnhwttt_clicked',"      HWT3     ",x+310,y+275)
QtBind.createList(gui_,395,105,90,150)
btnressc = QtBind.createButton(gui_,'btnressc_clicked',"        RESSC        ",x+390,y+100)
btntgsc = QtBind.createButton(gui_,'btntgsc_clicked',"         TGSC         ",x+390,y+125)
btnhpsc = QtBind.createButton(gui_,'btnhpsc_clicked',"         HPSC         ",x+390,y+150)
btnmpsc = QtBind.createButton(gui_,'btnmpsc_clicked',"         MPSC         ",x+390,y+175)
btndamagesc = QtBind.createButton(gui_,'btndamagesc_clicked',"    DAMAGESC    ",x+390,y+200)
btndamageabssc = QtBind.createButton(gui_,'btndamageabssc_clicked'," DAMAGEABSSC ",x+390,y+225)
QtBind.createList(gui_,395,255,185,55)
btntp= QtBind.createButton(gui_,'btntp_clicked',"        TP        ",x+390,y+250)
tbxtp = QtBind.createLineEdit(gui_,"A,B",x+465,y+248,100,20)
btncape= QtBind.createButton(gui_,'btncape_clicked',"      CAPE      ",x+390,y+275)
tbxcape = QtBind.createLineEdit(gui_,"RENK",x+465,y+273,100,20)
QtBind.createList(gui_,395,5,215,50)
lblbilgi = QtBind.createLabel(gui_,'Bulunduğun Char :',x+420,y)
lblcharname = QtBind.createLabel(gui_,'',x+510,y)
lblbilgii = QtBind.createLabel(gui_,'Lider Listesine',x+390,y+25)
btnliderekle= QtBind.createButton(gui_,'btnliderekle_clicked',"      EKLE      ",x+460,y+25)
btnlidercikart= QtBind.createButton(gui_,'btnlidercikart_clicked',"    ÇIKART    ",x+530,y+25)
QtBind.createList(gui_,395,55,315,25)
lblhotanftw = QtBind.createLabel(gui_,'Hotan Fortress :',x+390,y+50)
tbxhotandis = QtBind.createLineEdit(gui_,"DIS KAPI NO",x+475,y+47,70,20)
lblhotanftww = QtBind.createLabel(gui_,'dan',x+555,y+50)
tbxhotanic = QtBind.createLineEdit(gui_,"IC KAPI NO",x+585,y+47,70,20)
btnhotanftw = QtBind.createButton(gui_,'btnhotanftw_clicked'," GİT ",x+670,y+50)
QtBind.createList(gui_,395,75,315,25)
lbljanganftw = QtBind.createLabel(gui_,'Jangan Fortress :',x+390,y+70)
tbxjangandis = QtBind.createLineEdit(gui_,"DIS KAPI NO",x+475,y+67,70,20)
lbljanganftww = QtBind.createLabel(gui_,'dan',x+555,y+70)
tbxjanganic = QtBind.createLineEdit(gui_,"IC KAPI NO",x+585,y+67,70,20)
btnjanganftw = QtBind.createButton(gui_,'btnjanganftw_clicked'," GİT ",x+670,y+70)
QtBind.createList(gui_,488,115,232,55)
btnchat = QtBind.createButton(gui_,'btnchat_clicked',"         CHAT         ",x+560,y+110)
tbxchatcesit = QtBind.createLineEdit(gui_,"CESIT",x+485,y+135,50,20)
tbxchatmesaj = QtBind.createLineEdit(gui_,"MESAJ",x+540,y+135,168,20)
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
			if "PRIVATECHAT" in data:
				QtBind.setText(gui_, tbxprivatechat, data["PRIVATECHAT"])
			if "PROFIL" in data:
				QtBind.setText(gui_, tbxprofil, data["PROFIL"])
			if "INJECT" in data:
				QtBind.setText(gui_, tbxinject, data["INJECT"])
			if "RECALL" in data:
				QtBind.setText(gui_, tbxrecall, data["RECALL"])
			if "SCKUR" in data:
				QtBind.setText(gui_, tbxsckur, data["SCKUR"])
			if "ALANKUR" in data:
				QtBind.setText(gui_, tbxalankur, data["ALANKUR"])
			if "REVALAN" in data:
				QtBind.setText(gui_, tbxrevalan, data["REVALAN"])
			if "REVPLAYER" in data:
				QtBind.setText(gui_, tbxrevplayer, data["REVPLAYER"])
			if "GIY" in data:
				QtBind.setText(gui_, tbxgiy, data["GIY"])
			if "CIKART" in data:
				QtBind.setText(gui_, tbxcikart, data["CIKART"])
			if "TRACEPL" in data:
				QtBind.setText(gui_, tbxtraceplayer, data["TRACEPL"])
			if "KORKUR" in data:
				QtBind.setText(gui_, tbxkorkur, data["KORKUR"])
			if "RANGE" in data:
				QtBind.setText(gui_, tbxrange, data["RANGE"])
			if "TP" in data:
				QtBind.setText(gui_, tbxtp, data["TP"])
			if "CAPE" in data:
				QtBind.setText(gui_, tbxcape, data["CAPE"])
			if "HDIS" in data:
				QtBind.setText(gui_, tbxhotandis, data["HDIS"])
			if "HIC" in data:
				QtBind.setText(gui_, tbxhotanic, data["HIC"])
			if "JDIS" in data:
				QtBind.setText(gui_, tbxjangandis, data["JDIS"])
			if "JIC" in data:
				QtBind.setText(gui_, tbxjanganic, data["JIC"])
			if "CHATCESIT" in data:
				QtBind.setText(gui_, tbxchatcesit, data["CHATCESIT"])
			if "CHATMESAJ" in data:
				QtBind.setText(gui_, tbxchatmesaj, data["CHATMESAJ"])
def btnkaydet_clicked():
	if inGame:
		data = {}
		if os.path.exists(getConfig()):
			with open(getConfig(), 'r') as f:
				data = json.load(f)
			data["PRIVATECHAT"] = QtBind.text(gui_, tbxprivatechat)
			data["PROFIL"] = QtBind.text(gui_, tbxprofil)
			data["INJECT"] = QtBind.text(gui_, tbxinject)
			data["RECALL"] = QtBind.text(gui_, tbxrecall)
			data["SCKUR"] = QtBind.text(gui_, tbxsckur)
			data["ALANKUR"] = QtBind.text(gui_, tbxalankur)
			data["REVALAN"] = QtBind.text(gui_, tbxrevalan)
			data["REVPLAYER"] = QtBind.text(gui_, tbxrevplayer)
			data["GIY"] = QtBind.text(gui_, tbxgiy)
			data["CIKART"] = QtBind.text(gui_, tbxcikart)
			data["TRACEPL"] = QtBind.text(gui_, tbxtraceplayer)
			data["KORKUR"] = QtBind.text(gui_, tbxkorkur)
			data["RANGE"] = QtBind.text(gui_, tbxrange)
			data["TP"] = QtBind.text(gui_, tbxtp)
			data["CAPE"] = QtBind.text(gui_, tbxcape)
			data["HDIS"] = QtBind.text(gui_, tbxhotandis)
			data["HIC"] = QtBind.text(gui_, tbxhotanic)
			data["JDIS"] = QtBind.text(gui_, tbxjangandis)
			data["JIC"] = QtBind.text(gui_, tbxjanganic)
			data["CHATCESIT"] = QtBind.text(gui_, tbxchatcesit)
			data["CHATMESAJ"] = QtBind.text(gui_, tbxchatmesaj)
		with open(getConfig(), "w") as f:
			f.write(json.dumps(data, indent=4, sort_keys=True))
		log('Plugin Buton: CONFIG KAYIT EDİLDİ.. ')
def btnbotbaslat_clicked():
	if QtBind.isChecked(gui_,cbxAllChat):
		phBotChat.All('BASLAT')
		log('Plugin Buton: KOMUT ALL CHATE GÖNDERİLDİ.. ')
	if QtBind.isChecked(gui_,cbxPartyChat):
		phBotChat.Party('BASLAT')
		log('Plugin Buton: KOMUT PARTY CHATE GÖNDERİLDİ.. ')
	if QtBind.isChecked(gui_,cbxGuildChat):
		phBotChat.Guild('BASLAT')
		log('Plugin Buton: KOMUT GUILD CHATE  GÖNDERİLDİ.. ')
	if QtBind.isChecked(gui_,cbxUnionChat):
		phBotChat.Union('BASLAT')
		log('Plugin Buton: KOMUT UNION CHATE GÖNDERİLDİ.. ')
	if QtBind.isChecked(gui_,cbxprivateChat):
		toplayer = QtBind.text(gui_, tbxprivatechat)
		phBotChat.Private(toplayer, "BASLAT")
		log('Plugin Buton: KOMUT ' +toplayer+' A GÖNDERİLDİ.. ')
def btnbotdurdur_clicked():
	if QtBind.isChecked(gui_,cbxAllChat):
		phBotChat.All('DURDUR')
		log('Plugin Buton: KOMUT ALL CHATE GÖNDERİLDİ.. ')
	if QtBind.isChecked(gui_,cbxPartyChat):
		phBotChat.Party('DURDUR')
		log('Plugin Buton: KOMUT PARTY CHATE GÖNDERİLDİ.. ')
	if QtBind.isChecked(gui_,cbxGuildChat):
		phBotChat.Guild('DURDUR')
		log('Plugin Buton: KOMUT GUILD CHATE  GÖNDERİLDİ.. ')
	if QtBind.isChecked(gui_,cbxUnionChat):
		phBotChat.Union('DURDUR')
		log('Plugin Buton: KOMUT UNION CHATE GÖNDERİLDİ.. ')
	if QtBind.isChecked(gui_,cbxprivateChat):
		toplayer = QtBind.text(gui_, tbxprivatechat)
		phBotChat.Private(toplayer, "DURDUR")
		log('Plugin Buton: KOMUT ' +toplayer+' A GÖNDERİLDİ.. ')
def btntrace_clicked():
	if QtBind.isChecked(gui_,cbxAllChat):
		phBotChat.All('TRACE')
		log('Plugin Buton: KOMUT ALL CHATE GÖNDERİLDİ.. ')
	if QtBind.isChecked(gui_,cbxPartyChat):
		phBotChat.Party('TRACE')
		log('Plugin Buton: KOMUT PARTY CHATE GÖNDERİLDİ.. ')
	if QtBind.isChecked(gui_,cbxGuildChat):
		phBotChat.Guild('TRACE')
		log('Plugin Buton: KOMUT GUILD CHATE  GÖNDERİLDİ.. ')
	if QtBind.isChecked(gui_,cbxUnionChat):
		phBotChat.Union('TRACE')
		log('Plugin Buton: KOMUT UNION CHATE GÖNDERİLDİ.. ')
	if QtBind.isChecked(gui_,cbxprivateChat):
		toplayer = QtBind.text(gui_, tbxprivatechat)
		phBotChat.Private(toplayer, "TRACE")
		log('Plugin Buton: KOMUT ' +toplayer+' A GÖNDERİLDİ.. ')
def btnnotrace_clicked():
	if QtBind.isChecked(gui_,cbxAllChat):
		phBotChat.All('NOTRACE')
		log('Plugin Buton: KOMUT ALL CHATE GÖNDERİLDİ.. ')
	if QtBind.isChecked(gui_,cbxPartyChat):
		phBotChat.Party('NOTRACE')
		log('Plugin Buton: KOMUT PARTY CHATE GÖNDERİLDİ.. ')
	if QtBind.isChecked(gui_,cbxGuildChat):
		phBotChat.Guild('NOTRACE')
		log('Plugin Buton: KOMUT GUILD CHATE  GÖNDERİLDİ.. ')
	if QtBind.isChecked(gui_,cbxUnionChat):
		phBotChat.Union('NOTRACE')
		log('Plugin Buton: KOMUT UNION CHATE GÖNDERİLDİ.. ')
	if QtBind.isChecked(gui_,cbxprivateChat):
		toplayer = QtBind.text(gui_, tbxprivatechat)
		phBotChat.Private(toplayer, "NOTRACE")
		log('Plugin Buton: KOMUT ' +toplayer+' A GÖNDERİLDİ.. ')
def btntraceplayer_clicked():
	NICK = QtBind.text(gui_, tbxtraceplayer)
	if QtBind.isChecked(gui_,cbxAllChat):
		phBotChat.All('TRACE '+NICK)
		log('Plugin Buton: KOMUT ALL CHATE GÖNDERİLDİ.. ')
	if QtBind.isChecked(gui_,cbxPartyChat):
		phBotChat.Party('TRACE '+NICK)
		log('Plugin Buton: KOMUT PARTY CHATE GÖNDERİLDİ.. ')
	if QtBind.isChecked(gui_,cbxGuildChat):
		phBotChat.Guild('TRACE '+NICK)
		log('Plugin Buton: KOMUT GUILD CHATE  GÖNDERİLDİ.. ')
	if QtBind.isChecked(gui_,cbxUnionChat):
		phBotChat.Union('TRACE '+NICK)
		log('Plugin Buton: KOMUT UNION CHATE GÖNDERİLDİ.. ')
	if QtBind.isChecked(gui_,cbxprivateChat):
		toplayer = QtBind.text(gui_, tbxprivatechat)
		phBotChat.Private(toplayer, "TRACE "+NICK)
		log('Plugin Buton: KOMUT ' +toplayer+' A GÖNDERİLDİ.. ')
def btnfollow_clicked():
	if QtBind.isChecked(gui_,cbxAllChat):
		log('Plugin Buton: BU KOMUT YALNIZCA PARTY CHATTE KULLANILABİLİR..')
	if QtBind.isChecked(gui_,cbxPartyChat):
		phBotChat.Party('FOLLOW')
		log('Plugin Buton: KOMUT PARTY CHATE GÖNDERİLDİ.. ')
	if QtBind.isChecked(gui_,cbxGuildChat):
		log('Plugin Buton: BU KOMUT YALNIZCA PARTY CHATTE KULLANILABİLİR..')
	if QtBind.isChecked(gui_,cbxUnionChat):
		log('Plugin Buton: BU KOMUT YALNIZCA PARTY CHATTE KULLANILABİLİR..')
	if QtBind.isChecked(gui_,cbxprivateChat):
		log('Plugin Buton: BU KOMUT YALNIZCA PARTY CHATTE KULLANILABİLİR..')
def btnnofollow_clicked():
	if QtBind.isChecked(gui_,cbxAllChat):
		log('Plugin Buton: BU KOMUT YALNIZCA PARTY CHATTE KULLANILABİLİR..')
	if QtBind.isChecked(gui_,cbxPartyChat):
		phBotChat.Party('NOFOLLOW')
		log('Plugin Buton: KOMUT PARTY CHATE GÖNDERİLDİ.. ')
	if QtBind.isChecked(gui_,cbxGuildChat):
		log('Plugin Buton: BU KOMUT YALNIZCA PARTY CHATTE KULLANILABİLİR..')
	if QtBind.isChecked(gui_,cbxUnionChat):
		log('Plugin Buton: BU KOMUT YALNIZCA PARTY CHATTE KULLANILABİLİR..')
	if QtBind.isChecked(gui_,cbxprivateChat):
		log('Plugin Buton: BU KOMUT YALNIZCA PARTY CHATTE KULLANILABİLİR..')
def btnkorkur_clicked():
	XY = QtBind.text(gui_, tbxkorkur)
	if QtBind.isChecked(gui_,cbxAllChat):
		phBotChat.All('KORKUR '+XY)
		log('Plugin Buton: KOMUT ALL CHATE GÖNDERİLDİ.. ')
	if QtBind.isChecked(gui_,cbxPartyChat):
		phBotChat.Party('KORKUR '+XY)
		log('Plugin Buton: KOMUT PARTY CHATE GÖNDERİLDİ.. ')
	if QtBind.isChecked(gui_,cbxGuildChat):
		phBotChat.Guild('KORKUR '+XY)
		log('Plugin Buton: KOMUT GUILD CHATE  GÖNDERİLDİ.. ')
	if QtBind.isChecked(gui_,cbxUnionChat):
		phBotChat.Union('KORKUR '+XY)
		log('Plugin Buton: KOMUT UNION CHATE GÖNDERİLDİ.. ')
	if QtBind.isChecked(gui_,cbxprivateChat):
		toplayer = QtBind.text(gui_, tbxprivatechat)
		phBotChat.Private(toplayer, "KORKUR "+XY)
		log('Plugin Buton: KOMUT ' +toplayer+' A GÖNDERİLDİ.. ')
def btnkoral_clicked():
	if QtBind.isChecked(gui_,cbxAllChat):
		phBotChat.All('KORAL')
		log('Plugin Buton: KOMUT ALL CHATE GÖNDERİLDİ.. ')
	if QtBind.isChecked(gui_,cbxPartyChat):
		phBotChat.Party('KORAL')
		log('Plugin Buton: KOMUT PARTY CHATE GÖNDERİLDİ.. ')
	if QtBind.isChecked(gui_,cbxGuildChat):
		phBotChat.Guild('KORAL')
		log('Plugin Buton: KOMUT GUILD CHATE  GÖNDERİLDİ.. ')
	if QtBind.isChecked(gui_,cbxUnionChat):
		phBotChat.Union('KORAL')
		log('Plugin Buton: KOMUT UNION CHATE GÖNDERİLDİ.. ')
	if QtBind.isChecked(gui_,cbxprivateChat):
		toplayer = QtBind.text(gui_, tbxprivatechat)
		phBotChat.Private(toplayer, "KORAL")
		log('Plugin Buton: KOMUT ' +toplayer+' A GÖNDERİLDİ.. ')
def btnrange_clicked():
	range = QtBind.text(gui_, tbxrange)
	if QtBind.isChecked(gui_,cbxAllChat):
		phBotChat.All('RANGE '+range)
		log('Plugin Buton: KOMUT ALL CHATE GÖNDERİLDİ.. ')
	if QtBind.isChecked(gui_,cbxPartyChat):
		phBotChat.Party('RANGE '+range)
		log('Plugin Buton: KOMUT PARTY CHATE GÖNDERİLDİ.. ')
	if QtBind.isChecked(gui_,cbxGuildChat):
		phBotChat.Guild('RANGE '+range)
		log('Plugin Buton: KOMUT GUILD CHATE  GÖNDERİLDİ.. ')
	if QtBind.isChecked(gui_,cbxUnionChat):
		phBotChat.Union('RANGE '+range)
		log('Plugin Buton: KOMUT UNION CHATE GÖNDERİLDİ.. ')
	if QtBind.isChecked(gui_,cbxprivateChat):
		toplayer = QtBind.text(gui_, tbxprivatechat)
		phBotChat.Private(toplayer, "RANGE "+range)
		log('Plugin Buton: KOMUT ' +toplayer+' A GÖNDERİLDİ.. ')
def btnsckur_clicked():
	sckur = QtBind.text(gui_, tbxsckur)
	if QtBind.isChecked(gui_,cbxAllChat):
		phBotChat.All('SCKUR '+sckur)
		log('Plugin Buton: KOMUT ALL CHATE GÖNDERİLDİ.. ')
	if QtBind.isChecked(gui_,cbxPartyChat):
		phBotChat.Party('SCKUR '+sckur)
		log('Plugin Buton: KOMUT PARTY CHATE GÖNDERİLDİ.. ')
	if QtBind.isChecked(gui_,cbxGuildChat):
		phBotChat.Guild('SCKUR '+sckur)
		log('Plugin Buton: KOMUT GUILD CHATE  GÖNDERİLDİ.. ')
	if QtBind.isChecked(gui_,cbxUnionChat):
		phBotChat.Union('SCKUR '+sckur)
		log('Plugin Buton: KOMUT UNION CHATE GÖNDERİLDİ.. ')
	if QtBind.isChecked(gui_,cbxprivateChat):
		toplayer = QtBind.text(gui_, tbxprivatechat)
		phBotChat.Private(toplayer, "SCKUR "+sckur)
		log('Plugin Buton: KOMUT ' +toplayer+' A GÖNDERİLDİ.. ')
def btnalankur_clicked():
	alankur = QtBind.text(gui_, tbxalankur)
	if QtBind.isChecked(gui_,cbxAllChat):
		phBotChat.All('ALANKUR '+alankur)
		log('Plugin Buton: KOMUT ALL CHATE GÖNDERİLDİ.. ')
	if QtBind.isChecked(gui_,cbxPartyChat):
		phBotChat.Party('ALANKUR '+alankur)
		log('Plugin Buton: KOMUT PARTY CHATE GÖNDERİLDİ.. ')
	if QtBind.isChecked(gui_,cbxGuildChat):
		phBotChat.Guild('ALANKUR '+alankur)
		log('Plugin Buton: KOMUT GUILD CHATE  GÖNDERİLDİ.. ')
	if QtBind.isChecked(gui_,cbxUnionChat):
		phBotChat.Union('ALANKUR '+alankur)
		log('Plugin Buton: KOMUT UNION CHATE GÖNDERİLDİ.. ')
	if QtBind.isChecked(gui_,cbxprivateChat):
		toplayer = QtBind.text(gui_, tbxprivatechat)
		phBotChat.Private(toplayer, "ALANKUR "+alankur)
		log('Plugin Buton: KOMUT ' +toplayer+' A GÖNDERİLDİ.. ')
def btnprofil_clicked():
	profil = QtBind.text(gui_, tbxprofil)
	if QtBind.isChecked(gui_,cbxAllChat):
		phBotChat.All('PROFIL '+profil)
		log('Plugin Buton: KOMUT ALL CHATE GÖNDERİLDİ.. ')
	if QtBind.isChecked(gui_,cbxPartyChat):
		phBotChat.Party('PROFIL '+profil)
		log('Plugin Buton: KOMUT PARTY CHATE GÖNDERİLDİ.. ')
	if QtBind.isChecked(gui_,cbxGuildChat):
		phBotChat.Guild('PROFIL '+profil)
		log('Plugin Buton: KOMUT GUILD CHATE  GÖNDERİLDİ.. ')
	if QtBind.isChecked(gui_,cbxUnionChat):
		phBotChat.Union('PROFIL '+profil)
		log('Plugin Buton: KOMUT UNION CHATE GÖNDERİLDİ.. ')
	if QtBind.isChecked(gui_,cbxprivateChat):
		toplayer = QtBind.text(gui_, tbxprivatechat)
		phBotChat.Private(toplayer, "PROFIL "+profil)
		log('Plugin Buton: KOMUT ' +toplayer+' A GÖNDERİLDİ.. ')
def btninject_clicked():
	opcodedata = QtBind.text(gui_, tbxinject)
	if QtBind.isChecked(gui_,cbxAllChat):
		phBotChat.All('INJECT '+opcodedata)
		log('Plugin Buton: KOMUT ALL CHATE GÖNDERİLDİ.. ')
	if QtBind.isChecked(gui_,cbxPartyChat):
		phBotChat.Party('INJECT '+opcodedata)
		log('Plugin Buton: KOMUT PARTY CHATE GÖNDERİLDİ.. ')
	if QtBind.isChecked(gui_,cbxGuildChat):
		phBotChat.Guild('INJECT '+opcodedata)
		log('Plugin Buton: KOMUT GUILD CHATE  GÖNDERİLDİ.. ')
	if QtBind.isChecked(gui_,cbxUnionChat):
		phBotChat.Union('INJECT '+opcodedata)
		log('Plugin Buton: KOMUT UNION CHATE GÖNDERİLDİ.. ')
	if QtBind.isChecked(gui_,cbxprivateChat):
		toplayer = QtBind.text(gui_, tbxprivatechat)
		phBotChat.Private(toplayer, "INJECT "+opcodedata)
		log('Plugin Buton: KOMUT ' +toplayer+' A GÖNDERİLDİ.. ')
def btnrecall_clicked():
	recall = QtBind.text(gui_, tbxrecall)
	if QtBind.isChecked(gui_,cbxAllChat):
		phBotChat.All('RECALL '+recall)
		log('Plugin Buton: KOMUT ALL CHATE GÖNDERİLDİ.. ')
	if QtBind.isChecked(gui_,cbxPartyChat):
		phBotChat.Party('RECALL '+recall)
		log('Plugin Buton: KOMUT PARTY CHATE GÖNDERİLDİ.. ')
	if QtBind.isChecked(gui_,cbxGuildChat):
		phBotChat.Guild('RECALL '+recall)
		log('Plugin Buton: KOMUT GUILD CHATE  GÖNDERİLDİ.. ')
	if QtBind.isChecked(gui_,cbxUnionChat):
		phBotChat.Union('RECALL '+recall)
		log('Plugin Buton: KOMUT UNION CHATE GÖNDERİLDİ.. ')
	if QtBind.isChecked(gui_,cbxprivateChat):
		toplayer = QtBind.text(gui_, tbxprivatechat)
		phBotChat.Private(toplayer, "RECALL "+recall)
		log('Plugin Buton: KOMUT ' +toplayer+' A GÖNDERİLDİ.. ')
def btnrevreturn_clicked():
	if QtBind.isChecked(gui_,cbxAllChat):
		phBotChat.All('REVERSE RETURN')
		log('Plugin Buton: KOMUT ALL CHATE GÖNDERİLDİ.. ')
	if QtBind.isChecked(gui_,cbxPartyChat):
		phBotChat.Party('REVERSE RETURN')
		log('Plugin Buton: KOMUT PARTY CHATE GÖNDERİLDİ.. ')
	if QtBind.isChecked(gui_,cbxGuildChat):
		phBotChat.Guild('REVERSE RETURN')
		log('Plugin Buton: KOMUT GUILD CHATE  GÖNDERİLDİ.. ')
	if QtBind.isChecked(gui_,cbxUnionChat):
		phBotChat.Union('REVERSE RETURN')
		log('Plugin Buton: KOMUT UNION CHATE GÖNDERİLDİ.. ')
	if QtBind.isChecked(gui_,cbxprivateChat):
		toplayer = QtBind.text(gui_, tbxprivatechat)
		phBotChat.Private(toplayer, "REVERSE RETURN")
		log('Plugin Buton: KOMUT ' +toplayer+' A GÖNDERİLDİ.. ')
def btnrevolum_clicked():
	if QtBind.isChecked(gui_,cbxAllChat):
		phBotChat.All('REVERSE OLUM')
		log('Plugin Buton: KOMUT ALL CHATE GÖNDERİLDİ.. ')
	if QtBind.isChecked(gui_,cbxPartyChat):
		phBotChat.Party('REVERSE OLUM')
		log('Plugin Buton: KOMUT PARTY CHATE GÖNDERİLDİ.. ')
	if QtBind.isChecked(gui_,cbxGuildChat):
		phBotChat.Guild('REVERSE OLUM')
		log('Plugin Buton: KOMUT GUILD CHATE  GÖNDERİLDİ.. ')
	if QtBind.isChecked(gui_,cbxUnionChat):
		phBotChat.Union('REVERSE OLUM')
		log('Plugin Buton: KOMUT UNION CHATE GÖNDERİLDİ.. ')
	if QtBind.isChecked(gui_,cbxprivateChat):
		toplayer = QtBind.text(gui_, tbxprivatechat)
		phBotChat.Private(toplayer, "REVERSE OLUM")
		log('Plugin Buton: KOMUT ' +toplayer+' A GÖNDERİLDİ.. ')
def btnrevalan_clicked():
	alan = QtBind.text(gui_, tbxrevalan)
	if QtBind.isChecked(gui_,cbxAllChat):
		phBotChat.All('REVERSE ALAN '+alan)
		log('Plugin Buton: KOMUT ALL CHATE GÖNDERİLDİ.. ')
	if QtBind.isChecked(gui_,cbxPartyChat):
		phBotChat.Party('REVERSE ALAN '+alan)
		log('Plugin Buton: KOMUT PARTY CHATE GÖNDERİLDİ.. ')
	if QtBind.isChecked(gui_,cbxGuildChat):
		phBotChat.Guild('REVERSE ALAN '+alan)
		log('Plugin Buton: KOMUT GUILD CHATE  GÖNDERİLDİ.. ')
	if QtBind.isChecked(gui_,cbxUnionChat):
		phBotChat.Union('REVERSE ALAN '+alan)
		log('Plugin Buton: KOMUT UNION CHATE GÖNDERİLDİ.. ')
	if QtBind.isChecked(gui_,cbxprivateChat):
		toplayer = QtBind.text(gui_, tbxprivatechat)
		phBotChat.Private(toplayer, "REVERSE ALAN "+alan)
		log('Plugin Buton: KOMUT ' +toplayer+' A GÖNDERİLDİ.. ')
def btnrevplayer_clicked():
	revplayer = QtBind.text(gui_, tbxrevplayer)
	if QtBind.isChecked(gui_,cbxAllChat):
		phBotChat.All('REVERSE PLAYER '+revplayer)
		log('Plugin Buton: KOMUT ALL CHATE GÖNDERİLDİ.. ')
	if QtBind.isChecked(gui_,cbxPartyChat):
		phBotChat.Party('REVERSE PLAYER '+revplayer)
		log('Plugin Buton: KOMUT PARTY CHATE GÖNDERİLDİ.. ')
	if QtBind.isChecked(gui_,cbxGuildChat):
		phBotChat.Guild('REVERSE PLAYER '+revplayer)
		log('Plugin Buton: KOMUT GUILD CHATE  GÖNDERİLDİ.. ')
	if QtBind.isChecked(gui_,cbxUnionChat):
		phBotChat.Union('REVERSE PLAYER '+revplayer)
		log('Plugin Buton: KOMUT UNION CHATE GÖNDERİLDİ.. ')
	if QtBind.isChecked(gui_,cbxprivateChat):
		toplayer = QtBind.text(gui_, tbxprivatechat)
		phBotChat.Private(toplayer, "REVERSE PLAYER "+revplayer)
		log('Plugin Buton: KOMUT ' +toplayer+' A GÖNDERİLDİ.. ')
def btngiy_clicked():
	giy = QtBind.text(gui_, tbxgiy)
	if QtBind.isChecked(gui_,cbxAllChat):
		phBotChat.All('GIY '+giy)
		log('Plugin Buton: KOMUT ALL CHATE GÖNDERİLDİ.. ')
	if QtBind.isChecked(gui_,cbxPartyChat):
		phBotChat.Party('GIY '+giy)
		log('Plugin Buton: KOMUT PARTY CHATE GÖNDERİLDİ.. ')
	if QtBind.isChecked(gui_,cbxGuildChat):
		phBotChat.Guild('GIY '+giy)
		log('Plugin Buton: KOMUT GUILD CHATE  GÖNDERİLDİ.. ')
	if QtBind.isChecked(gui_,cbxUnionChat):
		phBotChat.Union('GIY '+giy)
		log('Plugin Buton: KOMUT UNION CHATE GÖNDERİLDİ.. ')
	if QtBind.isChecked(gui_,cbxprivateChat):
		toplayer = QtBind.text(gui_, tbxprivatechat)
		phBotChat.Private(toplayer, "GIY "+giy)
		log('Plugin Buton: KOMUT ' +toplayer+' A GÖNDERİLDİ.. ')
def btncikart_clicked():
	cikart = QtBind.text(gui_, tbxcikart)
	if QtBind.isChecked(gui_,cbxAllChat):
		phBotChat.All('CIKART '+cikart)
		log('Plugin Buton: KOMUT ALL CHATE GÖNDERİLDİ.. ')
	if QtBind.isChecked(gui_,cbxPartyChat):
		phBotChat.Party('CIKART '+cikart)
		log('Plugin Buton: KOMUT PARTY CHATE GÖNDERİLDİ.. ')
	if QtBind.isChecked(gui_,cbxGuildChat):
		phBotChat.Guild('CIKART '+cikart)
		log('Plugin Buton: KOMUT GUILD CHATE  GÖNDERİLDİ.. ')
	if QtBind.isChecked(gui_,cbxUnionChat):
		phBotChat.Union('CIKART '+cikart)
		log('Plugin Buton: KOMUT UNION CHATE GÖNDERİLDİ.. ')
	if QtBind.isChecked(gui_,cbxprivateChat):
		toplayer = QtBind.text(gui_, tbxprivatechat)
		phBotChat.Private(toplayer, "CIKART "+cikart)
		log('Plugin Buton: KOMUT ' +toplayer+' A GÖNDERİLDİ.. ')
def btnreturn_clicked():
	if QtBind.isChecked(gui_,cbxAllChat):
		phBotChat.All('RETURN')
		log('Plugin Buton: KOMUT ALL CHATE GÖNDERİLDİ.. ')
	if QtBind.isChecked(gui_,cbxPartyChat):
		phBotChat.Party('RETURN')
		log('Plugin Buton: KOMUT PARTY CHATE GÖNDERİLDİ.. ')
	if QtBind.isChecked(gui_,cbxGuildChat):
		phBotChat.Guild('RETURN')
		log('Plugin Buton: KOMUT GUILD CHATE  GÖNDERİLDİ.. ')
	if QtBind.isChecked(gui_,cbxUnionChat):
		phBotChat.Union('RETURN')
		log('Plugin Buton: KOMUT UNION CHATE GÖNDERİLDİ.. ')
	if QtBind.isChecked(gui_,cbxprivateChat):
		toplayer = QtBind.text(gui_, tbxprivatechat)
		phBotChat.Private(toplayer, "RETURN")
		log('Plugin Buton: KOMUT ' +toplayer+' A GÖNDERİLDİ.. ')
def btnzerk_clicked():
	if QtBind.isChecked(gui_,cbxAllChat):
		phBotChat.All('ZERK')
		log('Plugin Buton: KOMUT ALL CHATE GÖNDERİLDİ.. ')
	if QtBind.isChecked(gui_,cbxPartyChat):
		phBotChat.Party('ZERK')
		log('Plugin Buton: KOMUT PARTY CHATE GÖNDERİLDİ.. ')
	if QtBind.isChecked(gui_,cbxGuildChat):
		phBotChat.Guild('ZERK')
		log('Plugin Buton: KOMUT GUILD CHATE  GÖNDERİLDİ.. ')
	if QtBind.isChecked(gui_,cbxUnionChat):
		phBotChat.Union('ZERK')
		log('Plugin Buton: KOMUT UNION CHATE GÖNDERİLDİ.. ')
	if QtBind.isChecked(gui_,cbxprivateChat):
		toplayer = QtBind.text(gui_, tbxprivatechat)
		phBotChat.Private(toplayer, "ZERK")
		log('Plugin Buton: KOMUT ' +toplayer+' A GÖNDERİLDİ.. ')
def btndagil_clicked():
	if QtBind.isChecked(gui_,cbxAllChat):
		phBotChat.All('DAGIL')
		log('Plugin Buton: KOMUT ALL CHATE GÖNDERİLDİ.. ')
	if QtBind.isChecked(gui_,cbxPartyChat):
		phBotChat.Party('DAGIL')
		log('Plugin Buton: KOMUT PARTY CHATE GÖNDERİLDİ.. ')
	if QtBind.isChecked(gui_,cbxGuildChat):
		phBotChat.Guild('DAGIL')
		log('Plugin Buton: KOMUT GUILD CHATE  GÖNDERİLDİ.. ')
	if QtBind.isChecked(gui_,cbxUnionChat):
		phBotChat.Union('DAGIL')
		log('Plugin Buton: KOMUT UNION CHATE GÖNDERİLDİ.. ')
	if QtBind.isChecked(gui_,cbxprivateChat):
		toplayer = QtBind.text(gui_, tbxprivatechat)
		phBotChat.Private(toplayer, "DAGIL")
		log('Plugin Buton: KOMUT ' +toplayer+' A GÖNDERİLDİ.. ')
def btntp_clicked():
	tp = QtBind.text(gui_, tbxtp)
	if QtBind.isChecked(gui_,cbxAllChat):
		phBotChat.All('TP '+tp)
		log('Plugin Buton: KOMUT ALL CHATE GÖNDERİLDİ.. ')
	if QtBind.isChecked(gui_,cbxPartyChat):
		phBotChat.Party('TP '+tp)
		log('Plugin Buton: KOMUT PARTY CHATE GÖNDERİLDİ.. ')
	if QtBind.isChecked(gui_,cbxGuildChat):
		phBotChat.Guild('TP '+tp)
		log('Plugin Buton: KOMUT GUILD CHATE  GÖNDERİLDİ.. ')
	if QtBind.isChecked(gui_,cbxUnionChat):
		phBotChat.Union('TP '+tp)
		log('Plugin Buton: KOMUT UNION CHATE GÖNDERİLDİ.. ')
	if QtBind.isChecked(gui_,cbxprivateChat):
		toplayer = QtBind.text(gui_, tbxprivatechat)
		phBotChat.Private(toplayer, "TP "+tp)
		log('Plugin Buton: KOMUT ' +toplayer+' A GÖNDERİLDİ.. ')
def btndc_clicked():
	if QtBind.isChecked(gui_,cbxAllChat):
		phBotChat.All('DC')
		log('Plugin Buton: KOMUT ALL CHATE GÖNDERİLDİ.. ')
	if QtBind.isChecked(gui_,cbxPartyChat):
		phBotChat.Party('DC')
		log('Plugin Buton: KOMUT PARTY CHATE GÖNDERİLDİ.. ')
	if QtBind.isChecked(gui_,cbxGuildChat):
		phBotChat.Guild('DC')
		log('Plugin Buton: KOMUT GUILD CHATE  GÖNDERİLDİ.. ')
	if QtBind.isChecked(gui_,cbxUnionChat):
		phBotChat.Union('DC')
		log('Plugin Buton: KOMUT UNION CHATE GÖNDERİLDİ.. ')
	if QtBind.isChecked(gui_,cbxprivateChat):
		toplayer = QtBind.text(gui_, tbxprivatechat)
		phBotChat.Private(toplayer, "DC")
		log('Plugin Buton: KOMUT ' +toplayer+' A GÖNDERİLDİ.. ')
def btnptayril_clicked():
	if QtBind.isChecked(gui_,cbxAllChat):
		phBotChat.All('PTAYRIL')
		log('Plugin Buton: KOMUT ALL CHATE GÖNDERİLDİ.. ')
	if QtBind.isChecked(gui_,cbxPartyChat):
		phBotChat.Party('PTAYRIL')
		log('Plugin Buton: KOMUT PARTY CHATE GÖNDERİLDİ.. ')
	if QtBind.isChecked(gui_,cbxGuildChat):
		phBotChat.Guild('PTAYRIL')
		log('Plugin Buton: KOMUT GUILD CHATE  GÖNDERİLDİ.. ')
	if QtBind.isChecked(gui_,cbxUnionChat):
		phBotChat.Union('PTAYRIL')
		log('Plugin Buton: KOMUT UNION CHATE GÖNDERİLDİ.. ')
	if QtBind.isChecked(gui_,cbxprivateChat):
		toplayer = QtBind.text(gui_, tbxprivatechat)
		phBotChat.Private(toplayer, "PTAYRIL")
		log('Plugin Buton: KOMUT ' +toplayer+' A GÖNDERİLDİ.. ')
def btntargeton_clicked():
	if QtBind.isChecked(gui_,cbxAllChat):
		phBotChat.All('TARGETON')
		log('Plugin Buton: KOMUT ALL CHATE GÖNDERİLDİ.. ')
	if QtBind.isChecked(gui_,cbxPartyChat):
		phBotChat.Party('TARGETON')
		log('Plugin Buton: KOMUT PARTY CHATE GÖNDERİLDİ.. ')
	if QtBind.isChecked(gui_,cbxGuildChat):
		phBotChat.Guild('TARGETON')
		log('Plugin Buton: KOMUT GUILD CHATE  GÖNDERİLDİ.. ')
	if QtBind.isChecked(gui_,cbxUnionChat):
		phBotChat.Union('TARGETON')
		log('Plugin Buton: KOMUT UNION CHATE GÖNDERİLDİ.. ')
	if QtBind.isChecked(gui_,cbxprivateChat):
		toplayer = QtBind.text(gui_, tbxprivatechat)
		phBotChat.Private(toplayer, "TARGETON")
		log('Plugin Buton: KOMUT ' +toplayer+' A GÖNDERİLDİ.. ')
def btntargetoff_clicked():
	if QtBind.isChecked(gui_,cbxAllChat):
		phBotChat.All('TARGETOFF')
		log('Plugin Buton: KOMUT ALL CHATE GÖNDERİLDİ.. ')
	if QtBind.isChecked(gui_,cbxPartyChat):
		phBotChat.Party('TARGETOFF')
		log('Plugin Buton: KOMUT PARTY CHATE GÖNDERİLDİ.. ')
	if QtBind.isChecked(gui_,cbxGuildChat):
		phBotChat.Guild('TARGETOFF')
		log('Plugin Buton: KOMUT GUILD CHATE  GÖNDERİLDİ.. ')
	if QtBind.isChecked(gui_,cbxUnionChat):
		phBotChat.Union('TARGETOFF')
		log('Plugin Buton: KOMUT UNION CHATE GÖNDERİLDİ.. ')
	if QtBind.isChecked(gui_,cbxprivateChat):
		toplayer = QtBind.text(gui_, tbxprivatechat)
		phBotChat.Private(toplayer, "TARGETOFF")
		log('Plugin Buton: KOMUT ' +toplayer+' A GÖNDERİLDİ.. ')
def btndeffon_clicked():
	if QtBind.isChecked(gui_,cbxAllChat):
		phBotChat.All('DEFFON')
		log('Plugin Buton: KOMUT ALL CHATE GÖNDERİLDİ.. ')
	if QtBind.isChecked(gui_,cbxPartyChat):
		phBotChat.Party('DEFFON')
		log('Plugin Buton: KOMUT PARTY CHATE GÖNDERİLDİ.. ')
	if QtBind.isChecked(gui_,cbxGuildChat):
		phBotChat.Guild('DEFFON')
		log('Plugin Buton: KOMUT GUILD CHATE  GÖNDERİLDİ.. ')
	if QtBind.isChecked(gui_,cbxUnionChat):
		phBotChat.Union('DEFFON')
		log('Plugin Buton: KOMUT UNION CHATE GÖNDERİLDİ.. ')
	if QtBind.isChecked(gui_,cbxprivateChat):
		toplayer = QtBind.text(gui_, tbxprivatechat)
		phBotChat.Private(toplayer, "DEFFON")
		log('Plugin Buton: KOMUT ' +toplayer+' A GÖNDERİLDİ.. ')
def btndeffoff_clicked():
	if QtBind.isChecked(gui_,cbxAllChat):
		phBotChat.All('DEFFOFF')
		log('Plugin Buton: KOMUT ALL CHATE GÖNDERİLDİ.. ')
	if QtBind.isChecked(gui_,cbxPartyChat):
		phBotChat.Party('DEFFOFF')
		log('Plugin Buton: KOMUT PARTY CHATE GÖNDERİLDİ.. ')
	if QtBind.isChecked(gui_,cbxGuildChat):
		phBotChat.Guild('DEFFOFF')
		log('Plugin Buton: KOMUT GUILD CHATE  GÖNDERİLDİ.. ')
	if QtBind.isChecked(gui_,cbxUnionChat):
		phBotChat.Union('DEFFOFF')
		log('Plugin Buton: KOMUT UNION CHATE GÖNDERİLDİ.. ')
	if QtBind.isChecked(gui_,cbxprivateChat):
		toplayer = QtBind.text(gui_, tbxprivatechat)
		phBotChat.Private(toplayer, "DEFFOFF")
		log('Plugin Buton: KOMUT ' +toplayer+' A GÖNDERİLDİ.. ')
def btnhwt_clicked():
	if QtBind.isChecked(gui_,cbxAllChat):
		phBotChat.All('HWT1')
		log('Plugin Buton: KOMUT ALL CHATE GÖNDERİLDİ.. ')
	if QtBind.isChecked(gui_,cbxPartyChat):
		phBotChat.Party('HWT1')
		log('Plugin Buton: KOMUT PARTY CHATE GÖNDERİLDİ.. ')
	if QtBind.isChecked(gui_,cbxGuildChat):
		phBotChat.Guild('HWT1')
		log('Plugin Buton: KOMUT GUILD CHATE  GÖNDERİLDİ.. ')
	if QtBind.isChecked(gui_,cbxUnionChat):
		phBotChat.Union('HWT1')
		log('Plugin Buton: KOMUT UNION CHATE GÖNDERİLDİ.. ')
	if QtBind.isChecked(gui_,cbxprivateChat):
		toplayer = QtBind.text(gui_, tbxprivatechat)
		phBotChat.Private(toplayer, "HWT1")
		log('Plugin Buton: KOMUT ' +toplayer+' A GÖNDERİLDİ.. ')
def btnhwtt_clicked():
	if QtBind.isChecked(gui_,cbxAllChat):
		phBotChat.All('HWT2')
		log('Plugin Buton: KOMUT ALL CHATE GÖNDERİLDİ.. ')
	if QtBind.isChecked(gui_,cbxPartyChat):
		phBotChat.Party('HWT2')
		log('Plugin Buton: KOMUT PARTY CHATE GÖNDERİLDİ.. ')
	if QtBind.isChecked(gui_,cbxGuildChat):
		phBotChat.Guild('HWT2')
		log('Plugin Buton: KOMUT GUILD CHATE  GÖNDERİLDİ.. ')
	if QtBind.isChecked(gui_,cbxUnionChat):
		phBotChat.Union('HWT2')
		log('Plugin Buton: KOMUT UNION CHATE GÖNDERİLDİ.. ')
	if QtBind.isChecked(gui_,cbxprivateChat):
		toplayer = QtBind.text(gui_, tbxprivatechat)
		phBotChat.Private(toplayer, "HWT2")
		log('Plugin Buton: KOMUT ' +toplayer+' A GÖNDERİLDİ.. ')
def btnhwttt_clicked():
	if QtBind.isChecked(gui_,cbxAllChat):
		phBotChat.All('HWT3')
		log('Plugin Buton: KOMUT ALL CHATE GÖNDERİLDİ.. ')
	if QtBind.isChecked(gui_,cbxPartyChat):
		phBotChat.Party('HWT3')
		log('Plugin Buton: KOMUT PARTY CHATE GÖNDERİLDİ.. ')
	if QtBind.isChecked(gui_,cbxGuildChat):
		phBotChat.Guild('HWT3')
		log('Plugin Buton: KOMUT GUILD CHATE  GÖNDERİLDİ.. ')
	if QtBind.isChecked(gui_,cbxUnionChat):
		phBotChat.Union('HWT3')
		log('Plugin Buton: KOMUT UNION CHATE GÖNDERİLDİ.. ')
	if QtBind.isChecked(gui_,cbxprivateChat):
		toplayer = QtBind.text(gui_, tbxprivatechat)
		phBotChat.Private(toplayer, "HWT3")
		log('Plugin Buton: KOMUT ' +toplayer+' A GÖNDERİLDİ.. ')
def btncape_clicked():
	renk = QtBind.text(gui_, tbxcape)
	if QtBind.isChecked(gui_,cbxAllChat):
		phBotChat.All('CAPE '+renk)
		log('Plugin Buton: KOMUT ALL CHATE GÖNDERİLDİ.. ')
	if QtBind.isChecked(gui_,cbxPartyChat):
		phBotChat.Party('CAPE '+renk)
		log('Plugin Buton: KOMUT PARTY CHATE GÖNDERİLDİ.. ')
	if QtBind.isChecked(gui_,cbxGuildChat):
		phBotChat.Guild('CAPE '+renk)
		log('Plugin Buton: KOMUT GUILD CHATE  GÖNDERİLDİ.. ')
	if QtBind.isChecked(gui_,cbxUnionChat):
		phBotChat.Union('CAPE '+renk)
		log('Plugin Buton: KOMUT UNION CHATE GÖNDERİLDİ.. ')
	if QtBind.isChecked(gui_,cbxprivateChat):
		toplayer = QtBind.text(gui_, tbxprivatechat)
		phBotChat.Private(toplayer, "CAPE "+renk)
		log('Plugin Buton: KOMUT ' +toplayer+' A GÖNDERİLDİ.. ')
def btninfo_clicked():
	if QtBind.isChecked(gui_,cbxAllChat):
		phBotChat.All('INFO')
		log('Plugin Buton: KOMUT ALL CHATE GÖNDERİLDİ.. ')
	if QtBind.isChecked(gui_,cbxPartyChat):
		phBotChat.Party('INFO')
		log('Plugin Buton: KOMUT PARTY CHATE GÖNDERİLDİ.. ')
	if QtBind.isChecked(gui_,cbxGuildChat):
		phBotChat.Guild('INFO')
		log('Plugin Buton: KOMUT GUILD CHATE  GÖNDERİLDİ.. ')
	if QtBind.isChecked(gui_,cbxUnionChat):
		phBotChat.Union('INFO')
		log('Plugin Buton: KOMUT UNION CHATE GÖNDERİLDİ.. ')
	if QtBind.isChecked(gui_,cbxprivateChat):
		toplayer = QtBind.text(gui_, tbxprivatechat)
		phBotChat.Private(toplayer, "INFO")
		log('Plugin Buton: KOMUT ' +toplayer+' A GÖNDERİLDİ.. ')
def btnstrsc_clicked():
	if QtBind.isChecked(gui_,cbxAllChat):
		phBotChat.All('STRSC')
		log('Plugin Buton: KOMUT ALL CHATE GÖNDERİLDİ.. ')
	if QtBind.isChecked(gui_,cbxPartyChat):
		phBotChat.Party('STRSC')
		log('Plugin Buton: KOMUT PARTY CHATE GÖNDERİLDİ.. ')
	if QtBind.isChecked(gui_,cbxGuildChat):
		phBotChat.Guild('STRSC')
		log('Plugin Buton: KOMUT GUILD CHATE  GÖNDERİLDİ.. ')
	if QtBind.isChecked(gui_,cbxUnionChat):
		phBotChat.Union('STRSC')
		log('Plugin Buton: KOMUT UNION CHATE GÖNDERİLDİ.. ')
	if QtBind.isChecked(gui_,cbxprivateChat):
		toplayer = QtBind.text(gui_, tbxprivatechat)
		phBotChat.Private(toplayer, "STRSC")
		log('Plugin Buton: KOMUT ' +toplayer+' A GÖNDERİLDİ.. ')
def btnintsc_clicked():
	if QtBind.isChecked(gui_,cbxAllChat):
		phBotChat.All('INTSC')
		log('Plugin Buton: KOMUT ALL CHATE GÖNDERİLDİ.. ')
	if QtBind.isChecked(gui_,cbxPartyChat):
		phBotChat.Party('INTSC')
		log('Plugin Buton: KOMUT PARTY CHATE GÖNDERİLDİ.. ')
	if QtBind.isChecked(gui_,cbxGuildChat):
		phBotChat.Guild('INTSC')
		log('Plugin Buton: KOMUT GUILD CHATE  GÖNDERİLDİ.. ')
	if QtBind.isChecked(gui_,cbxUnionChat):
		phBotChat.Union('INTSC')
		log('Plugin Buton: KOMUT UNION CHATE GÖNDERİLDİ.. ')
	if QtBind.isChecked(gui_,cbxprivateChat):
		toplayer = QtBind.text(gui_, tbxprivatechat)
		phBotChat.Private(toplayer, "INTSC")
		log('Plugin Buton: KOMUT ' +toplayer+' A GÖNDERİLDİ.. ')
def btnhpsc_clicked():
	if QtBind.isChecked(gui_,cbxAllChat):
		phBotChat.All('HPSC')
		log('Plugin Buton: KOMUT ALL CHATE GÖNDERİLDİ.. ')
	if QtBind.isChecked(gui_,cbxPartyChat):
		phBotChat.Party('HPSC')
		log('Plugin Buton: KOMUT PARTY CHATE GÖNDERİLDİ.. ')
	if QtBind.isChecked(gui_,cbxGuildChat):
		phBotChat.Guild('HPSC')
		log('Plugin Buton: KOMUT GUILD CHATE  GÖNDERİLDİ.. ')
	if QtBind.isChecked(gui_,cbxUnionChat):
		phBotChat.Union('HPSC')
		log('Plugin Buton: KOMUT UNION CHATE GÖNDERİLDİ.. ')
	if QtBind.isChecked(gui_,cbxprivateChat):
		toplayer = QtBind.text(gui_, tbxprivatechat)
		phBotChat.Private(toplayer, "HPSC")
		log('Plugin Buton: KOMUT ' +toplayer+' A GÖNDERİLDİ.. ')
def btnmpsc_clicked():
	if QtBind.isChecked(gui_,cbxAllChat):
		phBotChat.All('MPSC')
		log('Plugin Buton: KOMUT ALL CHATE GÖNDERİLDİ.. ')
	if QtBind.isChecked(gui_,cbxPartyChat):
		phBotChat.Party('MPSC')
		log('Plugin Buton: KOMUT PARTY CHATE GÖNDERİLDİ.. ')
	if QtBind.isChecked(gui_,cbxGuildChat):
		phBotChat.Guild('MPSC')
		log('Plugin Buton: KOMUT GUILD CHATE  GÖNDERİLDİ.. ')
	if QtBind.isChecked(gui_,cbxUnionChat):
		phBotChat.Union('MPSC')
		log('Plugin Buton: KOMUT UNION CHATE GÖNDERİLDİ.. ')
	if QtBind.isChecked(gui_,cbxprivateChat):
		toplayer = QtBind.text(gui_, tbxprivatechat)
		phBotChat.Private(toplayer, "MPSC")
		log('Plugin Buton: KOMUT ' +toplayer+' A GÖNDERİLDİ.. ')
def btndamagesc_clicked():
	if QtBind.isChecked(gui_,cbxAllChat):
		phBotChat.All('DAMAGESC')
		log('Plugin Buton: KOMUT ALL CHATE GÖNDERİLDİ.. ')
	if QtBind.isChecked(gui_,cbxPartyChat):
		phBotChat.Party('DAMAGESC')
		log('Plugin Buton: KOMUT PARTY CHATE GÖNDERİLDİ.. ')
	if QtBind.isChecked(gui_,cbxGuildChat):
		phBotChat.Guild('DAMAGESC')
		log('Plugin Buton: KOMUT GUILD CHATE  GÖNDERİLDİ.. ')
	if QtBind.isChecked(gui_,cbxUnionChat):
		phBotChat.Union('DAMAGESC')
		log('Plugin Buton: KOMUT UNION CHATE GÖNDERİLDİ.. ')
	if QtBind.isChecked(gui_,cbxprivateChat):
		toplayer = QtBind.text(gui_, tbxprivatechat)
		phBotChat.Private(toplayer, "DAMAGESC")
		log('Plugin Buton: KOMUT ' +toplayer+' A GÖNDERİLDİ.. ')
def btndamageabssc_clicked():
	if QtBind.isChecked(gui_,cbxAllChat):
		phBotChat.All('DAMAGEABSSC')
		log('Plugin Buton: KOMUT ALL CHATE GÖNDERİLDİ.. ')
	if QtBind.isChecked(gui_,cbxPartyChat):
		phBotChat.Party('DAMAGEABSSC')
		log('Plugin Buton: KOMUT PARTY CHATE GÖNDERİLDİ.. ')
	if QtBind.isChecked(gui_,cbxGuildChat):
		phBotChat.Guild('DAMAGEABSSC')
		log('Plugin Buton: KOMUT GUILD CHATE  GÖNDERİLDİ.. ')
	if QtBind.isChecked(gui_,cbxUnionChat):
		phBotChat.Union('DAMAGEABSSC')
		log('Plugin Buton: KOMUT UNION CHATE GÖNDERİLDİ.. ')
	if QtBind.isChecked(gui_,cbxprivateChat):
		toplayer = QtBind.text(gui_, tbxprivatechat)
		phBotChat.Private(toplayer, "DAMAGEABSSC")
		log('Plugin Buton: KOMUT ' +toplayer+' A GÖNDERİLDİ.. ')
def btnressc_clicked():
	if QtBind.isChecked(gui_,cbxAllChat):
		phBotChat.All('RESSC')
		log('Plugin Buton: KOMUT ALL CHATE GÖNDERİLDİ.. ')
	if QtBind.isChecked(gui_,cbxPartyChat):
		phBotChat.Party('RESSC')
		log('Plugin Buton: KOMUT PARTY CHATE GÖNDERİLDİ.. ')
	if QtBind.isChecked(gui_,cbxGuildChat):
		phBotChat.Guild('RESSC')
		log('Plugin Buton: KOMUT GUILD CHATE  GÖNDERİLDİ.. ')
	if QtBind.isChecked(gui_,cbxUnionChat):
		phBotChat.Union('RESSC')
		log('Plugin Buton: KOMUT UNION CHATE GÖNDERİLDİ.. ')
	if QtBind.isChecked(gui_,cbxprivateChat):
		toplayer = QtBind.text(gui_, tbxprivatechat)
		phBotChat.Private(toplayer, "RESSC")
		log('Plugin Buton: KOMUT ' +toplayer+' A GÖNDERİLDİ.. ')
def btntgsc_clicked():
	if QtBind.isChecked(gui_,cbxAllChat):
		phBotChat.All('TGSC')
		log('Plugin Buton: KOMUT ALL CHATE GÖNDERİLDİ.. ')
	if QtBind.isChecked(gui_,cbxPartyChat):
		phBotChat.Party('TGSC')
		log('Plugin Buton: KOMUT PARTY CHATE GÖNDERİLDİ.. ')
	if QtBind.isChecked(gui_,cbxGuildChat):
		phBotChat.Guild('TGSC')
		log('Plugin Buton: KOMUT GUILD CHATE  GÖNDERİLDİ.. ')
	if QtBind.isChecked(gui_,cbxUnionChat):
		phBotChat.Union('TGSC')
		log('Plugin Buton: KOMUT UNION CHATE GÖNDERİLDİ.. ')
	if QtBind.isChecked(gui_,cbxprivateChat):
		toplayer = QtBind.text(gui_, tbxprivatechat)
		phBotChat.Private(toplayer, "TGSC")
		log('Plugin Buton: KOMUT ' +toplayer+' A GÖNDERİLDİ.. ')
def btnchat_clicked():
	cesit = QtBind.text(gui_, tbxchatcesit)
	mesaj = QtBind.text(gui_, tbxchatmesaj)
	if QtBind.isChecked(gui_,cbxAllChat):
		phBotChat.All('CHAT '+cesit+' '+mesaj)
		log('Plugin Buton: KOMUT ALL CHATE GÖNDERİLDİ.. ')
	if QtBind.isChecked(gui_,cbxPartyChat):
		phBotChat.Party('CHAT '+cesit+' '+mesaj)
		log('Plugin Buton: KOMUT PARTY CHATE GÖNDERİLDİ.. ')
	if QtBind.isChecked(gui_,cbxGuildChat):
		phBotChat.Guild('CHAT '+cesit+' '+mesaj)
		log('Plugin Buton: KOMUT GUILD CHATE  GÖNDERİLDİ.. ')
	if QtBind.isChecked(gui_,cbxUnionChat):
		phBotChat.Union('CHAT '+cesit+' '+mesaj)
		log('Plugin Buton: KOMUT UNION CHATE GÖNDERİLDİ.. ')
	if QtBind.isChecked(gui_,cbxprivateChat):
		toplayer = QtBind.text(gui_, tbxprivatechat)
		phBotChat.Private(toplayer,'CHAT '+cesit+' '+mesaj)
		log('Plugin Buton: KOMUT ' +toplayer+' A GÖNDERİLDİ.. ')
def btnhotanftw_clicked():
	dis = QtBind.text(gui_, tbxhotandis)
	ic = QtBind.text(gui_, tbxhotanic)
	if QtBind.isChecked(gui_,cbxAllChat):
		phBotChat.All('H'+dis+ic)
		log('Plugin Buton: KOMUT ALL CHATE GÖNDERİLDİ.. ')
	if QtBind.isChecked(gui_,cbxPartyChat):
		phBotChat.Party('H'+dis+ic)
		log('Plugin Buton: KOMUT PARTY CHATE GÖNDERİLDİ.. ')
	if QtBind.isChecked(gui_,cbxGuildChat):
		phBotChat.Guild('H'+dis+ic)
		log('Plugin Buton: KOMUT GUILD CHATE  GÖNDERİLDİ.. ')
	if QtBind.isChecked(gui_,cbxUnionChat):
		phBotChat.Union('H'+dis+ic)
		log('Plugin Buton: KOMUT UNION CHATE GÖNDERİLDİ.. ')
	if QtBind.isChecked(gui_,cbxprivateChat):
		toplayer = QtBind.text(gui_, tbxprivatechat)
		phBotChat.Private(toplayer, "H"+dis+ic)
		log('Plugin Buton: KOMUT ' +toplayer+' A GÖNDERİLDİ.. ')
def btnjanganftw_clicked():
	diss = QtBind.text(gui_, tbxjangandis)
	icc = QtBind.text(gui_, tbxjanganic)
	if QtBind.isChecked(gui_,cbxAllChat):
		phBotChat.All('J'+diss+icc)
		log('Plugin Buton: KOMUT ALL CHATE GÖNDERİLDİ.. ')
	if QtBind.isChecked(gui_,cbxPartyChat):
		phBotChat.Party('J'+diss+icc)
		log('Plugin Buton: KOMUT PARTY CHATE GÖNDERİLDİ.. ')
	if QtBind.isChecked(gui_,cbxGuildChat):
		phBotChat.Guild('J'+diss+icc)
		log('Plugin Buton: KOMUT GUILD CHATE  GÖNDERİLDİ.. ')
	if QtBind.isChecked(gui_,cbxUnionChat):
		phBotChat.Union('J'+diss+icc)
		log('Plugin Buton: KOMUT UNION CHATE GÖNDERİLDİ.. ')
	if QtBind.isChecked(gui_,cbxprivateChat):
		toplayer = QtBind.text(gui_, tbxprivatechat)
		phBotChat.Private(toplayer, "J"+diss+icc)
		log('Plugin Buton: KOMUT ' +toplayer+' A GÖNDERİLDİ.. ')
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
def btnliderekle_clicked():
	if inGame:
		player = QtBind.text(gui_, lblcharname)
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
		selectedItem = QtBind.text(gui_, lblcharname)
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
	if loc == 22:  # vsro
		p += struct.pack('<H', tid)
	elif loc == 56:  # trsro
		p += struct.pack('<I', tid)
	else:
		p += struct.pack('<I', tid)
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

def use_item_with_index(index):
	p = struct.pack('B', index)
	p += b'\x30\x0C\x0D\x0E'
	# CLIENT_INVENTORY_ITEM_USE_REQUEST
	log("Data: " + str(p))
	inject_joymax(0x704C, p, True)
def use_item_with_index_scroll(index):
	p = struct.pack('B', index)
	p += b'\x30\x0C\x0D\x01'
	# CLIENT_INVENTORY_ITEM_USE_REQUEST
	log("Data: " + str(p))
	inject_joymax(0x704C, p, True)
def use_item_with_index_scroll2(index):
	p = struct.pack('B', index)
	p += b'\x31\x0C\x0D\x01'
	# CLIENT_INVENTORY_ITEM_USE_REQUEST
	log("Data: " + str(p))
	inject_joymax(0x704C, p, True)
def use_item_with_index_scroll3(index):
	p = struct.pack('B', index)
	p += b'\x31\x0C\x0D\x06'
	# CLIENT_INVENTORY_ITEM_USE_REQUEST
	log("Data: " + str(p))
	inject_joymax(0x704C, p, True)
def get_item_count(searchingItem):
	count = 0
	if searchingItem is None:
		return count
	items = get_inventory()['items']
	for item in items:
		if item is not None and item['name'] == searchingItem['name']:
			count += item['quantity']
	return count
def parseData(data):
	data = data.split()
	if len(data) < 1:
		return None, None
	if len(data) == 1:
		return data[0], None
	if len(data) > 1:
		return data[0], data[1:]
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
		handle_commands(msg, player)
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
def handle_commands(data, player):
	data = data.strip()
	code, rest = parseData(data)
	if code in COMMANDS_CODES['ZERKPOT']:
		itemName = "Energy of life"
		item = GetItemByExpression(lambda n, s: itemName in n or itemName == s, 13)
		item_count = get_item_count(item)
		if item is None or item_count == 0:
			phBotChat.Private(player, "ZERK POT MEVCUT DEĞİL.")
		else:
			itemSlot = item['slot']
			log("Item slot: " + str(itemSlot))
			if rest is None:
				use_item_with_index(itemSlot)
				Timer(2.0, inject_joymax, (0x715F, b'\x99\x5B\x00\x00\x91\x5B\x00\x00', False)).start()
	elif code in COMMANDS_CODES['STRSC']:
		itemName = "Strength Scroll"
		item = GetItemByExpression(lambda n, s: itemName in n or itemName == s, 13)
		item_count = get_item_count(item)
		if item is None or item_count == 0:
			phBotChat.Private(player, "STR SCROLL BULUNAMADI..")
		else:
			itemSlot = item['slot']
			log("Item slot: " + str(itemSlot))
			if rest is None:
				use_item_with_index_scroll(itemSlot) or use_item_with_index_scroll2(itemSlot) or use_item_with_index(itemSlot) or use_item_with_index_scroll3(itemSlot)
	elif code in COMMANDS_CODES['INTSC']:
		itemName = "Intelligence Scroll"
		item = GetItemByExpression(lambda n, s: itemName in n or itemName == s, 13)
		item_count = get_item_count(item)
		if item is None or item_count == 0:
			phBotChat.Private(player, "INT SCROLL BULUNAMADI..")
		else:
			itemSlot = item['slot']
			log("Item slot: " + str(itemSlot))
			if rest is None:
				use_item_with_index_scroll(itemSlot) or use_item_with_index_scroll2(itemSlot) or use_item_with_index(itemSlot) or use_item_with_index_scroll3(itemSlot)
	elif code in COMMANDS_CODES['MPSC']:
		itemName = "MP+"
		item = GetItemByExpression(lambda n, s: itemName in n or itemName == s, 13)
		item_count = get_item_count(item)
		if item is None or item_count == 0:
			phBotChat.Private(player, "MP SCROLL BULUNAMADI..")
		else:
			itemSlot = item['slot']
			log("Item slot: " + str(itemSlot))
			if rest is None:
				use_item_with_index_scroll2(itemSlot) or use_item_with_index_scroll(itemSlot) or use_item_with_index(itemSlot) or use_item_with_index_scroll3(itemSlot)
	elif code in COMMANDS_CODES['HPSC']:
		itemName = "HP+"
		item = GetItemByExpression(lambda n, s: itemName in n or itemName == s, 13)
		item_count = get_item_count(item)
		if item is None or item_count == 0:
			phBotChat.Private(player, "HP SCROLL BULUNAMADI..")
		else:
			itemSlot = item['slot']
			log("Item slot: " + str(itemSlot))
			if rest is None:
				use_item_with_index_scroll2(itemSlot) or use_item_with_index_scroll(itemSlot) or use_item_with_index(itemSlot) or use_item_with_index_scroll3(itemSlot)
	elif code in COMMANDS_CODES['DAMAGESC']:
		itemName = "20% damage increase/absorption scroll"
		item = GetItemByExpression(lambda n, s: itemName in n or itemName == s, 13)
		item_count = get_item_count(item)
		if item is None or item_count == 0:
			phBotChat.Private(player, "DAMAGE SCROLL BULUNAMADI..")
		else:
			itemSlot = item['slot']
			log("Item slot: " + str(itemSlot))
			if rest is None:
				use_item_with_index_scroll2(itemSlot) or use_item_with_index_scroll(itemSlot) or use_item_with_index(itemSlot) or use_item_with_index_scroll3(itemSlot)
	elif code in COMMANDS_CODES['RESSC']:
		itemName = "Instant resurrection Scroll"
		item = GetItemByExpression(lambda n, s: itemName in n or itemName == s, 13)
		item_count = get_item_count(item)
		if item is None or item_count == 0:
			phBotChat.Private(player, "RESS SCROLL BULUNAMADI..")
		else:
			itemSlot = item['slot']
			log("Item slot: " + str(itemSlot))
			if rest is None:
				use_item_with_index_scroll2(itemSlot) or use_item_with_index_scroll(itemSlot) or use_item_with_index(itemSlot) or use_item_with_index_scroll3(itemSlot)
	elif code in COMMANDS_CODES['TGSC']:
		itemName = "Trigger Scroll"
		item = GetItemByExpression(lambda n, s: itemName in n or itemName == s, 13)
		item_count = get_item_count(item)
		if item is None or item_count == 0:
			phBotChat.Private(player, "TRIGGER SCROLL BULUNAMADI..")
		else:
			itemSlot = item['slot']
			log("Item slot: " + str(itemSlot))
			if rest is None:
				use_item_with_index_scroll2(itemSlot) or use_item_with_index_scroll(itemSlot) or use_item_with_index(itemSlot) or use_item_with_index_scroll3(itemSlot)
	elif code in COMMANDS_CODES['DAMAGEABSSC']:
		itemName = "20% damage absorption scroll"
		item = GetItemByExpression(lambda n, s: itemName in n or itemName == s, 13)
		item_count = get_item_count(item)
		if item is None or item_count == 0:
			phBotChat.Private(player, "DAMAGE ABS. SCROLL BULUNAMADI..")
		else:
			itemSlot = item['slot']
			log("Item slot: " + str(itemSlot))
			if rest is None:
				use_item_with_index_scroll2(itemSlot) or use_item_with_index_scroll(itemSlot) or use_item_with_index(itemSlot) or use_item_with_index_scroll3(itemSlot)
	elif code in COMMANDS_CODES['DAMAGEINCSC']:
		itemName = "20% damage increase scroll"
		item = GetItemByExpression(lambda n, s: itemName in n or itemName == s, 13)
		item_count = get_item_count(item)
		if item is None or item_count == 0:
			phBotChat.Private(player, "DAMAGE INC. SCROLL BULUNAMADI..")
		else:
			itemSlot = item['slot']
			log("Item slot: " + str(itemSlot))
			if rest is None:
				use_item_with_index_scroll2(itemSlot) or use_item_with_index_scroll(itemSlot) or use_item_with_index(itemSlot) or use_item_with_index_scroll3(itemSlot)
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
	if inGame:
		isim = get_character_data()['name']
		QtBind.setText(gui_, lblcharname, isim)
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
