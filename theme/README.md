# iClassic Galleria for Innioasis Y1

This is the downloadable **add-on** behind [hack my Y1](../index.html). It was derived from CarlosPixel’s iClassic 1.4 360p theme, itself based on Humberto Santana’s iClassic. The theme skin and artwork layout are shared under [CC BY-SA 3.0](https://creativecommons.org/licenses/by-sa/3.0/). Additional iLike credits: Alan Brito and H. Pearce.

The package ships original abstract demo covers. It does **not** contain the original iClassic assets, music, commercial album covers, the PictureFlow plugin or any Rockbox binary.

## Install the menu gallery

1. Install Rockbox for the **Innioasis Y1 360p** screen and install [iClassic v1.4 360p](https://github.com/rockbox-y1/themes/tree/main/iClassic_v1.4_360p/.rockbox). Confirm that iClassic works first.
2. Back up the player’s existing `.rockbox` folder.
3. Copy the **contents** of this package’s `.rockbox` directory into the player’s existing `.rockbox` directory. Merge folders. Do not replace the entire player directory.
4. Safely disconnect and choose **Settings → Theme Settings → Browse Themes → iClassic Galleria**.

The demo is ready to use. The left-hand menu and now-playing screen still rely on the original iClassic files: `.rockbox/wps/iClassic.wps`, `.rockbox/wps/iClassic/Battery.bmp`, `.rockbox/wps/iClassic/Hold Icon.bmp`, `.rockbox/wps/iClassic/Playing Status.bmp`, plus iClassic’s font, icons and backdrop.

## Use your own covers in the menu

On the computer, make a directory named `my-covers` inside this `theme` directory. Add between **2 and 43** image files (`.jpg`, `.jpeg`, `.png`, `.webp` or `.bmp`). Prefer names like `Artist - Album - 2025.jpg`; the year is optional. Other names also work, though the panel will use `MY LIBRARY` as the artist when it cannot split the filename.

From this `theme` directory, run:

```sh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python tools/build_gallery.py --covers my-covers
```

On Windows, use `py -m venv .venv`, `.venv\Scripts\activate`, and `python tools\build_gallery.py --covers my-covers` for the corresponding commands. The generator writes a new `.rockbox/wps/iClassic_Galleria.sbs` and the `soft/fade*.bmp` images. Copy those generated files into the player’s matching paths and reapply the theme. If you reduce the number of covers, remove any leftover old `fade*.bmp` files from the player’s `.rockbox/wps/iClassic_Galleria/soft` folder; the new skin only references its current files.

`python tools/build_gallery.py --covers my-covers --seed 17` creates a different, repeatable shuffled order. The sequence advances in ten-second clock slots. The transition uses sixteen pre-rendered frames and a four-pixel horizontal drift. More covers produce larger BMP files and can take longer to copy. The script modifies no audio files, tags or Rockbox firmware.

## PictureFlow is separate

After adding music, update Rockbox’s database. Open **Plugins → Demos → PictureFlow** to browse albums with the wheel. If artwork changes, use PictureFlow’s **Update Cache** or **Rebuild Cache**. This `.rockbox` add-on does not modify that plugin or its cache. Its menu gallery uses only images provided to the generator, so new albums require a new gallery build.

## Optional smooth refresh patch

Without the patch, the theme still shows the gallery, but the 16-frame fade may look stepped. The exact-build advanced patch and guarded restore process are in [ADVANCED.md](ADVANCED.md). It is not needed for themes or PictureFlow. No patched Rockbox binary is distributed.

## Undo

Select the original **iClassic** theme in Rockbox. You may then remove `iClassic Galleria.cfg`, `iClassic_Galleria.sbs` and the `iClassic_Galleria/soft` folder from the player after verifying that iClassic works. If you separately applied the refresh patch, use the guarded restore instructions in `ADVANCED.md`.
