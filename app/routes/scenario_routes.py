from flask import Blueprint, render_template, request, session, redirect, url_for, flash
from app.models.scenario import Scenario

scenario_bp = Blueprint('scenario', __name__, url_prefix='/scenarios')

@scenario_bp.route('/')
def index():
    scenarios = Scenario.get_all()
    active_scenario_id = session.get('active_scenario_id')
    return render_template('scenario/index.html', scenarios=scenarios, active_scenario_id=active_scenario_id)

@scenario_bp.route('/<int:id>/apply', methods=['POST'])
def apply_scenario(id):
    scenario = Scenario.get_by_id(id)
    if scenario:
        session['active_scenario_id'] = scenario.id
        session['active_scenario'] = {
            'caller_name': scenario.caller_name,
            'phone_number': scenario.caller_number,
            'voice_path': scenario.audio_file
        }
        flash(f"已成功套用【{scenario.title}】劇本", "success")
    else:
        flash("找不到該劇本", "error")
        
    return redirect(url_for('scenario.index'))

@scenario_bp.route('/new', methods=['GET', 'POST'])
def new_scenario():
    if request.method == 'POST':
        title = request.form.get('title')
        caller_name = request.form.get('caller_name')
        phone_number = request.form.get('phone_number')
        description = request.form.get('description')
        
        if not title or not caller_name or not phone_number:
            flash('劇本名稱、來電者名稱與電話號碼為必填', 'error')
            return render_template('scenario/new.html', title=title, caller_name=caller_name, phone_number=phone_number, description=description)
            
        Scenario.create(title, caller_name, phone_number, description=description)
        flash('成功新增自定義劇本！', 'success')
        return redirect(url_for('scenario.index'))
        
    return render_template('scenario/new.html')
