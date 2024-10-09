
from datetime import date
import json
import os


class GameAssetVerification:
	def __init__(self):
		self.filepath = os.path.realpath(__file__) + "/GameAssets"
		self.manifestLocalPath = self.filePath + "/manifest.json"
		self.manifestRemoteLink = "https://drive.google.com/file/d/1y-tB0zZSu-rWO1Arx0xBb_V1g9FuniLc/"
		self.localManifest : list[AssetManifestObject] = []
		self.remoteManifest :  list[AssetManifestObject] = []

	def verify(self):
		self.checkLocalPaths()
		self.loadManifests()

		changeList = self.compareManifest()

		self.updateFiles(changeList)


	def createManifest():
		#Create a new Manifest based on the files in a local directory, push that to the remote server
		pass

	def checkLocalPaths(self):
		if not os.path.exists(self.filepath):
			os.makedirs(self.filepath)

	def loadManifests(self):
		#local
		if os.path.isfile(self.manifestLocalPath):
			with open(self.manifestLocalPath) as manFile:
				jdata = json.load(manFile)
			for a in jdata:
				self.localManifest.append(AssetManifestObject(a['fileName'], a['path'], a['fileSize'], a['fileDate'], a['remoteLink']))
		
		#remote replace local manifest with remote
		remoteMan = ""

		filestream = open(self.manifestLocalPath, "wt+") #maybe just w, test this
		filestream.write(remoteMan)
		filestream.close()

		with open(self.manifestLocalPath) as manFile:
			jdata = json.load(manFile)
			for a in jdata:
				self.remoteManifest.append(AssetManifestObject(a['fileName'], a['path'], a['fileSize'], a['fileDate'], a['remoteLink']))

	def compareManifest(self) -> list[str]:
		retList = []
		for a in self.remotemanifest:
			if a not in self.localManifest:
				retList.append(a)

		return retList

	def updateFiles(self, changeList):
		for a in changeList:
			#download remote file
			#replace existing files if necessary

class AssetManifestObject:
	def __init__(self, fileName: str, path: str, fileSize: int, fileDate: date, remoteLink: str):
		self.fileName = fileName
		self.path = path
		self.fileSize = fileSize
		self.fileDate = fileDate
		self.remoteLink = remoteLink

	def __eq__(self, other):
		if not isinstance(other, AssetManifestObject):
			return False
		return self.fileName == other.fileName and self.path == other.path and self.fileSize == other.fileSize and self.fileDate == other.fileDate and self.remoteLink == other.remoteLink