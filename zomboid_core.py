from utils import arguments
from tools import backup, ban, chunks, restart
from install import linux_installer
from tools.skimmers import debug_skimmer

import time

def main():
    args = arguments.CMD_line_args()

    match args.command:
        case "install":
            install_mode(args.target)
        case "backup": 
            backup.backup_handler()
        case "restart":
            if args.scheduled:
                restart.restart_schedular()
            elif args.cancel:
                restart.cancel_restart()
            elif args.instant:
                restart.instant_restart()
            else:
                restart.restart_handler(args.message, args.delay, args.backup,
                    args.stop)
        case "chunk":
            if not args.range:
                chunks.chunks_by_file(args.file)
            else:
                chunks.chunks_by_range(args.chunk_one, args.chunk_two,
                    args.file_name)
        case "ban":
            ban.console_ban_handler(args.file)
        case _:
            if args.skimmer:
                debug_skimmer.monitor_directory()
            elif args.report:
                print("report")
            else:
                print("empty")

def install_mode(service):
    print("Hello, and welcome to the A Path Above computer aided "
        "lgsm + Utility installer.")
    time.sleep(1)
    if service:
        print("You've chosen to install the specific module: "
            f"{service}")

    match service:
        case "lgsm":
            print("Installing lgsm, this will take a moment.")
            linux_installer.deploy_lgsm()
            print("lgsm install complete")
        case "sysd":
            linux_installer.deploy_sysd()
        case "misc":
            linux_installer.misc_tasks()
        case _:
            print("Installing all modules now.")
            linux_installer.deploy_lgsm()
            print("lgsm install complete")
            time.sleep(10)
            print("Deploying systemd files")
            linux_installer.deploy_sysd()
            print("sysd files deployed and activated")
            time.sleep(10)
            print("finalizing tasks")
            linux_installer.misc_tasks()
            print("install complete")

if __name__ == '__main__':
    main()