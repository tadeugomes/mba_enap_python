from flask import jsonify

def hello_world(request):
    try:
        return jsonify({'message': 'Hello World'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500