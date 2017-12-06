# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals
from configparser import ConfigParser
from flask import jsonify, request, Flask, abort, json
import sys
from bosonnlp import BosonNLP

#define a function to display msg into console(stderr)
def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

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

@nlpServer.route('/nlp/sentiment', methods=['POST'])
def nlp_sentiment():

    if not request.json :
        abort(400)

    json_dict = request.json
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