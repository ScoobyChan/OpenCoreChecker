import os

missing=''
ACPI=False
Add=False
Arr=False
EC=False
Quirks=False
Q=''
B=''
####  APCI  ####
# Add
with open('config.plist') as c:
	line = c.readline()
	while line:
		line = c.readline()
		# Check For SSDT
		if 'ACPI' in line:
			ACPI=True
		if ACPI:
			if 'Add' in line:
				Add=True
		if Add:
			if '<array>' in line:
				Arr=True
			
			if '</array>' in line:
				Arr=False
				ACPI=False
				Add=False

		if Arr:
			if 'SSDT-EC' in line:
				EC=True

if not EC:
	missing+=' - SSDT-EC Catalina May break\n'


# Quirks
with open('config.plist') as c:
	# Quirks
	line = c.readline()
	while line:
		line = c.readline()
		# Check Quirks
		if 'ACPI' in line:
			ACPI=True
		if ACPI:
			if 'Quirks' in line:
				Quirks=True
		if Quirks:
			if '<dict>' in line:
				Arr=True

			if '</dict>' in line:
				Arr=False
				Quirks=False
				ACPI=False
		
		if Arr:
			if 'true/' in line:
				Q += f' - {prelin} needs to be false\n'
			prelin=line


	if not Q == '':
		# print(Q)
		missing+=Q
##############################


####  Booter  ####
B=''
with open('config.plist') as c:
	line = c.readline()
	while line:
		line = c.readline()
		if 'Booter' in line:
			ACPI=True
		if ACPI:
			if 'Quirks' in line:
				Quirks=True
		if Quirks:
			if '<dict>' in line:
				Arr=True

			if '</dict>' in line:
				Arr=False
				Quirks=False
				ACPI=False
		if Arr:
			if 'false/' in line and ('AvoidRuntimeDefrag' in prelin or 'EnableSafeModeSlide'  in prelin or 'EnableWriteUnprotector'  in line or 'ProvideCustomSlide'  in prelin):
				B += f' - {prelin} needs to be false\n'

			if 'true/' in line and ('DisableVariableWrite' in prelin or 'DiscardHibernateMap'  in prelin or 'ForceExitBootServices'  in prelin or 'ProtectCsmRegion'  in prelin or 'ShrinkMemoryMap' in prelin):
				B += f' - {prelin} needs to be true\n'
			
			prelin=line


	if not B == '':
		missing+=B
		


####  Kernel  ####
k=os.listdir('Kexts')
for kext in k:
	Kext=False
	with open('config.plist') as c:
		line = c.readline()
		while line:
			line = c.readline()
			if 'Kernel' in line:
				ACPI=True
			if ACPI:
				if 'Add' in line:
					Quirks=True
			if Quirks:
				if '<array>' in line:
					Arr=True

				if '</array>' in line:
					Arr=False
					Quirks=False
					ACPI=False
			if Arr:
				if f'{kext}' in line:
					Kext=True
			
		if not Kext:
			missing += f' - {kext} is missing from Config\n'


kq=''
with open('config.plist') as c:
	line = c.readline()
	while line:
		line = c.readline()
		if 'Kernel' in line:
			ACPI=True
		if ACPI:
			if 'Quirks' in line:
				Quirks=True
		if Quirks:
			if '<dict>' in line:
				Arr=True

			if '</dict>' in line:
				Arr=False
				Quirks=False
				ACPI=False
		if Arr:
			if 'true/' in line and ('AppleCpuPmCfgLock' in prelin or 'AppleXcpmCfgLock'  in prelin or 'AppleXcpmExtraMsrs'  in prelin or 'CustomSMBIOSGuid'  in prelin or 'CustomSMBIOSGuid'  in prelin  or 'ThirdPartyTrim'  in prelin or 'LapicKernelPanic'  in prelin):
				kq += f' - {prelin} needs to be false\n'

			if 'false/' in line and ('DisableIoMapper' in prelin or 'PanicNoKextDump'  in prelin or 'XhciPortLimit'  in prelin):
				kq += f' - {prelin} needs to be true\n'
			
			prelin=line

	if kq:
		missing+=kq

####  MISC  ####
# Debug
prelin = ''
md = ''

with open('config.plist') as c:
	line = c.readline()
	while line:
		line = c.readline()
		if '<key>Misc</key>' in line:
			ACPI=True

		if ACPI:
			if 'Debug' in line:
				Quirks=True
		if Quirks:
			if 'DisableWatchDog' in prelin and 'true' in line:
				md += ' - DisableWatchDog needs to be false\n'

			prelin=line


	if not md == '':
		missing+=md

# Security
prelin = ''
ms = ''
with open('config.plist') as c:
	line = c.readline()
	while line:
		line = c.readline()
		if 'Misc' in line:
			ACPI=True
		if ACPI:
			if 'Security' in line:
				Quirks=True
		# print(Quirks)
		if Quirks:
			if 'AllowNvramReset' in prelin:
				if 'true' in line:
					ms += ' - AllowNvramReset needs to be false\n'
					Arr = True
					break
				else:
					Arr = True
					break
			else:
				Arr = False

			prelin=line

	if not Arr:
		ms += ' - AllowNvramReset is missing\n'

	if not ms == '':
		missing+=ms

# Signature
prelin = ''
ms = ''
with open('config.plist') as c:
	line = c.readline()
	while line:
		line = c.readline()
		if 'Misc' in line:
			ACPI=True
		if ACPI:
			if 'Security' in line:
				Quirks=True
		# print(Quirks)
		if Quirks:
			if 'RequireSignature' in prelin:
				if 'true/' in line:
					ms += ' - RequireSignature needs to be false\n'
					Arr = True
					break
				elif 'false/' in line:
					Arr = True
					break
			else:
				Arr = False

			prelin=line

	if not Arr:
		ms += ' - RequireSignature is missing\n'

	if not ms == '':
		missing+=ms

# Require Vault
prelin = ''
ms = ''
with open('config.plist') as c:
	line = c.readline()
	while line:
		line = c.readline()
		if 'Misc' in line:
			ACPI=True
		if ACPI:
			if 'Security' in line:
				Quirks=True
		# print(Quirks)
		if Quirks:
			if 'RequireVault' in prelin:
				if 'true' in line:
					ms += ' - RequireVault needs to be false\n'
					Arr = True
					break
				else:
					Arr = True
					break
			else:
				Arr = False

			prelin=line

	if not Arr:
		ms += ' - RequireVault is missing\n'

	if not ms == '':
		missing+=ms

# Scan Policy
prelin = ''
ms = ''
with open('config.plist') as c:
	line = c.readline()
	while line:
		line = c.readline()
		if 'Misc' in line:
			ACPI=True
		if ACPI:
			if 'Security' in line:
				Quirks=True
		# print(Quirks)
		if Quirks:
			if 'ScanPolicy' in prelin:
				if not '<integer>0</integer>' in line:
					ms += ' - ScanPolicy needs to be 0\n'
					Arr = True
					break
				else:
					Arr = True
					break
			else:
				Arr = False

			prelin=line

	if not Arr:
		ms += ' - ScanPolicy is missing\n'

	if not ms == '':
		missing+=ms


####  UEFI  ####
# Drivers

d=os.listdir('Drivers')
prelin = ''
ms = ''

for driver in d:
	kext=False
	with open('config.plist') as c:
		line = c.readline()
		while line:
			line = c.readline()
			if 'UEFI' in line:
				ACPI=True
			if ACPI:
				if 'Drivers' in line:
					Quirks=True
			# print(Quirks)
			if Quirks:
				if '<array>' in line:
					Arr = True

				if '</array>' in line:
					Arr=False
					Quirks=False
					ACPI=False

			if Arr:	
				if f'{driver}' in line:
					kext=True
					

		if not kext:
			ms += f' - {driver} is missing\n'

if not ms == '':
	missing+=ms

# Quirks
B=''
with open('config.plist') as c:
	line = c.readline()
	while line:
		line = c.readline()
		if 'UEFI' in line:
			ACPI=True
		if ACPI:
			if 'Quirks' in line:
				Quirks=True
		if Quirks:
			if '<dict>' in line:
				Arr=True

			if '</dict>' in line:
				Arr=False
				Quirks=False
				ACPI=False
		if Arr:
			if 'false/' in line and ('ProvideConsoleGop' in prelin or 'RequestBootVarRouting'  in prelin):
				B += f' - {prelin} needs to be false\n'

			if 'true/' in line and ('AvoidHighAlloc' in prelin or 'IgnoreInvalidFlexRatio'  in prelin or 'IgnoreTextInGraphics'  in prelin or 'SanitiseClearScreen' in prelin or 'ReleaseUsbOwnership'  in prelin or 'ReplaceTabWithSpace'  in prelin or 'ClearScreenOnModeSwitch' in prelin):
				B += f' - {prelin} needs to be true\n'
			
			if not '<integer>0</integer>' in line and ('ExitBootServicesDelay' in prelin):
				B += f' - {prelin} needs to be 0\n'
			
			prelin=line


	if not B == '':
		missing+=B

# Check for Generic
with open('config.plist') as c:
	line = c.readline()
	num = 1
	lang='Please Remove'
	while line:
		line = c.readline()

		if num == 2:
			lang+=f'{line}\n'
			break

		if '<key>prev-lang:kbd</key>' in line:
			lang+=f'\n{line}\n'
			num += 1

	if not lang == 'Please Remove':
		missing+=lang

####  SMBIOS CHECK  ####
B=''
with open('config.plist') as c:
	line = c.readline()
	while line:
		line = c.readline()
		if '<key>SMBIOS</key>' in line:
			Quirks=True
		
		if Quirks:
			if '<dict>' in line:
				Arr=True

			if '</dict>' in line:
				Arr=False
				Quirks=False
				ACPI=False
		if Arr:
			if 'M000000000001' in line and 'BoardSerialNumber' in prelin:
				B += f' - {prelin} needs to be valid\n'

			if 'W0000000001' in line and 'SystemSerialNumber' in prelin:
				B += f' - {prelin} needs to be valid\n'

			if '00000000-0000-0000-0000-000000000000' in line and 'SystemUUID' in prelin:
				B += f' - {prelin} needs to be valid\n'

			prelin=line


	if not B == '':
		missing+=B


print(missing)