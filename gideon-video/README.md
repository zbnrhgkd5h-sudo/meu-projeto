# GIDEON Systems: launch film

A 48-second motion-graphics launch video (1920×1080, 60 fps, with soundtrack) for
**GIDEON Systems**, institutional derivatives trading middleware ([gideon.systems](https://gideon.systems)).

**Final video:** [`gideon-launch.mp4`](gideon-launch.mp4)

## Storyboard (120 BPM, cuts on the beat)

| Time | Scene |
|---|---|
| 0–4 s | Cold open: a field of noisy orders (32,000 per session) collapses into one precise green line. "Precision scales." |
| 4–8 s | Logo: the G mark draws on, GIDEON decodes letter by letter, then the tagline and CME status bar |
| 8–13 s | "Your strategy decides. GIDEON executes." The site's execution log types out live, ending in a tier-2 kill |
| 13–18 s | 01 How it works: signal sources → risk gate → CME Globex, with packets flowing and one blocked at the loss floor |
| 18–23 s | 02 Four-tier kill switch: Pause → Reduce → Flatten → Emergency Stop escalate on the beat |
| 23–30 s | 03 Audit trail: every record gets sealed, then CSV / JSON / SQL export ("Your data is yours.") |
| 30–35 s | The real gideon.systems site scrolls in a browser, flanked by the six pillars |
| 35–39 s | 04 Compliance by design: CFTC · NFA · CME Group · SEC 15c3-5, and what GIDEON is not |
| 39–43 s | 300 precise orders vs 32,000 noisy ones; 73,226 lines · 4+ yrs · iLink/MDP |
| 43–48 s | "Beta onboarding is open." REQUEST ACCESS, gideon.systems, and the site's own legal disclaimer |

All copy, figures and log lines come from gideon.systems. The fonts are the site's own
(Space Grotesk, IBM Plex Sans, JetBrains Mono), and so are the palette (#0A0C0B / #3FD68F) and
the grid. `assets/site/full.webp` is a full-page capture of the live site, rendered locally.
Third-party names (CME, Rithmic, CQG, TT) appear as text only, as they do on the site.

## Rebuild

Requires Node 18+, Python 3 with `numpy scipy pillow`, and `ffmpeg`
(or `pip install imageio-ffmpeg` and `FFMPEG=$(python3 -c "import imageio_ffmpeg;print(imageio_ffmpeg.get_ffmpeg_exe())")`).

```bash
npm install                      # Playwright (headless Chromium)
python3 music.py                 # synthesized soundtrack → music.wav
npm run render                   # renders every frame → gideon-launch.mp4
node render.mjs --preview 5,20   # PNG stills of specific frames in previews/
```

Open `index.html` in a browser to watch it live, or use `index.html?t=12.5` to freeze a frame.
