#!/usr/bin/env bash
# Builds the 30× to Remember APK with the plain Android SDK tools (no Gradle).
# Needs ANDROID_HOME (or ANDROID_SDK_ROOT) with a platform and build-tools installed.
# Usage: android/build.sh <versionCode> <versionName> <out.apk>
set -euo pipefail
cd "$(dirname "$0")"
CODE="${1:-1}"; NAME="${2:-dev}"; OUT="${3:-build/30x-to-remember.apk}"
SDK="${ANDROID_HOME:-${ANDROID_SDK_ROOT:?set ANDROID_HOME}}"
BT="$(ls -d "$SDK"/build-tools/* | sort -V | tail -1)"
PLAT="$(ls -d "$SDK"/platforms/android-* | grep -E 'android-[0-9]+$' | sort -V | tail -1)"
JAR="$PLAT/android.jar"
echo "build-tools: $BT"; echo "platform: $PLAT"
rm -rf build && mkdir -p build/res build/classes build/gen build/dex
"$BT/aapt2" compile --dir res -o build/res.zip
"$BT/aapt2" link -I "$JAR" --manifest AndroidManifest.xml -A assets \
  --min-sdk-version 24 --target-sdk-version 34 \
  --version-code "$CODE" --version-name "$NAME" \
  --java build/gen -o build/unsigned.apk build/res.zip
javac -encoding UTF-8 -source 8 -target 8 -Xlint:-options -bootclasspath "$JAR" -cp "$JAR" \
  -d build/classes $(find src build/gen -name '*.java')
"$BT/d8" --release --min-api 24 --lib "$JAR" --output build/dex $(find build/classes -name '*.class')
(cd build/dex && zip -q -j ../unsigned.apk classes.dex)
"$BT/zipalign" -f -p 4 build/unsigned.apk build/aligned.apk
if [ -n "${KEYSTORE_FILE:-}" ]; then
  KS="$KEYSTORE_FILE"; KSPASS="${KEYSTORE_PASS:?}"; ALIAS="${KEY_ALIAS:-toremember}"
else
  echo "No KEYSTORE_FILE given: signing with a throwaway key (fine for testing, but it can't update over an earlier install)."
  KS=build/throwaway.jks; KSPASS=throwaway; ALIAS=toremember
  keytool -genkeypair -keystore "$KS" -storepass "$KSPASS" -keypass "$KSPASS" -alias "$ALIAS" \
    -keyalg RSA -keysize 2048 -validity 10000 -dname "CN=Kralnu Games" >/dev/null 2>&1
fi
mkdir -p "$(dirname "$OUT")"
"$BT/apksigner" sign --ks "$KS" --ks-pass "pass:$KSPASS" --ks-key-alias "$ALIAS" --out "$OUT" build/aligned.apk
"$BT/apksigner" verify "$OUT"
echo "Built $OUT"
