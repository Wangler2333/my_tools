#!/bin/bash

LIST_PROBES_ONLY=0
FORCE_KICK_CONNECTION=0
ASTRIS_EXPLORER_FILE=a_xplorer.ax
OPEN_ASTRIS=0
SELECTED_DEVICE=''
RELAYS_SET=0
DONT_SPAWN_TERMINALS=0
MUXED_PROBES=0
NO_MUX=0
BLUE_MAGIC=1

ME=$(echo $0 | rev | cut -d / -f1 | rev)

function usage
{
	printf "$ME is a script to set relays on your Gibraltar-system debug probes.\n\n"
	printf "Usage:    $ME [options]\n"
	printf "\nOptions:\n"
	printf "    -p: Print the connected target of each probe and exit. Do not set relays.\n"
	printf "    -f: Force-kick any applications using your relays.\n"
	printf "    -a: Open an Astris session to the H9m probe (-f is implied).\n"
	printf "    -d: Pick the H9m probe that is connected the specified device {x589, j137, j140, j680, j132} (case-sensitive).\n"
	printf "    -x: Don't spawn terminals. Just set the relays.\n"
	printf "    -o: Don't attempt to mux the H9M and x86 probes - Valid for single Chimps connected to XB.\n"
	printf "    -b: Skip scanning BlueMagic cables.\n"
	printf "    -h: Display this help.\n"
}

function identify_embedded_device
{
	if [ $RELAYS_SET -eq 1 ]; then
		for probe in ${AP_PROBE[@]}; do
			astris $probe
		done
	fi
}

function loopset_relay_on_probe
{
	if [ "$1" != "" ] && [ "$2" != "" ] && [ "$3" != "" ]; then
		PR=-255

		while [ "$PR" -ne "$3" ]; do
			astrisctl --probe $1 relay $2 $3 >> /dev/null
			sleep 1
			PR=$(astrisctl --probe $1 relay $2 | tr '\n' ' ' | sed -E "s/.*][[:space:]]+(.*)/\1/")
		done
	else
		printf "ERROR: In loopset_relay_on_probe, supply probe followed by relay followed by value.\n"
		exit -126
	fi
}

# Get the list of Chimp probes.
which astrisctl >> /dev/null

if [ $? -ne 0 ]; then
	printf "ERROR: astrictl not found. Please install the latest HomeDiagnostic.dmg from /SWE/iOS/Images/iOSNonUI/Pyramid/CurrentPyramid.\n"
	exit -1
fi

# http://stackoverflow.com/a/18414091 - This is why only 'd' is suffixed with a :.
while getopts ":pfhaxobd:" opt; do
	case $opt in
		p)
			LIST_PROBES_ONLY=1
			;;
		f)
			FORCE_KICK_CONNECTION=1
			;;
		a)
			OPEN_ASTRIS=1
			FORCE_KICK_CONNECTION=1
			;;
		d)
			if  [ "$OPTARG" = "x589" ] ||
				[ "$OPTARG" = "j137" ] ||
				[ "$OPTARG" = "j140" ] ||
				[ "$OPTARG" = "j680" ] ||
				[ "$OPTARG" = "j132" ]; then
				SELECTED_DEVICE=$OPTARG
			else
				printf "ERROR: Unrecognized option to -d: \"%s\".\n" $OPTARG
				usage
				exit -254
			fi
			;;
		x)
			DONT_SPAWN_TERMINALS=1
			;;
		o)
			NO_MUX=1
			;;
		b)
			BLUE_MAGIC=0
			;;
		h)
			usage
			exit 0
			;;
		*)
			printf "%s: Unrecognized switch.\n" $ME
			usage
			exit -255
			;;
	esac
done

# Prepare a script for Astris scan to check for Gibraltar.
if [ -f $ASTRIS_EXPLORER_FILE ]; then
	rm -f $ASTRIS_EXPLORER_FILE
fi

echo "puts \"\"" > $ASTRIS_EXPLORER_FILE

PROBES=($(astrisctl list | grep -iE 'Chimp'))
PROBECOUNT=${#PROBES[@]}

if [ $BLUE_MAGIC -eq 1 ]; then # We got BlueMagic here!
	BLUE_MAGIC_CABLES=($(ls /dev | grep -o BLUMAG.*$ | uniq | tr '\n' ' '))

	echo "NOTE: Found the following BlueMagic cables: " ${BLUE_MAGIC_CABLES[@]}

	for bmc in ${BLUE_MAGIC_CABLES[@]}; do
		PROBECOUNT=$(($PROBECOUNT+1))	
	done
fi

if [ $PROBECOUNT -ne 0 ]; then
	printf "NOTE: %u probes found.\n" $PROBECOUNT
else
	printf "ERROR: No Chimp probes found.\n"
	exit -2
fi

declare -a AP_PROBE
declare -a x86_PROBE
declare -a NON_H9M_PROBE
declare -a H9M_PROBE
declare -a PRODUCT_NAMES

for probe in ${PROBES[@]}; do
	printf "NOTE: Starting identification of probe %s...\n" $probe

	# Check if probe is busy.
	if [ "$(astrisctl --probe $probe list status | grep -i 'busy')" != "" ]; then
		printf "NOTE: Probe %s is busy. " $probe

		if [ $FORCE_KICK_CONNECTION -eq 1 ]; then
			printf "Force removing current connection.\n"
			astrisctl --probe $probe --force-kick info >> /dev/null
			if [ $? -ne 0 ]; then
				printf "WARNING: Force-kicking failed. Skipping.\n"
				continue
			fi
		else
			printf "NOTE: Skipping.\n"
			continue
		fi
	fi

	# Get the version of the probe firmware.
	PROBE_FW_VER=$(astrisctl --probe $probe info | grep "Firmware version" | awk '{ print $3; }')

	if [ "$PROBE_FW_VER" != "" ]; then
		# Check if it's lower than 0.29.
		if [ $(bc <<< "$PROBE_FW_VER >= 0.29") -eq 0 ]; then
			# Too old. Report and bail.
			printf "WARNING: Probe %'s firmware is too old (%s). Please refer to: https://connectme.apple.com/docs/DOC-476267\n" $probe $PROBE_FW_VER
			continue
		fi
	else
		printf "ERROR: Unable to get firmware version from probe %s.\n" $probe
		continue
	fi

	# Check if the probe's connected to a device.
	VCONN_V_RELAY=$(astrisctl --probe $probe relay vconn_v | tr '\n' ' ' | sed -E "s/.*][[:space:]]+(.*)/\1/")

	# Check for railed value.
	if [ $VCONN_V_RELAY -eq 65535 ]; then
		printf "WARNING: Probe %s is not connected to a device. Will skip.\n" $probe
		continue
	fi

	# Past 0.29, we know that the tgtUart is good to detect an x86 probe. Use relay instead of relays to minimize ROM table exploration.
	TGTUART_RELAY=$(astrisctl --probe $probe relay tgtUart | tr '\n' ' ' | sed -E "s/.*][[:space:]]+(.*)/\1/")

	if [ $TGTUART_RELAY -ne 0 ]; then #x86
		printf "NOTE: Probe %s is an x86 probe.\n" $probe

		# Clear dockfifo relays.
		astrisctl --probe $probe relay hippochannels 0 >> /dev/null
		sleep 1
		astrisctl --probe $probe relay dbgfifo 0 >> /dev/null

		# Set its tgtSWD relay.
		loopset_relay_on_probe $probe tgtSWD 3

		x86_PROBE[${#x86_PROBE[@]}]=$probe

	else
		printf "NOTE: Probe %s is an AP probe - will check for H9m presence.\n" $probe
		AP_PROBE[${#AP_PROBE[@]}]=$probe
	fi

done

# Check if only an x86 probe is connected and optionally attempt to probe a possible mux'd H9M.
if [ ${#AP_PROBE[@]} -eq 0 ] && [ ${#x86_PROBE[@]} -eq 1 ]; then
	if [ $NO_MUX -ne 1 ]; then
		MUXED_PROBES=1
		printf "NOTE: Enabling AP support, for possible muxing.\n" $probe
		AP_PROBE[${#AP_PROBE[@]}]=${x86_PROBE[0]}
	fi
fi

# Filter out the non-H9M probes on the Chimp.
printf "NOTE: Starting lazy-check of targets on AP probes...\n"
for probe in ${AP_PROBE[@]}; do
	# Don't do this if we're muxing.
	if [ $MUXED_PROBES -eq 0 ]; then
		loopset_relay_on_probe $probe tgtSWD 6
	else
		# Set the sink.
		### Note that this has been commented out because I'm seeing weird problems with the tgtUart et al relays dropping off.
		#astrisctl --probe $probe relay sink 1 >> /dev/null
		if [ $NO_MUX -eq 0 ]; then
			astrisctl --probe $probe relay hippochannels 1 >> /dev/null
			printf "NOTE: Sleeping to allow the probe to reconnect...\n"
			sleep 3
			printf "NOTE: Pulsing the dbgfifo relay...\n"
			astrisctl --probe $probe relay dbgfifo 0 >> /dev/null
			sleep 1
			astrisctl --probe $probe relay dbgfifo 1 >> /dev/null
		fi
	fi

	# Establish that the SoC is a Gibraltar.
	if [ "$(astris --script $ASTRIS_EXPLORER_FILE $probe | grep Gibraltar)" != "" ]; then
		printf "NOTE: Probe %s is an H9m probe.\n" $probe
		H9M_PROBE[${#H9M_PROBE[@]}]=$probe


		if [ $LIST_PROBES_ONLY -eq 0 ] && [ $MUXED_PROBES -eq 0 ]; then

			# Set the sink.
			#astrisctl --probe $probe relay sink 1 >> /dev/null

			astrisctl --probe $probe relay hippochannels 1 >> /dev/null
			printf "NOTE: Sleeping to allow the probe to reconnect...\n"
			sleep 3
			printf "NOTE: Pulsing the dbgfifo relay...\n"
			astrisctl --probe $probe relay dbgfifo 0 >> /dev/null
			sleep 1
			astrisctl --probe $probe relay dbgfifo 1 >> /dev/null
		fi

	else
		# Check for failure.
		if [ "$(astris --script $ASTRIS_EXPLORER_FILE $probe | grep -i "explore failed")" != "" ]; then
			printf "WARNING: JTAG scan failed on probe %s.\n" $probe
		else
			NON_H9M_PROBE[${#NON_H9M_PROBE[@]}]=$probe
			printf "NOTE: Probe %s will be skipped since the attached SoC is not a Gibraltar.\n" $probe
		fi
	fi
done

if [ $BLUE_MAGIC -eq 1 ]; then # We got BlueMagic here!
	BLUE_MAGIC_CABLES=($(ls /dev | grep -o BLUMAG.*$ | uniq | tr '\n' ' '))
	for bmc in ${BLUE_MAGIC_CABLES[@]}; do
		x86_PROBE[${#x86_PROBE[@]}]=$bmc
	done
fi

if [ ${#AP_PROBE[@]} -eq 0 ] && [ ${#x86_PROBE[@]} -eq 0 ] && [ ${#NON_H9M_PROBE[@]} -eq 0 ]; then
	# Clearly a firmware version issue.
	printf "ERROR: Please update all your Chimp probes to the latest firmware.\n"
elif [ ${#AP_PROBE[@]} -eq 0 ] && [ ${#x86_PROBE[@]} -eq 0 ] && [ ${#NON_H9M_PROBE[@]} -ne 0 ]; then
	printf "ERROR: No x86 or H9m probes detected.\n"
else
	printf "NOTE: Found %u x86 and %u H9m probes" ${#x86_PROBE[@]} ${#H9M_PROBE[@]}
	if [ $LIST_PROBES_ONLY -eq 0 ];  then
		printf " and their relevant relays have been set"
	fi
	printf ".\n"
fi

if [ $LIST_PROBES_ONLY -eq 1 ];  then
	exit -200
fi

# Parse the PRODUCT_NAMES for the one specified with a -d.
MATCHED_AP_PROBE=''
MATCHED_x86_PROBE=''

if [ "$SELECTED_DEVICE" != "" ]; then
	for probe in ${H9M_PROBE[@]}; do
		THIS_PRODUCT=$(astris --script $ASTRIS_EXPLORER_FILE $probe | grep Product | awk '{ print $3; }')
		PRODUCT_NAMES[${#PRODUCT_NAMES[@]}]=$THIS_PRODUCT
		# Astris
		printf "NOTE: AP probe detects product to be: %s\n" $THIS_PRODUCT
		echo "$THIS_PRODUCT" | grep -i "$SELECTED_DEVICE" >> /dev/null
		if [ $? -eq 0 ]; then
			MATCHED_AP_PROBE=$probe
			break
		fi
	done

	if [ ${#x86_PROBE[@]} -gt 1 ]; then

		printf "QUERY: Which of these x86 probes is the one attached to XB on your device ?\n"

		INDEX=0
		for x86probe in ${x86_PROBE[@]}; do
			INDEX=$(($INDEX+1))
			printf "%u) %s\n" $INDEX $x86probe
		done

		printf "QUERY: Pick one of [1...%u]\n" ${#x86_PROBE[@]}

		read

		if [ "$REPLY" != "" ]; then
			REPLY=$(($REPLY-1))

			if [ $REPLY -ge ${#x86_PROBE[@]} ]; then
				printf "ERROR: Picked probe is out of bounds (%u). Exiting.\n" $REPLY
				exit -9
			fi

			if [ "$MATCHED_AP_PROBE" != "" ]; then
				printf "NOTE: Matched x86 probe %s with H9m probe %s.\n" ${x86_PROBE[$REPLY]} $MATCHED_AP_PROBE
			fi

			MATCHED_x86_PROBE=${x86_PROBE[$REPLY]}
		else
			printf "ERROR: You'll need to pick one of [1...%u]. Exiting\n" ${#x86_PROBE[@]}
			exit -10
		fi
	else
		MATCHED_x86_PROBE=${x86_PROBE[0]}
	fi

	if [ "$MATCHED_AP_PROBE" = "" ]; then
		printf "WARNING: No suitable AP probe found. No terminals will be spawned for the H9M.\n"
	fi

	if [ "$MATCHED_x86_PROBE" = "" ]; then
		printf "WARNING: No suitable x86 probe found. No terminals will be spawned for it.\n"
	fi
fi


#=============================================================================#
# Proceed to launch the necessary terminals.
#=============================================================================#
LAUNCH_SHELL_TO_x86_PROBE=
LAUNCH_SHELL_TO_H9M_PROBE=
H9M_RAW_PROBE=
x86_RAW_PROBE=
NO_H9M_SPAWNED=0
NO_x86_SPAWNED=0

if [ $DONT_SPAWN_TERMINALS -ne 1 ]; then
	if [ "$SELECTED_DEVICE" = "" ]; then
		# Pick probes.
		if [ ${#x86_PROBE[@]} -gt 1 ]; then
			INDEX=0
			printf "NOTE: More than one x86 probe detected.\n"

			for x86probe in ${x86_PROBE[@]}; do
				INDEX=$(($INDEX+1))
				printf "%u) %s\n" $INDEX $x86probe
			done

			printf "QUERY: Pick one of [1...%u]\n" ${#x86_PROBE[@]}

			read

			if [ "$REPLY" != "" ]; then
				REPLY=$(($REPLY-1))

				if [ $REPLY -ge ${#x86_PROBE[@]} ]; then
					printf "ERROR: Picked probe is out of bounds (%u). Exiting.\n" $REPLY
					exit -9
				fi

				x86_RAW_PROBE=${x86_PROBE[$REPLY]}
			fi
		elif [ ${#x86_PROBE[@]} -gt 0 ]; then
			x86_RAW_PROBE=${x86_PROBE[0]}
		fi

		if [ ${#H9M_PROBE[@]} -gt 1 ]; then
			INDEX=0
			printf "NOTE: More than one H9m probe detected.\n"

			for h9mprobe in ${H9M_PROBE[@]}; do
				INDEX=$(($INDEX+1))
				printf "%u) %s\n" $INDEX $h9mprobe
			done

			printf "QUERY: Pick one of [1...%u]\n" ${#H9M_PROBE[@]}

			read

			if [ "$REPLY" != "" ]; then
				REPLY=$(($REPLY-1))

				if [ $REPLY -ge ${#H9M_PROBE[@]} ]; then
					printf "ERROR: Picked probe is out of bounds (%u). Exiting.\n" $REPLY
					exit -9
				fi

				H9M_RAW_PROBE=${H9M_PROBE[$REPLY]}
			fi
		elif [ ${#H9M_PROBE[@]} -gt 0 ]; then
			H9M_RAW_PROBE=${H9M_PROBE[0]}
		fi

		if [ "$x86_RAW_PROBE" != "" ]; then
			echo $x86_RAW_PROBE | grep BLUM >> /dev/null

			if [ $? -ne 0 ]; then
				LAUNCH_SHELL_TO_x86_PROBE="/dev/cu.chimp-$(echo ${x86_RAW_PROBE} | cut -d '-' -f2)"
			else
				LAUNCH_SHELL_TO_x86_PROBE="/dev/cu.usbserial-$(echo ${x86_RAW_PROBE})"
			fi
		fi

		if [ "$H9M_RAW_PROBE" != "" ]; then
			LAUNCH_SHELL_TO_H9M_PROBE="/dev/cu.chimp-$(echo ${H9M_RAW_PROBE} | cut -d '-' -f2)"
		fi

	else
		if [ "$MATCHED_AP_PROBE" != "" ]; then
			LAUNCH_SHELL_TO_H9M_PROBE="/dev/cu.chimp-$(echo ${MATCHED_AP_PROBE} | cut -d '-' -f2)"
			H9M_RAW_PROBE=${MATCHED_AP_PROBE}
		fi

		if [ "$MATCHED_x86_PROBE" != "" ]; then
			echo $MATCHED_x86_PROBE | grep BLUM >> /dev/null

			if [ $? -ne 0 ]; then
				LAUNCH_SHELL_TO_x86_PROBE="/dev/cu.chimp-$(echo ${MATCHED_x86_PROBE} | cut -d '-' -f2)"
			else
				LAUNCH_SHELL_TO_x86_PROBE="/dev/cu.usbserial-$(echo ${MATCHED_x86_PROBE})"
			fi
		fi
	fi

	if [ "$LAUNCH_SHELL_TO_x86_PROBE" != "" ]; then
		printf "NOTE: Opening a nanokdp session to the x86 probe: %s\n" $LAUNCH_SHELL_TO_x86_PROBE
		printf "NOTE: Checking if probe's already occupied...\n"
		ps | egrep "[n]ano.*$LAUNCH_SHELL_TO_x86_PROBE" >> /dev/null
		if [ $? -ne 0 ]; then
			printf "NOTE: Probe's available.\n"

			# I've realized that there's many use cases where hippochannels can leak into the x86 probe. I'm therefore defaulting to
			# using nanohippo, to avoid "unknown packet type" errors.
			osascript -e 'tell application "Terminal"
				do script "nanohippo --timestamp=\"%T.ssss x86> \" -d '$LAUNCH_SHELL_TO_x86_PROBE' -c 1250000,n,8,1 -K -k 0"
			end tell' >> /dev/null
		else
			PID=$(ps | egrep "[n]ano.*$LAUNCH_SHELL_TO_x86_PROBE" | awk '{ print $1 }')
			printf "NOTE: Probe's occupied and the nanocom terminal @ PID=$PID will not be killed.\n"
			NO_x86_SPAWNED=1
		fi
	fi

	if [ "$LAUNCH_SHELL_TO_H9M_PROBE" != "" ]; then
		printf "NOTE: Opening a nanohippo session to the H9m probe: %s, as well as the necessary netcat sessions.\n" $LAUNCH_SHELL_TO_H9M_PROBE

		printf "NOTE: Checking if probe's already occupied...\n"
		ps | egrep "[n]ano.*$LAUNCH_SHELL_TO_H9M_PROBE" >> /dev/null
		if [ $? -ne 0 ]; then
			printf "NOTE: Probe's available.\n"

			if [ -f "/usr/local/lib/nanocom/libnanocom_udp.dylib" ]; then
				serial_log_reader='nanocom --timestamp=\"%T.ssss arm> \" -P /usr/local/lib/nanocom/libnanocom_udp.dylib -d udp://localhost:'
			else
				serial_log_reader="stty raw ; nc -4 -u localhost "
			fi

			H9M_AP_PORT=31337
			H9M_SMC_PORT=31339
			# Check if 31337 and 31339 are occupied.
			OCCUPIED=($(ps x | egrep -o "localhost.*[3]133[79]" | tr '\n' ' '))

			if [ ${#OCCUPIED[@]} -ge 2 ]; then
				printf "NOTE: Both default H9M serial ports are occupied. Picking alternates...\n"
				H9M_AP_PORT=31341
				H9M_SMC_PORT=31343
			elif [ ${#OCCUPIED[@]} -eq 1 ]; then
				# Get the probe port.
				PROBE_PORT=$(echo ${OCCUPIED[0]} | perl -pe 's|.*?(\d+)$|\1|')

				if [ "$PROBE_PORT" = "$H9M_AP_PORT" ]; then
					printf "NOTE: Default H9M AP serial port is occupied. Picking alternate...\n"
					H9M_AP_PORT=31341
				else
					printf "NOTE: Default H9M SMC serial port is occupied. Picking alternate...\n"
					H9M_SMC_PORT=31343
				fi
			fi

			H9M_SERIAL_STREAM="${serial_log_reader}${H9M_AP_PORT}"
			SMC_SERIAL_STREAM="${serial_log_reader}${H9M_SMC_PORT}"

			if [ $MUXED_PROBES -eq 0 ]; then
				osascript -e 'tell application "Terminal"
					activate
					tell application "System Events" to tell process "Terminal" to keystroke "n" using command down
					delay 1
					tell application "Terminal" to do script "nanohippo -d '$LAUNCH_SHELL_TO_H9M_PROBE' -p 41140" in selected tab of the front window

					tell application "System Events" to tell process "Terminal" to keystroke "t" using command down
					delay 1
					tell application "Terminal" to do script "'"$H9M_SERIAL_STREAM"'" in selected tab of the front window

					tell application "System Events" to tell process "Terminal" to keystroke "t" using command down
					delay 1
					tell application "Terminal" to do script  "'"$SMC_SERIAL_STREAM"'" in selected tab of the front window
				end tell' >> /dev/null

		else
				osascript -e 'tell application "Terminal"
					activate
					tell application "System Events" to tell process "Terminal" to keystroke "n" using command down
					delay 1
					tell application "Terminal" to do script "'"$H9M_SERIAL_STREAM"'" in selected tab of the front window

					tell application "System Events" to tell process "Terminal" to keystroke "t" using command down
					delay 1
					tell application "Terminal" to do script  "'"$SMC_SERIAL_STREAM"'" in selected tab of the front window
				end tell' >> /dev/null
		fi
		else
			PID=$(ps | egrep "[n]ano.*$LAUNCH_SHELL_TO_H9M_PROBE" | awk '{ print $1 }')
			printf "NOTE: Probe's occupied and the nanocom terminal @ PID=$PID will not be killed.\n"
			NO_H9M_SPAWNED=1
		fi

		if [ $OPEN_ASTRIS -eq 1 ]; then
			if [ $NO_H9M_SPAWNED -eq 1 ]; then
				KEYSTROKE=n
			else
				KEYSTROKE=t
			fi

			printf "NOTE: Opening an Astris session to the H9m probe: %s\n" $LAUNCH_SHELL_TO_H9M_PROBE
			osascript -e 'tell application "Terminal"
				activate
				tell application "System Events" to tell process "Terminal" to keystroke "'$KEYSTROKE'" using command down
				delay 1
				tell application "Terminal" to do script "astris '$H9M_RAW_PROBE'" in selected tab of the front window
			end tell' >> /dev/null
		fi
	fi
fi

# Cleanup
if [ -f $ASTRIS_EXPLORER_FILE ]; then
	rm -f $ASTRIS_EXPLORER_FILE
fi
