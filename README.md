# APA-Server-Core

Core set of utilities and scripts to deploy and service zomboid with [lgsm](https://linuxgsm.com/servers/pzserver/).

##Pre-Requisits

Assuming Ubuntu 22
Add a new user of your choice

```bash
adduser [username]
```

Install prereqs

```bash
sudo dpkg --add-architecture i386; sudo apt update; sudo apt install binutils bsdmainutils bzip2 lib32gcc-s1 lib32stdc++6 libsdl2-2.0-0:i386 openjdk-21-jre pigz rng-tools5 steamcmd unzip
```

##Usage

Update the config.json file to apply to your system.

To run the main script:

```bash
python3 ~/APA-Server-Core/Server-Core/zomboid_core.py
```

Available Commands from the console:

```bash
#<required>
#<required|choose one>
#[Optional]
#[Optional|Choose|one]

#Installs lgsm, rcon, and systemctl files. Optionally you can install each piece individually.
zomboid_core.py install [lgsm|sysd|rcon]
#Initiates a 15 minute reboot with a full backup.
zomboid_core.py backup
#Initiates a 15 minute reboot or stop, optional message.
zomboid_core.py restart [optional-message]
#Chunk tools, restore defaults to daily backup.
zomboid_core.py chunk <remove|restore>  <chunk|range> <###_###|x1,y1,x2,y2> [daily|recent]
#Parses a .txt file formated with each steamid per line.
zomboid_core.py banparse <file>
```