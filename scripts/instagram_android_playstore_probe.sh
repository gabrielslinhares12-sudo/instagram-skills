#!/usr/bin/env bash
# Read-only Play Store availability probe in an ephemeral GitHub-hosted Android emulator.
# No credentials, installations or publishing.
set -euo pipefail
mkdir -p cloud-probe
adb wait-for-device
ANDROID_VER=$(adb shell getprop ro.build.version.release | tr -d '\r')
PLAY_STORE=$(adb shell pm list packages com.android.vending | tr -d '\r' || true)
INSTAGRAM=$(adb shell pm list packages com.instagram.android | tr -d '\r' || true)
echo "ANDROID_VERSION=$ANDROID_VER"
if grep -q '^package:com.android.vending$' <<< "$PLAY_STORE"; then
  echo 'GOOGLE_PLAY_STORE_INSTALLED=true'
  echo 'GOOGLE_PLAY_STORE_INSTALLED=true' > cloud-probe/store-status.txt
  adb shell am start -a android.intent.action.VIEW -d 'market://details?id=com.instagram.android' \
      > cloud-probe/instagram-market-intent.txt 2>&1 || true
  sleep 8
  adb exec-out screencap -p > cloud-probe/playstore-instagram-page.png
else
  echo 'GOOGLE_PLAY_STORE_INSTALLED=false'
  echo 'GOOGLE_PLAY_STORE_INSTALLED=false' > cloud-probe/store-status.txt
fi
if grep -q '^package:com.instagram.android$' <<< "$INSTAGRAM"; then
  echo 'INSTAGRAM_INSTALLED=true'
else
  echo 'INSTAGRAM_INSTALLED=false'
fi
echo 'AUTHENTICATION_ATTEMPTED=false'
echo 'APK_DOWNLOAD_ATTEMPTED=false'
echo 'POST_ATTEMPTED=false'
