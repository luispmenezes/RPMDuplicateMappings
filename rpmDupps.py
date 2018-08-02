import os
import sys
import re
import argparse

def getRpmDependencies(rpmFolderPath, mapping):
	dependencyTree=os.popen('mvn -f %s dependency:tree' % rpmFolderPath).read().splitlines()
	startIdx=0
	endIdx=0
	jarName =  mapping[:re.search("\d", mapping).start()-1]

	for idx,deps in enumerate(dependencyTree):
		if ":tree" in deps:
			startIdx=idx+2
		elif startIdx>0 and "[INFO] " in deps:
			dependencyTree[idx]=deps[7:]
		if jarName in deps:
			endIdx=idx+1

	dependencyTree[startIdx]= dependencyTree[startIdx].replace("+","\\")

	return dependencyTree[startIdx:endIdx]


targetFolder = sys.argv[1] 
reverseMap = dict()

rpmList=os.popen('find %s -name \'*.rpm\'' % targetFolder).read().splitlines()

for rpm in rpmList:
	mappingList=os.popen('rpm -qpl %s' % rpm).read().splitlines()
	for mapping in mappingList:
		reverseMap.setdefault(mapping, []).append(rpm)

for mapping in reverseMap:
	if len(reverseMap[mapping]) > 1:
		print("\033[7m>"+mapping+"\033[0m")
		for rpmMapping in reverseMap[mapping]:
			print("\033[1m-"+rpmMapping[rpmMapping.rfind("/")+1:]+"\033[0m")
			if mapping.endswith(".jar"):
				dependencyT = getRpmDependencies(rpmMapping[:rpmMapping.find("target/")],mapping[mapping.rfind("/")+1:])
				for dep in dependencyT:
					print dep
			print("")