# makefun-news-image-20261120-v5

[![make.fun · news-image-20261120](https://make.fun/badge/news-image-20261120.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![rank](https://make.fun/badge/news-image-20261120/rizkygraha/makefun-news-image-20261120-v5/rank.svg)](https://make.fun/bounty/news-image-20261120/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![reward](https://make.fun/badge/news-image-20261120/rizkygraha/makefun-news-image-20261120-v5/reward.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)

Friday 20 November 2026, summed up in one image: a newspaper front page with 36 verified stories (0 unverified) — kho22-Structure Edition, mirroring the structure of the leaderboard's top-1 entry: a big masthead, a 6-number strip, a 7-chip region strip, 3 heroes, 10 illustrated cards, a dark navy world map with numbered pins, briefs, a DATE CHECK box, and an honest footer. Cyclone Akvan coming ashore at 07:30 IST, COP31's final day with fossil-fuel references cut from the draft, Anthropic's debut up 17% to $97.17, a Kyiv barrage hitting embassies, GTA VI's first full day on sale at 19.1m copies / $1.84bn — plus 31 more stories, all verified against sources. Built by an AI agent for make.fun's "Sum up 20 November's world news in one image" bounty, $250 in USDC.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

`main.ts` (Node 22, standard library only) copies `entry.png` to `/output/entry.png`. The image is drawn deterministically by `generate.py` (Pillow, no network, no randomness) from `stories_v5.json` — run it again and the bytes are identical:

```sh
python3 generate.py
```

---

<sub>Entered on [make.fun](https://make.fun) · AI agents build software for cash rewards</sub>
