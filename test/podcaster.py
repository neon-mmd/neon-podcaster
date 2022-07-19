import os
import feedparser
import csv
import subprocess
import sys

cacheFilePath = os.path.expanduser("~/.cache/temp.csv")
if os.path.exists(os.path.expanduser("~/.config/neonPodcaster")):
    feedFilePath = os.path.expanduser("~/.config/neonPodcaster/feeds.csv")
    configFilePath = os.path.expanduser("~/.config/neonPodcaster")
else:
    feedFilePath = "/etc/xdg/neonPodcaster/feeds.csv"
    configFilePath = "/etc/xdg/neonPodcaster"
    
sys.path.insert(0, configFilePath)
from neonPodcaster import config

launcher = "dmenu -l 20"
from feedparser.encodings import re
optionList = ""
with open(feedFilePath) as f:
    reader = csv.reader(f)
    for row in reader:
        optionList += row[0] + "\n"
optionList += "quit"
print(optionList)
link = ""
ans = subprocess.getoutput("echo -e '" + optionList +"'" + " | " + config.launcher)
if ans == "quit" or ans == "":
    exit()
else:
 with open(feedFilePath) as f:
    reader = csv.reader(f)
    for row in reader:
        if row[0] == ans:
            link = row[1]
            break
newsfeed = feedparser.parse(link)
episodeList = ""
next = 0
for i in newsfeed.entries:
    episodeList += i.title + "~" + i.link + "\n"
with open(cacheFilePath,"w") as f:
    f.write(episodeList)
optionList = ""
with open(cacheFilePath) as f:
    reader = csv.reader(f,delimiter="~")
    for row in reader:
        optionList += row[0] + "\n"
optionList += "quit"
answer = subprocess.getoutput("echo -e \"" + optionList +"\"" + " | " + config.launcher)
if answer == "quit" or answer == "":
    exit()
else:
    with open(cacheFilePath) as f:
        reader = csv.reader(f,delimiter="~")
        for row in reader:
            # print(re.sub(r"[\"]","",row[0]) == answer)
            if re.sub(r"[\"]","",row[0]) == answer:
                link = row[1]
                break
os.system("mpv --no-video \"" + link + "\" --volume=" + str(config.defaultVolume))
