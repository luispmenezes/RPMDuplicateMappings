#!/bin/bash

#List duplicate file mappings from RPMs in folder   

declare -A rpmMappings

if [ "$1" == "-h" ] || [ "$#" -gt 4 ]; then
  echo "Usage: `basename $0` FILES [-f PATTERN]"
  exit 0
fi

for f in $(find $1 -name '*.rpm'); do
	for m in $(rpm -qpl $f);do
		if [ "$#" -gt 2 ] && [ "$2" == "-f" ];then
			if [[ "$m" =~ "$3" ]]; then 
				rpmMappings[$m]+="| $f\n"
			fi
		else
			rpmMappings[$m]+="| $f\n"	
		fi			
	done 
done

for k in "${!rpmMappings[@]}";do
	if [ $(echo "${rpmMappings[$k]}" | grep -o "|" | wc -l) -gt 2 ]; then
		echo -e "\e[7m > $k\e[0m"
		echo -e "${rpmMappings[$k]}"
	fi
done 
