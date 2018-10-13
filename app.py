from flask import Flask, request
import json
import urllib
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/', methods=['GET','POST'])
def web_scrap():
	if 'url' not in request.args.keys():
		return 'please post url link for the web scrapping'
	url = request.args['url']
	print(url)
	page = urllib.request.urlopen(url)
	soup = BeautifulSoup(page, 'html.parser')
	data = {}
	parse_title(soup, data)
	parse_attr(soup, data)
	parse_img(soup, data)
	return json.dumps(data)

def parse_img(soup, data):
	images = soup.select_one('div.gallery div.swipe-wrap img')
	data['image'] = images['src']
	return data
    
def parse_title(soup, data):
	title = soup.select_one('h2.postingtitle > span.postingtitletext > span#titletextonly')
	title_tokens = title.text.split(sep=" ")
	year = title_tokens[0] if is_int(title_tokens[0]) else None
	data['year'] = year
	model = " ".join(title_tokens[1:])
	data['model'] = model
	price = soup.select_one('h2.postingtitle > span.postingtitletext > span.price')
	data['price'] = price.text

def parse_attr(soup, data):
	tags = soup.select('p.attrgroup span')
	tokens = tags[0].text.split(sep=":")
	if len(tokens) == 1:
		t = tokens[0].split(sep=" ")
		data['year'] = t[0]
		data['model'] = " ".join(t[1:])
	for tag in tags:
	    tokens = tag.text.split(sep=':')
	    if len(tokens) > 1:
	        data[tokens[0].strip()] = tokens[1].strip()
	return data

def is_int(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')