#!/system/bin/sh
# Optional advanced step. Run as root on the exact tested Y1 build only.
set -eu
BB=/system/xbin/busybox
ORIGINAL=f3820e6c7547df588518ae003a5d956e958bf27457dd13efbc1fdad9efd5c1ac
PATCHED=725991af7371f2747065a4ee4fba45a49ff4a7c349cbd5d542620c5818a63148
LIB=/system/lib/librockbox.so
STAGED=/data/local/tmp/librockbox-smooth.so
BACKUP=/data/local/y1-gallery/librockbox-original.so
digest() { "$BB" sha256sum "$1" | "$BB" cut -d ' ' -f 1; }
[ "$(id -u)" = 0 ] || { echo 'STOP: root shell required'; exit 1; }
[ -x "$BB" ] || { echo 'STOP: BusyBox unavailable'; exit 1; }
[ "$(digest "$LIB")" = "$ORIGINAL" ] || { echo 'STOP: installed library is not the tested original'; exit 1; }
[ "$(digest "$STAGED")" = "$PATCHED" ] || { echo 'STOP: staged patch has wrong hash'; exit 1; }
"$BB" mkdir -p /data/local/y1-gallery
"$BB" chmod 700 /data/local/y1-gallery
if [ -e "$BACKUP" ]; then
  [ "$(digest "$BACKUP")" = "$ORIGINAL" ] || { echo 'STOP: existing backup has wrong hash'; exit 1; }
else
  "$BB" cp "$LIB" "$BACKUP"
  "$BB" chmod 600 "$BACKUP"
fi
[ "$(digest "$BACKUP")" = "$ORIGINAL" ] || { echo 'STOP: backup verification failed'; exit 1; }
am force-stop org.rockbox || true
"$BB" mount -o remount,rw /system
trap '"$BB" mount -o remount,ro /system' EXIT
[ ! -e "$LIB.galleria-new" ] || { echo 'STOP: stale temporary file'; exit 1; }
"$BB" cp "$STAGED" "$LIB.galleria-new"
"$BB" chown 0:0 "$LIB.galleria-new"
"$BB" chmod 644 "$LIB.galleria-new"
[ "$(digest "$LIB.galleria-new")" = "$PATCHED" ] || { echo 'STOP: copied patch failed verification'; exit 1; }
"$BB" mv "$LIB.galleria-new" "$LIB"
"$BB" sync
"$BB" mount -o remount,ro /system
trap - EXIT
[ "$(digest "$LIB")" = "$PATCHED" ] || { echo 'STOP: final hash mismatch'; exit 1; }
echo 'Refresh patch installed and verified. Reopen Rockbox.'
