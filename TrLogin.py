from phBot import *
import QtBind
import json
import os
from datetime import timedelta
from datetime import datetime
from threading import Timer

pName = 'TrLogin'
pVersion = '0.0.2'
pUrl = 'https://raw.githubusercontent.com/TheMoB41/TrPlugins/main/TrLogin.py'
timerCheck = None
character_data = None
gui = QtBind.init(__name__,pName)
cbxEnabled = QtBind.createCheckBox(gui,'checkbox_clicked',''+pName+' ETKİNLEŞTİR.',21,13)
lblFromTime = QtBind.createLabel(gui,"SAAT",21,45)
strFromTime = "00:00"
tbxFromTime = QtBind.createLineEdit(gui,strFromTime,55,43,37,20)
lblToTime = QtBind.createLabel(gui," - ",101,45)
strToTime = "23:59"
tbxToTime = QtBind.createLineEdit(gui,strToTime,121,43,37,20)
lblFromTime2 = QtBind.createLabel(gui,"ARASI OYUNDA OL..",165,45)
btnSaveTimes = QtBind.createButton(gui,'btnSaveTimes_clicked',"  KAYDET  ",85,70)
x=10
y=10
btnhakkinda = QtBind.createButton(gui,'btnhakkinda_clicked',"         HAKKINDA         ",x+600,y+280)
def getPath():
	return get_config_dir()+pName+"\\"
def getConfig():
	return getPath()+character_data["server"]+"_"+character_data["name"]+".json"
def loadDefaultConfig():
	QtBind.setChecked(gui,cbxEnabled,False)
	strFromTime = "00:00"
	QtBind.setText(gui, tbxFromTime,strFromTime)
	strToTime = "23:59"
	QtBind.setText(gui, tbxToTime,strToTime)
def loadConfig():
	loadDefaultConfig()
	if os.path.exists(getConfig()):
		data = {}
		with open(getConfig(),"r") as f:
			data = json.load(f)
		if "FROM" in data:
			global strFromTime
			strFromTime = data["FROM"]
			QtBind.setText(gui,tbxFromTime,strFromTime)
		if "TO" in data:
			global strToTime
			strToTime = data["TO"]
			QtBind.setText(gui,tbxToTime,strToTime)
		if "Enabled" in data:
			QtBind.setChecked(gui,cbxEnabled,data["Enabled"])
			if data["Enabled"]:
				CheckTimer()
		else:
			QtBind.setChecked(gui,cbxEnabled,False)
def btnhakkinda_clicked():
	log('\n\nTrLogin:\n * TheMoB TARAFINDAN DUZENLENMISTIR. \n * FEEDBACK SISTEMLI BIR YAZILIMDIR. \n * HATA VE ONERI BILDIRIMLERINIZI BANA ULASTIRABILIRSINIZ.\n\n    # BU PLUGIN ILE HERHANGİ BİR CHARIN GÜN İÇERİSİNDE HANGİ SAAT\nARALIKLARINDA OYUNDA KALMASINI İSTEDİĞİNİZİ BELİRLEYEBİLİRSİNİZ.\n BELİRTİLEN SAATLER HARİCİ BOT AÇIK KALIR CHAR OFFLİNE KALIR.\n NOT: HER CHAR İÇİN AYRI CONFİG KAYDI VARDIR.')
def joined_game():
	global character_data
	character_data = get_character_data()
	loadConfig()
def saveConfig(key,value):
	if key:
		data = {}
		if os.path.exists(getConfig()):
			with open(getConfig(),"r") as f:
				data = json.load(f)
		data[key] = value
		with open(getConfig(),"w") as f:
			f.write(json.dumps(data, indent=4, sort_keys=True))
def checkbox_clicked(checked):
	if character_data:
		enabled = QtBind.isChecked(gui,cbxEnabled)
		saveConfig("Enabled",enabled)
		if enabled:
			CheckTimer()
			log('Plugin: '+pName+' ETKİNLEŞTİRİLDİ.')
		else:
			StopTimer()
			log('Plugin: '+pName+' DEVRE DIŞI BIRAKILDI.')
def btnSaveTimes_clicked():
	if character_data:
		tempFromTime = None
		tempToTime = None
		try:
			tempFromTime = QtBind.text(gui,tbxFromTime)
			tempFromTime = datetime.strptime(tempFromTime, '%H:%M')
		except:
			log('Plugin: HATA! BAŞLANGIÇ SAAT FORMATI (00:00) OLMALIDIR.')
			return
		try:
			tempToTime = QtBind.text(gui,tbxToTime)
			tempToTime = datetime.strptime(tempToTime, '%H:%M')
		except:
			log('Plugin: HATA! BİTİŞ SAAT FORMATI (00:00) OLMALIDIR.')
			return
		if tempFromTime == tempToTime:
			log('Plugin: HATA! ZAMANLAR EŞİT OLAMAZ.')
			return
		global strFromTime,strToTime
		strFromTime = tempFromTime.strftime('%H:%M')
		strToTime = tempToTime.strftime('%H:%M')
		saveConfig("FROM",strFromTime)
		saveConfig("TO",strToTime)
		log("Plugin: SÜRE ARALIKLARI KAYIT EDİLDİ..!")
def CheckTimer():
	timeNow = datetime.now()
	timeFrom = datetime(timeNow.year, timeNow.month, timeNow.day, int(strFromTime.split(':')[0]), int(strFromTime.split(':')[1]), 0)
	timeTo = datetime(timeNow.year, timeNow.month, timeNow.day, int(strToTime.split(':')[0]), int(strToTime.split(':')[1]), 0)
	if timeFrom > timeTo:
		timeTo += timedelta(days=1)
	if timeNow >= timeFrom and timeNow <= timeTo:
		reconnect(True)
	else:
		stop_bot()
		reconnect(False)
		disconnect()
	RestartCheckTimer(30.0)
def StopTimer():
	global timerCheck
	if timerCheck:
		timerCheck.cancel()
		timerCheck = None
def RestartCheckTimer(interval):
	global timerCheck
	if timerCheck:
		timerCheck.cancel()
	timerCheck = Timer(interval,CheckTimer)
	timerCheck.start()
log("Plugin: "+pName+" v"+pVersion+" BASARIYLA YUKLENDI.")
if not os.path.exists(getPath()):
	os.makedirs(getPath())
	log('Plugin: '+pName+' CONFIG KLASORU OLUSTURULDU.')
