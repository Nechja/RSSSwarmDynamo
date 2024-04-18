from ..domain.entities import Task, Status, Occurance
from flask import Flask, request, jsonify

class FlaskService:
    def __init__(self, config):
        self.config = config
        self.app = Flask(__name__)
        self.setup_routes()
        print("Flask Started Up")

    def setup_routes(self):
        @self.app.route('/webhook', methods=['POST']) 
        def webhook():
            data = request.get_json()
            if not data:
                return jsonify({'error': 'No JSON data received'}), 400
            
            try:
                task = Task(
                    id=data['id'],
                    name=data['name'],
                    status=Status(data['status']),
                    action=data['action'],
                    occurance=Occurance(data['occurance']),
                    assignee=data.get('assignee', None),
                    last_run=data.get('last_run', None)
                )
                # Log or process the task here
                return jsonify({'message': 'Task received', 'task': task.name}), 200
            except (KeyError, ValueError) as e:
                return jsonify({'error': str(e)}), 400
        
    def run(self):
        self.app.run(debug=self.config.DEBUG)