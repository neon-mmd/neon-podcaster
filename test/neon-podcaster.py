#!/usr/bin/env python

# ------------------imports--------------------
import os
from feedparser import parse
import csv
import subprocess
from argparse import ArgumentParser
from re import sub

# -----------------defining some variables--------------------------
cacheFilePath = os.path.expanduser("~/.cache/temp.csv")
feedFilePath = os.path.expanduser("~/.config/neonPodcaster/feeds.csv")
defaultVolume = 30
launcher = "dmenu -l 20"

# ------------------The working code----------------------------------


def podcast_client():
    # Put all the podcast channel names list in the launcher of choice and ask the user to choose one
    optionList = ""
    with open(feedFilePath) as f:
        reader = csv.reader(f)
        for row in reader:
            optionList += row[0] + "\n"
    optionList += "quit"

    # Take the name of the podcast channel chosen and grab its equivalent url in the list
    link = ""
    ans = subprocess.getoutput(
        "echo -e '" + optionList + "'" + " | " + launcher)
    if ans == "quit" or ans == "":
        exit()
    else:
        with open(feedFilePath) as f:
            reader = csv.reader(f)
            for row in reader:
                if row[0] == ans:
                    link = row[1]
                    break

    # Take the podcast channel rss feed and parse it and give the latest rss episode list
    # with episode name and link
    rssFeed = parse(link)
    episodeList = ""
    for i in rssFeed.entries:
        episodeList += i.title + "~" + i.link + "\n"

    # write the episode list to csv file
    with open(cacheFilePath, "w") as f:
        f.write(episodeList)

    # Put all the episode name list in the launcher of choice and ask the user to choose one
    optionList = ""
    with open(cacheFilePath) as f:
        reader = csv.reader(f, delimiter="~")
        for row in reader:
            optionList += row[0] + "\n"
    optionList += "quit"

    # Take the name of the episode chosen and grab its equivalent url in the list
    answer = subprocess.getoutput(
        "echo -e \"" + optionList + "\"" + " | " + launcher)
    if answer == "quit" or answer == "":
        exit()
    else:
        with open(cacheFilePath) as f:
            reader = csv.reader(f, delimiter="~")
            for row in reader:
                # print(re.sub(r"[\"]","",row[0]) == answer)
                if sub(r"[\"]", "", row[0]) == answer:
                    link = row[1]
                    break

    # Open the chosen episode link in mpv without video.
    os.system("mpv --no-video \"" + link + "\" --volume=" + str(defaultVolume))

# ----------------------build podcast channel feed list-------------------


def buildFeedForPodcast():
    if not os.path.exists(os.path.expanduser("~/.config/neonPodcaster")):
        os.mkdir(os.path.expanduser("~/.config/neonPodcaster"))
    numberOfFeeds = int(input("enter the number of feeds to add: "))
    with open(feedFilePath, "w") as f:
        for i in range(numberOfFeeds):
            csv_writer = csv.writer(f)
            channelName = input("Channel Name: ")
            channelUrl = input("Url: ")
            csv_writer.writerow([channelName, channelUrl])

# ---------------------delete a podcast channel from feed list---------------


def DelPodChannelFromFeedFile():
    # Put all the podcast channel names list in the launcher of choice and ask the user to choose one
    tempList = []
    optionList = ""
    with open(feedFilePath) as f:
        reader = csv.reader(f)
        for row in reader:
            optionList += row[0] + "\n"
            tempList.append(row)
    optionList += "quit"

    # Take the name of the podcast channel chosen and do not write it into the new file
    ans = subprocess.getoutput(
        "echo -e '" + optionList + "'" + " | " + launcher)
    if ans == "quit" or ans == "":
        exit()
    else:
        os.remove(feedFilePath)
        with open(feedFilePath, "w") as f:
            csv_writer = csv.writer(f)
            for line in tempList:
                if line[0] != ans:
                    csv_writer.writerow(line)


# -------------------------parse the arguments------------------------
parser = ArgumentParser(description="A command line Podcast Client App")
parser.add_argument("-p", help="run the podcast client", action="store_true")
parser.add_argument(
    "-b", help="build the podcast channel feed file", action="store_true")
parser.add_argument(
    "-l", help="provide the launcher to use (default: 'dmenu -l 20')")
parser.add_argument(
    "-v", help="provide the default volume to launch with (default: '30')", type=int)
parser.add_argument(
    "-d", help="delete a podcast channel from the feed file", action="store_true")
args = parser.parse_args()

if args.l:
    launcher = args.l
if args.v:
    defaultVolume = args.v
if args.b:
    buildFeedForPodcast()
if args.p:
    podcast_client()
if args.d:
    DelPodChannelFromFeedFile()
