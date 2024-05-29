from tools.linux_files import LinuxFiles
import sys

def range_generator(locationX1, locationY1, locationX2, locationY2):

    for x in range(locationX1, locationY1+1):
        for y in range (locationX2, locationY2+1):
            print(str(x)+"_"+str(y))#, file=open(outputFile, 'a'))




# #!/bin/bash
# SAVEDIR="$1"
# LISTFILE="$2"

# if [ -z "$SAVEDIR" ];
# then
# 	echo "no save directory given. use chunk_remove_start.sh"
# else
# 	if [ -z "$LISTFILE" ];
# 	then
# 		echo "no list file given. use chunk_remove_start.sh"
# 	else
# 		echo "processing $LISTFILE ($FILENAME)"

# 		while read -r line;
# 		do
# 			[[ -e "$SAVEDIR/map_$line.bin" ]] && rm "$SAVEDIR/map_$line.bin"
# 			[[ -e "$SAVEDIR/isoregiondata/datachunk_$line.bin" ]] && rm "$SAVEDIR/isoregiondata/datachunk_$line.bin"
# 		done < "$LISTFILE"
# 	fi
# fi