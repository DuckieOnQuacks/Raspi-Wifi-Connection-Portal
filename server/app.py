from flask import Flask, request, jsonify, redirect, render_template
import os
import subprocess

############################## Setup ###########################################

HOST_NAME = "scoreboard.portal"
FRONTEND_FOLDER = "./templates"

app = Flask(__name__, static_folder=FRONTEND_FOLDER)

@app.route("/")
def serve_frontend():
    return render_template("index.html")

############################# Middleware #######################################

@app.before_request
def redirect_to_hostname():
    print(f"Received request for {request.path} from {request.host}")
    if request.host.split(":")[0] != HOST_NAME:
        print(f"Redirecting to http://{HOST_NAME}")
        return redirect(f"http://{HOST_NAME}")
    return None

############################## Endpoints #######################################

@app.route("/hotspot-detect.html")
def hotspot_detect():
    print("Received request for /hotspot-detect.html")
    return render_template("index.html")  # Serve your captive portal page

@app.route("/ncsi.txt")
def ncsi_txt():
    print("Received request for /ncsi.txt")
    return "Microsoft NCSI", 200

@app.route("/generate_204")
def generate_204():
    print("Received request for /generate_204")
    return "", 204

@app.route("/connecttest.txt")
def connect_test():
    return "", 200  # Return an empty response with 200 OK

@app.route("/ipv6check")
def ipv6_check():
    return "", 200  # Return an empty response

@app.route("/204")
def no_content():
    return "", 204  # Return 204 No Content to signal no captive portal

@app.route("/connect", methods=["POST"])
def connect_network():
    data = request.get_json()
    ssid = data.get("ssid")
    password = data.get("password")

    if not ssid or not password:
        return jsonify({"message": "SSID and password are required"}), 400

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

        return jsonify({"message": "Network configuration applied successfully."}), 200
    except PermissionError:
        print("Permission denied. Requires root privileges.")
        return jsonify({"message": "Permission denied. Requires root privileges."}), 403
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"message": "Failed to apply network configuration."}), 500

############################# Server Listening #################################
if __name__ == "__main__":
    PORT = 3000
    print(f"⚡ Raspberry Pi Server listening on port {PORT}")
    app.run(host="0.0.0.0", port=PORT, use_reloader=False)
