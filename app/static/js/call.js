document.addEventListener('DOMContentLoaded', () => {
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
    
    // 處理音檔播放 (如果瀏覽器有自動播放限制，可能需要這段來確保使用者點擊後能播)
    const audio = document.getElementById('scenario-audio');
    if (audio) {
        // 嘗試播放，若被阻擋則等待使用者互動
        const playPromise = audio.play();
        if (playPromise !== undefined) {
            playPromise.catch(error => {
                console.log('Autoplay prevented. User interaction required.');
                // Add event listener to body to start playing on first click
                document.body.addEventListener('click', () => {
                    audio.play();
                }, { once: true });
            });
        }
    }
});
