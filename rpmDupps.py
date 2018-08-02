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


parser = argparse.ArgumentParser(description='Analyze duplicate RPM file mappings (and their dependency tree) in target folders')
parser.add_argument('files', nargs='+')
parser.add_argument("-f","--filter", help="apply filter to mapping")
parser.add_argument("-t","--noTree", help="disable dependency tree generation", action='store_true')

args = parser.parse_args()

targetFolder = ' '.join([str(x) for x in args.files]) 
reverseMap = dict()

filterPattern = re.compile("./*")
if args.filter is not None:
	filterPattern = re.compile(args.filter)

rpmList=os.popen('find %s -name \'*.rpm\'' % targetFolder).read().splitlines()

for rpm in rpmList:
	mappingList=os.popen('rpm -qpl %s' % rpm).read().splitlines()
	for mapping in mappingList:
		if filterPattern.match(mapping):  
			reverseMap.setdefault(mapping, []).append(rpm)

for mapping in reverseMap:
	if len(reverseMap[mapping]) > 1:
		print("\033[7m>"+mapping+"\033[0m")
		for rpmMapping in reverseMap[mapping]:
			print("\033[1m-"+rpmMapping[rpmMapping.rfind("/")+1:]+"\033[0m")
			if mapping.endswith(".jar") and not args.noTree:
				dependencyT = getRpmDependencies(rpmMapping[:rpmMapping.find("target/")],mapping[mapping.rfind("/")+1:])
				for dep in dependencyT:
					print(dep)
			print("")