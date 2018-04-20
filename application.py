import flask

base_url = 'flaskapitest-env.elasticbeanstalk.com'

application = flask.Flask(__name__)

#Set application.debug=true to enable tracebacks on Beanstalk log output.
#Make sure to remove this line before deploying to production.
application.debug=True

tasks = [
    {
        'id': 1,
        'title': u'Buy groceries',
        'description': u'Milk, Cheese, Pizza, Fruit, Tylenol',
        'done': False
    },
    {
        'id': 2,
        'title': u'Learn Python',
        'description': u'Need to find a good Python tutorial on the web',
        'done': False
    }
]

@application.errorhandler(400)
def not_found(error):
    return flask.make_response(flask.jsonify( { 'error': 'Bad request' } ), 400)

@application.errorhandler(404)
def not_found(error):
    return flask.make_response(flask.jsonify( { 'error': 'Not found' } ), 404)

@application.route('/')
def hello_world():
    return "Hello world!"

@application.route('/todo/api/v1.0/tasks', methods = ['GET'])
def get_tasks():
    return flask.jsonify( { 'tasks': map(make_public_task, tasks) } )

def make_public_task(task):
    new_task = {}
    for field in task:
        if field == 'id':
            new_task['uri'] = base_url + '/todo/api/v1.0/task/' + str(task[field])
        else:
            new_task[field] = task[field]
    return new_task


if __name__ == '__main__':
    application.run(host='0.0.0.0', debug=True)