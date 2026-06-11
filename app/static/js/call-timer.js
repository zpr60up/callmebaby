/**
 * Call Timer & Active Call — 通話中控制邏輯
 * 計時器、靜音、擴音、鍵盤、掛斷
 */

let timerInterval = null;
let timerSeconds = 0;
let keypadDisplay = '';

/**
 * 啟動通話中畫面
 */
function startActiveCall() {
    // 更新狀態列時間
    updateStatusTime();
    setInterval(updateStatusTime, 1000);

    // 啟動計時器
    startTimer();

    // 播放預錄語音
    const voiceFile = document.getElementById('caller-voice');
    const voiceGender = document.getElementById('caller-voice-gender');
    if (voiceFile && voiceFile.value) {
        const gender = (voiceGender && voiceGender.value) ? voiceGender.value : 'female';
        audioManager.playVoice(voiceFile.value, gender);
    }
}

/**
 * 啟動通話計時器
 */
function startTimer() {
    timerSeconds = 0;
    updateTimerDisplay();

    timerInterval = setInterval(() => {
        timerSeconds++;
        updateTimerDisplay();
    }, 1000);
}

/**
 * 更新計時器顯示
 */
function updateTimerDisplay() {
    const mins = Math.floor(timerSeconds / 60).toString().padStart(2, '0');
    const secs = (timerSeconds % 60).toString().padStart(2, '0');
    const display = document.getElementById('call-timer');
    if (display) display.textContent = `${mins}:${secs}`;
}

/**
 * 切換靜音
 */
function toggleMute() {
    const muted = audioManager.toggleMute();
    const icon = document.getElementById('icon-mute');
    const label = document.getElementById('label-mute');

    if (icon) {
        if (muted) {
            icon.classList.add('active');
            icon.querySelector('.material-icons-round').textContent = 'mic_off';
        } else {
            icon.classList.remove('active');
            icon.querySelector('.material-icons-round').textContent = 'mic';
        }
    }
    if (label) label.textContent = muted ? '取消靜音' : '靜音';
}

/**
 * 切換擴音
 */
function toggleSpeaker() {
    const speaker = audioManager.toggleSpeaker();
    const icon = document.getElementById('icon-speaker');
    const label = document.getElementById('label-speaker');

    if (icon) {
        if (speaker) {
            icon.classList.add('active');
        } else {
            icon.classList.remove('active');
        }
    }
    if (label) label.textContent = speaker ? '關閉擴音' : '擴音';
}

/**
 * 切換數字鍵盤
 */
function toggleKeypad() {
    const overlay = document.getElementById('keypad-overlay');
    if (!overlay) return;

    if (overlay.style.display === 'none' || !overlay.style.display) {
        overlay.style.display = 'block';
    } else {
        overlay.style.display = 'none';
    }
}

/**
 * 按下數字鍵
 */
function pressKey(key) {
    keypadDisplay += key;
    const display = document.getElementById('keypad-display');
    if (display) display.textContent = keypadDisplay;

    // DTMF 音效
    playDTMF(key);
}

/**
 * 播放 DTMF 音效
 */
function playDTMF(key) {
    try {
        const ctx = new (window.AudioContext || window.webkitAudioContext)();
        const dtmfFreqs = {
            '1': [697, 1209], '2': [697, 1336], '3': [697, 1477],
            '4': [770, 1209], '5': [770, 1336], '6': [770, 1477],
            '7': [852, 1209], '8': [852, 1336], '9': [852, 1477],
            '*': [941, 1209], '0': [941, 1336], '#': [941, 1477]
        };

        const freqs = dtmfFreqs[key];
        if (!freqs) return;

        freqs.forEach(freq => {
            const osc = ctx.createOscillator();
            const gain = ctx.createGain();
            osc.frequency.value = freq;
            osc.type = 'sine';
            gain.gain.value = 0.1;
            osc.connect(gain);
            gain.connect(ctx.destination);
            osc.start();
            osc.stop(ctx.currentTime + 0.15);
        });

        setTimeout(() => ctx.close(), 200);
    } catch (e) {
        // 忽略
    }
}

/**
 * 結束通話
 */
function endActiveCall() {
    // 停止計時器
    if (timerInterval) {
        clearInterval(timerInterval);
        timerInterval = null;
    }

    // 停止音訊
    audioManager.endCall();

    // 轉場動畫
    const screen = document.getElementById('call-active-screen');
    if (screen) screen.classList.add('ending');

    // 返回設定頁
    const setupUrl = document.getElementById('setup-url');
    setTimeout(() => {
        if (setupUrl) {
            window.location.href = setupUrl.value;
        }
    }, 400);
}

/**
 * 更新狀態列時間（在 call-incoming.js 也有，這裡重複定義以防獨立載入）
 */
if (typeof updateStatusTime === 'undefined') {
    function updateStatusTime() {
        const now = new Date();
        const h = now.getHours().toString().padStart(2, '0');
        const m = now.getMinutes().toString().padStart(2, '0');
        const timeStr = `${h}:${m}`;
        const el = document.getElementById('call-status-time');
        if (el) el.textContent = timeStr;
    }
}
