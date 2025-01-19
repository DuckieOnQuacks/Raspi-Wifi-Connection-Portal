import json
import os
import re
import subprocess
import sys

from setup.cli import query_yes_no
from setup.colorConsole import ColorPrint, cyan, magenta, green


def print_header():
    header = """
    ###################################################
    #########       Raspi Captive Portal      #########
    #########   A Raspberry Pi Access Point   #########
    #########  & Captive Portal setup script  #########
    ###################################################
    """
    ColorPrint.print(green, header)


def check_super_user():
    print()
    ColorPrint.print(green, "▶ Check sudo")

    # Is root?
    if os.geteuid() != 0:
        print("You need root privileges to run this script.")
        print('Please try again using "sudo"')
        sys.exit(1)
    else:
        print("Running as root user, continue.")


def install_apt_dependencies():
    """Install system dependencies using apt"""
    ColorPrint.print(cyan, "Installing system dependencies using apt...")
    subprocess.call("sudo apt update", shell=True)
    subprocess.call("sudo apt install -y python3 python3-pip python3-venv", shell=True)


def setup_virtual_env():
    """Create and activate a Python virtual environment in the server directory"""
    ColorPrint.print(cyan, "Creating a Python virtual environment...")

    server_dir = os.path.abspath("server")
    venv_dir = os.path.join(server_dir, "venv")

    if not os.path.exists(venv_dir):
        subprocess.run(f"python3 -m venv {venv_dir}", shell=True, check=True)
        ColorPrint.print(cyan), f"Virtual environment created at {venv_dir}")
    else:
        ColorPrint.print(cyan, "Virtual environment already exists, skipping creation.")


def install_python_dependencies():
    """Install Python dependencies inside the virtual environment"""
    ColorPrint.print(cyan, "Installing Python dependencies using pip in virtual environment...")

    server_dir = os.path.abspath("server")
    venv_bin = os.path.join(server_dir, "venv/bin")

    pip_path = os.path.join(venv_bin, "pip")

    subprocess.run(f"{pip_path} install --upgrade pip", shell=True, check=True)
    subprocess.run(f"{pip_path} install -r {server_dir}/requirements.txt", shell=True, check=True)


def setup_access_point():
    print()
    ColorPrint.print(green, "▶ Setup Access Point (WiFi)")

    print("We will now set up the Raspi as Access Point to connect to via WiFi.")
    print("The following commands will execute as sudo user.")
    answer = query_yes_no("Continue?", default="yes")

    if not answer:
        return sys.exit(0)

    subprocess.run("sudo chmod a+x ./access-point/setup-access-point.sh", shell=True, check=True)
    subprocess.run("./setup-access-point.sh", shell=True, cwd="./access-point", check=True)


def setup_server_service():
    print()
    ColorPrint.print(green, "▶ Configure Flask server to start at boot")

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
    ColorPrint.print(green, "▶ Done")

    final_msg = (
        "Awesome, we are done here. Grab your phone and look for the\n"
        'Scoredboard\' WiFi (password: "raspberrypi").'
        "\n"
        "When you reboot the Raspi, wait 2 minutes, then the WiFi network\n"
        "and the server should be up and running again automatically.\n"
        "\n"
    )
    ColorPrint.print(green, final_msg)


def execute_all():

    print_header()
    check_super_user()
    install_apt_dependencies()
    setup_virtual_env()
    install_python_dependencies()

    setup_access_point()
    setup_server_service()

    done()


if __name__ == "__main__":
    execute_all()
