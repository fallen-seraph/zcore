from sys import argv
from time import sleep
from discord.external.linux_files import linux_files

def help():
    print("install <lgsm|sysd|rcon>", "Installs lgsm, rcon, and systemctl files. Optionally you can install each piece individually.")
    print("backup", "Initiates a 15 minute reboot with a full backup.")
    print("restart <optional-message>", "Initiates a 15 minute reboot or stop, optional message.")
    print("chunk <remove|restore>  <chunk|range> <###_###|x1,y1,x2,y2 <daily|recent>", "Chunk tools, restore defaults to daily backup.")
    print("banparse <file>", "Parses a .txt file formated with each steamid per line.")

def main():
    match argv[1]:
        case "install":
            if argv[2]:
                installer(argv[2])
            else:
                print("Hello, and welcome to the A Path Above computer aided lgsm + Utility installer.")
                sleep(5)
                print("Now beginning the lgsm install. Be prepared to answer questions as needed.")
                installer("lgsm")
                print("Thank you, lgsm install complete")
                sleep(5)
                print("deploying systemd files")
                installer("sysd")
                sleep(5)
                print("Installing rcon.")
                installer("rcon")
        case "backup": 
            print("backup code")
        case "restart":
            print("restart code")
        case "chunk":
            print("chunk code")
        case "banparse":
            print("banparse code")
        case "?" | "-?" | "--help":
            help()
        case _:
            print("Unrecognized Switch.")
            help()

def installer(service):
    match service:
        case "lgsm":
            linux_files.create_lgsm_folder()
            linux_files.create_linuxgsm()
            linux_files.download_pzserver()
        case "sysd":
            linux_files.create_sysd_folders()
            linux_files.deploy_sysd_files()
        case "rcon":
            print("Download rcon")

if __name__ == '__main__':
    main()