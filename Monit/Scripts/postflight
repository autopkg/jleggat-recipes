#!/bin/bash
SOURCE_D=$1/Contents/Resources

# only install monit config file if it doesn't exist.
if [ ! -f /private/etc/monitrc ]; then
    sudo /usr/bin/install -m 600 -g wheel -o root ${WORK_D}/private/etc/monitrc.default /private/etc/monitrc
fi

if [ -f /Library/LaunchDaemons/com.monit.mmonit.plist ]; then
    sudo launchctl load -w /Library/LaunchDaemons/com.monit.mmonit.plist
fi

exit 0
