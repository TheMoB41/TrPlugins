from phBot import *
import QtBind
import urllib.request
import re
import os
import shutil

pName = 'TrUpdater'
pVersion = '1.0.0'
pUrl = 'https://raw.githubusercontent.com/TheMoB41/TrPlugins/main/TrUpdater.py'

# ______________________________ YUKLEME ______________________________ #
# KULLANICI ARAYUZU
gui = QtBind.init(__name__,pName)
lblPlugins = QtBind.createLabel(gui,"BILGISAYARDA BULUNAN PLUGINLER :",21,11)
lvwPlugins = QtBind.createList(gui,21,30,700,200)
lstPluginsData = []
btnCheck = QtBind.createButton(gui,'btnCheck_clicked',"  GUNCELLEMELERI KONTROL ET  ",300,8)
btnUpdate = QtBind.createButton(gui,'btnUpdate_clicked',"  SECILEN PLUGINI GUNCELLE  ",480,8)
lblPlugins2 = QtBind.createLabel(gui,"TrUpdater:\n * TheMoB TARAFINDAN DUZENLENMISTIR. \n * FEEDBACK SISTEMLI BIR YAZILIMDIR. \n * HATA VE ONERI BILDIRIMLERINIZI BANA ULASTIRABILIRSINIZ.",21,230)
# ______________________________ METHODLAR ______________________________ #
# PLUGIN KLASORUNU KONTROL ETME
def GetPluginsFolder():
	return str(os.path.dirname(os.path.realpath(__file__)))
def btnCheck_clicked():
	QtBind.clear(gui,lvwPlugins)
	pyFolder = GetPluginsFolder()
	files = os.listdir(pyFolder)
	global lstPluginsData
	for filename in files:
		if filename.endswith(".py"):
			pyFile = pyFolder+"\\"+filename
			with open(pyFile,"r",errors='ignore') as f:
				pyCode = str(f.read())
				if re.search("\npVersion = [0-9a-zA-Z.'\"]*",pyCode):
					pyVersion = re.search("\npVersion = ([0-9a-zA-Z.'\"]*)",pyCode).group(0)[13:-1]
					pyName = filename[:-3]
					if re.search("\npName = ([0-9a-zA-Z'\"]*)",pyCode):
						pyName = re.search("\npName = ([0-9a-zA-Z'\"]*)",pyCode).group(0)[10:-1]
					pyUrl = pyCode.find("\npUrl = ")
					pyInfo = filename+" ("+pyName+" v"+pyVersion+") - "
					pData = {}
					pData['canUpdate'] = False
					if pyUrl != -1:
						pyUrl = pyCode[pyUrl+9:].split('\n')[0][:-1]
						pyNewVersion = getVersion(pyUrl)
						if pyNewVersion and compareVersion(pyVersion,pyNewVersion):
							pData['canUpdate'] = True
							pData['url'] = pyUrl
							pData['filename'] = filename
							pData['pName'] = pyName
							pyInfo += "GUNCELLEME MEVCUT (v"+pyNewVersion+")"
						else:
							pyInfo += "GUNCELLENDI"
					else:
						pyInfo += "GUNCELLEME BASARISIZ. URL BULUNAMADI."
					QtBind.append(gui,lvwPlugins,pyInfo)
					lstPluginsData.append(pData)
def getVersion(url):
	try:
		req = urllib.request.Request(url, headers={'User-Agent' : "Mozilla/5.0 (Windows NT 6.2; WOW64; rv:22.0) Gecko/20100101 Firefox/22.0"})
		with urllib.request.urlopen(req) as w:
			pyCode = str(w.read().decode("utf-8"))
			if re.search("\npVersion = [0-9.'\"]*",pyCode):
				return re.search("\npVersion = ([0-9a-zA-Z.'\"]*)",pyCode).group(0)[13:-1]
	except:
		pass
	return None
def compareVersion(a, b):
	a = tuple(map(int, (a.split("."))))
	b = tuple(map(int, (b.split("."))))
	return a < b
def btnUpdate_clicked():
	indexSelected = QtBind.currentIndex(gui,lvwPlugins)
	if indexSelected >= 0:
		pyData = lstPluginsData[indexSelected]
		if "canUpdate" in pyData and pyData['canUpdate']:
			pyUrl = pyData['url']
			try:
				req = urllib.request.Request(pyUrl, headers={'User-Agent' : "Mozilla/5.0 (Windows NT 6.2; WOW64; rv:22.0) Gecko/20100101 Firefox/22.0"})
				with urllib.request.urlopen(req) as w:
					pyCode = str(w.read().decode("utf-8"))
					pyVersion = re.search("\npVersion = ([0-9a-zA-Z.'\"]*)",pyCode).group(0)[13:-1]
					pyFolder = GetPluginsFolder()+'\\'
					shutil.copyfile(pyFolder+pyData['filename'],pyFolder+pyData['pName']+".py.bkp")
					os.remove(pyFolder+pyData['filename'])
					with open(pyFolder+pyData['pName']+".py","w+") as f:
						f.write(pyCode)
					QtBind.removeAt(gui,lvwPlugins,indexSelected)
					QtBind.append(gui,lvwPlugins,pyData['pName']+".py ("+pyData['pName']+" v"+pyVersion+") - Updated recently")
					log('Plugin: "'+pyData['pName']+'" PLUGIN BASARIYLA GUNCELLENDI')
			except:
				log("Plugin: GUNCELLEME YAPILIRKEN HATA OLUSTU.")
# PLUGIN YUKLENDI
log('Plugin: '+pName+' v'+pVersion+' BASARIYLA YUKLENDI.')
