from flask import Blueprint, render_template, request, jsonify, redirect, url_for
from app.models.scenario import Scenario
from app.models.custom_caller import CustomCaller
from app.models import caller as caller_model

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    scenarios = Scenario.get_all()
    custom_callers = CustomCaller.get_all()
    saved_callers = caller_model.get_all()
    return render_template('index.html', 
                           scenarios=scenarios, 
                           custom_callers=custom_callers, 
                           saved_callers=saved_callers)

@bp.route('/api/scenarios')
def api_scenarios():
    scenarios = Scenario.get_all()
    return jsonify([dict(id=s.id, title=s.title, caller_name=s.caller_name, caller_phone=s.caller_phone, avatar_path=s.avatar_path, category=s.category, description=s.description) for s in scenarios])

@bp.route('/call')
def call():
    caller_name = request.args.get('caller_name', 'Unknown')
    caller_phone = request.args.get('caller_phone', '')
    avatar_path = request.args.get('avatar_path', '/static/images/default_avatar.png')
    audio_path = request.args.get('audio_path', '')
    
    return render_template('call.html', 
                           caller_name=caller_name, 
                           caller_phone=caller_phone,
                           avatar_path=avatar_path,
                           audio_path=audio_path)

@bp.route('/api/custom_callers', methods=['POST'])
def save_custom_caller():
    data = request.json
    caller_name = data.get('caller_name')
    caller_phone = data.get('caller_phone')
    avatar_path = data.get('avatar_path', '/static/images/default_avatar.png')
    
    if not caller_name or not caller_phone:
        return jsonify({'error': 'Name and phone are required'}), 400
        
    caller_id = CustomCaller.create(caller_name, caller_phone, avatar_path)
    return jsonify({'success': True, 'id': caller_id})

@bp.route('/api/custom_callers/<int:caller_id>', methods=['DELETE'])
def delete_custom_caller(caller_id):
    CustomCaller.delete(caller_id)
    return jsonify({'success': True})
