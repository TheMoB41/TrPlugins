from phBot import *
import QtBind
import json
import os

pName = 'TrPacketTooL'
pVersion = '2.0.0'
pUrl = "https://raw.githubusercontent.com/TheMoB41/TrPlugins/main/TrPacketTool.py"
# ______________________________ KURULUM ______________________________ #
# KULLANICI ARAYUZU
gui = QtBind.init(__name__,pName)
lblInject = QtBind.createLabel(gui,'PAKET GÖRÜNTÜLEME PLUGINI..',6,10)
# FILTRE
_x=720-176
_y=12
QtBind.createLineEdit(gui,"",_x-30,_y,1,265)
cbxSro = QtBind.createCheckBox(gui, 'cbxShowClient_checked','CLIENT PAKETLERINI GOSTER [C->S]',_x-23,_y)
cbxShowClient = False
_y+=20
cbxJmx = QtBind.createCheckBox(gui, 'cbxShowServer_checked','SERVER PAKETLERINI GOSTER [S->C]',_x-23,_y)
cbxShowServer = False
_y+=40
cbxDontShow = QtBind.createCheckBox(gui, 'cbxDontShow_clicked',"FILITRELEME",_x+5,_y)
cbxOnlyShow = QtBind.createCheckBox(gui, 'cbxOnlyShow_clicked',"FILITRELE",_x+100,_y)
QtBind.setChecked(gui,cbxDontShow,True) 
cbxDontShow_checked = True
_y+=20
lblOpcodes = QtBind.createLabel(gui,"EKLENEN OPCODE'LARI FILTRELE :",_x,_y)
_y+=18
tbxOpcodes = QtBind.createLineEdit(gui,"",_x,_y,100,20)
btnAddOpcode = QtBind.createButton(gui,'btnAddOpcode_clicked',"      EKLE      ",_x+100+2,_y-2)
_y+=20
lstOpcodes = QtBind.createList(gui,_x,_y,176,120)
lstOpcodesData = []
btnRemOpcode = QtBind.createButton(gui,'btnRemOpcode_clicked',"     SIL     ",_x+88-32,_y-1+120)
lblNpcs = QtBind.createLabel(gui,"YAKINDAKI NPCLER :",6,85)
btnNpcs = QtBind.createButton(gui,'btnNpcs_clicked',"  LISTEYI YENILE  ",6,202)
lstNpcs = QtBind.createList(gui,6,101,400,100)
btnhakkinda = QtBind.createButton(gui,'btnhakkinda_clicked',"         HAKKINDA         ",610,290)
# ______________________________ METHODLAR ______________________________ #
# CONFIG DOSYA YOLUNDAN DEVAM ET
def getConfig():
	return get_config_dir()+pName+".json"
# VARSAYILAN CONFIGI YUKLE
def loadDefaultConfig():
	# DATAYI TEMIZLE
	global lstOpcodesData
	lstOpcodesData = []
	QtBind.clear(gui,lstOpcodes)
# CONFIGDE KAYITLI OPCODELARI YENILE
def loadConfigs():
	loadDefaultConfig()
	if os.path.exists(getConfig()):
		data = {}
		with open(getConfig(),"r") as f:
			data = json.load(f)
		if "FILITRELE" in data:
			global lstOpcodesData
			lstOpcodesData = data["FILITRELE"]
			for opcode in lstOpcodesData:
				QtBind.append(gui,lstOpcodes,'0x{:02X}'.format(opcode))
		if "FILITRELEME" in data:
			global cbxDontShow_checked
			cbxDontShow_checked = data["FILITRELEME"]
			QtBind.setChecked(gui,cbxDontShow,data["FILITRELEME"])
			QtBind.setChecked(gui,cbxOnlyShow,not data["FILITRELEME"])	
# TUM CONFIGI KAYDET
def saveConfigs():
	data = {}
	data['FILITRELEME'] = cbxDontShow_checked
	data['FILITRELE'] = lstOpcodesData
	with open(getConfig(),"w") as f:
		f.write(json.dumps(data, indent=4, sort_keys=True))
def btnhakkinda_clicked():
	log('\n\nTrPacketTool:\n * TheMoB TARAFINDAN DUZENLENMISTIR. \n * FEEDBACK SISTEMLI BIR YAZILIMDIR. \n * HATA VE ONERI BILDIRIMLERINIZI BANA ULASTIRABILIRSINIZ.\n\n    # BU PLUGIN CLIENTTEN SERVERA GONDERILEN OPCODE PAKETLERINI VEYA SERVERDAN CLIENTE GELEN OPCODE PAKETLERINI GOSTERMEKTEDIR.\n    # EK OLARAK CEVRENIZDEKI NPCLERIN DATALARINA ULASABILIRSINIZ.')
# CLIENT PAKETLERINI GOSTER CHECKBOX KONTROLU
def cbxShowClient_checked(checked):
	global cbxShowClient
	cbxShowClient = checked
#  SERVER PAKETLERINI GOSTER CHECKBOX KONTROLU
def cbxShowServer_checked(checked):
	global cbxShowServer
	cbxShowServer = checked
# FILTRELEME CHECKBOX KONTROLU
def cbxDontShow_clicked(checked):
	cbxDontShow_editConfig(checked)
	QtBind.setChecked(gui,cbxOnlyShow,not checked)
# FILTRELE CHECKBOX KONTROLU
def cbxOnlyShow_clicked(checked):
	cbxDontShow_editConfig(not checked)
	QtBind.setChecked(gui,cbxDontShow,not checked)
# FILTRELEME KAPALIYKEN CONFIG KAYDI
def	cbxDontShow_editConfig(checked):
	global cbxDontShow_checked
	cbxDontShow_checked = checked
	saveConfigs()
# EKLE BUTONUNA TIKLANDIGINDA
def btnAddOpcode_clicked():
	opcode = QtBind.text(gui,tbxOpcodes)
	if not opcode:
		return
	try:
		opcode = int(opcode,16)
	except Exception as ex:
		log("Plugin: HATA ["+str(ex)+"]")
		return
	global lstOpcodesData
	if not opcode in lstOpcodesData:
		lstOpcodesData.append(opcode)
		strOpcode = '0x{:02X}'.format(opcode)
		QtBind.append(gui,lstOpcodes,strOpcode)
		saveConfigs()
		QtBind.setText(gui, tbxOpcodes,"")
		log("Plugin: OPCODE EKLENDI ["+strOpcode+"]")
# SIL BUTONUNA TIKLANDIGINDA
def btnRemOpcode_clicked():
	selectedIndex = QtBind.currentIndex(gui,lstOpcodes)
	if selectedIndex >= 0:
		strOpcode = '0x{:02X}'.format(lstOpcodesData[selectedIndex])
		del lstOpcodesData[selectedIndex]
		QtBind.removeAt(gui,lstOpcodes,selectedIndex)
		saveConfigs()
		log("Plugin: OPCODE SILINDI ["+strOpcode+"]")
# LOGDA PAKETLERI GOSTERME
def CanShowPacket(opcode):
	if opcode in lstOpcodesData:
		if not cbxDontShow_checked:
			return True
	elif cbxDontShow_checked:
		return True
	return False
# ______________________________ ETKINLIKLER ______________________________ #
def handle_silkroad(opcode, data):
	if cbxShowClient:
		if CanShowPacket(opcode):
			log("Client: (Opcode) 0x" + '{:02X}'.format(opcode) + " (Data) "+ ("None" if not data else ' '.join('{:02X}'.format(x) for x in data)))
	return True
def handle_joymax(opcode, data):
	if cbxShowServer:
		if CanShowPacket(opcode):
			log("Server: (Opcode) 0x" + '{:02X}'.format(opcode) + " (Data) "+ ("None" if not data else ' '.join('{:02X}'.format(x) for x in data)))
	return True
def btnNpcs_clicked():
	npcs = get_npcs()
	QtBind.clear(gui,lstNpcs)
	QtBind.append(gui,lstNpcs,'[ISIM] [SV ISMI] [MODEL ID] (UNIQUE ID)')
	if npcs:
		QtBind.append(gui,lstNpcs,' -')
		for UniqueID, NPC in npcs.items():
			QtBind.append(gui,lstNpcs,"["+NPC['name'] + "] ["+NPC['servername']+"] ["+str(NPC['model'])+"] ("+str(UniqueID)+")")
# PLUGIN YUKLENDI
log('Plugin: '+pName+' v'+pVersion+' BASARIYLA YUKLENDI')
loadConfigs()
