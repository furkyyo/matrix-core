#!/bin/bash

# Renkler
GREEN='\033[0;32m'
CYAN='\033[0;36m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${CYAN}--- MATRIX_CORE AUTOMATED INSTALLER ---${NC}"

# 1. Bağımlılıkları kontrol et ve kur
echo "Checking Python dependencies (psutil, rich, pyinstaller)..."
pip3 install psutil rich pyinstaller > /dev/null 2>&1

# 2. PyInstaller ile derleme (Build) işlemini başlat
echo -e "${CYAN}Building Matrix_Core for your system architecture...${NC}"
python3 -m PyInstaller --onefile main.py > /dev/null 2>&1

# 3. Derleme başarılıysa sisteme kopyala
if [ -f "dist/main" ]; then
    echo -e "System authorization required for global installation..."
    sudo cp dist/main /usr/local/bin/matrix
    sudo chmod +x /usr/local/bin/matrix
    
    echo -e "${GREEN}SUCCESS: 'matrix' command is now available globally!${NC}"
    echo -e "Usage: type 'matrix', 'matrix green', or 'matrix purple' in your terminal."
else
    echo -e "${RED}ERROR: Build failed. Please ensure PyInstaller is working correctly.${NC}"
    exit 1
fi