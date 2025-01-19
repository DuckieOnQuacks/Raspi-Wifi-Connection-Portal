import json
import os
import re
import subprocess
import sys

from setup.cli import query_yes_no
from setup.colorConsole import ColorPrint, cyan, magenta


def print_header():
    header = """
    ###################################################
    #########       Raspi Captive Portal      #########
    #########   A Raspberry Pi Access Point   #########
    #########  & Captive Portal setup script  #########
    ###################################################
    """
    ColorPrint.print(cyan, header)


def check_super_user():
    print()
    ColorPrint.print(cyan, "▶ Check sudo")

    # Is root?
    if os.geteuid() != 0:
        print("You need root privileges to run this script.")
        print('Please try again using "sudo"')
        sys.exit(1)
    else:
        print("Running as root user, continue.")


def install_server_dependencies():
    print()
    ColorPrint.print(cyan, "▶ Install Flask dependencies for backend")

    # Ensure pip dependencies are installed
    subprocess.call("sudo apt install -r requirements.txt", shell=True, cwd="./server")


def setup_access_point():
    print()
    ColorPrint.print(cyan, "▶ Setup Access Point (WiFi)")

    print("We will now set up the Raspi as Access Point to connect to via WiFi.")
    print("The following commands will execute as sudo user.")
    answer = query_yes_no("Continue?", default="yes")

    if not answer:
        return sys.exit(0)

    subprocess.run("sudo chmod a+x ./access-point/setup-access-point.sh", shell=True, check=True)
    subprocess.run("./setup-access-point.sh", shell=True, cwd="./access-point", check=True)


def setup_server_service():
    print()
    ColorPrint.print(cyan, "▶ Configure Flask server to start at boot")

    # Replace path in file
    server_path = os.path.abspath("server")
    server_config_path = "./access-point/access-point-server.service"

    with open(server_config_path, "r", encoding="utf-8") as f:
        filedata = f.read()

    filedata = re.sub(r"WorkingDirectory=.*", f"WorkingDirectory={server_path}", filedata)
    filedata = re.sub(r"ExecStart=.*", f"ExecStart=/usr/bin/python3 {server_path}/app.py", filedata)

    with open(server_config_path, "w", encoding="utf-8") as f:
        f.write(filedata)

    print("We will now register the Flask app as a Linux service and configure")
    print("it to start at boot time.")

    print("The following commands will execute as sudo user.")
    answer = query_yes_no("Continue?", default="yes")

    if not answer:
        return sys.exit(0)

    subprocess.run("sudo chmod a+x ./setup-server.sh", shell=True, cwd="./access-point", check=True)
    subprocess.run("./setup-server.sh", shell=True, cwd="./access-point", check=True)


def done():
    print()
    ColorPrint.print(cyan, "▶ Done")

    final_msg = (
        "Awesome, we are done here. Grab your phone and look for the\n"
        'Scoredboard\' WiFi (password: "raspberrypi").'
        "\n"
        "When you reboot the Raspi, wait 2 minutes, then the WiFi network\n"
        "and the server should be up and running again automatically.\n"
        "\n"
    )
    ColorPrint.print(magenta, final_msg)


def execute_all():
    print_header()
    check_super_user()

    setup_access_point()

    install_server_dependencies()
    setup_server_service()

    done()


if __name__ == "__main__":
    execute_all()
