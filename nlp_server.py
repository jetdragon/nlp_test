# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals
from configparser import ConfigParser
import sys
from flask import jsonify, request, Flask, abort, json
# from bosonnlp import BosonNLP


#read config file    
cfg = ConfigParser()
cfg.read('config.ini')

sec = cfg.sections()
token = cfg.get('nlp','nlp_token')
rest_host = cfg.get('server','host')
rest_port = int(float(cfg.get('server', 'port')))

#ini boson
# nlp = BosonNLP(token)

#REST API server
nlp = Flask(__name__)
#nlp_server.config['JSON_AS_ASCII'] = False

#define a function to display msg into console(stderr)
def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

@nlp.route('/nlp/sentiment', methods=['POST'])
def nlp_sentiment():

    if not request.json or \
    not 'Text' in request.json:
        abort(400)

    json_dict = request.json
    for k, v in json_dict.items():
        eprint(k, v['Text'])
        # eprint(nlp.sentiment(v['Text']))

    return jsonify(str(json_dict['0']['Text']))
    
if __name__ == '__main__':
    nlp.run(host=rest_host, port=rest_port, debug=True)