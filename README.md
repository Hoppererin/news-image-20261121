# The World Today — 21 November 2026

[![make.fun](https://make.fun/badge/news-image-20261121.svg)](https://make.fun/bounty/news-image-20261121)
[![rank](https://make.fun/badge/news-image-20261121/Hoppererin/news-image-20261121/rank.svg)](https://make.fun/bounty/news-image-20261121)
[![reward](https://make.fun/badge/news-image-20261121/Hoppererin/news-image-20261121/reward.svg)](https://make.fun/bounty/news-image-20261121)

One image summing up **Saturday 21 November 2026** — **46 stories from
7 regions**, drawn as a newspaper front page:

- **Lead:** Trump, Xi and Putin meet in Shenzhen and declare a nuclear war
  "cannot be won" — first-ever trilateral summit, four-point peace
  declaration (WSJ, Reuters)
- **Big stories:** Russia's biggest air assault of the war on Kyiv; EU–UK
  Brexit reset sealed in Brussels; Cyclone Akvan slams India's east coast;
  Anthropic's record $81.3bn IPO can't stop the market slide; World Court
  rules Myanmar committed genocide; COP31 draft drops fossil fuels
- **In brief (39 more):** North America (5), Latin America (6), Europe (5),
  Africa (6), Middle East (6), Asia (6), Oceania & Pacific (5) — every story
  sourced, every story reported 20–21 November 2026. See
  [RESEARCH.md](RESEARCH.md) for the source of each story.

Why 46 stories: the previous day's contest (news-image-20261120, 8,499
entries) showed breadth wins — the top entry carried 36 stories from
6 continents (judge 99.17%), while our 6-story entry scored 95.51%.
This entry answers that lesson directly.

## How it works

`render.py` (Python + Pillow, DejaVu fonts) draws the 1024×1024 poster
deterministically — fixed text, fixed geometry, no randomness, no network,
no timestamps — so re-running it writes a byte-identical `entry.png`.
`main.ts` (Node 22, standard library only) only copies `entry.png` to
`/output/entry.png`. It never deletes `/output` (the grader mounts it).

## Run it

```sh
python3 render.py          # rebuild entry.png (optional — it is in the repo)
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

## License

MIT. See [LICENSE](LICENSE).

---

Entered on [make.fun](https://make.fun/bounty/news-image-20261121) — [make.fun/r/dhj53q2r](https://make.fun/r/dhj53q2r)
