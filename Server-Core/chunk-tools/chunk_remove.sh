#!/bin/bash
SAVEDIR="$1"
LISTFILE="$2"

if [ -z "$SAVEDIR" ];
then
	echo "no save directory given. use chunk_remove_start.sh"
else
	if [ -z "$LISTFILE" ];
	then
		echo "no list file given. use chunk_remove_start.sh"
	else
		echo "processing $LISTFILE ($FILENAME)"

		while read -r line;
		do
			[[ -e "$SAVEDIR/map_$line.bin" ]] && rm "$SAVEDIR/map_$line.bin"
			[[ -e "$SAVEDIR/isoregiondata/datachunk_$line.bin" ]] && rm "$SAVEDIR/isoregiondata/datachunk_$line.bin"
		done < "$LISTFILE"
	fi
fi
