from phBot import *
from threading import Timer
import struct

pName = 'TrBalon'
pVersion = '1.0.0'
pUrl = 'https://raw.githubusercontent.com/TheMoB41/TrPlugins/main/TrBalon.py'
INFLATE_BALLOON_LEVEL_STOP = 6
INFLATE_BALLOON_LEVELUP_DELAY = 4.0 # seconds

isInflating = False
inflatingLevel = 0
def GetItemByExpression(_lambda):
	items = get_inventory()['items']
	for slot, item in enumerate(items):
		if item:
			if _lambda(item['name'],item['servername']):
				item['slot'] = slot
				return item
	return None
def InflateNewBalloon():
	item = GetItemByExpression(lambda n,s: s.startswith('ITEM_ETC_E101216_BALLOON_'))
	if item:
		global inflatingLevel
		inflatingLevel = 1
		p = struct.pack('B',item['slot'])
		p += b'\x30\x0C\x09\x00'
		log('Plugin: KULLANILIYOR : "'+item['name']+'"...')
		inject_joymax(0x704C,p,True)
		Timer(INFLATE_BALLOON_LEVELUP_DELAY,LevelUpBalloon).start()
	else:
		global isInflating
		isInflating = False
		log('Plugin: BALON BULUNAMADI.. RETURN SCROLL KULLANILIYOR...')
		use_return_scroll()
		start_bot()
def LevelUpBalloon():
	global inflatingLevel
	if inflatingLevel >= INFLATE_BALLOON_LEVEL_STOP:
		log('Plugin: BALON ÖDÜLÜ ALINDI : (Lv.'+str(inflatingLevel)+')')
		inject_joymax(0x7574,b'\x02',False)
		inflatingLevel = 0
		Timer(INFLATE_BALLOON_LEVELUP_DELAY,LevelUpBalloon).start()
	elif inflatingLevel:
		log('Plugin: BALON ŞİŞİRİLİYOR..')
		inject_joymax(0x7574,b'\x01',False)
		Timer(INFLATE_BALLOON_LEVELUP_DELAY,LevelUpBalloon).start()
	else:
		InflateNewBalloon()
def InflateBalloons():
	if not isInflating:
		inflate_balloons([])
def inflate_balloons(args):
	item = GetItemByExpression(lambda n,s: s.startswith('ITEM_ETC_E101216_BALLOON_'))
	if item:
		stop_bot()
		global isInflating
		isInflating = True
		log('Plugin: BALON ŞİŞİRMEYE BAŞLANIYOR...')
		Timer(0.001,InflateNewBalloon).start()
	else:
		log('Plugin: ENVANTERDE BALON BULUNAMADI..')
	return 0
def handle_joymax(opcode,data):
	if opcode == 0xB574 and isInflating:
		if data[0] == 1:
			global inflatingLevel
			if data[1] == 1:
				inflatingLevel += 1
			elif data[1] == 2:
				inflatingLevel = 0
	return True
log("Plugin: "+pName+" v"+pVersion+" BASARIYLA YUKLENDI.")
