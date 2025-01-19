from flask import Flask, request, jsonify, redirect, send_from_directory
import os
import subprocess

############################## Setup ###########################################

HOST_NAME = 'scoreboard.portal'
FRONTEND_FOLDER = "./templates"

app = Flask(__name__, static_folder=FRONTEND_FOLDER)

############################# Middleware #######################################

#@app.before_request
def redirect_to_hostname():
    if request.host.split(':')[0] != HOST_NAME:
        return redirect(f"http://{HOST_NAME}")
#
############################## Endpoints #######################################

@app.route("/")
def serve_frontend():
    return send_from_directory(FRONTEND_FOLDER, 'index.html')

@app.route("/api/connect", methods=["POST"])
def connect_network():
    data = request.get_json()
    ssid = data.get("ssid")
    password = data.get("password")

    if not ssid or not password:
        return jsonify({"message": "SSID and password are required"})

    print(f"Received network configuration: {ssid}, {password}")

    # Construct the network config block
    network_config = f"""
    network={{
        ssid="{ssid}"
        psk="{password}"
    }}
    """

    # Append network config to wpa_supplicant.conf
    try:
        with open("/etc/wpa_supplicant/wpa_supplicant.conf", "a") as file:
            file.write(network_config)
        print("Successfully wrote to wpa_supplicant.conf")

        subprocess.run(["sudo", "systemctl", "restart", "dhcpcd"], check=True)
        print("Successfully restarted network service.")
        
        return jsonify({"message": "Network configuration applied successfully."})
    except PermissionError:
        return jsonify({"message": "Permission denied. Requires root privileges."})
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"message": "Failed to apply network configuration."})

############################# Server Listening #################################

if __name__ == "__main__":
    PORT = 3000
    print(f"⚡ Raspberry Pi Server listening on port {PORT}")
    app.run(host="0.0.0.0", port=PORT, use_reloader=False)
