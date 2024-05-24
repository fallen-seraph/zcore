import argparse
from time import sleep
from discord.external.linux_files import linux_files

def cmd_line_args():
    parser = argparse.ArgumentParser(prog="zomboid_core.py", description="Basic tools available from the command line.")
    subparsers = parser.add_subparsers(dest="command")
    parser_install = subparsers.add_parser("install")
    parser_install.add_argument("--install_target", choices=["lgsm", "sysd", "rcon"], default=None)
    parser_backup = subparsers.add_parser("backup")
    parser_restart = subparsers.add_parser("restart")
    parser_restart.add_argument("--message")
    parser_chunk = subparsers.add_parser("chunk")
    parser_ban = subparsers.add_parser("banparse")

    return parser.parse_args()

def main():
    args = cmd_line_args()

    match args.command:
        case "install":
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
            print("lgsm")
            #linux_files.create_lgsm_folder()
            #linux_files.create_linuxgsm()
            #linux_files.download_pzserver()
        case "sysd":
            print("sysd")
            #linux_files.create_sysd_folders()
            #linux_files.deploy_sysd_files()
        case "rcon":
            print("Download rcon")

if __name__ == '__main__':
    main()