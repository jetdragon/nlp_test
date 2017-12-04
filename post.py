from flask import jsonify, request, Flask, abort

post = Flask(__name__)

students = []

@post.route('/student', method=['POST'])
def add_student():
    if not request.json or \
    not 'id' in request.json or \
    not 'age' in request.json or \
    not 'birthplace' in request.json or \
    not 'grade' in request.json :
        abort(400)

    student = {
        'id' : request.json['id'],
        'age' : request.json['age'],
        'birthplace' : request.json['birthplace'],
        'grade' : request.json['grade'],
        'status' : 'success'
    }

    students.append(student)
    return jsonify(students)

if __name__ = '__main__'：
    post.run(host='127.0.0.1', port=5000, debug=True)