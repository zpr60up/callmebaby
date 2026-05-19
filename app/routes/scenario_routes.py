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
        session['active_scenario_id'] = scenario['id']
        session['active_scenario'] = {
            'caller_name': scenario['caller_name'],
            'phone_number': scenario['phone_number'],
            'voice_path': scenario['voice_path']
        }
        flash(f"已成功套用【{scenario['title']}】劇本", "success")
    else:
        flash("找不到該劇本", "error")
        
    return redirect(url_for('scenario.index'))
