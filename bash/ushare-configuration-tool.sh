#!/bin/bash

#*********************************************************************************************#
# Script to set up a Ushare session                                                           #
# Script by Chema Martin.                                                                     #
# Version 0.1 - 02/12/2010                                                                    #
#*********************************************************************************************#

# Set the script path correctly
progdir=`dirname $0`
cd $progdir

# Check if Ushare is installed
if [[ "$(which ushare)" ]]; then
  
  # Check if Ushare is already running
  if [[ "$(ps -ef | grep ushare | wc -l)" -gt 1 ]]; then
   
    ROOT_UID=0
    
    # Get user privileges to kill all ushare instances
    if [ "$UID" -ne "$ROOT_UID" ]; then
      zenity --warning --text "A Ushare streaming session is already active, but it must be terminated before a new one can be started.\n\nAdministrator privileges are required to manage existing Ushare sessions.  \n\nClick OK to continue."
      gksu "./UCT.sh"
    else
      # A Ushare session is already running, let the user decide what to do next.  
      Choice="$(zenity --width=500 --height=150 --list --radiolist --text 'What do you want to do?' --column 'Select...' --column 'Action Name' TRUE 'Kill the existing Ushare session' FALSE 'Nothing, just get me out of here!')"
    
      # Loop until a proper choice is made
      while [[ $Choice == "" ]]; do
        zenity --error --text "You must select an option from the list!!"
        Choice="$(zenity --width=500 --height=150 --list --radiolist --text 'What do you want to do?' --column 'Select...' --column 'Action Name' TRUE 'Kill the existing Ushare session' FALSE 'Nothing, just get me out of here!')"
      done
    
      case $Choice in
        "Kill the existing Ushare session")
          killall ushare
          exit 0
          ;;
        "Nothing, just get me out of here!")
          exit 0
          ;;
      esac
    fi       
  else
    # Start the script, welcome the user.
    zenity --info --text "Welcome to the Ushare Configuration Tool (UCT).  \n\nThis tool will allow you to configure an adhoc Ushare session from the GUI.  \n\nClick OK to continue"
      
    # Select an Interface
    Interface="$(zenity --height=275 --list --radiolist --text 'Select the interface to be used:' --column 'Select...' --column 'Interface Name' FALSE 'eth0' TRUE 'wlan0' FALSE 'eth1' FALSE 'wlan1' FALSE 'eth2' FALSE 'wlan2' FALSE 'Other...')"

    # Loop until an interface is selected
    while [[ $Interface == "" ]]; do
      zenity --error --text "You must select an Interface!"
      Interface="$(zenity --list --radiolist --text 'Select the interface to be used:' --column 'Select...' --column 'Interface Name' FALSE 'eth0' TRUE 'wlan0' FALSE 'eth1' FALSE 'wlan1' FALSE 'eth2' FALSE 'wlan2' FALSE 'Other...')"
    done

    if [[ $Interface == "Other..." ]]; then
      zenity --warning --text "You chose an unlisted interface.  UCT will therefore not be able to properly set up a streaming session for you.  \n\nClick OK to exit."
    else 
      # Select a name for the Ushare session
      Name="$(zenity --entry --text 'Enter the name of this streaming session:')"  
    
      if [[ $Name == "" ]]; then
        # Default session name to 'Ushare'
        Name="Ushare"
      fi
  
      # Select a Device
      Device="$(zenity --list --radiolist --text 'Select the device you will be streaming to:' --column 'Select...' --column 'Device Name' TRUE 'Playstation 3' FALSE 'XBox 360')"  
  
      # Loop until a Device is selected
      while [[ $Device == "" ]]; do
        zenity --error --text "You must select a device!"
        Device="$(zenity --list --radiolist --text 'Select the device you will be streaming to:' --column 'Select...' --column 'Device Name' TRUE 'Playstation 3' FALSE 'XBox 360')"  
      done  
    
      # Select a folder to be shared
      Share="$(zenity --file-selection --directory --text 'Select which folder you want Ushare to stream over your network.')"

      # Loop until a folder is selected    
      while [[ $Share == "" ]]; do
        zenity --error --text "You must select a folder to be shared!"
        Share="$(zenity --file-selection --directory --text 'Select which folder you want Ushare to stream over your network.')"
      done

      # And we are done!
      zenity --info --text "DONE!!  \n\nClick OK now to start Ushare...  Happy streaming!!"
    
      # Start Ushare for the device of choice.
      if [[ $Device == "XBox 360" ]]; then
        ushare -D --xbox --name "$Name" --interface $Interface --content="$Share"      
      else
        ushare -D --dlna --name "$Name" --interface $Interface --content="$Share"   
      fi   
    fi
  fi    
else
  # Ushare is not installed.  Exit.
  zenity --error --text "Ushare is not installed!!  \n\nUshare must be installed for UCT to work!  \n\nClick OK to exit."
fi
