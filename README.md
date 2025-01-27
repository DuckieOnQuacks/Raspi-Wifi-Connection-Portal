# 📡 Raspi WiFi Connection Portal  

🚧 **This project is still in development! This project is part of a larger project that im currently working on.** 🚧  

A **Raspberry Pi WiFi Connection Portal** that allows users to connect to a Raspberry Pi device and configure WiFi settings through a simple web interface. This project is ideal for **headless Raspberry Pi setups**, making it easy to switch networks without manually editing configuration files.  

---

## ✨ Features (Planned & Implemented)  

✅ **WiFi Hotspot Mode** – The Raspberry Pi acts as an access point for initial setup.  
✅ **Web-Based Configuration** – Users can connect to a local web portal to configure WiFi settings.  
✅ **Automatic Network Switching** – Saves credentials and connects to known networks automatically.  
✅ **Minimal Dependencies** – Designed to be lightweight and efficient.  
✅ **Headless-Friendly** – No need for keyboard or monitor access.  
🚀 **Future Enhancements** – Better UI, multi-network support, improved security features.  

---

## 🛠️ Getting Started  

### 📋 Prerequisites  

Ensure you have the following before proceeding:  

- A **Raspberry Pi** (any model with WiFi support)  
- A **fresh Raspberry Pi OS installation** (Lite recommended for headless use)  
- Internet connection for initial setup  
- SSH access enabled (optional, but recommended)  

### 📦 Installation  

1. **Clone the repository:**  
   ```sh
   git clone https://github.com/DuckieOnQuacks/Raspi-Wifi-Connection-Portal.git
   cd Raspi-Wifi-Connection-Portal
   ```

2. **Run the setup script:**  
   ```sh
   chmod +x setup.sh
   ./setup.sh
   ```

3. **Reboot the Raspberry Pi:**  
   ```sh
   sudo reboot
   ```

4. **Connect to the WiFi portal:**  
   - After rebooting, your Raspberry Pi should broadcast a WiFi network (e.g., `Raspi-Setup`).  
   - Connect to this network and navigate to `http://192.168.4.1` in your web browser.  
   - Configure and save your WiFi settings.  

---

## 🚀 Usage  

1. **Initial Setup**  
   - Power on the Raspberry Pi and wait for the WiFi setup network to appear.  
   - Connect to the setup network from your phone or computer.  

2. **Accessing the Portal**  
   - Open a web browser and go to `http://192.168.4.1`.  
   - Enter your WiFi details and save changes.  

3. **Switching Networks**  
   - If the Raspberry Pi is moved to a new location, repeat the setup process to update WiFi credentials.  

---

## 📜 License  

This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for details.  

---
