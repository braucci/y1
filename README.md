# hack my Y1

An Innioasis Y1 project by **Biagio Raucci**.

An English, single-page tutorial for turning the Innioasis Y1’s Rockbox 360p iClassic theme into **iClassic Galleria** and using Rockbox **PictureFlow** as a wheel-controlled album browser.

The website is plain HTML, CSS and JavaScript; no build step or backend is needed. The site includes real screenshots from the author’s Y1, an interactive progress checklist, and a downloadable theme add-on containing original demo artwork and a generator for personal album covers.

## Put it on GitHub Pages

1. Extract the outer `hack-my-Y1-github.zip` on your computer. Upload the **contents** of the extracted `hack-my-y1` folder to the root of a GitHub repository. Keep `index.html`, `assets/`, `theme/` and `downloads/` together. Uploading the ZIP without extracting it will not create the page.
2. On GitHub, open **Settings → Pages**, choose **Deploy from a branch**, select `main` and `/ (root)`, then save.
3. Open the Pages URL GitHub gives you. The theme download button links to `downloads/iClassic-Galleria-theme.zip` in the same repository, so it works without editing the HTML.

You can also open `index.html` locally. The Google font import is optional; system fonts are used if it cannot load. The page has no tracking or external scripts.

## Where to edit later

- `index.html`: tutorial text, links and sections.
- `assets/styles.css`: layout, colours and responsive design.
- `assets/main.js`: carousel, menu, copy button and local checklist.
- `assets/images/`: original screenshots used by the page.
- `theme/`: theme source, generator, demo covers, patch scripts and instructions.
- `downloads/iClassic-Galleria-theme.zip`: the ready-to-download copy of `theme/`. Rebuild this ZIP if you edit theme files.

The website shows album covers only inside screenshots of a personal Y1 for tutorial context. The downloadable theme contains original abstract demo sleeves, not commercial album art. The base iClassic theme and Rockbox are obtained separately from their respective projects.

## Credit and scope

iClassic: Humberto Santana; Y1 360p adaptation: CarlosPixel; iLike elements: Alan Brito and H. Pearce. The iClassic-derived theme adaptation is shared under [CC BY-SA 3.0](https://creativecommons.org/licenses/by-sa/3.0/). The exact-build refresh patch is optional and includes no Rockbox binary.
