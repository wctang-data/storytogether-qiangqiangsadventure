#!/usr/bin/env python3

import os
import datetime
import pydub
import re

def main():
    base = "https://wctang-data.github.io/storytogether-qiangqiangsadventure"
    name = "一起說故事 - 強強歷險記"
    _now = datetime.datetime.now()

    rex = re.compile(r'\d+_(.*)\.mp3')

    with open("feed.xml", "w", encoding="utf-8", newline='\n') as out:
        print(f'''<rss xmlns:itunes="http://www.itunes.com/dtds/podcast-1.0.dtd" version="2.0">
<channel>
<title>{name}</title>
<description>{name}</description>
<itunes:image href="{base}/logo.jpg"/>
<link>{base}/</link>
<language/>
<pubDate>{_now}</pubDate>
<author>wctang-data</author>''', file=out)

        idx = 0
        items = []
        for dirpath, _, filenames in os.walk("."):
            dirpath = dirpath[2:]
            if dirpath.startswith(".git"):
                continue
            for filename in filenames:
                if not (m := rex.match(filename)):
                    continue
                info = pydub.utils.mediainfo(f'{filename}')
                items.append((f'{m[1]}', filename, info["size"], info["duration"]))

        for idx, item in enumerate(items):
            print(f'<item><title>{item[0]}</title><pubDate>{_now+datetime.timedelta(days=-len(items)+idx)}</pubDate><enclosure url="{base}/{item[1]}" type="audio/mpeg" length="{item[2]}"/><itunes:duration>{int(float(item[3]))}</itunes:duration></item>', file=out)

        print('''</channel>
</rss>''', file=out)


if __name__ == '__main__':
    main()
