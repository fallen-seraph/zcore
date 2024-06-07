# zcore

Core set of utilities and scripts to deploy and service zomboid with [lgsm](https://linuxgsm.com/servers/pzserver/).

## Pre-Requisits

Assuming Ubuntu
Add a new user of your choice
```bash
adduser [username]
```

Install linux prereqs
```bash
sudo dpkg --add-architecture i386; sudo apt update; sudo apt install -y binutils bsdmainutils bzip2 lib32gcc-s1 lib32stdc++6 libsdl2-2.0-0:i386 openjdk-21-jre pigz rng-tools5 steamcmd unzip python3-pip
```

Logout from root and into the user created above. This is necessary for systemctl --user statements to correctly run. 

The zcore needs to be unzipped to your home directory for all the pathing to be correct.
```bash
unzip ~/source.zip
```

Install python modules
```bash
pip install -r ~/zcore/requirements.txt --break-system-packages
```

## Usage

Update the config.json file to apply to your system.

If you need a full system install use the following. 
```bash
python3 ~/zcore/zomboid_core.py install
```

If you already have zomboid installed and it's installed to ~/Zomboid then run the following to install sysd and misc.
```bash
python3 ~/zcore/zomboid_core.py install sysd
python3 ~/zcore/zomboid_core.py install misc
```

After running `install` or `install misc` you can log out and log back in or run the following to update aliases.
```bash
. ~/.bash_aliases
```

From here you can use `zcore -h` or `zcore [command] -h` to view arguments as needed for commands. 

Systemctl services installed and enabled:
```bash
zomboid_core.service    - Zomboid Server
zomboid_reboot.service  - Runs the restart Schedular
zomboid_reboot.timer    - Triggers zomboid_reboot.service every 10 minutes
zomboid_notify.service  - Is triggered if the zomboid server fails to restart itself twice
zomboid_skimmer.service - Scrapes the debug log for mod reboots and steam mainteance starts.
```

Start the server with:
```bash
systemctl --user start zomboid_core
```

Start the reboot timer with:
```bash
systemctl --user start zomboid_reboot.timer
```

Start the log scraper:
```bash
systemctl --user start zomboid_skimmer
```