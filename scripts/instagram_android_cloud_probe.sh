#!/usr/bin/env bash
# Cloud-only diagnostic: no Instagram login, publishing, credentials, or changes to the queue.
set -euo pipefail
mkdir -p cloud-probe
python3 - <<'PY'
import json,hashlib,pathlib,urllib.request
q=json.loads(pathlib.Path("content/schedule.json").read_text(encoding="utf-8"))
post=next(x for x in q["posts"] if x["id"]=="halloween-2026-10-31-historia-8-laminas")
assert post["approved"] is True and post["kind"] == "carousel"
assert len(post["media_urls"]) == len(post["media_sha256"]) == 8
dest=pathlib.Path("cloud-probe/media"); dest.mkdir(parents=True,exist_ok=True)
for i,(url,sha) in enumerate(zip(post["media_urls"],post["media_sha256"]),1):
    assert url.startswith("https://raw.githubusercontent.com/gabrielslinhares12-sudo/instagram-skills/")
    assert url.endswith(f"/{i:02d}-historia-halloween.jpg")
    with urllib.request.urlopen(url,timeout=30) as response:
        body=response.read(10_000_001)
    assert len(body)<=10_000_000
    actual=hashlib.sha256(body).hexdigest()
    assert actual == sha, f"SHA mismatch in page {i}"
    (dest/f"{i:02d}-historia-halloween.jpg").write_bytes(body)
print("ASSETS_VERIFIED=8 original JPEGs matching GitHub SHA256 manifest")
PY
adb wait-for-device
adb shell getprop sys.boot_completed | grep -q '1'
echo "ANDROID_VERSION=$(adb shell getprop ro.build.version.release | tr -d '\r')"
echo "ANDROID_DEVICE_COUNT=$(adb devices | awk 'NR>1 && $2==\"device\" {n++} END {print n+0}')"
adb shell mkdir -p /sdcard/Pictures/InstagramTUEProbe
adb push cloud-probe/media/. /sdcard/Pictures/InstagramTUEProbe/
for i in {01..08}; do
  adb shell am broadcast -a android.intent.action.MEDIA_SCANNER_SCAN_FILE \
    -d "file:///sdcard/Pictures/InstagramTUEProbe/${i}-historia-halloween.jpg" >/dev/null || true
done
echo "ASSETS_ON_ANDROID=$(adb shell ls /sdcard/Pictures/InstagramTUEProbe/ | grep -c '\.jpg' | tr -d '\r')"
adb shell am start -a android.intent.action.GET_CONTENT -c android.intent.category.OPENABLE -t 'image/*' --ez android.intent.extra.ALLOW_MULTIPLE true 2>&1 | tee cloud-probe/gallery-intent.txt || true
sleep 4
adb exec-out screencap -p > cloud-probe/android-file-picker.png
PACKAGE_MATCHES=$(adb shell pm list packages com.instagram.android | tr -d '\r' || true)
if grep -q '^package:com.instagram.android$' <<< "$PACKAGE_MATCHES"; then
  echo "INSTAGRAM_APP_INSTALLED=true" | tee cloud-probe/instagram-app-status.txt
else
  echo "INSTAGRAM_APP_INSTALLED=false" | tee cloud-probe/instagram-app-status.txt
fi
echo "RESULT=cloud_emulator_and_8_photos_checked; instagram_login_music_and_post_not_tested"
