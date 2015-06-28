import re
from datetime import datetime


template = """+++
date = "{0}"
title = "{1}"
categories = "{2}"
+++
{3}"""

counter = {}

def save_as_md(article):
    lines = article.splitlines()
    if len(lines) < 12:
        return
    date = datetime.strptime(lines[9][6:], "%m/%d/%Y %H:%M:%S")
    title = lines[1][7:]
    categories = lines[7][10:]
    body = article.split("-----\n")[1][6:-1].replace("\n", "  \n").replace("http://zaburoapp.blog.fc2.com/img/", "/images/").replace("<u>","").replace("</u>","").replace("http://blog-imgs-74.fc2.com/z/a/b/zaburoapp/","/images/")

    filename = date.strftime("%Y%m%d")
    if filename in counter.keys():
        counter[filename] += 1
        filename = "{0}_{1}.md".format(filename, counter[filename])
    else:
        counter[filename] = 0
        filename = "{0}_0.md".format(filename)

    f = open(filename, "w")
    f.write(template.format(
        date.strftime("%Y-%m-%dT%H:%M:%S+09:00"),
        title,
        categories,
        body))


if __name__ == '__main__':
    f = open("zaburoapp.txt", "r")
    all_articles = f.read().split("--------\n")
    f.close()

    for article in all_articles:
        save_as_md(article)
