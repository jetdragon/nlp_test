#!flask/bin/python
from flask import Flask, jsonify
app = Flask(__name__)

tasks = [
    {
        'id': 1,
        'title': u'Buy groceries',
        'description': u'牛奶, Cheese, Pizza, Fruit, Tylenol',
        'done': False
    },
    {
        'id': 2,
        'title': u'Learn Python',
        'description': u'Need to find a good Python tutorial on the web',
        'done': False
    }
]

@app.route('/todo/api/v1.0/tasks/<int:task_id>',methods=['GET'])
def get_task(task_id):
    task = filter(lambda t: t['id'] == task_id, tasks)
    if filter.__itemsize__ == 0:
        not_found(404)
    return jsonify({'task':list(task)[0]})

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not Found'})

if __name__ == '__main__':
    app.run(host='127.0.0.1',port=5000,debug=True)