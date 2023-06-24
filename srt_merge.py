import argparse
import sys
from datetime import timedelta
from pathlib import Path

# REQUIRED MODULE: pip3 install srt
import srt


def nearest(items, pivot):
    return min(items, key=lambda x: abs(x.start - pivot))


if __name__ == '__main__':
    id = 'aUBawr1hUwo'
    path_zh = "static/" + id + "/" + id + ".zh-CN.vtt"
    path_en = "static/" + id + "/" + id + ".en.vtt"

    srt1_path = Path(path_zh)
    srt2_path = Path(path_en)

    with srt1_path.open(encoding='utf-8') as fi1:
        subs1 = {s.index: s for s in srt.parse(fi1)}

    with srt2_path.open(encoding='utf-8') as fi2:
        subs2 = {s.index: s for s in srt.parse(fi2)}

    # iterate all subs in srt2 and find the closest EXISTING slot in srt1
    sub: srt.Subtitle
    start: int
    for idx, sub in subs2.items():
        start: timedelta = sub.start
        sub_nearest_slot: srt.Subtitle = nearest(subs1.values(), start)
        sub_nearest_slot.content = f'{sub_nearest_slot.content}<br>{sub.content}'
        subs1[sub_nearest_slot.index] = sub_nearest_slot

    generated_srt = Path("static/" + id + "/" + id + ".bi.vtt")

    with generated_srt.open(mode='w', encoding='utf-8') as fout:
        fout.write(srt.compose(list(subs1.values())))
