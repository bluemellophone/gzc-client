
# IMPORTANT: Make sure that "Enable access for assistive devices" is checked in System Preferences>>Universal Access. It is required for the AppleScript to work. You may have to reboot after this change (it doesn't work otherwise on Mac OS X Server 10.4).

cd ~/code/gzc-client/build
echo "Creating Working Files, Directory, and Variables"
gzc_source=pack.temp
gzc_working=pack.temp.dmg
gzc_title=GZCClient
gzc_applicationName=GZCClient.app
gzc_size=256000
gzc_backgroundPictureName=background.png
gzc_finalDMGName=GZCClient.dmg

# Unmount if it already exists
if [ -d /Volumes/"${gzc_title}" ]; then
	echo "GZCClient Already Mounted! Unmounting..."
    hdiutil unmount /Volumes/"${gzc_title}"
    sleep 10
fi

mkdir "${gzc_source}"
echo "Copying Application"
cp -r ../dist/"${gzc_applicationName}" "${gzc_source}"/"${gzc_applicationName}"
echo "Creating DMG"
hdiutil create -srcfolder "${gzc_source}" -volname "${gzc_title}" -fs HFS+ -fsargs "-c c=64,a=16,e=16" -format UDRW -size ${gzc_size}k "${gzc_working}"
echo "Mouting DMG"
gzc_device=$(hdiutil attach -readwrite -noverify -noautoopen ""${gzc_working}"" | egrep '^/dev/' | sed 1q | awk '{print $1}')
echo "Formatting DMG"
mkdir /Volumes/"${gzc_title}"/.background
cp ../_installers/"${gzc_backgroundPictureName}" /Volumes/"${gzc_title}"/.background/"${gzc_backgroundPictureName}"
echo '
      tell application "Finder"
       tell disk "'${gzc_title}'"
             open
             set current view of container window to icon view
             set toolbar visible of container window to false
             set statusbar visible of container window to false
             set theViewOptions to the icon view options of container window
             set arrangement of theViewOptions to not arranged
             set icon size of theViewOptions to 72
             set background picture of theViewOptions to file ".background:'${gzc_backgroundPictureName}'"
             set the bounds of container window to {400, 100, 885, 430}
             make new alias file at container window to POSIX file "/Applications" with properties {name:"Applications"}
             set position of item "'${gzc_applicationName}'" of container window to {100, 100}
             set position of item "Applications" of container window to {375, 100}
             close
             open
             update without registering applications
             delay 5
          end tell
      end tell
      ' | osascript

echo "Convert & Saving DMG"
sync
sync
hdiutil detach ${gzc_device}
hdiutil convert "${gzc_working}" -format UDZO -imagekey zlib-level=9 -o "${gzc_finalDMGName}"
echo "Removing Working Files and Directory"
rm -f "${gzc_working}"
rm -rf "${gzc_source}"
mv -f "${gzc_finalDMGName}" ../dist/"${gzc_finalDMGName}"
echo "Completed"
