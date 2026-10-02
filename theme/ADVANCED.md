# Optional: smoother Galleria transitions on one tested Y1 build

**This step modifies a system library. The theme and PictureFlow work without it.** It was tested on the author’s Innioasis Y1, Rockbox build `230f848142-260516`, with the exact original `/system/lib/librockbox.so` whose SHA-256 is:

```
f3820e6c7547df588518ae003a5d956e958bf27457dd13efbc1fdad9efd5c1ac
```

The patch changes three timing constants (menu wait 100→3 ticks, file-browser wait 50→3, SBS minimum refresh 14→2). On the tested device, the output SHA-256 is:

```
725991af7371f2747065a4ee4fba45a49ff4a7c349cbd5d542620c5818a63148
```

The patcher refuses any different hash or instruction and writes nothing if validation fails. Do not attempt to adapt the byte offsets to another build without analyzing its source and binary. A system update may replace this library; more frequent menu updates may affect battery life. A rooted ADB shell and a known recovery route are required. The commands below are for someone comfortable restoring the Y1 if Rockbox stops launching.

## Create and retain an off-device backup

Connect the Y1 with ADB and, from this `theme` directory:

```sh
adb shell id
adb pull /system/lib/librockbox.so librockbox-original.so
python3 tools/patch_refresh.py librockbox-original.so librockbox-smooth.so
```

Stop if `adb shell id` does not show `uid=0(root)`. Keep `librockbox-original.so` on your computer. `patch_refresh.py` will stop if it is not the precise tested file. On Windows, use `py tools\patch_refresh.py librockbox-original.so librockbox-smooth.so`.

## Install only after the patcher succeeds

```sh
adb push librockbox-smooth.so /data/local/tmp/librockbox-smooth.so
adb push tools/install_checked.sh /data/local/tmp/install_checked.sh
adb shell sh /data/local/tmp/install_checked.sh
```

`install_checked.sh` checks root, the original and staged hashes, makes a second original backup at `/data/local/y1-gallery/librockbox-original.so`, stops Rockbox, replaces the library atomically, restores `/system` to read-only and verifies the final hash. It does not run if the current library is unknown. Open Rockbox again and check the menus and playback.

## Restore the original

If the patched build runs but you want to undo it:

```sh
adb push tools/restore_checked.sh /data/local/tmp/restore_checked.sh
adb shell sh /data/local/tmp/restore_checked.sh
```

This restore script only operates if both the installed patched file and the device backup have their expected hashes. It stops Rockbox, atomically puts back the original library, remounts `/system` read-only and verifies it. Keep the off-device backup even after restoring. If Rockbox no longer launches, use the Y1’s normal recovery route before trying another system change.

No Rockbox binaries are included in this repository. The Python script is a transparent, exact-build transform applied to a library from your own device.
