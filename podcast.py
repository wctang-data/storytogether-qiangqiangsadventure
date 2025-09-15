#!/usr/bin/env python3

from pprint import pprint
import os
import datetime
import re
import pydub
from dotenv import load_dotenv
from xml.etree import ElementTree

RFC822 = "%a, %d %b %Y %H:%M:%S %z"


def main():
    load_dotenv(override=True)

    name = os.getenv("PODCAST_NAME")
    base = f"https://wctang-data.github.io/{os.getenv('REPO_NAME')}"
    rex = re.compile(r'^(.*)\.(mp3|m4a)$')

    items = {}
    for dirpath, _, filenames in os.walk("."):
        dirpath = dirpath[2:]
        if dirpath.startswith(".git"):
            continue
        for filename in filenames:
            if not (m := rex.match(filename)):
                continue

            info = pydub.utils.mediainfo(f'{filename}')
            items[filename] = [m[1], info["size"], info["duration"], None]

    # print(items)

    # old_items = {}
    if os.path.exists("feed.xml"):
        with open("feed.xml", "r", encoding="utf-8") as f:
            xx = ElementTree.fromstring(f.read())
            for item in xx.findall(".//item"):
                url = item.find("enclosure").get("url")
                filename = url[url.rfind("/")+1:]
                # pub = datetime.datetime.strptime(, RFC822)

                if filename in items:
                    items[filename][3] = item.find("pubDate").text


    _now = datetime.datetime.now().astimezone()
    for filename, vv in items.items():
        if vv[3] is None:
            vv[3] = datetime.datetime.strptime(filename[:8], "%Y%m%d").replace(tzinfo=_now.tzinfo).strftime(RFC822)
            # print(filename, vv[3])


    with open("feed.xml", "w", encoding="utf-8", newline='\n') as out:
        print(f'<rss xmlns:itunes="http://www.itunes.com/dtds/podcast-1.0.dtd" version="2.0"><channel><title>{name}</title><description>{name}</description><itunes:image href="{base}/logo.png"/><link>{base}/</link><language/><pubDate>{_now.strftime(RFC822)}</pubDate><author>wctang-data</author>', file=out)
        for filename, vv in sorted(items.items()):
            print(f'<item><title>{vv[0]}</title><pubDate>{vv[3]}</pubDate><enclosure url="{base}/{filename}" type="audio/mpeg" length="{vv[1]}"/><itunes:duration>{int(float(vv[2]))}</itunes:duration></item>', file=out)
        print('</channel></rss>', file=out)

    with open("index.html", "w", encoding="utf-8", newline='\n') as out:
        print(f'<!DOCTYPE html><html><head><title>{name}</title></head><body><h1>{name}</h1><p><img src="{base}/logo.png" /></p><a href="{base}/feed.xml">feed</a><ul>', file=out)
        for filename, vv in sorted(items.items()):
            print(f'<li><a href="{base}/{filename}">{vv[0]}</a></li>', file=out)
        print(f'</ul></body><p>{_now}</p></html>', file=out)


if __name__ == '__main__':
    main()
