"""
Call Routes — 來電模擬功能路由
處理來電者管理（CRUD）與來電畫面顯示。
"""

from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from app.models import caller as caller_model

call_bp = Blueprint('call', __name__, url_prefix='/call')


# ─────────────────────────────────────────────
# 來電設定頁面
# ─────────────────────────────────────────────

@call_bp.route('/setup')
def setup():
    """顯示來電者管理頁面，列出所有已儲存的來電者。"""
    callers = caller_model.get_all()
    return render_template('call/setup.html', callers=callers)


# ─────────────────────────────────────────────
# 來電者 CRUD
# ─────────────────────────────────────────────

@call_bp.route('/callers', methods=['POST'])
def create_caller():
    """新增一位來電者。"""
    name = request.form.get('name', '').strip()
    phone = request.form.get('phone', '').strip()
    avatar = request.form.get('avatar', 'avatar_default.png')
    voice_file = request.form.get('voice_file', 'voice_family')
    call_style = request.form.get('call_style', 'ios')

    if not name or not phone:
        flash('名稱和電話號碼為必填欄位！', 'error')
        return redirect(url_for('call.setup'))

    caller_model.create({
        'name': name,
        'phone': phone,
        'avatar': avatar,
        'voice_file': voice_file,
        'call_style': call_style
    })
    flash(f'已新增來電者「{name}」！', 'success')
    return redirect(url_for('call.setup'))


@call_bp.route('/callers/<int:caller_id>/update', methods=['POST'])
def update_caller(caller_id):
    """更新來電者資料。"""
    name = request.form.get('name', '').strip()
    phone = request.form.get('phone', '').strip()
    avatar = request.form.get('avatar', 'avatar_default.png')
    voice_file = request.form.get('voice_file', 'voice_family')
    call_style = request.form.get('call_style', 'ios')

    if not name or not phone:
        flash('名稱和電話號碼為必填欄位！', 'error')
        return redirect(url_for('call.setup'))

    caller_model.update(caller_id, {
        'name': name,
        'phone': phone,
        'avatar': avatar,
        'voice_file': voice_file,
        'call_style': call_style
    })
    flash(f'已更新來電者「{name}」！', 'success')
    return redirect(url_for('call.setup'))


@call_bp.route('/callers/<int:caller_id>/delete', methods=['POST'])
def delete_caller(caller_id):
    """刪除來電者。"""
    c = caller_model.get_by_id(caller_id)
    caller_model.delete(caller_id)
    if c:
        flash(f'已刪除來電者「{c["name"]}」。', 'success')
    return redirect(url_for('call.setup'))


# ─────────────────────────────────────────────
# 來電畫面 (支援 ID 及 Query Parameters 載入)
# ─────────────────────────────────────────────

@call_bp.route('/incoming')
@call_bp.route('/incoming/<int:caller_id>')
def incoming(caller_id=None):
    """顯示模擬來電畫面（可由 ID 載入或由 Query Parameters 載入）。"""
    if caller_id:
        c = caller_model.get_by_id(caller_id)
        if not c:
            flash('找不到該來電者！', 'error')
            return redirect(url_for('call.setup'))
        caller_data = {
            'id': c['id'],
            'name': c['name'],
            'phone': c['phone'],
            'avatar': c['avatar'],
            'voice_file': c['voice_file'],
            'call_style': c['call_style']
        }
    else:
        caller_data = {
            'id': 0,
            'name': request.args.get('name', '未知'),
            'phone': request.args.get('phone', '0900-000-000'),
            'avatar': request.args.get('avatar', 'avatar_default.png'),
            'voice_file': request.args.get('voice_file', 'voice_family'),
            'call_style': request.args.get('call_style', 'ios')
        }
    
    back_url = request.args.get('back_url') or request.referrer or url_for('call.setup')
    if 'incoming' in back_url or 'active' in back_url:
        back_url = url_for('call.setup')

    style = caller_data['call_style'] if caller_data['call_style'] in ('ios', 'android') else 'ios'
    template = f'call/incoming_{style}.html'
    return render_template(template, caller=caller_data, back_url=back_url)


@call_bp.route('/active/<int:caller_id>')
def active_call(caller_id):
    """顯示通話中畫面。"""
    c = caller_model.get_by_id(caller_id)
    if not c:
        flash('找不到該來電者！', 'error')
        return redirect(url_for('call.setup'))

    return render_template('call/in_call.html', caller=c)


# ─────────────────────────────────────────────
# API（供前端 JS 使用）
# ─────────────────────────────────────────────

@call_bp.route('/api/caller/<int:caller_id>')
def api_get_caller(caller_id):
    """JSON 回傳來電者資料。"""
    c = caller_model.get_by_id(caller_id)
    if not c:
        return jsonify({'error': 'not found'}), 404

    return jsonify({
        'id': c['id'],
        'name': c['name'],
        'phone': c['phone'],
        'avatar': c['avatar'],
        'voice_file': c['voice_file'],
        'call_style': c['call_style']
    })


@call_bp.route('/incoming_msg')
@call_bp.route('/incoming_msg/<int:caller_id>')
def incoming_msg(caller_id=None):
    """顯示模擬訊息接收（鎖定/推播通知）畫面。"""
    if caller_id:
        c = caller_model.get_by_id(caller_id)
        if not c:
            flash('找不到該來電者！', 'error')
            return redirect(url_for('call.setup'))
        caller_data = {
            'id': c['id'],
            'name': c['name'],
            'phone': c['phone'],
            'avatar': c['avatar'],
            'voice_file': c['voice_file'],
            'call_style': c['call_style']
        }
    else:
        caller_data = {
            'id': 0,
            'name': request.args.get('name', '未知'),
            'phone': request.args.get('phone', '0900-000-000'),
            'avatar': request.args.get('avatar', 'avatar_default.png'),
            'voice_file': request.args.get('voice_file', 'voice_family'),
            'call_style': request.args.get('call_style', 'ios')
        }

    back_url = request.args.get('back_url') or request.referrer or url_for('call.setup')
    if 'incoming' in back_url or 'active' in back_url:
        back_url = url_for('call.setup')

    # 取得自訂訊息內容，若為空則依語音情境代入預設範本
    message_text = request.args.get('message', '').strip()
    if not message_text:
        default_msgs = {
            'voice_family': '爸：你怎麼還沒回家？快點回來，媽媽在找你！',
            'voice_boss': '老闆：今晚的專案報告有問題，你現在能回公司一趟嗎？',
            'voice_friend': '好朋友：我們在唱歌，快過來啦！就差你了！'
        }
        message_text = default_msgs.get(caller_data['voice_file'], '你在哪？快回來！')

    return render_template('call/incoming_msg.html', caller=caller_data, message=message_text, back_url=back_url)
