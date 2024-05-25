import argparse
from time import sleep
import tools.linux_installer as li

def CmdLineArgs():
    parser = argparse.ArgumentParser(prog="zomboid_core.py", description=
        "Basic tools available from the command line. More functionaliy \
            available in discord")
    subparsers = parser.add_subparsers(dest="command")
    parser_install = subparsers.add_parser("install", help="Deploys lgsm \
        , sysd files, and rcon. Follow install with --install-target \
            [service] to deploy a service individually.")
    parser_install.add_argument("--install_target", choices=["lgsm", 
        "sysd", "rcon"], default=None, dest="target", help="You can choose \
            one of these to deploy individually.")
    parser_backup = subparsers.add_parser("backup")
    parser_restart = subparsers.add_parser("restart")
    parser_restart.add_argument("--message")
    parser_chunk = subparsers.add_parser("chunk")
    parser_ban = subparsers.add_parser("banparse")

    return parser.parse_args()

def main():
    args = CmdLineArgs()

    match args.command:
        case "install":
            Installer(args.target)
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

def Installer(service):
    print("Hello, and welcome to the A Path Above computer aided \
        lgsm + Utility installer.")
    sleep(1)
    if service:
        print(f"You've chosen to install the specific module: \
            {service}")

    match service:
        case "lgsm":
            print("Installing lgsm, this will take a moment.")
            li.DeployLgsm()
            print("lgsm install complete")
        case "sysd":
            print("sysd")
            li.DeploySysdFiles()
        case "rcon":
            print("Download rcon")
        case _:
            print("Installing all modules now.")
            li.DeployLgsm()
            print("lgsm install complete")
            sleep(10)
            print("Deploying systemd files")
            li.DeploySysdFiles()
            print("sysd files deployed and activated")
            sleep(10)
            print("Installing rcon.")

if __name__ == '__main__':
    main()