from subprocess import run, PIPE, CalledProcessError

def systemctl_interface(task, service):
    try:
        result = run(["systemctl", "--user", task, service], stdout=PIPE
                    , check=True, text=True, shell=False
                    , capture_output=True)
        return result.output
    except CalledProcessError as e:
        print(f"An error occured: {e}.")
        print(f"Further information: {result.error}")