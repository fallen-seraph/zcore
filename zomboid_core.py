import install.linux_installer as installer
import tools.backup as backup
import argparse
import time

def CmdLineArgs():
    parser = argparse.ArgumentParser(prog="zomboid_core.py", description=
        "Basic tools available from the command line. More functionaliy \
            available in discord")
    subparsers = parser.add_subparsers(dest="command")
    parser_install = subparsers.add_parser("install", help="Deploys lgsm \
        , sysd files, and rcon. Follow install with --install-target \
            [service] to deploy a service individually.")
    parser_install.add_argument("--install_target", choices=["lgsm", 
        "sysd"], default=None, dest="target", help="You can choose \
            one of these to deploy individually.")
    subparsers.add_parser("backup", description="Runs a rsync backup, \
        compresses it, deletes the configured oldest backup.")
    parser_restart = subparsers.add_parser("timedRestart")
    parser_restart.add_argument("--message", default=None, dest="target",
        help="You can choose one of these to deploy individually.")
    parser_chunk = subparsers.add_parser("chunk")
    parser_ban = subparsers.add_parser("banparse")

    return parser.parse_args()

def main():
    args = CmdLineArgs()

    match args.command:
        case "install":
            InstallMode(args.target)
        case "backup": 
            backup.main()
        case "restart":
            print("restart code")
        case "chunk":
            print("chunk code")
        case "banparse":
            print("banparse code")
        case _:
            print("temp")

def InstallMode(service):
    print("Hello, and welcome to the A Path Above computer aided \
        lgsm + Utility installer.")
    time.sleep(1)
    if service:
        print(f"You've chosen to install the specific module: \
            {service}")

    match service:
        case "lgsm":
            print("Installing lgsm, this will take a moment.")
            installer.deploy_lgsm()
            print("lgsm install complete")
        case "sysd":
            print("sysd")
            installer.deploy_sysd()
        case _:
            print("Installing all modules now.")
            installer.deploy_lgsm()
            print("lgsm install complete")
            time.sleep(10)
            print("Deploying systemd files")
            installer.deploy_sysd()
            print("sysd files deployed and activated")
            time.sleep(10)
            print("finalizing tasks")
            installer.misc_tasks()
            print("install complete")

if __name__ == '__main__':
    main()