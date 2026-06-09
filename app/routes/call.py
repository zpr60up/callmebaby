"""
Call Routes — 來電模擬功能路由
處理來電者管理（CRUD）與來電畫面顯示。
"""

import os
import time
import uuid
import sqlite3
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from app.models import caller as caller_model
from app.models import recording as recording_model

call_bp = Blueprint('call', __name__, url_prefix='/call')


# ─────────────────────────────────────────────
# 來電設定頁面
# ─────────────────────────────────────────────

@call_bp.route('/setup')
def setup():
    """顯示來電者管理頁面，列出所有已儲存的來電者。"""
    callers = caller_model.get_all()
    recordings = recording_model.get_all()
    return render_template('call/setup.html', callers=callers, recordings=recordings)


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

    # 處理自訂錄音檔案上傳
    if voice_file == 'custom_recording':
        uploaded_file = request.files.get('voice_file_upload')
        if uploaded_file and uploaded_file.filename:
            ext = os.path.splitext(uploaded_file.filename)[1]
            if not ext:
                ext = '.webm'
            filename = f"recording_{int(time.time())}_{uuid.uuid4().hex[:8]}{ext}"
            
            # 確保 static/audio 目錄存在
            audio_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'app', 'static', 'audio')
            os.makedirs(audio_dir, exist_ok=True)
            
            save_path = os.path.join(audio_dir, filename)
            uploaded_file.save(save_path)
            voice_file = filename
        else:
            flash('自訂錄音失敗，請重新錄音！', 'error')
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

    # 處理自訂錄音檔案上傳
    if voice_file == 'custom_recording':
        uploaded_file = request.files.get('voice_file_upload')
        if uploaded_file and uploaded_file.filename:
            ext = os.path.splitext(uploaded_file.filename)[1]
            if not ext:
                ext = '.webm'
            filename = f"recording_{int(time.time())}_{uuid.uuid4().hex[:8]}{ext}"
            
            # 確保 static/audio 目錄存在
            audio_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'app', 'static', 'audio')
            os.makedirs(audio_dir, exist_ok=True)
            
            save_path = os.path.join(audio_dir, filename)
            uploaded_file.save(save_path)
            voice_file = filename
        else:
            # 如果沒有新上傳錄音，保留原本的聲音檔名
            old_caller = caller_model.get_by_id(caller_id)
            if old_caller:
                voice_file = old_caller['voice_file']

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
# 來電畫面
# ─────────────────────────────────────────────

@call_bp.route('/incoming/<int:caller_id>')
def incoming(caller_id):
    """顯示模擬來電畫面（依據來電者設定的風格）。"""
    c = caller_model.get_by_id(caller_id)
    if not c:
        flash('找不到該來電者！', 'error')
        return redirect(url_for('call.setup'))

    style = c['call_style'] if c['call_style'] in ('ios', 'android') else 'ios'
    template = f'call/incoming_{style}.html'
    return render_template(template, caller=c)


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
@call_bp.route('/incoming_msg/<int:caller_id>')
def incoming_msg(caller_id):
    """顯示模擬訊息接收（鎖定/推播通知）畫面。"""
    c = caller_model.get_by_id(caller_id)
    if not c:
        flash('找不到該來電者！', 'error')
        return redirect(url_for('call.setup'))

    # 取得自訂訊息內容，若為空則依語音情境代入預設範本
    message_text = request.args.get('message', '').strip()
    if not message_text:
        default_msgs = {
            'voice_family': '爸：你怎麼還沒回家？快點回來，媽媽在找你！',
            'voice_boss': '老闆：今晚的專案報告有問題，你現在能回公司一趟嗎？',
            'voice_friend': '好朋友：我們在唱歌，快過來啦！就差你了！'
        }
        message_text = default_msgs.get(c['voice_file'], '你在哪？快回來！')

    return render_template('call/incoming_msg.html', caller=c, message=message_text)



# ─────────────────────────────────────────────
# 錄音系統管理
# ─────────────────────────────────────────────

@call_bp.route('/recordings')
def recordings():
    """顯示錄音系統主頁面。"""
    recs = recording_model.get_all()
    # 取得正在使用中的錄音檔名
    callers = caller_model.get_all()
    used_filenames = {c['voice_file'] for c in callers}
    return render_template('call/recordings.html', recordings=recs, used_filenames=used_filenames)


@call_bp.route('/recordings/upload', methods=['POST'])
def upload_recording():
    """上傳 AJAX 錄音 Blob 並存檔。"""
    display_name = request.form.get('display_name', '').strip()
    uploaded_file = request.files.get('audio')

    if not display_name:
        display_name = f"錄音_{int(time.time())}"

    if not uploaded_file or not uploaded_file.filename:
        return jsonify({'success': False, 'error': '沒有收到錄音檔案'}), 400

    ext = os.path.splitext(uploaded_file.filename)[1]
    if not ext:
        ext = '.webm'
    
    # 產出唯一檔案名稱
    filename = f"recording_{int(time.time())}_{uuid.uuid4().hex[:8]}{ext}"
    
    # 確保 static/audio 目錄存在
    audio_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'app', 'static', 'audio')
    os.makedirs(audio_dir, exist_ok=True)
    
    save_path = os.path.join(audio_dir, filename)
    uploaded_file.save(save_path)

    # 寫入 recordings 資料庫
    rec_id = recording_model.create(filename, display_name)
    if rec_id:
        return jsonify({
            'success': True,
            'id': rec_id,
            'filename': filename,
            'display_name': display_name
        })
    else:
        return jsonify({'success': False, 'error': '寫入資料庫失敗'}), 500


@call_bp.route('/recordings/<int:rec_id>/delete', methods=['POST'])
def delete_recording(rec_id):
    """刪除一筆錄音記錄與實體檔案，並重設關聯的來電者語音。"""
    rec = recording_model.get_by_id(rec_id)
    if not rec:
        flash('找不到該錄音記錄！', 'error')
        return redirect(url_for('call.recordings'))

    filename = rec['filename']
    
    # 1. 刪除資料庫記錄
    recording_model.delete(rec_id)

    # 2. 刪除實體檔案
    audio_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'app', 'static', 'audio')
    file_path = os.path.join(audio_dir, filename)
    if os.path.exists(file_path):
        try:
            os.remove(file_path)
        except Exception as e:
            print(f"[Call Routes] 刪除音訊檔案失敗 {file_path}: {e}")

    # 3. 將有關聯的來電者的語音重設為預設 'voice_family'
    try:
        conn = sqlite3.connect(caller_model.DB_PATH)
        conn.execute('UPDATE callers SET voice_file = "voice_family" WHERE voice_file = ?', (filename,))
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"[Call Routes] 重設來電者語音關聯失敗: {e}")

    flash(f'已刪除自訂錄音「{rec["display_name"]}」。', 'success')
    return redirect(url_for('call.recordings'))
