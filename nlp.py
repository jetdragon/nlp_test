# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals
from configparser import ConfigParser
from flask import jsonify, request, Flask, abort, json

cfg = ConfigParser()
cfg.read('config.ini')

sec = cfg.sections()
token = cfg.get('nlp','nlp_token')
rest_host = cfg.get('server','host')
rest_port = int(float(cfg.get('server', 'port')))

#REST API server
nlp = Flask(__name__)
nlp.config['JSON_AS_ASCII'] = False

nlp_str = []

@nlp.route('/nlp/sentiment', methods=['POST'])
def nlp_sentiment():
    # if not request.json :
    #     abort(400)

    # return json.loads(request.data.decode("gbk").encode("utf-8"))['0']
    # json_dict = json.loads(request.get_data().decode("gbk"))
    # return jsonify(str(json_dict['0']['Text']))
    # return request.get_json()
    #return json.dumps(str(request.get_data()), ensure_ascii=False)
    return json.loads(str(request.get_data()))

if __name__ == '__main__':
    nlp.run(host=rest_host, port=rest_port, debug=True)