#!/system/bin/sh
set -eu
BB=/system/xbin/busybox
ORIGINAL=f3820e6c7547df588518ae003a5d956e958bf27457dd13efbc1fdad9efd5c1ac
PATCHED=725991af7371f2747065a4ee4fba45a49ff4a7c349cbd5d542620c5818a63148
LIB=/system/lib/librockbox.so
BACKUP=/data/local/y1-gallery/librockbox-original.so
digest() { "$BB" sha256sum "$1" | "$BB" cut -d ' ' -f 1; }
[ "$(id -u)" = 0 ] || { echo 'STOP: root shell required'; exit 1; }
[ -x "$BB" ] || { echo 'STOP: BusyBox unavailable'; exit 1; }
[ "$(digest "$LIB")" = "$PATCHED" ] || { echo 'STOP: installed library is not our patch'; exit 1; }
[ "$(digest "$BACKUP")" = "$ORIGINAL" ] || { echo 'STOP: original backup unavailable or wrong'; exit 1; }
am force-stop org.rockbox || true
"$BB" mount -o remount,rw /system
trap '"$BB" mount -o remount,ro /system' EXIT
[ ! -e "$LIB.galleria-restore" ] || { echo 'STOP: stale temporary file'; exit 1; }
"$BB" cp "$BACKUP" "$LIB.galleria-restore"
"$BB" chown 0:0 "$LIB.galleria-restore"
"$BB" chmod 644 "$LIB.galleria-restore"
[ "$(digest "$LIB.galleria-restore")" = "$ORIGINAL" ] || { echo 'STOP: restored copy failed verification'; exit 1; }
"$BB" mv "$LIB.galleria-restore" "$LIB"
"$BB" sync
"$BB" mount -o remount,ro /system
trap - EXIT
[ "$(digest "$LIB")" = "$ORIGINAL" ] || { echo 'STOP: final hash mismatch'; exit 1; }
echo 'Original Rockbox library restored. Reopen Rockbox.'
