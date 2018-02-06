#!/usr/bin/env python3
import subprocess
import bs4
import re
from pprint import pprint
import requests

head = '''<!doctype html>
<html lang="en">
<head>
	<meta charset="utf-8">
	<title>HN test</title>
	<meta name="viewport" content="width=100, initial-scale=1.0, maximum-scale=1.0, minimum-scale=1.0,target-densitydpi=device-dpi, user-scalable=no" />
	<style type="text/css">
		
body {
	background-color: rgb(10, 10, 10);
	font-family: sans-serif;
	color: rgb(150, 150, 150);
	font-size: 1em;
	line-height: 2em;
}
ol {
	margin-top: 30px;
	margin-left: 3%;
}
.title:link {
	font-size: 1.1em;
	font-weight: bold;
	color: rgb(230, 230, 230);
}
.title:hover {
	color: rgb(170, 170, 170);
}

.title:visited {
	color: rgb(130, 130, 130);
}
.underline {
	margin-top: -10px;
	font-size: 0.9em;
	margin-bottom: 10px;
}

a:link {
	color: rgb(180, 180, 180);
	text-decoration: none;
}
a:visited {
	color: rgb(180, 180, 180);
}
a:hover {
	color: rgb(120,120,120);
}
a:active {
	color: rgb(120,120,120);
}
	</style>
</head>
<body>
<ol>
'''

tail = '''</ol>
</body>
</html>
'''


def parse_html(doc):
	soup = bs4.BeautifulSoup(doc, 'html.parser')

	body = soup

	# 1, 3, 6

	for i in [0, 1, 0, 0, 4, 0, 0]:
		body = list(body.children)[i]


	body = [item for i, item in enumerate(list(body)[1:]) if (i % 5 == 0) or ((i - 1) % 5 == 0)][:-1]
	posts = [item for i, item in enumerate(body) if i % 2 == 0]
	meta = [item for i, item in enumerate(body) if (i - 1) % 2 == 0]
	body = zip(posts, meta)
	body = [(list(list(post.children)[4].children)[0], list(meta.children)[1]) for post, meta in body]
	body = [(post, list(meta.children)[1:][:-1]) for post, meta in body]
	body = [(post, [entry for entry in meta if str(entry) not in [' | ', '', ' ', ' by ']]) for post, meta in body]

	hn = []

	for post, meta in body:
		postdata = {
			'title': post.get_text().strip('\n'),
			'url': re.search('(?<=href=")[^"]*', str(post)).group(),
			'comments': 0,
			'score': 0
		}
		for entry in meta:
			if re.search("<span class=\"age\"><a href=\"item\?id=\d+\"", str(entry)):
				postdata['id'] = re.search("(?=<span class=\"age\"><a href=\"item\?id=).+(?<=\")", str(entry)).group()[35:-1]
				postdata['age'] = entry.get_text()
			if re.search("\d+\scomment", str(entry)):
				postdata['comments'] = re.search("\d+\scomment", str(entry)).group()[:-8]
			if re.search("<span class=\"score\"", str(entry)):
				postdata['score'] =  entry.get_text()[:-7]
		hn.append(postdata)
	return hn

def write_html(hn):
	ret = head.split('\n')
	for post in hn:
		ret.append('<li>')
		ret.append('	<div><a class="title" href="' + post['url'] + '">' + post['title'] + '</a></div>')
		ret.append('	<div class="underline">')
		com = '<a href="https://news.ycombinator.com/item?id=' + post['id'] + '" >' + str(post['comments']) + ' comments</a>'
		ret.append('		' + str(post['score']) + ' points, ' + post['age'] + ', ' + com)
		ret.append('	</div>')
		ret.append('</li>')
	ret += tail.split('\n')
	ret = '\n'.join(ret).encode('utf-8')
	return ret

	
			

def getbody(download = True):
	if download:
		hn = []
		for i in range(1):
			doc = requests.get('https://news.ycombinator.com/news?p=' + str(i)).content
			hn += parse_html(doc)
	else:
		path = open('tmp/index.html', 'rb')
		doc = path.read()
		path.close()
		hn = parse_html(doc)
	return write_html(hn)

def test():
	print(getbody(False))


if __name__ == '__main__':
	test()
