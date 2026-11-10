#!/usr/bin/env python3
"""将 bishun_data/ 下按单字划分的 JSON 合并为按 Unicode 区段（codepoint >> 8）划分的 bundle 文件。

用法: python3 bundle_bishun.py
输出: bishun_bundle/b<index>.json，结构为 { "字": { "strokes": [...], ... }, ... }
"""
import json
import os
import sys
from collections import defaultdict

SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)), "bishun_data")
DST = os.path.join(os.path.dirname(os.path.abspath(__file__)), "bishun_bundle")

if not os.path.isdir(SRC):
    sys.exit("未找到 bishun_data 目录")

os.makedirs(DST, exist_ok=True)

bundles = defaultdict(dict)
total = 0
for name in os.listdir(SRC):
    if not name.endswith(".json"):
        continue
    ch = name[:-5]  # 去掉 .json
    with open(os.path.join(SRC, name), "r", encoding="utf-8") as f:
        data = json.load(f)
    if not isinstance(data, dict):
        continue
    idx = ord(ch[0]) >> 8
    bundles[idx][ch] = data
    total += 1

count = 0
for idx, chars in sorted(bundles.items()):
    out = os.path.join(DST, "b%d.json" % idx)
    with open(out, "w", encoding="utf-8") as f:
        json.dump(chars, f, ensure_ascii=False, separators=(",", ":"))
    count += 1

print("完成：%d 个单字文件 -> %d 个 bundle 文件" % (total, count))
