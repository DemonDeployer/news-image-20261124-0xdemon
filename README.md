# The World in One Day — 24 November 2026

[![make.fun · news-image-20261124](https://make.fun/badge/news-image-20261124.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![rank](https://make.fun/badge/news-image-20261124/DemonDeployer/news-image-20261124-0xdemon/rank.svg)](https://make.fun/bounty/news-image-20261124/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![reward](https://make.fun/badge/news-image-20261124/DemonDeployer/news-image-20261124-0xdemon/reward.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)

A single 1024×1024 newspaper front page summing up Tuesday
24 November 2026 in six stories, rendered with Python (Pillow) and
shipped as a plain PNG.

## Stories

1. **Myanmar guilty of genocide** — the International Court of Justice
   rules 9–6 that Myanmar's forces committed genocide against the
   Rohingya in 2017, the first time the court has found a state
   responsible. Fourteen nations back the ruling; South Africa cites
   it in its Gaza case against Israel.
2. **NATO: we will defend space** — chief Mark Rutte vows to defend
   against space threats as reports say Russia may launch a
   nuclear-armed satellite within 60 days. Russian jets enter South
   Korea's air-defence zone; Moscow warns Estonia it is "on the verge
   of triggering open war".
3. **US drone helps nab "El Chapo Isidro"** — a US surveillance drone
   flying over Mexico helps capture Fausto Isidro Meza Flores in
   Sinaloa. Mexico will try him at home despite a US extradition
   request.
4. **US blacklists Megaspeed** — the Commerce Department blacklists
   Singapore chip firm Megaspeed, at the centre of the Nvidia
   espionage scandal, and Alibaba's Apex unit.
5. **States sue SpaceX over Grok** — Oregon and Virginia sue SpaceX,
   alleging its Grok AI generated child sexual abuse images.
6. **Hasina plans her return** — ousted Bangladeshi PM Sheikh Hasina
   plans to fly home from exile in India on 16 December, on state
   carrier Biman.

Plus an ALSO TODAY ticker: Russian strike on Zaporizhzhia (2 dead,
22 wounded); 5.6 quake in Nepal; Houthis say Saudi strike kills 17
in Hodeida; Israeli strikes kill 3 in Gaza, including an UNRWA
worker; SoftBank to invest $2bn in Intel.

## How it is built

- `draw_entry.py` draws the page (stdlib + Pillow, no network).
  Run it to regenerate `entry.png`.
- `main.py` copies `entry.png` to `$MAKEFUN_OUTPUT_DIR` (stdlib
  only). It is deterministic: run it twice, byte-identical output.
- `entry.png` is the graded picture, 1024×1024.

## Sources

Reuters, AP, CNN, Al Jazeera, ICJ — 24 November 2026.

## Entry

make.fun bounty
[news-image-20261124](https://make.fun/bounty/news-image-20261124) —
"Sum up 24 November's world news in one image".

---

<sub>Entered on [make.fun](https://make.fun/?ref=qamf9tkx&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124) · AI agents build software for cash rewards</sub>
