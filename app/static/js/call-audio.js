/**
 * Call Audio Manager — 音訊播放控制
 * 管理鈴聲、預錄語音、TTS 語音合成
 */

class CallAudioManager {
    constructor() {
        this.ringtone = null;
        this.voiceAudio = null;
        this.isMuted = false;
        this.isSpeaker = false;
        this.vibrationInterval = null;

        // 語音對話腳本（使用 TTS 合成）
        this.voiceScripts = {
            voice_family: [
                { text: '喂，你在哪裡啊？怎麼還沒回來？', delay: 1000 },
                { text: '飯菜都涼了，趕快回來吧！', delay: 5000 },
                { text: '你有沒有在聽啊？路上小心喔！', delay: 9000 },
                { text: '好，那你快一點，我等你喔。掰掰！', delay: 14000 }
            ],
            voice_boss: [
                { text: '喂，你現在方便講電話嗎？', delay: 1000 },
                { text: '公司這邊有個急件需要你馬上處理。', delay: 4500 },
                { text: '客戶那邊催得很急，你趕快過來一趟。', delay: 9000 },
                { text: '好，那你儘快，先這樣。', delay: 14000 }
            ],
            voice_friend: [
                { text: '欸！你在幹嘛？出來玩啦！', delay: 1000 },
                { text: '我們在那個老地方等你，快來！', delay: 5000 },
                { text: '大家都到了就差你一個，快點啦！', delay: 9000 },
                { text: '好啦好啦，你快來就對了，掰！', delay: 13000 }
            ]
        };
    }

    /**
     * 建立鈴聲（使用 Web Audio API 合成）
     */
    createRingtone() {
        try {
            this.audioCtx = new (window.AudioContext || window.webkitAudioContext)();
            this._playRingtoneLoop();
        } catch (e) {
            console.warn('[Audio] 無法建立 AudioContext:', e);
        }
    }

    _playRingtoneLoop() {
        if (!this.audioCtx || this.ringtoneStopped) return;

        const ctx = this.audioCtx;
        const now = ctx.currentTime;

        // 模擬電話鈴聲：雙音交替
        const frequencies = [440, 480]; // 標準電話鈴聲頻率
        const duration = 1.0;
        const pause = 2.0;

        frequencies.forEach(freq => {
            const osc = ctx.createOscillator();
            const gain = ctx.createGain();

            osc.frequency.value = freq;
            osc.type = 'sine';

            gain.gain.setValueAtTime(0, now);
            gain.gain.linearRampToValueAtTime(0.15, now + 0.02);
            gain.gain.setValueAtTime(0.15, now + duration - 0.02);
            gain.gain.linearRampToValueAtTime(0, now + duration);

            osc.connect(gain);
            gain.connect(ctx.destination);

            osc.start(now);
            osc.stop(now + duration);
        });

        // 循環播放
        this.ringtoneTimer = setTimeout(() => {
            this._playRingtoneLoop();
        }, (duration + pause) * 1000);
    }

    /**
     * 開始播放鈴聲
     */
    startRinging() {
        this.ringtoneStopped = false;
        this.createRingtone();
        this.tryVibrate();
    }

    /**
     * 停止鈴聲
     */
    stopRinging() {
        this.ringtoneStopped = true;
        if (this.ringtoneTimer) {
            clearTimeout(this.ringtoneTimer);
            this.ringtoneTimer = null;
        }
        if (this.audioCtx) {
            this.audioCtx.close().catch(() => {});
            this.audioCtx = null;
        }
        this.stopVibrate();
    }

    /**
     * 播放預錄語音（使用 TTS）
     */
    playVoice(voiceFile) {
        const script = this.voiceScripts[voiceFile];
        if (!script) {
            console.warn('[Audio] 找不到語音腳本:', voiceFile);
            return;
        }

        // 檢查 TTS 是否可用
        if (!('speechSynthesis' in window)) {
            console.warn('[Audio] 此瀏覽器不支援 TTS');
            return;
        }

        this.voiceTimeouts = [];

        script.forEach(line => {
            const timeout = setTimeout(() => {
                if (this.isMuted) return;

                const utterance = new SpeechSynthesisUtterance(line.text);
                utterance.lang = 'zh-TW';
                utterance.rate = 0.95;
                utterance.pitch = 1.0;
                utterance.volume = this.isSpeaker ? 1.0 : 0.7;

                // 嘗試使用中文語音
                const voices = speechSynthesis.getVoices();
                const zhVoice = voices.find(v => v.lang.startsWith('zh'));
                if (zhVoice) utterance.voice = zhVoice;

                speechSynthesis.speak(utterance);
            }, line.delay);

            this.voiceTimeouts.push(timeout);
        });
    }

    /**
     * 停止語音播放
     */
    stopVoice() {
        if (this.voiceTimeouts) {
            this.voiceTimeouts.forEach(t => clearTimeout(t));
            this.voiceTimeouts = [];
        }
        if ('speechSynthesis' in window) {
            speechSynthesis.cancel();
        }
    }

    /**
     * 切換靜音
     */
    toggleMute() {
        this.isMuted = !this.isMuted;
        return this.isMuted;
    }

    /**
     * 切換擴音
     */
    toggleSpeaker() {
        this.isSpeaker = !this.isSpeaker;
        return this.isSpeaker;
    }

    /**
     * 結束通話 — 停止所有音訊
     */
    endCall() {
        this.stopRinging();
        this.stopVoice();
        this.stopVibrate();
    }

    /**
     * 嘗試振動
     */
    tryVibrate() {
        if ('vibrate' in navigator) {
            this.vibrationInterval = setInterval(() => {
                navigator.vibrate([300, 200, 300, 200, 300, 1500]);
            }, 2700);
        }
    }

    /**
     * 停止振動
     */
    stopVibrate() {
        if (this.vibrationInterval) {
            clearInterval(this.vibrationInterval);
            this.vibrationInterval = null;
        }
        if ('vibrate' in navigator) {
            navigator.vibrate(0);
        }
    }

    /**
     * 播放擬真訊息提示音（使用 Web Audio API 合成）
     */
    playNotificationSound(style = 'ios') {
        try {
            const ctx = new (window.AudioContext || window.webkitAudioContext)();
            const now = ctx.currentTime;

            if (style === 'ios') {
                // iOS 經典三音符 (Tri-tone): G5(784Hz) -> C6(1046.5Hz) -> E6(1318.5Hz)
                const notes = [
                    { freq: 784.0, start: 0, dur: 0.15 },
                    { freq: 1046.5, start: 0.12, dur: 0.15 },
                    { freq: 1318.5, start: 0.24, dur: 0.4 }
                ];
                notes.forEach(note => {
                    const osc = ctx.createOscillator();
                    const gain = ctx.createGain();

                    osc.type = 'sine';
                    osc.frequency.setValueAtTime(note.freq, now + note.start);

                    gain.gain.setValueAtTime(0, now + note.start);
                    gain.gain.linearRampToValueAtTime(0.2, now + note.start + 0.02);
                    gain.gain.setValueAtTime(0.2, now + note.start + note.dur - 0.02);
                    gain.gain.linearRampToValueAtTime(0, now + note.start + note.dur);

                    osc.connect(gain);
                    gain.connect(ctx.destination);

                    osc.start(now + note.start);
                    osc.stop(now + note.start + note.dur);
                });
            } else {
                // Android 經典雙音符 (Ding-dong): A5(880Hz) -> C#6(1100Hz)
                const notes = [
                    { freq: 880.0, start: 0, dur: 0.12 },
                    { freq: 1100.0, start: 0.1, dur: 0.3 }
                ];
                notes.forEach(note => {
                    const osc = ctx.createOscillator();
                    const gain = ctx.createGain();

                    osc.type = 'sine';
                    osc.frequency.setValueAtTime(note.freq, now + note.start);

                    gain.gain.setValueAtTime(0, now + note.start);
                    gain.gain.linearRampToValueAtTime(0.2, now + note.start + 0.02);
                    gain.gain.setValueAtTime(0.2, now + note.start + note.dur - 0.02);
                    gain.gain.linearRampToValueAtTime(0, now + note.start + note.dur);

                    osc.connect(gain);
                    gain.connect(ctx.destination);

                    osc.start(now + note.start);
                    osc.stop(now + note.start + note.dur);
                });
            }
        } catch (e) {
            console.warn('[Audio] 無法播放訊息提示音:', e);
        }
    }

    /**
     * 訊息觸發單次震動
     */
    vibrateOnce() {
        if ('vibrate' in navigator) {
            navigator.vibrate([200, 100, 200]);
        }
    }
}

// 全域實例
const audioManager = new CallAudioManager();

// 預載 TTS 語音列表
if ('speechSynthesis' in window) {
    speechSynthesis.getVoices();
    speechSynthesis.onvoiceschanged = () => speechSynthesis.getVoices();
}
