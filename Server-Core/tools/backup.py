#systemctl --user stop apathabove

#rsync -aq --exclude 'backups' --delete /home/apathabove/Zomboid /home/apathabove/backups/temp/

#tar -czf /home/apathabove/backups/$(date '+%d_%m_%Y')_backup.tar.gz -C /home/apathabove/backups/temp .

#systemctl --user start apathabove

#if [[ -f /home/apathabove/backups/$(date --date="3 days ago" '+%d_%m_%Y')_backup.tar.gz ]]; then
        #rm /home/apathabove/backups/$(date --date="3 days ago" '+%d_%m_%Y')_backup.tar.gz
#fi


