document.addEventListener('DOMContentLoaded', () => {
    // Web Audio API: DTMF 撥號音產生器
    const audioCtx = new (window.AudioContext || window.webkitAudioContext)();
    
    function playDTMF(value) {
        const frequencies = {
            '1': [697, 1209], '2': [697, 1336], '3': [697, 1477],
            '4': [770, 1209], '5': [770, 1336], '6': [770, 1477],
            '7': [852, 1209], '8': [852, 1336], '9': [852, 1477],
            '*': [941, 1209], '0': [941, 1336], '#': [941, 1477]
        };

        if (!frequencies[value]) return;

        const [f1, f2] = frequencies[value];
        const osc1 = audioCtx.createOscillator();
        const osc2 = audioCtx.createOscillator();
        const gainNode = audioCtx.createGain();

        osc1.frequency.value = f1;
        osc2.frequency.value = f2;
        osc1.type = 'sine';
        osc2.type = 'sine';

        gainNode.gain.setValueAtTime(0.1, audioCtx.currentTime);
        gainNode.gain.exponentialRampToValueAtTime(0.0001, audioCtx.currentTime + 0.5);

        osc1.connect(gainNode);
        osc2.connect(gainNode);
        gainNode.connect(audioCtx.destination);

        osc1.start();
        osc2.start();
        osc1.stop(audioCtx.currentTime + 0.5);
        osc2.stop(audioCtx.currentTime + 0.5);
    }

    // 處理通話計時
    const timerElement = document.getElementById('timer');
    if (timerElement) {
        let seconds = 0;
        
        function updateTimer() {
            seconds++;
            const mins = Math.floor(seconds / 60).toString().padStart(2, '0');
            const secs = (seconds % 60).toString().padStart(2, '0');
            timerElement.textContent = `${mins}:${secs}`;
        }
        
        setInterval(updateTimer, 1000);
    }
    
    // 處理按鈕點擊
    const btnMute = document.getElementById('btn-mute');
    const btnKeypad = document.getElementById('btn-keypad');
    const btnSpeaker = document.getElementById('btn-speaker');
    const btnAddCall = document.getElementById('btn-add-call');
    const btnFaceTime = document.getElementById('btn-facetime');
    const btnContacts = document.getElementById('btn-contacts');
    
    const keypadOverlay = document.getElementById('keypad-overlay');
    const btnHideKeypad = document.getElementById('btn-hide-keypad');
    const keypadDisplay = document.getElementById('keypad-display');
    const numBtns = document.querySelectorAll('.num-btn');

    if (btnMute) {
        btnMute.addEventListener('click', () => {
            btnMute.classList.toggle('active');
            const label = btnMute.querySelector('.label');
            if (btnMute.classList.contains('active')) {
                console.log('Muted');
            }
        });
    }

    if (btnSpeaker) {
        btnSpeaker.addEventListener('click', () => {
            btnSpeaker.classList.toggle('active');
            if (btnSpeaker.classList.contains('active')) {
                console.log('Speaker on');
            }
        });
    }

    if (btnKeypad) {
        btnKeypad.addEventListener('click', () => {
            keypadOverlay.style.display = 'flex';
        });
    }

    if (btnHideKeypad) {
        btnHideKeypad.addEventListener('click', () => {
            keypadOverlay.style.display = 'none';
        });
    }

    numBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            const val = btn.getAttribute('data-val');
            keypadDisplay.textContent += val;
            
            // 播放撥號音
            playDTMF(val);
            
            console.log('Pressed:', val);
        });
    });

    if (btnAddCall) {
        btnAddCall.addEventListener('click', () => {
            alert('正在跳轉至撥號介面...');
        });
    }

    if (btnFaceTime) {
        btnFaceTime.addEventListener('click', () => {
            alert('FaceTime 目前不可用');
        });
    }

    if (btnContacts) {
        btnContacts.addEventListener('click', () => {
            alert('正在開啟聯絡人...');
        });
    }

    // 語音內容定義 (可根據 scenario 名稱調整)
    const voiceScripts = {
        '媽媽': '喂？兒子啊，你怎麼還不回家？都幾點了，大家都在等你吃飯，趕快回來！',
        '老闆': '喂，那個，小王啊，現在有個緊急會議，你人在哪裡？能不能十分鐘內回辦公室？',
        '王大明': '喂！兄弟！趕快過來救火，我現在在便利商店這邊遇到大麻煩了，快點！'
    };

    let hasSpoken = false;

    function speakScenario() {
        if (hasSpoken) return; // 如果已經說過，就直接返回
        
        const callerNameElement = document.querySelector('.caller-name');
        if (!callerNameElement) return;

        const callerName = callerNameElement.textContent;
        const msg = new SpeechSynthesisUtterance();
        msg.text = voiceScripts[callerName] || '喂？聽得到嗎？你好？';
        msg.lang = 'zh-TW';
        msg.rate = 1.0;
        
        msg.onstart = () => { hasSpoken = true; }; // 開始說話時標記為已播放
        
        window.speechSynthesis.speak(msg);
    }

    // 處理音檔播放與 TTS
    const audio = document.getElementById('scenario-audio');
    if (audio) {
        // 先嘗試啟動 TTS
        speakScenario();

        // 嘗試播放實體音檔
        const playPromise = audio.play();

        if (playPromise !== undefined) {
            playPromise.catch(error => {
                console.log('Autoplay prevented. User interaction required.');
                document.body.addEventListener('click', () => {
                    audio.play();
                    speakScenario(); // 使用者互動後重試，但會被 hasSpoken 擋住若已在說話
                }, { once: true });
            });
        }
    }

    // 掛斷按鈕與卸載時強制停止所有語音
    const btnEnd = document.querySelector('.btn-end');
    if (btnEnd) {
        btnEnd.addEventListener('click', () => {
            window.speechSynthesis.cancel();
        });
    }

    // 當使用者離開頁面（例如按回上一頁）也停止語音
    window.addEventListener('beforeunload', () => {
        window.speechSynthesis.cancel();
    });
});
