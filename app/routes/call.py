from flask import Blueprint, request, redirect, url_for, render_template
from app.models.scenario import Scenario

call_bp = Blueprint('call', __name__, url_prefix='/call')

@call_bp.route('/trigger', methods=['POST'])
def trigger():
    """
    接收表單參數，並導向到來電畫面。
    """
    os_style = request.form.get('os_style', 'ios')
    scenario_id = request.form.get('scenario_id')
    
    if not scenario_id:
        return redirect(url_for('main.index'))
        
    return redirect(url_for('call.incoming', os_style=os_style, scenario_id=scenario_id))

@call_bp.route('/incoming', methods=['GET'])
def incoming():
    """
    來電響鈴畫面。
    """
    os_style = request.args.get('os_style', 'ios')
    scenario_id = request.args.get('scenario_id')
    
    scenario = Scenario.get_by_id(scenario_id)
    if not scenario:
        return redirect(url_for('main.index'))
        
    return render_template('call/incoming.html', os_style=os_style, scenario=scenario)

@call_bp.route('/active', methods=['GET'])
def active():
    """
    通話進行中畫面。
    """
    os_style = request.args.get('os_style', 'ios')
    scenario_id = request.args.get('scenario_id')
    
    scenario = Scenario.get_by_id(scenario_id)
    if not scenario:
        return redirect(url_for('main.index'))
        
    return render_template('call/active.html', os_style=os_style, scenario=scenario)

