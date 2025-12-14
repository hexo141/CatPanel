// 玻璃消息模块
window.showMessage = (function() {
    // 创建容器（如果不存在）
    const initContainer = () => {
        let container = document.getElementById('glass-message-container');
        if (!container) {
            container = document.createElement('div');
            container.id = 'glass-message-container';
            document.body.appendChild(container);
        }
        return container;
    };

    // 创建消息元素
    const createMessageElement = (type, content) => {
        const message = document.createElement('div');
        message.className = `glass-message ${type}`;
        
        // 添加图标
        const icons = {
            success: '✓',
            error: '✗',
            warning: '!',
            info: 'i'
        };
        
        message.innerHTML = `
            <span class="icon">${icons[type] || 'i'}</span>
            <span class="content">${content}</span>
            <button class="close-btn" aria-label="关闭消息">&times;</button>
            <div class="progress">
                <div class="progress-bar"></div>
            </div>
        `;
        
        return message;
    };

    // 显示消息
    const showMessage = (type, content) => {
        // 验证类型
        const validTypes = ['success', 'error', 'warning', 'info'];
        if (!validTypes.includes(type)) {
            type = 'info';
        }
        
        // 初始化容器
        const container = initContainer();
        
        // 创建消息元素
        const message = createMessageElement(type, content);
        container.prepend(message);
        
        // 强制重排以触发动画
        void message.offsetWidth;
        
        // 显示消息
        setTimeout(() => {
            message.classList.add('show');
        }, 10);
        
        // 进度条元素
        const progressBar = message.querySelector('.progress-bar');
        let closeTimer;
        
        // 播放音效
        const audio = new Audio('/GetAssets/Mes_audio');
        // 调整声音大小
        audio.volume = 0.4;
        audio.play();

        // 设置自动关闭
        const startAutoClose = () => {
            closeTimer = setTimeout(() => {
                closeMessage(message);
            }, 3000);
        };
        
        // 暂停自动关闭
        const pauseAutoClose = () => {
            clearTimeout(closeTimer);
            message.classList.add('paused');
        };
        
        // 恢复自动关闭
        const resumeAutoClose = () => {
            message.classList.remove('paused');
            // 重新计时，考虑已经过去的时间
            const computedStyle = window.getComputedStyle(progressBar);
            const animationDuration = parseFloat(computedStyle.animationDuration) * 1000; // 3000ms
            const animationPlayState = computedStyle.animationPlayState;
            const animationCurrentTime = progressBar.getAnimations()[0]?.currentTime || 0;
            
            if (animationCurrentTime > 0) {
                const remainingTime = animationDuration - animationCurrentTime;
                closeTimer = setTimeout(() => {
                    closeMessage(message);
                }, remainingTime);
            } else {
                startAutoClose();
            }
        };
        
        // 关闭消息
        const closeMessage = (msg) => {
            msg.classList.remove('show');
            // 移除元素
            setTimeout(() => {
                if (msg && msg.parentNode) {
                    msg.parentNode.removeChild(msg);
                }
            }, 400);
        };
        
        // 添加关闭按钮事件
        message.querySelector('.close-btn').addEventListener('click', (e) => {
            e.stopPropagation();
            clearTimeout(closeTimer);
            closeMessage(message);
        });
        
        // 鼠标悬停暂停
        message.addEventListener('mouseenter', () => {
            pauseAutoClose();
        });
        
        // 鼠标离开恢复
        message.addEventListener('mouseleave', () => {
            resumeAutoClose();
        });
        
        // 启动自动关闭
        startAutoClose();
        
        return {
            close: () => {
                clearTimeout(closeTimer);
                closeMessage(message);
            }
        };
    };
    
    // 返回公共API
    return showMessage;
})();