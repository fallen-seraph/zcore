import argparse
from time import sleep
from discord.external.linux_files import linux_files

def cmd_line_args():
    parser = argparse.ArgumentParser(prog="zomboid_core.py", description="Basic tools available from the command line.")
    subparsers = parser.add_subparsers(dest="command")
    parser_install = subparsers.add_parser("install")
    parser_install.add_argument("--install_target", choices=["lgsm", "sysd", "rcon"], default=None, dest="target")
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
            installer(args.target)
        case "backup": 
            print("backup code")
        case "restart":
            print("restart code")
        case "chunk":
            print("chunk code")
        case "banparse":
            print("banparse code")
        case _:
            print("temp")

def installer(service):
    print("Hello, and welcome to the A Path Above computer aided lgsm + Utility installer.")
    sleep(5)
    if service:
        print(f"You've chosen to install the specific module: {service}")
    match service:
        case "lgsm":
            print("Installing lgsm")
            linux_files.create_lgsm_folder()
            linux_files.create_linuxgsm()
            linux_files.download_pzserver()
            print("lgsm install complete")
        case "sysd":
            print("sysd")
            #linux_files.create_sysd_folders()
            #linux_files.deploy_sysd_files()
        case "rcon":
            print("Download rcon")
        case _:
            print("Installing all modules now.")
            linux_files.create_lgsm_folder()
            linux_files.create_linuxgsm()
            linux_files.download_pzserver()
            print("lgsm install complete")
            sleep(10)
            print("Deploying systemd files")
            linux_files.create_sysd_folders()
            linux_files.deploy_sysd_files()
            print("sysd files deployed and activated")
            sleep(10)
            print("Installing rcon.")

if __name__ == '__main__':
    main()