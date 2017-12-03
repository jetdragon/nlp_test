from configparser import ConfigParser
cfg = ConfigParser()
cfg.read('config.ini')

secs = cfg.sections()
url = cfg.get('nlp','nlp_url')
token = cfg.get('nlp','nlp_token')
print(secs)
print(url)
print(token)

rest_host = cfg.get('server','host')
rest_port = cfg.get('server','port')

print(rest_host)
print(rest_port)