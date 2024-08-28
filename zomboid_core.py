import time
from utils import arguments
from install import linux_installer
from tools import (
    ban,
    backup,
    chunks,
    report,
    restart,
    scheduler,
    utilities,
    linux_services
)

from tools.skimmers import skimmer_main

def main():
    args = arguments.CMD_line_args()

    match args.command:
        case "install":
            install_mode(args.target)
        case "backup": 
            backup.backup_handler(args.backupForce)
        case "restart":
            if args.scheduled:
                scheduler.restart_scheduler()
            elif args.cancel:
                utilities.cancel_pending_restart(args.cancel)
            elif args.instant:
                linux_services.core_service("restart")
            else:
                restart.restart_server_with_messages(
                    args.message,
                    args.delay,
                    args.backup,
                    args.stop
                )
        case "chunk":
            active = linux_services.get_service_status(
                "zomboid_core.service")[1]
            
            if active != "active" or args.force:                
                if not args.range:
                    chunks.delete_chunks_from_file(args.file)
                elif args.file_name:
                    chunks.create_chunk_list_file(
                        args.chunk_one,
                        args.chunk_two,
                        args.file_name
                    )
                else:
                    chunks.delete_chunks_from_given_range(
                        args.chunk_one,
                        args.chunk_two
                    )
            else:
                print("Warning: Deleting Files - Shutdown server or force "
                    "with --force.")
        case "ban":
            ban.console_ban_handler(args.file)
        case _:
            if args.skimmer:
                skimmer_main.monitor_logs()
            elif args.report:
                report.crash_report()
            else:
                print("empty")

def install_mode(service):
    print("Hello, and welcome to the A Path Above computer aided "
        "lgsm + Utility installer.")
    time.sleep(1)
    if service:
        print("You've chosen to install the specific module: "
            f"{service}")
    linuxInstaller = linux_installer.Installer()
    match service:
        case "lgsm":
            print("Installing lgsm, this will take a moment.")
            linuxInstaller.deploy_lgsm()
            print("lgsm install complete")
        case "sysd":
            linuxInstaller.deploy_sysd()
        case "misc":
            linuxInstaller.misc_tasks()
        case _:
            print("Installing all modules now.")
            linuxInstaller.deploy_lgsm()
            print("lgsm install complete")
            time.sleep(10)
            print("Deploying systemd files")
            linuxInstaller.deploy_sysd()
            print("sysd files deployed and activated")
            time.sleep(10)
            print("finalizing tasks")
            linuxInstaller.misc_tasks()
            print("install complete")

if __name__ == '__main__':
    main()