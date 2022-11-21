from phBot import *
import QtBind
from threading import Timer
import struct
import json
import os

pName = 'TrBOI'
pVersion = '1.0.1'
pUrl = 'https://raw.githubusercontent.com/TheMoB41/TrPlugins/main/TrBOI.py'
path = get_config_dir()+pName+"\\"

Online = False
Started = False
Registering = False
Attacking = False
Picking = False
WaitingforParty = False
Inside = False
SkillDelay = 500
RegDelay = 4000
DelayCounter = 0 

SoloCount = 0
PartyCount = 0

CastSkill = []
ActiveSkills = []
MorphID = 0

gui = QtBind.init(__name__,pName)

lbl = QtBind.createLabel(gui,'ATAK RANGE: ',400,20)
txtRadius = QtBind.createLineEdit(gui,"40",470,15,25,20)
  
lbl = QtBind.createLabel(gui,'BAŞLAMADAN ÖNCE           PARTİ ÜYESİNİN GİRMESİNİ BEKLEYİN.',400,40)
txtPartyMembers = QtBind.createLineEdit(gui,"1",500,35,25,20)

cbxChange = QtBind.createCheckBox(gui, 'cbxChange_clicked','SOLO TAMAMLANDIĞINDA PT MODUNA GEÇ.', 400, 70)
lbl = QtBind.createLabel(gui,'PT MOD PROFİLİ: ',430,90)
txtPartyProfile = QtBind.createLineEdit(gui,"",520,88,90,20)

cbxFinished = QtBind.createCheckBox(gui, 'cbxFinished_clicked','BİTTİĞİNDE RETURN SCROLL KULLAN VE BOTU BAŞLAT.', 400, 110)
lbl = QtBind.createLabel(gui,'KASILMA PROFİLİ: ',430,130)
txtFinishedProfile = QtBind.createLineEdit(gui,"",520,128,90,20)

lbl = QtBind.createLabel(gui,'GÜNCEL AŞAMA: ',10,250)
lblStage = QtBind.createLabel(gui,'0',95,250)

cbxSolo71to80 = QtBind.createCheckBox(gui, 'cbxSolo71to80_clicked','SOLO LEVEL (71-80)', 10, 20)
cbxPT71to80 = QtBind.createCheckBox(gui, 'cbxPT71to80_clicked','PARTY LEVEL (71-80)', 10, 40)
cbxYeoha = QtBind.createCheckBox(gui, 'cbxYeoha_clicked','Yeoha (A)', 145, 30)
cbxSeiren = QtBind.createCheckBox(gui, 'cbxSeiren_clicked','Seiren (B)', 255, 30)

cbxSolo81to90 = QtBind.createCheckBox(gui, 'cbxSolo81to90_clicked','SOLO LEVEL (81-90)', 10, 70)
cbxPT81to90 = QtBind.createCheckBox(gui, 'cbxPT81to90_clicked','PARTY LEVEL (81-90)', 10, 90)
cbxNiyaShaman = QtBind.createCheckBox(gui, 'cbxNiyaShaman_clicked','Niya Shaman (A)', 145, 80)
cbxSlaveWatcher = QtBind.createCheckBox(gui, 'cbxSlaveWatcher_clicked','Slave Watcher (B)', 255, 80)

cbxSolo91to100 = QtBind.createCheckBox(gui, 'cbxSolo91to100_clicked','SOLO LEVEL (91-100)', 10, 120)
cbxPT91to100 = QtBind.createCheckBox(gui, 'cbxPT91to100_clicked','PARTY LEVEL (91-100)', 10, 140)
cbxDemonShaitan = QtBind.createCheckBox(gui, 'cbxDemonShaitan_clicked','Demon Shaitan (A)', 145, 130)
cbxImhotep = QtBind.createCheckBox(gui, 'cbxImhotep_clicked','Imhotep (B)', 255, 130)

cbxSolo101to110 = QtBind.createCheckBox(gui, 'cbxSolo101to110_clicked','SOLO LEVEL (101-110)', 10, 170)
cbxPT101to110 = QtBind.createCheckBox(gui, 'cbxPT101to110_clicked','PARTY LEVEL (101-110)', 10, 190)
cbxNephthys = QtBind.createCheckBox(gui, 'cbxNephthys_clicked','Nephthys (A)', 145, 180)
cbxTombSnakeLady = QtBind.createCheckBox(gui, 'cbxTombSnakeLady_clicked','Tomb Snake Lady (B)', 255, 180)

buttonStartStop = QtBind.createButton(gui, 'button_start', '  BAŞLAT  ', 25, 220)

RegCheckBoxes = [cbxSolo71to80,cbxPT71to80,cbxSolo81to90,cbxPT81to90,cbxSolo91to100,cbxPT91to100,cbxSolo101to110,cbxPT101to110]
MorphCheckBoxes = [cbxYeoha,cbxSeiren,cbxNiyaShaman,cbxSlaveWatcher,cbxDemonShaitan,cbxImhotep,cbxNephthys,cbxTombSnakeLady]

QtBind.createLabel(gui,'TrBOI:\n * TheMoB TARAFINDAN DUZENLENMISTIR. \n * FEEDBACK SISTEMLI BIR YAZILIMDIR. \n * HATA VE ONERI BILDIRIMLERINIZI BANA ULASTIRABILIRSINIZ.',400,225)

#type checkboxes
def cbxSolo71to80_clicked(checked):
	if checked:
		ClearGUI('Morph',cbxYeoha,cbxSeiren)
		ClearGUI('Reg',cbxSolo71to80)
def cbxPT71to80_clicked(checked):
	if checked:
		ClearGUI('Morph',cbxYeoha,cbxSeiren)
		ClearGUI('Reg',cbxPT71to80)
def cbxSolo81to90_clicked(checked):
	if checked:
		ClearGUI('Morph',cbxNiyaShaman,cbxSlaveWatcher)
		ClearGUI('Reg',cbxSolo81to90)
def cbxPT81to90_clicked(checked):
	if checked:
		ClearGUI('Morph',cbxNiyaShaman,cbxSlaveWatcher)
		ClearGUI('Reg',cbxPT81to90)
def cbxSolo91to100_clicked(checked):
	if checked:
		ClearGUI('Morph',cbxDemonShaitan,cbxImhotep)
		ClearGUI('Reg',cbxSolo91to100)
def cbxPT91to100_clicked(checked):
	if checked:
		ClearGUI('Morph',cbxDemonShaitan,cbxImhotep)
		ClearGUI('Reg',cbxPT91to100)
def cbxSolo101to110_clicked(checked):
	if checked:
		ClearGUI('Morph',cbxNephthys,cbxTombSnakeLady)
		ClearGUI('Reg',cbxSolo101to110)
def cbxPT101to110_clicked(checked):
	if checked:
		ClearGUI('Morph',cbxNephthys,cbxTombSnakeLady)
		ClearGUI('Reg',cbxPT101to110)
def cbxYeoha_clicked(checked):
	if QtBind.isChecked(gui,cbxSolo71to80) or QtBind.isChecked(gui,cbxPT71to80):
		if checked:
			ClearGUI('Morph',cbxYeoha)
	else:
		log('Plugin: YANLIŞ SEÇİM!')
		QtBind.setChecked(gui,cbxYeoha,False)
def cbxSeiren_clicked(checked):
	if QtBind.isChecked(gui,cbxSolo71to80) or QtBind.isChecked(gui,cbxPT71to80):
		if checked:
			ClearGUI('Morph',cbxSeiren)
	else:
		log('Plugin: YANLIŞ SEÇİM!')
		QtBind.setChecked(gui,cbxSeiren,False)
def cbxNiyaShaman_clicked(checked):
	if QtBind.isChecked(gui,cbxSolo81to90) or QtBind.isChecked(gui,cbxPT81to90):
		if checked:
			ClearGUI('Morph',cbxNiyaShaman)
	else:
		log('Plugin: YANLIŞ SEÇİM!')
		QtBind.setChecked(gui,cbxNiyaShaman,False)
def cbxSlaveWatcher_clicked(checked):
	if QtBind.isChecked(gui,cbxSolo81to90) or QtBind.isChecked(gui,cbxPT81to90):
		if checked:
			ClearGUI('Morph',cbxSlaveWatcher)
	else:
		log('Plugin: YANLIŞ SEÇİM!')
		QtBind.setChecked(gui,cbxSlaveWatcher,False)
def cbxDemonShaitan_clicked(checked):
	if QtBind.isChecked(gui,cbxSolo91to100) or QtBind.isChecked(gui,cbxPT91to100):
		if checked:
			ClearGUI('Morph',cbxDemonShaitan)
	else:
		log('Plugin: YANLIŞ SEÇİM!')
		QtBind.setChecked(gui,cbxDemonShaitan,False)
def cbxImhotep_clicked(checked):
	if QtBind.isChecked(gui,cbxSolo91to100) or QtBind.isChecked(gui,cbxPT91to100):
		if checked:
			ClearGUI('Morph',cbxImhotep)
	else:
		log('Plugin: YANLIŞ SEÇİM!')
		QtBind.setChecked(gui,cbxImhotep,False)
def cbxNephthys_clicked(checked):
	if QtBind.isChecked(gui,cbxSolo101to110) or QtBind.isChecked(gui,cbxPT101to110):
		if checked:
			ClearGUI('Morph',cbxNephthys)
	else:
		log('Plugin: YANLIŞ SEÇİM!')
		QtBind.setChecked(gui,cbxNephthys,False)
def cbxTombSnakeLady_clicked(checked):
	if QtBind.isChecked(gui,cbxSolo101to110) or QtBind.isChecked(gui,cbxPT101to110):
		if checked:
			ClearGUI('Morph',cbxTombSnakeLady)
	else:
		log('Plugin: YANLIŞ SEÇİM!')
		QtBind.setChecked(gui,cbxTombSnakeLady,False)


def ClearGUI(type,DontClear,DontClear2=None):
	if type == 'Reg':
		for cbx in RegCheckBoxes:
			if cbx != DontClear and cbx != DontClear2:
				QtBind.setChecked(gui,cbx,False)
	elif type == 'Morph':
		for cbx in MorphCheckBoxes:
			if cbx != DontClear and cbx != DontClear2:
				QtBind.setChecked(gui,cbx,False)

def button_start():
	global Started, Registering, Attacking, WaitingforParty, Picking, Inside
	stop_bot()
	if Started == False:
		if OptionsSelected():
			if Online:
				SaveConfig()
			Started = True
			QtBind.setText(gui,buttonStartStop,'  DURDUR  ')
			if WheresWaldo():
				log('Plugin: PLUGINI DIŞARIDA BAŞLAT!')
			else:
				Registering = True
			return
	elif Started == True:
		Started = False
		Attacking = False
		Registering = False
		WaitingforParty = False
		Picking = False
		Inside = False
		QtBind.setText(gui,buttonStartStop,'  BAŞLAT  ')


def Register():
	if OptionsSelected():
		npcs = get_npcs()
		for key, npc in npcs.items():
			if npc['servername'] == r"NPC_BATTLE_ARENA_MANAGER":
				type = GetBOIType()
				packet = struct.pack('<I', key)
				packet += b'\x02'
				packet += struct.pack('<I', type)
				inject_joymax(0x705A,packet,False)
				return
		log('Plugin: ARENA MANAGER YAKININDA DEĞİL !')

def BeginBattle():
	move_to(14675.0, 2592.0, 0.0)
	npcs = get_npcs()
	for key, npc in npcs.items():
		if npc['name'] == r"Dungeon Manager" or npc['name'] == r"Zindan Müdürü":
			packet = struct.pack('<I', key)
			inject_joymax(0x7045,packet,False)
			Timer(2.0, inject_joymax, [0x7588, b'\x01', False]).start()
			Timer(3.0, inject_joymax, [0x704B, packet, False]).start()
			Timer(3.0, move_to, [14709.0, 2592.0, 0.0]).start()
			Timer(8.0, ChangetoMob, ()).start()
def ChangetoMob():
	SetSkills()
	global Attacking
	if QtBind.isChecked(gui,cbxYeoha):
		type = "Yeoha Morphstone"
	elif QtBind.isChecked(gui,cbxSeiren):
		type = "Seiren Morphstone"
	elif QtBind.isChecked(gui,cbxNiyaShaman):
		type = "Niya Shaman Morphstone"
	elif QtBind.isChecked(gui,cbxSlaveWatcher):
		type = "Slave Watcher Morphstone"
	elif QtBind.isChecked(gui,cbxDemonShaitan):
		type = "Demon Shaitan Morphstone"
	elif QtBind.isChecked(gui,cbxImhotep):
		type = "Imhotep Morphstone"
	elif QtBind.isChecked(gui,cbxNephthys):
		type = "Nephthys Morphstone"
	elif QtBind.isChecked(gui,cbxTombSnakeLady):
		type = "Tomb Snake Lady Morphstone"
	npcs = get_npcs()
	for key, npc in npcs.items():
		if npc['name'] == type:
			packet = b'\x03'
			packet += struct.pack('<I', key)
			inject_joymax(0x7588,packet,False)
			Timer(1.0, move_to, [14730.0, 2587.0, 0.0]).start()
			Timer(5.0, move_to, [14737.0, 2593.0, 0.0]).start()
			Timer(6.0, StartAttack, ()).start()
def StartAttack():
	global Attacking
	Attacking = True
def SetSkills():
	global CastSkills
	if QtBind.isChecked(gui,cbxSolo71to80):
		if QtBind.isChecked(gui,cbxYeoha):
			CastSkills = [34574]
		elif QtBind.isChecked(gui,cbxSeiren):
			CastSkills = [34576]
	elif QtBind.isChecked(gui,cbxPT71to80):
		if QtBind.isChecked(gui,cbxYeoha):
			CastSkills = [34582]
		elif QtBind.isChecked(gui,cbxSeiren):
			CastSkills = [34584]
	elif QtBind.isChecked(gui,cbxSolo81to90):
		if QtBind.isChecked(gui,cbxNiyaShaman):
			CastSkills = [34578]
		elif QtBind.isChecked(gui,cbxSlaveWatcher):
			CastSkills = [34580]
	elif QtBind.isChecked(gui,cbxPT81to90):
		if QtBind.isChecked(gui,cbxNiyaShaman):
			CastSkills = [34586]
		elif QtBind.isChecked(gui,cbxSlaveWatcher):
			CastSkills = [34588]
	elif QtBind.isChecked(gui,cbxSolo91to100):
		if QtBind.isChecked(gui,cbxDemonShaitan):
			CastSkills = [34590]
		elif QtBind.isChecked(gui,cbxImhotep):
			CastSkills = [34592]
	elif QtBind.isChecked(gui,cbxPT91to100):
		if QtBind.isChecked(gui,cbxDemonShaitan):
			CastSkills = [34598]
		elif QtBind.isChecked(gui,cbxImhotep):
			CastSkills = [34600]
	elif QtBind.isChecked(gui,cbxSolo101to110):
		if QtBind.isChecked(gui,cbxNephthys):
			CastSkills = [34594]
		elif QtBind.isChecked(gui,cbxTombSnakeLady):
			CastSkills = [34596]
	elif QtBind.isChecked(gui,cbxPT101to110):
		if QtBind.isChecked(gui,cbxNephthys):
			CastSkills = [34602]
		elif QtBind.isChecked(gui,cbxTombSnakeLady):
			CastSkills = [34604]
def GetBOIType():
	if QtBind.isChecked(gui,cbxSolo71to80):
		return 228
	elif QtBind.isChecked(gui,cbxSolo81to90):
		return 229
	elif QtBind.isChecked(gui,cbxSolo91to100):
		return 232
	elif QtBind.isChecked(gui,cbxSolo101to110):
		return 233
	elif QtBind.isChecked(gui,cbxPT71to80):
		return 230
	elif QtBind.isChecked(gui,cbxPT81to90):
		return 231
	elif QtBind.isChecked(gui,cbxPT91to100):
		return 234
	elif QtBind.isChecked(gui,cbxPT101to110):
		return 235
def AttackMob(Skill,MobID):
	if MobID > 0:
		packet = b'\x01\x04'
		packet += struct.pack('<I',Skill)
		packet += b'\x01'
		packet += struct.pack('<I',MobID)
		inject_joymax(0x7074,packet,False)
def RemoveSkill(SkillID):
	if SkillID in ActiveSkills:
		ActiveSkills.remove(SkillID)
def UseSkill():
	global ActiveSkills, SkillDelay
	MobID = GetMobID()
	if Started:
		for skill in CastSkills:
			if skill not in ActiveSkills:
				AttackMob(skill,MobID)
				SelectMob(MobID)
				return
def SelectMob(targetID):
	packet = struct.pack('<I',targetID)
	inject_joymax(0x7045,packet,False)
def GetMobID():
	AttackRadius = int(QtBind.text(gui,txtRadius))
	Mobs = get_monsters()
	if Mobs:
		for key, mob in Mobs.items():
			dist = CalcRadiusFromME(mob['x'],mob['y'])
			if dist < AttackRadius:
				return key
			else:
				return 0
	elif not AtAttackArea():
		move_to(14737.0, 2593.0, 0.0)
		return 0
def AtAttackArea():
	X = 14737.0
	Y = 2593.0
	px = get_character_data()['x']
	py = get_character_data()['y']
	if px == X and py == Y:
		return True
	else:
		return False
def MovetoPick():
	move_to(14762.0, 2592.0, 0.0)
	set_training_position(0, 14762.0, 2592.0, 0)
	start_bot()
def CalcRadiusFromME(Px,Py):
	my = get_position()
	dist = ((my['x'] - Px)**2 + (my['y'] - Py)**2)**0.5
	return dist
def WheresWaldo():
	region = get_character_data()['region']
	if region == 27091 or region == 27092:
		return True
def party_count():
	pt = get_party()
	count = 0
	if pt:
		for key, char in pt.items():
			count += 1
		return count - 1
def CheckforParty():
	global WaitingforParty
	WaitFor = int(QtBind.text(gui,txtPartyMembers))
	MembersInside = 0
	party = get_party()
	if WaitingforParty and Started:
		if party:
			for key, player in party.items():
				if player['player_id'] > 0:
					MembersInside += 1
					if MembersInside >= WaitFor:
						log('Plugin: TÜM PARTİ ÜYELERİ GİRİŞ YAPTI. SAVAŞ BAŞLIYOR.')
						WaitingforParty = False
						Timer(5.0, BeginBattle, ()).start()
						return
			log('Plugin: TÜM PARTİ ÜYELERİ GİRİŞ YAPMADI..BEKLENİYOR..')
			Timer(5.0, CheckforParty, ()).start()
def OptionsSelected():
	if QtBind.isChecked(gui,cbxSolo71to80) or QtBind.isChecked(gui,cbxSolo81to90) or QtBind.isChecked(gui,cbxSolo91to100) or QtBind.isChecked(gui,cbxSolo101to110) or QtBind.isChecked(gui,cbxPT71to80) or QtBind.isChecked(gui,cbxPT81to90) or QtBind.isChecked(gui,cbxPT91to100) or QtBind.isChecked(gui,cbxPT101to110):
		return True
	log('Plugin: LÜTFEN GEREKLİ TÜM SEÇENEKLERİ SEÇİN.')
	return False
# script command BOI,type,morph
#ex..BOI,solo,A .... BOI,party,B
def BOI(args):
	ClearGUI('Morph',None)
	ClearGUI('Reg',None)
	type = args[1]
	morph = args[2]
	lvl =  get_character_data()['level']
	if lvl >= 71 and lvl <= 80:
		if type == 'solo':
			QtBind.setChecked(gui,cbxSolo71to80,True)
		if type == 'party':
			QtBind.setChecked(gui,cbxPT71to80,True)
		if morph == 'A':
			QtBind.setChecked(gui,cbxYeoha,True)
		if morph == 'B':
			QtBind.setChecked(gui,cbxSeiren,True)
	elif lvl >= 81 and lvl <= 90:
		if type == 'solo':
			QtBind.setChecked(gui,cbxSolo81to90,True)
		if type == 'party':
			QtBind.setChecked(gui,cbxPT81to90,True)
		if morph == 'A':
			QtBind.setChecked(gui,cbxNiyaShaman,True)
		if morph == 'B':
			QtBind.setChecked(gui,cbxSlaveWatcher,True)
	elif lvl >= 91 and lvl <= 100:
		if type == 'solo':
			QtBind.setChecked(gui,cbxSolo91to100,True)
		if type == 'party':
			QtBind.setChecked(gui,cbxPT91to100,True)
		if morph == 'A':
			QtBind.setChecked(gui,cbxDemonShaitan,True)
		if morph == 'B':
			QtBind.setChecked(gui,cbxImhotep,True)
	elif lvl >= 101 and lvl <= 110:
		if type == 'solo':
			QtBind.setChecked(gui,cbxSolo101to110,True)
		if type == 'party':
			QtBind.setChecked(gui,cbxPT101to110,True)
		if morph == 'A':
			QtBind.setChecked(gui,cbxNephthys,True)
		if morph == 'B':
			QtBind.setChecked(gui,cbxTombSnakeLady,True)
	log('Plugin: BOI SEÇENEKLERİ AYARLANIYOR..')
	Timer(1.0, button_start, ()).start()
	return 0
def ChangetoParty():
	ClearGUI('Morph',None)
	ClearGUI('Reg',None)
	lvl =  get_character_data()['level']
	profile = QtBind.text(gui,txtPartyProfile)
	if profile:
		set_profile(profile)
	if lvl >= 71 and lvl <= 80:
		QtBind.setChecked(gui,cbxPT71to80,True)
		QtBind.setChecked(gui,cbxYeoha,True)
	elif lvl >= 81 and lvl <= 90:
		QtBind.setChecked(gui,cbxPT81to90,True)
		QtBind.setChecked(gui,cbxNiyaShaman,True)
	elif lvl >= 91 and lvl <= 100:
		QtBind.setChecked(gui,cbxPT91to100,True)
		QtBind.setChecked(gui,cbxDemonShaitan,True)
	elif lvl >= 101 and lvl <= 110:
		QtBind.setChecked(gui,cbxPT101to110,True)
		QtBind.setChecked(gui,cbxNephthys,True)
def ReturntoTraining():
	global Started, Registering, Attacking, WaitingforParty, Picking, PartyCount, SoloCount, Inside
	if QtBind.isChecked(gui,cbxFinished):
		log('Plugin: KASILMA ALANINA DEVAM EDİLİYOR..')
		ClearGUI('Morph',None)
		ClearGUI('Reg',None)
		Started = False
		Attacking = False
		Registering = False
		WaitingforParty = False
		Picking = False
		Inside = False
		PartyCount = 0
		SoloCount = 0
		QtBind.setText(gui,buttonStartStop,'  Start  ')
		profile = QtBind.text(gui,txtFinishedProfile)
		if profile:
			set_profile(profile)
		Timer(1.0, use_return_scroll, ()).start()
		Timer(10.0, start_bot, ()).start()
def SoloDone():
	if SoloCount >= 2:
		return True
	else:
		return False

def PartyDone():
	if PartyCount >= 2:
		return True
	else:
		return False
def teleported():
	global Registering, Attacking, Picking, WaitingforParty, SoloCount, PartyCount, Inside
	if Started:
		if Registering:
			if QtBind.isChecked(gui,cbxSolo71to80) or QtBind.isChecked(gui,cbxSolo81to90) or QtBind.isChecked(gui,cbxSolo91to100) or QtBind.isChecked(gui,cbxSolo101to110):
				SoloCount += 1
				PartyCount = 0
			if QtBind.isChecked(gui,cbxPT71to80) or QtBind.isChecked(gui,cbxPT81to90)  or QtBind.isChecked(gui,cbxPT91to100) or QtBind.isChecked(gui,cbxPT101to110):
				PartyCount += 1
				SoloCount = 0
			Registering = False
			Inside = True
			log('Plugin: BAŞARILI BİR ŞEKİLDE SAVAŞA GİRİLDİ.')
			if not get_party():
				Timer(5.0, BeginBattle, ()).start()
			else:
				WaitingforParty = True
				log('Plugin: PARTİ ÜYELERİNİN GİRİŞ YAPMASI BEKLENİYOR.')
				Timer(8.0, CheckforParty, ()).start()
		elif Attacking:
			Inside = False
			if PartyCount >= 2:
				Timer(1.0, ReturntoTraining, ()).start()
			Attacking = False
			Registering = True
			QtBind.setText(gui,lblStage,'0')
		#successful
		elif Picking:
			if PartyCount >= 2:
				Timer(1.0, ReturntoTraining, ()).start()
			Registering = True
			Picking = False
			Inside = False
			stop_bot()
			QtBind.setText(gui,lblStage,'0')
			log('Plugin: BOI DÖNGÜSÜ TAMAMLANDI.')
		#party didnt enter
		elif WaitingforParty:
			if PartyCount >= 2:
				Timer(1.0, ReturntoTraining, ()).start()
			log('Plugin: PARTİ ÜYELERİ GEREKLİ SÜRE İÇİNDE GİRİŞ YAPMADI.')
			WaitingforParty = False
			Registering = True
			Inside = False
			QtBind.setText(gui,lblStage,'0')
def event_loop():
	global DelayCounter
	if Started and Attacking:
		DelayCounter += 500
		if DelayCounter >= SkillDelay:
			DelayCounter = 0
			UseSkill()
			return
	if Started and Registering:
		DelayCounter += 500
		if DelayCounter >= RegDelay:
			DelayCounter = 0
			if QtBind.isChecked(gui,cbxPT71to80) or QtBind.isChecked(gui,cbxPT81to90)  or QtBind.isChecked(gui,cbxPT91to100) or QtBind.isChecked(gui,cbxPT101to110):
				partycount = party_count()
				WaitFor = int(QtBind.text(gui,txtPartyMembers))
				if partycount >= WaitFor:
					Register()
				else:
					log('Plugin: KAYIT YAPILMADAN ÖNCE PARTİ ÜYELERİ BEKLENİYOR.')
			else:
				Register()
def handle_joymax(opcode, data):
	global Attacking, Picking
	if opcode == 0xB05A and Registering:
		if data[0] == 2 and data[2] == 28:
			response = data[1]
			if response == 60:
				log('Plugin: HENÜZ YENİDEN İÇERİ GİRİŞ YAPAMAZSIN!')
			elif response == 42:
				log('Plugin: PARTİDE DEĞİLSİN!')
			elif response == 44:
				log('Plugin: GİRİŞ İÇİN YETERLİ SEVİYEYE SAHİP DEĞİLSİN!')
			elif response == 39:
				log("Plugin: ÇOK FAZLA GİRİŞ YAPTIN!")
				if QtBind.isChecked(gui,cbxChange):
					ChangetoParty()
				elif QtBind.isChecked(gui,cbxFinished):
					ReturntoTraining()
			elif response == 40:
				log("Plugin: PARTİ LİDERİ ÖNCE GİRİŞ YAPMALIDIR!")
			elif response == 66:
				log("Plugin: SOLO GİRİŞ YAPMAK İÇİN PARTİDE OLAMAZSIN..")
				if QtBind.isChecked(gui,cbxSolo71to80) or QtBind.isChecked(gui,cbxSolo81to90) or QtBind.isChecked(gui,cbxSolo91to100) or QtBind.isChecked(gui,cbxSolo101to110):
					#leave party
					inject_joymax(0x7061,b'',False)
					log('Plugin: PARTİDEN AYRILINIYOR..')
	elif opcode == 0xB0BD and Inside and not Picking:
		global MorphID
		SelfID = get_character_data()['player_id']
		packetIndex = 0
		PlayerID  = struct.unpack_from("<I",data,packetIndex)[0]
		if SelfID == PlayerID:
			packetIndex = 8
			MorphID = struct.unpack_from("<I",data,packetIndex)[0]
	#Skill removed
	elif opcode == 0xB072 and Inside and not Picking:
		packetIndex = 1
		SkillID  = struct.unpack_from("<I",data,packetIndex)[0]
		if SkillID == MorphID:
			log('Plugin: BİÇİM KAYBEDİLDİ, TEKRAR BİÇİMLENDİRİLİYOR..')
			Attacking = False
			Timer(1.0, move_to, [14709.0, 2592.0, 0.0]).start()
			Timer(3.0, ChangetoMob, ()).start()
	elif opcode == 0x3011 and Attacking:
		p = b'\x81' 
		inject_joymax(0x3053,p,True)
		Attacking = False
		Timer(3.0, move_to, [14709.0, 2592.0, 0.0]).start()
		Timer(7.0, ChangetoMob, ()).start()
	elif opcode == 0x3592 and Inside:
		if data[0] == 255 and data[1] == 65:
			stage = int(data[2])
			if stage:
				QtBind.setText(gui,lblStage,str(stage))
		elif data[0] == 255 and data[1] == 66:
			if data[2] == 1:
				QtBind.setText(gui,lblStage,'Finished')
				Attacking = False
				Picking = True
				MovetoPick()
	elif opcode == 0xB070 and Attacking:
		if data[1] == 2:
			packetIndex = 3
			Skill  = struct.unpack_from("H",data,packetIndex)[0]
			packetIndex = 7
			AttackerID  = struct.unpack_from("<I",data,packetIndex)[0]
			SelfID = get_character_data()['player_id']
			if AttackerID == SelfID:
				ActiveSkills.append(Skill)
				CoolDown = 5
				Timer(CoolDown,RemoveSkill,[Skill]).start()
	return True
def joined_game():
	global Online
	Online = True
	Timer(10.0, loadDefaults, ()).start()
def GetConfig():
	return path + get_character_data()['server'] + "_" + get_character_data()['name'] + ".json"
def SaveConfig():
	data = {}
	data["AttackRadius"] = int(QtBind.text(gui,txtRadius))
	data["PartyAmount"] = int(QtBind.text(gui,txtPartyMembers))
	data["PartyMode"] = QtBind.isChecked(gui,cbxChange)
	data["PartyProfile"] = QtBind.text(gui,txtPartyProfile)
	data["Finished"] = QtBind.isChecked(gui,cbxFinished)
	data["TrainingAreaProfile"] = QtBind.text(gui,txtFinishedProfile)
	with open(GetConfig(),"w") as f:
		f.write(json.dumps(data, indent=4))
	log("Plugin: CONFİG KAYIT EDİLDİ.")
def LoadConfigs():
	if os.path.exists(GetConfig()):
		data = {}
		with open(GetConfig(),"r") as f:
			data = json.load(f)
		if "AttackRadius" in data:
			QtBind.setText(gui,txtRadius,str(data["AttackRadius"]))
		if "PartyAmount" in data:
			QtBind.setText(gui,txtPartyMembers,str(data["PartyAmount"]))
		if "PartyMode" in data:
			QtBind.setChecked(gui,cbxChange,data["PartyMode"])
		if "PartyProfile" in data:
			QtBind.setText(gui,txtPartyProfile,data["PartyProfile"])
		if "Finished" in data:
			QtBind.setChecked(gui,cbxFinished,data["Finished"])
		if "TrainingAreaProfile" in data:
			QtBind.setText(gui,txtFinishedProfile,data["TrainingAreaProfile"])
def loadDefaults():
	LoadConfigs()
	lvl =  get_character_data()['level']
	if lvl >= 71 and lvl <= 80:
		QtBind.setChecked(gui,cbxSolo71to80,True)
		QtBind.setChecked(gui,cbxYeoha,True)
	elif lvl >= 81 and lvl <= 90:
		QtBind.setChecked(gui,cbxSolo81to90,True)
		QtBind.setChecked(gui,cbxNiyaShaman,True)
	elif lvl >= 91 and lvl <= 100:
		QtBind.setChecked(gui,cbxSolo91to100,True)
		QtBind.setChecked(gui,cbxDemonShaitan,True)
	elif lvl >= 101 and lvl <= 110:
		QtBind.setChecked(gui,cbxSolo101to110,True)
		QtBind.setChecked(gui,cbxNephthys,True)
Timer(1.0, loadDefaults, ()).start()
log("Plugin: "+pName+" v"+pVersion+" BASARIYLA YUKLENDI.")
if not os.path.exists(path):
	os.makedirs(path)
	log('Plugin: '+pName+' CONFIG KLASORU OLUSTURULDU.')
