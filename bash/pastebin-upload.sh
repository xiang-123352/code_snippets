#!/bin/bash
# Upload a given file to Pastebin.com
# Can upload to a Pastebin.com account or anonymously (default)
# and even put the paste URL into your clipboard!
#
# Dependencies: curl (for uploading the file to pastebin)
# Optional: xclip (for putting the paste URL into the clipboard),
#           sox (for sound playing capability),
#           libnotify-bin (for notifications)
#
# Author: Michael Koch (Emkay443) (m<DOT>koch<AT>emkay443<DOT>de)
# Version: 2013-08-27
# License: Copyleft

#################
# CONFIGURATION #
#################

# Change this to your personal Pastebin.com Developer API Key
# which can be found at http://pastebin.com/api#1
api_dev_key="0123456789abcdef0123456789abcdef"

# Change this to your Pastebin.com user name and password
# and set use_login to true if you want to upload the paste to your own Pastebin.com account
use_login=false
api_user_name="username"
api_user_password="topsecret"

# Paste expiration time (N = never, 10M = 10 minutes, 1H = 1 hour, 1D = 1 day, 1W = 1 week, 2W = 2 weeks, 1M = 1 month)
api_paste_expire_date="N"

# Paste privacy (0 = public, 1 = unlisted, 2 = private)
api_paste_private="1"

# Enable playing the given sound file (using sox' play command) on a successful paste
sound_success_enabled=true
sound_success_file="/usr/share/sounds/freedesktop/stereo/complete.oga"

# Enable notification (using libnotify) on a successful paste
notification_enabled=true

# Enable copying the paste's URL to the clipboard (using xclip)
clipboard_enabled=true

# Enable opening a browser window to your paste on a successful paste
open_browser_enabled=true

#########################################################################################
# WARNING: You should be careful when changing any code below. Modify at your own risk! #
#########################################################################################

# If there is a first parameter and it is a file, run the program.
if [ ! -z "$1" ] && [ -f "$*" ]; then

	######################
	## HELPER FUNCTIONS ##
	######################

	function get_api_format {
		if [ ! -z $1 ]; then
			mime_type="$(mimetype -b $1)"
			if [[ $mime_type == *x-shellscript* ]]; then
				echo bash
			elif [[ $mime_type == *x-c* ]]; then
				echo c
			elif [[ $mime_type == *x-c++src* ]]; then
				echo cpp
			elif [[ $mime_type == *x-php* ]]; then
				echo php
			elif [[ $mime_type == *x-python* ]]; then
				echo python
			elif [[ $mime_type == *x-haskell* ]]; then
				echo haskell
			elif [[ $mime_type == *x-html* ]]; then
				echo html5
			elif [[ $mime_type == *x-java* ]]; then
				echo java
			elif [[ $mime_type == *javascript* ]]; then
				echo javascript
			elif [[ $mime_type == *x-lua* ]]; then
				echo lua
			elif [[ $mime_type == *x-pascal* ]]; then
				echo pascal
			elif [[ $mime_type == *x-perl* ]]; then
				echo perl
			elif [[ $mime_type == *x-cobol* ]]; then
				echo cobol
			elif [[ $mime_type == *css* ]]; then
				echo css
			elif [[ $mime_type == *sql* ]]; then
				echo sql
			elif [[ $mime_type == *xml* ]]; then
				echo xml
			elif [[ $mime_type == *yaml* ]]; then
				echo yaml
			elif [[ $mime_type == *x-wine-extension-ini* ]]; then
				echo ini
			elif [[ $mime_type == *x-matlab* ]]; then
				echo matlab
			else
				echo text
			fi
		fi
	}

	function get_api_user_key {
		if $use_login; then
			curl_data="api_dev_key=$api_dev_key&api_user_name=$api_user_name&api_user_password=$api_user_password"
			echo "&api_user_key="$(curl --data "$curl_data" http://pastebin.com/api/api_login.php)			
		fi
	}

	##################
	## MAIN PROGRAM ##
	##################

	paste_file="$1"
	api_paste_name="$(basename $paste_file)"
	api_post_url="http://pastebin.com/api/api_post.php"
	api_option="paste"
	api_user_key="$(get_api_user_key)" 
	api_paste_format="$(get_api_format $paste_file)"
	curl_data="api_option=paste&api_dev_key=$api_dev_key&api_paste_name=$api_paste_name&api_paste_format=$api_paste_format&api_paste_expire_date=$api_paste_expire_date&api_paste_private=$api_paste_private$api_user_key"

	paste_url=$(curl --data "$curl_data" --data-urlencode "api_paste_code@$paste_file" $api_post_url)

	if [[ $paste_url == *Bad\ API\ request* ]]; then
		echo "Bad API request!"
		if $notification_enabled; then notify-send "Pastebin Upload" "You Pastebin Upload was not successful!\n\nReason: $paste_url"; fi
	else
		if $clipboard_enabled; then echo $paste_url | xclip -sel clip; fi
		if $notification_enabled; then notify-send "Pastebin Upload" "You Pastebin Upload was successful!\n\nURL: <a href='$paste_url'>$paste_url</a>"; fi
		if $sound_success_enabled; then	play $sound_success_file; fi
		if $open_browser_enabled; then x-www-browser $paste_url; fi
	fi

else
	echo "This program requires one parameter - the file that you want to paste!"
	exit 1
fi
exit 0

