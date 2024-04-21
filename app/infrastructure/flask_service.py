from ..domain.entities import Task, Status, Occurance, NodeInfo
from ..application.services import FollowerHttpService, LeaderHttpService
from .logger_service import LoggerService
from flask import Flask, request, jsonify

class FlaskFollowerService:
    def __init__(self, config, httpclient: FollowerHttpService, logger_service: LoggerService):
        self.config = config
        self.app = Flask(__name__)
        self.leader = None
        self.httpclient = httpclient
        self.logger_service = logger_service
        self.setup_routes()
        self.logger_service.info("Flask Started Up")

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
                return jsonify({'message': 'Task received', 'task': task.name}), 200
            except (KeyError, ValueError) as e:
                return jsonify({'error': str(e)}), 400
        @self.app.route('/leader', methods=['POST'])
        def leader_registration():
            leader = request.get_json() 
            self.leader = leader
            self.logger_service.console(f"Leader registered: {leader['ip']}")
            self.httpclient.register_leader(self.leader['ip'])
            return jsonify({'message': 'Leader registered'}), 200

            
        
        @self.app.route('/health', methods=['GET'])
        def health():
            return jsonify({'status': 'ok'}), 200
        
    def run(self):
        self.app.run(host='0.0.0.0',port=3333,debug=self.config.DEBUG)


class FlaskLeaderService:
    def __init__(self, config, httpclient: LeaderHttpService):
        self.config = config
        self.app = Flask(__name__)
        self.nodes = []
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
                return jsonify({'message': 'Task received', 'task': task.name}), 200
            except (KeyError, ValueError) as e:
                return jsonify({'error': str(e)}), 400
        @self.app.route('/nodes', methods=['POST'])
        def node_registration():
            node = request.get_json() 
            self.nodes.append(node)
            print(f"Node registered: {node['ip']}")
            return jsonify({'message': 'Node registered'}), 200

            
        
        @self.app.route('/health', methods=['GET'])
        def health():
            return jsonify({'status': 'ok'}), 200
        
    def run(self):
        self.app.run(host='0.0.0.0',port=3333,debug=self.config.DEBUG)