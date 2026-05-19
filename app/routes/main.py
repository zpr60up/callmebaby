from flask import Blueprint, render_template
from app.models.scenario import Scenario

main_bp = Blueprint('main', __name__)

@main_bp.route('/', methods=['GET'])
def index():
    """
    首頁：顯示所有可用的語音情境與介面風格選項。
    """
    scenarios = Scenario.get_all()
    return render_template('index.html', scenarios=scenarios)

