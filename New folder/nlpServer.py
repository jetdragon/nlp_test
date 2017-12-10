# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals
from configparser import ConfigParser
from flask import jsonify, request, Flask, abort, json
import sys
from bosonnlp import BosonNLP

from bs4 import BeautifulSoup
import requests
import pandas
import urllib

#define a function to display msg into console(stderr)
def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

# def return_result(*args):
#     return args

#read config file    
cfg = ConfigParser()
cfg.read('config.ini')

sec = cfg.sections()
token = cfg.get('nlp','nlp_token')
rest_host = cfg.get('server','host')
rest_port = int(float(cfg.get('server', 'port')))

#REST API server
nlpServer = Flask(__name__)
nlpServer.config['JSON_AS_ASCII'] = False

nlp_result = []
nlp = BosonNLP(token)

def getNewsDetails(link):
    subres = requests.get(link)
    subres.encoding = 'utf-8'

    ssoup = BeautifulSoup(subres.text, 'html.parser')
    pList = ssoup.select('#artibody p')  # .article
    tDiv = ssoup.select('.date-source')  # '.date-source span a'


    try:
        spanList = tDiv[0].select('span')
        date = spanList[0].text
        src = spanList[1].text
    except IndexError:
        try:
            # print('first try', link)
            date = ssoup.select('.time-source')[0].contents[0].strip()  # lstrip('content need to be removed')
            src = ssoup.select('.time-source span a')[0].text
        except IndexError:
            try:
                # print('second try', link)
                date = ssoup.select('#pub_date')[0].contents[0].strip()
                src = ssoup.select('#media_name')[0].text.strip('\n').strip('xa0')
            except IndexError:
                # print('other', link)
                date = '2017年'
                src = '新浪新闻'

    article = []
    # pList = sDiv[0].select('p')
    for p in pList:  # ' '.join([p.text.strip() for p in ssoup.select('#artibody p')])
        if p.text != ' ' and p.text.rfind('function') == -1:
            article.append(p.text.strip())

    sArticle = ' '.join(article)  # '\n'.join(article)

    info = [date, src, sArticle]

    return info

@nlpServer.route('/search', methods=['GET'])
def WNspider():
# def WNspider(kw='microsoft'):
    #kw = 'microsoft'
    # kw = '微软'
    # kw = 'LETV'
    if 'key' in request.args:
        kw = request.args['key']
    else:
        abort(400)
        
    newsSet = []
    global spyder_result
    spyder_result = []

    for page in range(1, 2):
        # newsurl = 'http://search.sina.com.cn/?q={0}&c=news&from=channel&ie=utf-8'.format(kw)
        newsurl = 'http://search.sina.com.cn/?q={}&c=news&from=channel&ie=utf-8&col=&range=&source=&country=\
        &size=&time=&a=&page={}&pf=2131425464&ps=2134309112&dpc=1'.format(urllib.parse.quote(kw), page)

        res = requests.get(newsurl)

        soup = BeautifulSoup(res.text, 'html.parser')

        dList = soup.select('.box-result .r-info2')

        for div in dList:
            h2 = div.select('h2 a')[0].text
            link = div.select('a')[0]['href']
            # source = div.select('.fgray_time')[0].text

            content = getNewsDetails(link)
            newsSet.append([h2, content[0], content[1], content[2]])
            print(content)

    df = pandas.DataFrame(newsSet)
    df.columns = ['Tile', 'Date','Source', 'Text']
    # global spyder_result 
    # spyder_result = df.to_json(path_or_buf=None, orient='index', force_ascii=False)
    spyder_result.append(df.to_json(path_or_buf=None, orient='index', force_ascii=False))
    # eprint(df.to_json(path_or_buf=None, orient='index', force_ascii=False))
    json_dict = df.to_dict(orient='index')
    # return nlp_sentiment(json_dict)
    return 'Done'

@nlpServer.route('/nlp/sentiment', methods=['POST'])
def nlpServer_sentiment():
    # kw = request.args.items()

    if not request.json :
        abort(400)

    json_dict = request.json
    return nlp_sentiment(json_dict)

@nlpServer.route('/spyder/result', methods=['GET'])
def nlpServer_spyder_result():
    if 'pageNumber' in request.args:
        pageNumber = int(float(request.args['pageNumber']))
    else:
        abort(400)
    eprint(spyder_result[pageNumber-1])
    eprint(pageNumber)
    return spyder_result[pageNumber-1], 200, {'Content-Type': 'application/json; charset=utf-8'}

def nlp_sentiment(json_dict):   
    for k, v in json_dict.items():
        # eprint(k, v['Text'])
        result = nlp.sentiment(v['Text'])
        # timestamp = nlp.convert_time(v['Date'])
        # eprint(result[0][0],result[0][1],timestamp)
        nlp_item = {
        'log_id' : k,
        'keyword' : v['Tile'],
        'text' : v['Text'],
        'timestamp' : v['Date'],
        'positive_prob' : result[0][0],
        'negative_prob' : result[0][1],
        'status' : 'WIP'
        }
        # eprint(nlp_item)
        nlp_result.append(nlp_item)
        
    # eprint(jsonify(nlp_result))
    return jsonify(nlp_result)
    
if __name__ == '__main__':
    nlpServer.run(host=rest_host, port=rest_port, debug=True)