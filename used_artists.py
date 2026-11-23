#!/usr/bin/env python3
"""おすすめ済みのアーティストを数える（2026-11-23 本人指示「おすすめのアーティストが被らないように」）。

決まり: 1 組のアーティストは、サイト全体で 1 つの記事でしかおすすめしない（[[shop:<名前> CD|…]] で数える）。
その記事の主役（「〇〇が好きな人に」の〇〇）は数えない。

使い方:
  python3 used_artists.py            … おすすめ済みの一覧と、2 回以上の被り
  python3 used_artists.py --free     … ~/knowledge-os/wiki に経歴があり、まだおすすめしていない人
  python3 used_artists.py --check    … 被りがあれば終了コード 1
"""
import re, sys, glob, os
from collections import defaultdict
HERE = os.path.dirname(os.path.abspath(__file__))
WIKI = os.path.expanduser("~/knowledge-os/wiki")
used = defaultdict(list)
for f in sorted(glob.glob(os.path.join(HERE, "content", "*.md"))):
    slug = os.path.basename(f)[11:-3]
    for a in dict.fromkeys(re.findall(r"\[\[shop:(.+?) CD\|", open(f, encoding="utf-8").read())):
        used[a].append(slug)
dups = {a: s for a, s in used.items() if len(s) > 1}
if "--free" in sys.argv:
    for p in sorted(glob.glob(os.path.join(WIKI, "*の経歴.md"))):
        n = os.path.basename(p)[:-len("の経歴.md")]
        if n not in used:
            print(n)
elif "--check" in sys.argv:
    for a, s in sorted(dups.items(), key=lambda x: -len(x[1])):
        print("被り %d: %s … %s" % (len(s), a, ", ".join(s)))
    sys.exit(1 if dups else 0)
else:
    for a, s in sorted(used.items()):
        print("%s … %s" % (a, ", ".join(s)))
    print("\n被り: %d 組" % len(dups))
