#!/bin/bash
RED='\033[0;31m'
NC='\033[0m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
Dir=Kexts/
missingFiles='Missing:'

# Check Essential Kexts
# FakeSMC/VirtualSMC
echo -e "${CYAN}Checking Drivers${NC}"
if [ -d "${Dir}VirtualSMC.kext" ] || [ -f "${Dir}FakeSMC.kext" ]; then
	echo -e "${PURPLE}VirtualSMC or FakeSMC exists"
	
else
	missingFiles="${missingFiles}\n - VirtualSMC or FakeSMC kext"
fi

# WEG
if [ -d "${Dir}WhateverGreen.kext" ]; then
	echo -e "${PURPLE}WEG exists"
else
	missingFiles="${missingFiles}\n - WEG kext"
fi

# Lilu
if [ -d "${Dir}Lilu.kext" ]; then
	echo -e "${PURPLE}Lilu exists"
else
	missingFiles="${missingFiles}\n - Lilu kext"
fi

# NullCPUPowerManagement
if [ -d "${Dir}NullCPUPowerManagement.kext" ]; then
	echo -e "${PURPLE}NullCPUPowerManagement exists"
else
	missingFiles="${missingFiles}\n - NullCPUPowerManagement kext\n\n\n"
fi


# Check Main Drivers
# ApfsDriverLoader
echo -e "${CYAN}Checking Drivers${NC}"
Dir=Drivers/
if [ -f "${Dir}ApfsDriverLoader.efi" ]; then
	echo -e "${PURPLE}ApfsDriverLoader exists"
else
	missingFiles="${missingFiles}\n - ApfsDriverLoader.efi"
fi

# FwRuntimeServices
if [ -f "${Dir}FwRuntimeServices.efi" ]; then
	echo -e "${PURPLE}FwRuntimeServices exists"
else
	missingFiles="${missingFiles}\n - FwRuntimeServices.efi"
fi

# HFSPlus and VBoxHfs
if [ -f "${Dir}HFSPlus.efi" ] || [ -d "${Dir}VBoxHfs.efi" ]; then
	echo -e "${PURPLE}VBoxHfs or HFSPlus exists"
else
	missingFiles="${missingFiles}\n - VBoxHfs or HFSPlus.efi"
fi

# Config Essentials
FILE=config.plist
if [ -f "$FILE" ]; then
	echo -e "${PURPLE}Config.plist exists${RED}"
	python configCheck.py
else
	missingFiles="${missingFiles}\n - Config.plist"
fi

echo -e "${RED} ${missingFiles} ${NC}"