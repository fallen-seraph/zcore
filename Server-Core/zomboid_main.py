from sys import argv
#import tools_main

def help():
    print("install", "Installs lgsm, rcon, and systemctl files.")
    print("backup", "Initiates a 15 minute reboot with a full backup.")
    print("restart <optional-message>", "Initiates a 15 minute reboot or stop, optional message.")
    print("chunk <remove|restore>  <chunk|range> <###_###|x1,y1,x2,y2 <daily|recent>", "Chunk tools, restore defaults to daily backup.")
    print("banparse <file>", "Parses a .txt file formated with each steamid per line.")

def main():
    match argv[1]:
        case "install":
            print("install code")
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

if __name__ == '__main__':
    main()