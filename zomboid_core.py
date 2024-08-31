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

from skimmers import skimmer_main

parser = arguments.CMD_line_args()
args = parser.parse_args()

active = linux_services.get_service_status(
    "zomboid_core.service")[1]

def main():
    try:
        match args.command:
            case "install":
                install_mode(args.target)
            case "backup": 
                parse_backup_arguments()
            case "restart":
                parse_restart_arguments()
            case "chunk":
                parse_chunk_arguments()
            case "ban":
                ban.console_ban_handler(args.file)
            case _:
                parse_misc_or_no_arguments()
    except (KeyboardInterrupt, SystemExit):
        print("Cancelling")

def install_mode(service):
    print("Starting install mode")
    time.sleep(1)
    if service:
        print(f"installing {service} service")
    linuxInstaller = linux_installer.Installer()
    linuxInstallerFunctions = [
        linuxInstaller.deploy_lgsm,
        linuxInstaller.deploy_sysd,
        linuxInstaller.misc_tasks
    ]
    match service:
        case "lgsm":
            print("Installing lgsm, this will take a moment.")
            linuxInstallerFunctions[0]()
            print("lgsm install complete")
        case "sysd":
            linuxInstallerFunctions[1]()
        case "misc":
            linuxInstallerFunctions[2]()
        case _:
            print("Installing all modules now.")
            for installer in linuxInstallerFunctions:
                installer()

def parse_backup_arguments():
    if active != "active" or args.backupForce:
        thread = backup.backup_handler()
        if thread:
            thread.join()
    else:
        print("Server is online. Shutdown before backing up or force backup")

def parse_restart_arguments():
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

def parse_chunk_arguments():
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
        
def parse_misc_or_no_arguments():
    if args.skimmer:
        skimmer_main.monitor_logs()
    elif args.report:
        report.crash_report()
    else:
        parser.print_help()

if __name__ == '__main__':
    main()