#!/usr/bin/env bash
# Compile and install our original, non-networked Android file-picker test app.
set -euo pipefail
export ANDROID_HOME="${ANDROID_HOME:-${ANDROID_SDK_ROOT:-/usr/local/lib/android/sdk}}"
ROOT="$(pwd)/cloud-probe/picker-harness"
mkdir -p "$ROOT/src/com/temumaexplicacao/pickerprobe" "$ROOT/classes" "$ROOT/dex"
cat > "$ROOT/AndroidManifest.xml" <<'XML'
<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
  package="com.temumaexplicacao.pickerprobe">
  <application android:label="TUE Photo Picker Test" android:usesCleartextTraffic="false">
    <activity android:name=".MainActivity" android:exported="true">
      <intent-filter>
        <action android:name="android.intent.action.MAIN"/>
        <category android:name="android.intent.category.LAUNCHER"/>
      </intent-filter>
    </activity>
  </application>
</manifest>
XML
cat > "$ROOT/src/com/temumaexplicacao/pickerprobe/MainActivity.java" <<'JAVA'
package com.temumaexplicacao.pickerprobe;

import android.app.Activity;
import android.os.Bundle;
import android.content.ClipData;
import android.content.Intent;
import android.net.Uri;
import android.provider.DocumentsContract;
import android.util.Log;
import android.widget.TextView;

public final class MainActivity extends Activity {
  @Override
  public void onCreate(Bundle state) {
    super.onCreate(state);
    TextView info = new TextView(this);
    info.setText("Automated offline photo picker test — no Instagram login or publishing.");
    info.setTextSize(20);
    setContentView(info);
    Intent picker = new Intent(Intent.ACTION_OPEN_DOCUMENT);
    picker.addCategory(Intent.CATEGORY_OPENABLE);
    picker.setType("image/jpeg");
    picker.putExtra(Intent.EXTRA_ALLOW_MULTIPLE, true);
    picker.putExtra(DocumentsContract.EXTRA_INITIAL_URI, Uri.parse(
      "content://com.android.externalstorage.documents/document/primary%3APictures%2FInstagramTUEProbe"));
    startActivityForResult(picker, 1);
  }
  @Override
  protected void onActivityResult(int requestCode, int resultCode, Intent data) {
    super.onActivityResult(requestCode, resultCode, data);
    if (requestCode == 1) {
      int n=0;
      if (resultCode == RESULT_OK && data != null) {
        ClipData clip=data.getClipData();
        if (clip != null) n=clip.getItemCount();
        else if(data.getData()!=null) n=1;
      }
      Log.i("TUEPickerProbe","PICKER_RESULT_COUNT="+n+" RESULT_OK="+(resultCode==RESULT_OK));
      TextView text=new TextView(this);
      text.setText("Picker returned "+n+" images. No post was made.");
      setContentView(text);
    }
  }
}
JAVA
BUILD_TOOLS="$(find "$ANDROID_HOME/build-tools" -mindepth 1 -maxdepth 1 -type d | sort -V | tail -n1)"
if [[ ! -x "$BUILD_TOOLS/aapt2" || ! -x "$BUILD_TOOLS/d8" || ! -x "$BUILD_TOOLS/apksigner" ]]; then
  echo 'ANDROID_BUILD_TOOLS_MISSING=true'; exit 1
fi
javac -source 8 -target 8 -classpath "$ANDROID_HOME/platforms/android-30/android.jar" \
  -d "$ROOT/classes" "$ROOT/src/com/temumaexplicacao/pickerprobe/MainActivity.java"
"$BUILD_TOOLS/d8" --min-api 23 --output "$ROOT/dex" \
  "$ROOT/classes/com/temumaexplicacao/pickerprobe/MainActivity.class"
"$BUILD_TOOLS/aapt2" link -o "$ROOT/unsigned.apk" --manifest "$ROOT/AndroidManifest.xml" \
  -I "$ANDROID_HOME/platforms/android-30/android.jar" --min-sdk-version 23 --target-sdk-version 30
(cd "$ROOT/dex" && zip -q -u "$ROOT/unsigned.apk" classes.dex)
"$BUILD_TOOLS/zipalign" -f 4 "$ROOT/unsigned.apk" "$ROOT/aligned.apk"
keytool -genkeypair -keystore "$ROOT/debug.keystore" -storepass android -keypass android \
  -alias pickerprobe -keyalg RSA -keysize 2048 -validity 2 \
  -dname "CN=Temporary TUE CI Test" >/dev/null 2>&1
"$BUILD_TOOLS/apksigner" sign --ks "$ROOT/debug.keystore" \
  --ks-key-alias pickerprobe --ks-pass pass:android --key-pass pass:android \
  --out "$ROOT/pickerprobe.apk" "$ROOT/aligned.apk"
adb install -r "$ROOT/pickerprobe.apk"
echo 'PICKER_PROBE_APP_INSTALLED=true'
echo 'INSTAGRAM_APP_INSTALLED=false'
echo 'INSTAGRAM_CREDENTIALS_USED=false'
