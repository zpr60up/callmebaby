// App State
let currentConfig = {
    caller_name: '',
    caller_phone: '',
    avatar_path: '',
    audio_path: ''
};
let triggerTimeout = null;

// DOM Elements
document.addEventListener('DOMContentLoaded', () => {
    // Tab Switching
    const tabBtns = document.querySelectorAll('.tab-btn');
    const tabContents = document.querySelectorAll('.tab-content');
    
    tabBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            tabBtns.forEach(b => b.classList.remove('active'));
            tabContents.forEach(c => c.classList.remove('active'));
            
            btn.classList.add('active');
            document.getElementById(btn.dataset.target).classList.add('active');
        });
    });

    // Slider
    const delaySlider = document.getElementById('delay-slider');
    const timerVal = document.getElementById('timer-val');
    
    if (delaySlider) {
        delaySlider.addEventListener('input', (e) => {
            const val = parseInt(e.target.value);
            if (val === 0) {
                timerVal.textContent = '即時';
            } else if (val < 60) {
                timerVal.textContent = `${val} 秒`;
            } else {
                const mins = Math.floor(val / 60);
                const secs = val % 60;
                timerVal.textContent = secs > 0 ? `${mins}分 ${secs}秒` : `${mins}分鐘`;
            }
        });
    }

    // Trigger Button
    const triggerBtn = document.getElementById('trigger-btn');
    if (triggerBtn) {
        triggerBtn.addEventListener('click', startTriggerProcess);
    }

    // Cancel Button
    const cancelBtn = document.getElementById('cancel-btn');
    if (cancelBtn) {
        cancelBtn.addEventListener('click', cancelTrigger);
    }

    // Custom Form Submit
    const customForm = document.getElementById('custom-form');
    if (customForm) {
        customForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const name = document.getElementById('custom_name').value;
            const phone = document.getElementById('custom_phone').value;
            
            try {
                const res = await fetch('/api/custom_callers', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ caller_name: name, caller_phone: phone })
                });
                const data = await res.json();
                if (data.success) {
                    alert('已儲存自訂來電者！');
                    window.location.reload(); // Quick refresh to show in list
                }
            } catch (err) {
                console.error(err);
            }
        });
        
        // Also update selection when typing
        document.getElementById('custom_name').addEventListener('input', updateCustomSelection);
        document.getElementById('custom_phone').addEventListener('input', updateCustomSelection);
    }

    // Call Screen logic (if we are on the call page)
    if (document.getElementById('incoming-state')) {
        playRingtone();
    }
});

// Functions
function selectScenario(name, phone, avatar) {
    currentConfig = { caller_name: name, caller_phone: phone, avatar_path: avatar, audio_path: '' };
    updateUISelection();
}

function fillCustom(name, phone) {
    document.getElementById('custom_name').value = name;
    document.getElementById('custom_phone').value = phone;
    updateCustomSelection();
}

function updateCustomSelection() {
    const name = document.getElementById('custom_name').value;
    const phone = document.getElementById('custom_phone').value;
    if (name) {
        currentConfig = { caller_name: name, caller_phone: phone, avatar_path: '', audio_path: '' };
        updateUISelection();
    }
}

function updateUISelection() {
    document.getElementById('display-name').textContent = currentConfig.caller_name;
    document.getElementById('display-phone').textContent = currentConfig.caller_phone || '無號碼';
    document.getElementById('trigger-btn').disabled = false;
}

function startTriggerProcess() {
    const delaySlider = document.getElementById('delay-slider');
    const delaySeconds = parseInt(delaySlider.value);
    
    if (delaySeconds === 0) {
        executeCall();
    } else {
        document.getElementById('countdown-overlay').classList.remove('hidden');
        triggerTimeout = setTimeout(executeCall, delaySeconds * 1000);
    }
}

function cancelTrigger() {
    if (triggerTimeout) {
        clearTimeout(triggerTimeout);
        triggerTimeout = null;
    }
    document.getElementById('countdown-overlay').classList.add('hidden');
}

function executeCall() {
    let avatar = 'avatar_default.png';
    if (currentConfig.avatar_path) {
        avatar = currentConfig.avatar_path.substring(currentConfig.avatar_path.lastIndexOf('/') + 1);
        if (!avatar || avatar.indexOf('.') === -1) {
            avatar = 'avatar_default.png';
        }
    }
    
    // Resolve voice file
    let voiceFile = 'voice_family';
    if (currentConfig.audio_path) {
        const s = currentConfig.audio_path.toLowerCase();
        if (s.includes('family') || s.includes('mom') || s.includes('dad')) voiceFile = 'voice_family';
        else if (s.includes('boss') || s.includes('work') || s.includes('overtime')) voiceFile = 'voice_boss';
        else if (s.includes('delivery') || s.includes('friend') || s.includes('sing') || s.includes('social')) voiceFile = 'voice_friend';
    } else {
        // Fallback checks on caller name to make it look smart
        const n = currentConfig.caller_name || '';
        if (n.includes('爸') || n.includes('媽') || n.includes('母') || n.includes('家')) voiceFile = 'voice_family';
        else if (n.includes('老闆') || n.includes('主管') || n.includes('經理') || n.includes('公')) voiceFile = 'voice_boss';
        else if (n.includes('友') || n.includes('歌') || n.includes('快遞')) voiceFile = 'voice_friend';
    }

    const params = new URLSearchParams({
        name: currentConfig.caller_name || '未知',
        phone: currentConfig.caller_phone || '0900-000-000',
        avatar: avatar,
        voice_file: voiceFile,
        call_style: 'ios',
        back_url: window.location.pathname
    });

    window.location.href = `/call/incoming?${params.toString()}`;
}

// Call Screen Logic
let callTimerInterval = null;
let callSeconds = 0;

function playRingtone() {
    // Play vibration or sound if possible
    if ("vibrate" in navigator) {
        navigator.vibrate([1000, 1000, 1000, 1000, 1000, 1000]);
    }
}

function acceptCall() {
    // Stop ringing
    if ("vibrate" in navigator) navigator.vibrate(0);
    
    document.getElementById('incoming-state').classList.remove('active');
    document.getElementById('active-state').classList.add('active');
    
    // Start timer
    callSeconds = 0;
    const timerDisplay = document.getElementById('call-timer');
    
    callTimerInterval = setInterval(() => {
        callSeconds++;
        const m = Math.floor(callSeconds / 60).toString().padStart(2, '0');
        const s = (callSeconds % 60).toString().padStart(2, '0');
        timerDisplay.textContent = `${m}:${s}`;
    }, 1000);
}

function rejectCall() {
    if ("vibrate" in navigator) navigator.vibrate(0);
    window.location.href = '/';
}

function endCall() {
    if (callTimerInterval) clearInterval(callTimerInterval);
    window.location.href = '/';
}
