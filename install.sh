#!/bin/bash

# Warna untuk output
GREEN="\033[0;32m"
RED="\033[0;31m"
RESET="\033[0m"

echo -e "${GREEN}=== Installer for S1C0N ===${RESET}"

# Update dan upgrade sistem
echo -e "${GREEN}[+] Updating system...${RESET}"
sudo apt update || { echo -e "${RED}[-] Failed to update system${RESET}"; exit 1; }

# Fungsi untuk mengecek apakah sebuah perintah tersedia
command_exists() {
    command -v "$1" &> /dev/null
}

# Install Nmap
if command_exists nmap; then
    echo -e "${GREEN}[✓] Nmap is already installed${RESET}"
else
    echo -e "${GREEN}[+] Installing Nmap...${RESET}"
    sudo apt install -y nmap || { echo -e "${RED}[-] Failed to install Nmap${RESET}"; exit 1; }
fi

# Install wafw00f
if command_exists wafw00f; then
    echo -e "${GREEN}[✓] wafw00f is already installed${RESET}"
else
    echo -e "${GREEN}[+] Installing wafw00f...${RESET}"
    sudo apt install -y wafw00f || { echo -e "${RED}[-] Failed to install wafw00f${RESET}"; exit 1; }
fi

# Install Sublist3r
if command_exists sublist3r; then
    echo -e "${GREEN}[✓] Sublist3r is already installed${RESET}"
else
    echo -e "${GREEN}[+] Installing Sublist3r...${RESET}"
    sudo apt install -y git python3 python3-pip
    git clone https://github.com/aboul3la/Sublist3r.git || { echo -e "${RED}[-] Failed to clone Sublist3r${RESET}"; exit 1; }
    cd Sublist3r || exit
    pip3 install -r requirements.txt || { echo -e "${RED}[-] Failed to install Sublist3r dependencies${RESET}"; exit 1; }
    sudo cp sublist3r.py /usr/local/bin/sublist3r && sudo chmod +x /usr/local/bin/sublist3r
    cd ..
fi

# Install Subfinder using GoLang
if command_exists subfinder; then
    echo -e "${GREEN}[✓] Subfinder is already installed${RESET}"
else
    echo -e "${GREEN}[+] Installing Subfinder using GoLang...${RESET}"
    sudo apt install -y golang-go || { echo -e "${RED}[-] Failed to install GoLang${RESET}"; exit 1; }
    go install github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest || { echo -e "${RED}[-] Failed to install Subfinder with GoLang${RESET}"; exit 1; }
    sudo cp ~/go/bin/subfinder /usr/local/bin/ && sudo chmod +x /usr/local/bin/subfinder
fi

# Install Assetfinder
if command_exists assetfinder; then
    echo -e "${GREEN}[✓] Assetfinder is already installed${RESET}"
else
    echo -e "${GREEN}[+] Installing Assetfinder...${RESET}"
    curl -Lo assetfinder https://github.com/tomnomnom/assetfinder/releases/latest/download/assetfinder-linux-amd64 || { echo -e "${RED}[-] Failed to download Assetfinder${RESET}"; exit 1; }
    sudo mv assetfinder /usr/local/bin/ && sudo chmod +x /usr/local/bin/assetfinder
fi

# Install Dirsearch
if [ -d "dirsearch" ]; then
    echo -e "${GREEN}[✓] Dirsearch is already installed${RESET}"
else
    echo -e "${GREEN}[+] Installing Dirsearch...${RESET}"
    git clone https://github.com/maurosoria/dirsearch.git || { echo -e "${RED}[-] Failed to clone Dirsearch${RESET}"; exit 1; }
    sudo ln -s "$(pwd)/dirsearch/dirsearch.py" /usr/local/bin/dirsearch
fi

# Install Httprobe
if command_exists httprobe; then
    echo -e "${GREEN}[✓] Httprobe is already installed${RESET}"
else
    echo -e "${GREEN}[+] Installing Httprobe...${RESET}"
    sudo apt install -y golang-go || { echo -e "${RED}[-] Failed to install GoLang${RESET}"; exit 1; }
    go install github.com/tomnomnom/httprobe@latest
    sudo cp ~/go/bin/httprobe /usr/local/bin/ || { echo -e "${RED}[-] Failed to copy httprobe${RESET}"; exit 1; }
fi
# Install PyQt5
if python3 -c "import PyQt5" &> /dev/null; then
    echo -e "${GREEN}[✓] PyQt5 is already installed${RESET}"
else
    echo -e "${GREEN}[+] Installing PyQt5...${RESET}"
    pip3 install PyQt5 || { echo -e "${RED}[-] Failed to install PyQt5${RESET}"; exit 1; }
fi

# Install requests
if python3 -c "import requests" &> /dev/null; then
    echo -e "${GREEN}[✓] requests is already installed${RESET}"
else
    echo -e "${GREEN}[+] Installing requests...${RESET}"
    pip3 install requests || { echo -e "${RED}[-] Failed to install requests${RESET}"; exit 1; }
fi

# Install python-nmap
if python3 -c "import nmap" &> /dev/null; then
    echo -e "${GREEN}[✓] python-nmap is already installed${RESET}"
else
    echo -e "${GREEN}[+] Installing python-nmap...${RESET}"
    pip3 install python-nmap || { echo -e "${RED}[-] Failed to install python-nmap${RESET}"; exit 1; }
fi

# Install builtwith
if python3 -c "import builtwith" &> /dev/null; then
    echo -e "${GREEN}[✓] builtwith is already installed${RESET}"
else
    echo -e "${GREEN}[+] Installing builtwith...${RESET}"
    pip3 install builtwith || { echo -e "${RED}[-] Failed to install builtwith${RESET}"; exit 1; }
fi
# Selesai
echo -e "${GREEN}[+] Installation completed successfully!${RESET}"
echo -e "${GREEN}Tools Installed:${RESET}"
echo " - Nmap"
echo " - wafw00f"
echo " - Sublist3r"
echo " - Subfinder"
echo " - Assetfinder"
echo " - Dirsearch"
echo " - Httprobe"
