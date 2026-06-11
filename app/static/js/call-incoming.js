/**
 * Call Incoming — 來電畫面互動邏輯
 * 處理接聽、拒接、狀態時間更新
 */

let currentStyle = 'ios';

/**
 * 啟動來電畫面
 */
function startIncomingCall(style) {
    currentStyle = style;

    // 更新狀態列時間
    updateStatusTime();
    setInterval(updateStatusTime, 1000);

    // 播放鈴聲
    audioManager.startRinging(style);

    // 添加振鈴動畫
    const screen = document.getElementById(style === 'ios' ? 'ios-call-screen' : 'android-call-screen');
    if (screen) screen.classList.add('ringing');

    // 嘗試全螢幕
    tryFullscreen();
}

/**
 * 接聽來電
 */
function acceptCall() {
    // 停止鈴聲
    audioManager.stopRinging();

    // 移除振鈴動畫
    const screenId = currentStyle === 'ios' ? 'ios-call-screen' : 'android-call-screen';
    const screen = document.getElementById(screenId);
    if (screen) {
        screen.classList.remove('ringing');
        screen.classList.add('fading-out');
    }

    // 轉場到通話中
    const activeUrl = document.getElementById('active-call-url');
    setTimeout(() => {
        if (activeUrl) {
            window.location.href = activeUrl.value;
        }
    }, 400);
}

/**
 * 拒接來電
 */
function declineCall() {
    // 停止鈴聲
    audioManager.stopRinging();

    const screenId = currentStyle === 'ios' ? 'ios-call-screen' : 'android-call-screen';
    const screen = document.getElementById(screenId);
    if (screen) {
        screen.classList.remove('ringing');
        screen.classList.add('fading-out');
    }

    // 返回設定頁
    const setupUrl = document.getElementById('setup-url');
    setTimeout(() => {
        if (setupUrl) {
            window.location.href = setupUrl.value;
        }
    }, 400);
}

/**
 * 更新狀態列時間
 */
function updateStatusTime() {
    const now = new Date();
    const h = now.getHours().toString().padStart(2, '0');
    const m = now.getMinutes().toString().padStart(2, '0');
    const timeStr = `${h}:${m}`;

    // iOS
    const iosTime = document.getElementById('ios-status-time');
    if (iosTime) iosTime.textContent = timeStr;

    // Android
    const androidTime = document.getElementById('android-status-time');
    if (androidTime) androidTime.textContent = timeStr;

    // In-call
    const callTime = document.getElementById('call-status-time');
    if (callTime) callTime.textContent = timeStr;
}

/**
 * 嘗試進入全螢幕
 */
function tryFullscreen() {
    const el = document.documentElement;
    if (el.requestFullscreen) {
        el.requestFullscreen().catch(() => {});
    } else if (el.webkitRequestFullscreen) {
        el.webkitRequestFullscreen();
    }
}

// iOS 滑動接聽手勢（用於滑動模式）
(function initSlideGesture() {
    const thumb = document.getElementById('ios-slide-thumb');
    if (!thumb) return;

    const track = thumb.parentElement;
    let startX = 0;
    let isDragging = false;

    thumb.addEventListener('touchstart', (e) => {
        isDragging = true;
        startX = e.touches[0].clientX;
        thumb.style.transition = 'none';
    });

    document.addEventListener('touchmove', (e) => {
        if (!isDragging) return;
        const dx = e.touches[0].clientX - startX;
        const maxDx = track.clientWidth - thumb.clientWidth - 8;
        const clampedDx = Math.max(0, Math.min(dx, maxDx));
        thumb.style.left = (4 + clampedDx) + 'px';
    });

    document.addEventListener('touchend', () => {
        if (!isDragging) return;
        isDragging = false;
        thumb.style.transition = 'left 0.3s ease';

        const maxDx = track.clientWidth - thumb.clientWidth - 8;
        const currentLeft = parseInt(thumb.style.left) - 4;

        if (currentLeft > maxDx * 0.7) {
            thumb.style.left = (4 + maxDx) + 'px';
            setTimeout(() => acceptCall(), 200);
        } else {
            thumb.style.left = '4px';
        }
    });
})();
