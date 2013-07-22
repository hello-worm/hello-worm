TZ_adjust=-7;d=$(date +%s);t=$(echo "60*60*$TZ_adjust/1" | bc);echo T$(echo $d+$t | bc ) > /dev/tty.usbmodemfd121
