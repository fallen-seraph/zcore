import argparse

def install_commands(subparsers):
    parser_install = subparsers.add_parser("install", help="Deploys lgsm, "
        "and sysd files. Follow install with --install-target "
        "[service] to deploy a service individually.")
    parser_install.add_argument("-it", "--install_target", choices=["lgsm", 
        "sysd", "misc"], default=None, dest="target",
        help="install a service individually")
    
def restart_commands(subparsers):
    parser_restart = subparsers.add_parser("restart", help="Initiates a "
        "server restart. Default message and timing.")
    
    exclusive_group = parser_restart.add_mutually_exclusive_group()
    exclusive_group.add_argument("-i", "--instant", default=None,
        action="store_true", help="Instantly restarts the server. "
        "USE CAREFULLY!")
    exclusive_group.add_argument("-c", "--cancel", default=None,
        action="store_true", help="Cancels a timed reboot.")
    exclusive_group.add_argument("-sc", "--scheduled", default=None,
        action="store_true", help="Initiates the scheduled reboots.")
    
    normal_restart_group = parser_restart.add_argument_group("Custom Restart",
        "Options ignored if -c or -i are used.")
    normal_restart_group.add_argument("-m", "--message", default=None,
        dest="message", help="Provided message to make a part of restart "
        "message.")
    normal_restart_group.add_argument("-d", "--delay", default=None,
        dest="delay", type=int, help="Delay before restart, will be rounded "
        "up to the nearest interval of 5.")
    normal_restart_group.add_argument("-b", "--backup", default=None,
        dest="backup", action="store_true", help="Will trigger a backup "
        "with the restart.")
    normal_restart_group.add_argument("-s", "--stop", default=None,
        action="store_true", help="Stops the server instead "
        "of starting it after restart.")
    
def chunk_commands(subparsers):
    parser_chunk = subparsers.add_parser("chunk", help="Removes map.bin "
        "files from a given file or generated list from given chunk "
        "coordinates.")
    parser_chunk.add_argument("-f", "--file", default=None, dest="file",
        type=argparse.FileType('r'), help="File with a list of chunk "
        "coordinates.")
    
    range = parser_chunk.add_subparsers(dest="range")
    range_sub_commands = range.add_parser("range")
    range_sub_commands.add_argument("chunk_one", metavar="X_Y", type=str,
        help="X_Y of first chunk")
    range_sub_commands.add_argument("chunk_two", metavar="X_Y", type=str,
        help="X_Y of second chunk")
    range_sub_commands.add_argument("-fn", "--file_name", default=None,
        type=str, help="name of the file this will generate.")

def CMD_line_args():
    parser = argparse.ArgumentParser(prog="zomboid_core.py", description=
        "Basic tools available from the command line. More functionaliy "
        "available in discord")
    
    parser.add_argument("--skimmer", dest="skimmer", action="store_true", help=argparse.SUPPRESS)
    parser.add_argument("--report", dest="report", action="store_true", help=argparse.SUPPRESS)
    
    subparsers = parser.add_subparsers(dest="command")

    install_commands(subparsers)
    
    subparsers.add_parser("backup", help="Runs a rsync backup, "
        "compresses it, deletes the configured oldest backup.")
    
    restart_commands(subparsers)

    chunk_commands(subparsers)

    parser_ban = subparsers.add_parser("ban", help="Takes a file with a "
        "list of steamids to be banned.")
    parser_ban.add_argument("-f", "--file", required=True, 
        type=argparse.FileType('r'), help="File with a list of chunk "
        "coordinates.")
    
    return parser.parse_args()