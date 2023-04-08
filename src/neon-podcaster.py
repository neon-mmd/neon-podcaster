#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""A command line podcast client"""

# ------------------imports--------------------
from os.path import exists, expanduser
from os import mkdir, remove, system
from typing import Tuple
from feedparser import parse
from csv import reader, writer
from subprocess import getoutput
from argparse import ArgumentParser
from re import sub

# -----------------defining some variables--------------------------
CACHE_FILE: str = expanduser("~/.cache/temp.csv")
FEED_FILE: str = expanduser("~/.config/neonPodcaster/feeds.csv")
DEFAULT_VOLUME: int = 30
DEFAULT_LAUNCHER: str = "dmenu -l 20"

# ------------------The working code----------------------------------


def podcast_client() -> None:
    """A function which handles the launching and playing of the podcast client by first giving
    him the channel list to choose from using the config file and then using the channel name and
    config file to retrieve that channel's rss feed url and then fetching the rss feed and wrtting
    it into a temporary/cache file and then showing the list of episodes using the cache file
    and then allowing the user to choose from it and then using the episode name and cache file
    to retrieve it's url respectively and playing it in mpv"""

    optionList: str = (
        f"{chr(10).join(map(lambda line: line[0], reader(open(FEED_FILE))))}\nquit"
    )

    link = ""
    ans = getoutput(f"echo -e '{optionList}' | {DEFAULT_LAUNCHER}")
    if ans in ("quit", ""):
        exit()
    else:
        link: str = next(
            filter(lambda line: line[0] == "Coldfusion", reader(open(FEED_FILE)))
        )[1]

    with open(CACHE_FILE, "w") as f:
        f.write(
            "\n".join(
                map(lambda entry: f"{entry.title}~{entry.link}", parse(link).entries)
            )
        )

    optionList: str = f"{chr(10).join(map(lambda line: line[0], reader(open(CACHE_FILE),delimiter='~')))}\nquit"

    answer: str = getoutput(f'echo -e "{optionList}" | {DEFAULT_LAUNCHER}')
    if answer in ("quit", ""):
        exit()
    else:
        link: str = next(
            filter(
                lambda row: row[0] == sub(r"[\"]", "", row[0]),
                reader(open(CACHE_FILE), delimiter="~"),
            )
        )[1]

    system(f'mpv --no-video "{link}" --volume={DEFAULT_VOLUME}')


# ----------------------build podcast channel feed list-------------------


def buildFeedForPodcast() -> None:
    """A function which handles the building of the config file and writing of the
    config file (if it already exists) by taking the entries of {channel_name} and
    {channel_rss_feed_url}"""

    if not exists(expanduser("~/.config/neonPodcaster")):
        mkdir(expanduser("~/.config/neonPodcaster"))

    numberOfFeeds: int = int(input("enter the number of feeds to add: "))
    csv_writer = writer(open(FEED_FILE, "a"))

    for _ in range(numberOfFeeds):
        channel_name: str = input("Channel Name: ")
        channel_rss_feed_url: str = input("Url: ")
        csv_writer.writerow((channel_name, channel_rss_feed_url))


# ---------------------delete a podcast channel from feed list---------------


def DelPodChannelFromFeedFile() -> None:
    """A function which deletes the selected channel name from the config file"""

    tempList: Tuple = tuple(reader(open(expanduser(FEED_FILE))))
    optionList: str = f"{chr(10).join(map(lambda line: line[0], tempList))}\nquit"

    ans: str = getoutput(f"echo -e '{optionList}' | {DEFAULT_LAUNCHER}")
    if ans in ("quit", ""):
        exit()
    else:
        remove(FEED_FILE)
        csv_writer = writer(open(FEED_FILE, "w"))
        csv_writer.writerows(filter(lambda line: line[0] != ans, tempList))


# -------------------------parse the arguments------------------------
parser = ArgumentParser(description="A command line Podcast Client App")
parser.add_argument("-p", help="run the podcast client", action="store_true")
parser.add_argument(
    "-b", help="build the podcast channel feed file", action="store_true"
)
parser.add_argument("-l", help="provide the launcher to use (default: 'dmenu -l 20')")
parser.add_argument(
    "-v", help="provide the default volume to launch with (default: '30')", type=int
)
parser.add_argument(
    "-d", help="delete a podcast channel from the feed file", action="store_true"
)
args = parser.parse_args()

if args.l:
    DEFAULT_LAUNCHER: str = args.l
if args.v:
    DEFAULT_VOLUME: int = args.v
if args.b:
    buildFeedForPodcast()
if args.p:
    podcast_client()
if args.d:
    DelPodChannelFromFeedFile()
