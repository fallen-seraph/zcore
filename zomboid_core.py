import configs.arguments as arguments
import install.linux_installer as installer
import tools.tools_backup as tools_backup
import tools.tools_restart as restart
import tools.tools_chunks as chunks
import time

def main():
    args = arguments.CMD_line_args()

    match args.command:
        case "install":
            install_mode(args.target)
        case "backup": 
            tools_backup.backup_handler()
        case "restart":
            restart.restart_handler(args.message, args.delay, args.backup, args.stop)
        case "chunk":
            if args.range:
                print(args.chunk_one, args.chunk_two)
                print(args.file_name)
            else:
                print(args.file)
        case "ban":
            print(args.file)
        case _:
            print("temp")

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
            installer.deploy_lgsm()
            print("lgsm install complete")
        case "sysd":
            installer.deploy_sysd()
        case "misc":
            installer.misc_tasks()
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