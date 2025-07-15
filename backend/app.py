from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from functools import wraps

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@db:5432/postgres'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['API_TOKEN'] = 'secret-token'
db = SQLAlchemy(app)

class LogEvent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    table_name = db.Column(db.String(50))
    operation = db.Column(db.String(10))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    details = db.Column(db.Text)

def require_token(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if token != f"Bearer {app.config['API_TOKEN']}":
            return jsonify({'message': 'Unauthorized'}), 401
        return f(*args, **kwargs)
    return decorated

@app.route('/logs', methods=['GET'])
@require_token
def get_logs():
    table = request.args.get('table')
    since = request.args.get('since')

    query = LogEvent.query
    if table:
        query = query.filter_by(table_name=table)
    if since:
        try:
            since_time = datetime.fromisoformat(since)
            query = query.filter(LogEvent.timestamp >= since_time)
        except ValueError:
            return jsonify({'error': 'Invalid timestamp format'}), 400

    logs = query.order_by(LogEvent.timestamp.desc()).limit(50).all()
    return jsonify([{
        'id': log.id,
        'table_name': log.table_name,
        'operation': log.operation,
        'timestamp': log.timestamp.isoformat(),
        'details': log.details
    } for log in logs])

@app.route('/simulate-replay', methods=['POST'])
@require_token
def simulate_replay():
    data = request.get_json()
    start = datetime.fromisoformat(data.get('start'))
    end = datetime.fromisoformat(data.get('end'))

    logs = LogEvent.query.filter(LogEvent.timestamp.between(start, end)).all()
    return jsonify({'message': f'Simulated replay of {len(logs)} operations from {start} to {end}'})

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5000)
