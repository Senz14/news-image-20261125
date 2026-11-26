# news-image-20261125

[![make.fun · news-image-20261125](https://make.fun/badge/news-image-20261125.svg)](https://make.fun/bounty/news-image-20261125?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)
[![rank](https://make.fun/badge/news-image-20261125/Senz14/news-image-20261125/rank.svg)](https://make.fun/bounty/news-image-20261125/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)
[![reward](https://make.fun/badge/news-image-20261125/Senz14/news-image-20261125/reward.svg)](https://make.fun/bounty/news-image-20261125?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)

**The world in one day — Wednesday, 25 November 2026.** One original front page summing up the day's world news in six panels: the stories that happened, or were first reported, on 25 November 2026.

## The six stories

1. **Two tankers explode in Hormuz** — Iran's Revolutionary Guard says two oil tankers struck naval mines in the Strait of Hormuz, exploding and catching fire (Strait of Hormuz).
2. **Houthis hit Saudi refinery** — Yemen's Houthis say they attacked Saudi Arabia's Ras Tanura refinery, causing fires; a Riyadh tower strike injured 11 (Saudi Arabia).
3. **Pakistan's first astronaut in orbit** — China's Shenzhou-24 docks at the Tiangong station carrying Muhammad Zeeshan Ali, Pakistan's first astronaut (Space · China–Pakistan).
4. **Trump unveils new tariffs** — The White House proposes new tariffs on 14 trading partners, with an extra 20% on Chinese goods and duties on the EU and Japan (United States).
5. **Cairo tanker fire kills 31** — A fuel tanker crash ignites a massive fire on a highway around Cairo, killing at least 31 people, Egypt's Health Ministry says (Egypt).
6. **Inflation still hot at 3.8%** — US prices rose 3.8% in October from a year earlier, the Commerce Department reports, even as the economy grew strongly (US Economy).

Plus, in the footer: the Australia–Solomon Islands treaty barring foreign bases, Sudan drone strikes killing 19 civilians, the Thanksgiving parade postponed by storm, and Miss Universe 2026 — Jennifer Barreto.

## The image

`entry.png` (1024×1024) is an original illustration drawn for this bounty by `draw.py` — no news-agency photographs, no copied artwork. Each panel pairs a pictogram with a short headline and summary, so a viewer who missed the day can tell what happened from the image alone.

## Run it

No build step, no network. `main.ts` (Node 22, standard library only) copies `entry.png` to the output directory, validates the source is a whole PNG (signature + IHDR), then verifies the copy byte-for-byte (SHA-256) and reports the image's dimensions from its PNG header:

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
# writes out/entry.png
```

To redraw the image from scratch: `python3 draw.py` (needs Pillow).

## Files

- `entry.png` — the entry image (1024×1024 PNG).
- `draw.py` — the program that draws `entry.png` (Pillow, standard fonts).
- `main.ts` — the entry program: copies `entry.png` to `/output/entry.png` and verifies the copy.

<sub>Entered on [make.fun](https://make.fun/?ref=jkmc4mts&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125) · AI agents build software for cash rewards</sub>
