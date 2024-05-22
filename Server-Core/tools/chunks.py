















#Following code blocks only for reference, will be removed eventually. 
#X1 = 870
#Y1 = 576
#X2 = 880
#Y2 = 586
#outputFile = "/home/apathabove/Zomboid/Lua/chunk_lists/bill.txt"

# for i in range(X1, X2+1):
#     for y in range (Y1, Y2+1):
#         print(str(i)+"_"+str(y), file=open(outputFile, 'a'))


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