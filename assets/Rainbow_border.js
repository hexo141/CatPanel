// rainbow-border.js
(function() {
    // 创建样式
    const style = document.createElement('style');
    style.textContent = `
    #rainbow-border-container {
        position: fixed;
        pointer-events: none;
        z-index: 2147483647; /* 最高层 */
        transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1);
        transform: translate3d(0, 0, 0); /* 创建新合成层 */
        visibility: hidden;
        opacity: 0;
        backdrop-filter: none !important;
        -webkit-backdrop-filter: none !important;
        isolation: isolate;
        background: transparent !important;
    }
    #rainbow-border {
        width: 100%;
        height: 100%;
        border-radius: inherit;
        border: 2.2px solid white;
        box-shadow: 0 0 0 1px rgba(255, 255, 255, 0.3);
        /* 补充：防止子元素触发模糊 */
        backdrop-filter: none !important;
        -webkit-backdrop-filter: none !important;
    }
`;
    document.head.appendChild(style);

    // 创建边框容器
    const container = document.createElement('div');
    container.id = 'rainbow-border-container';
    container.innerHTML = '<div id="rainbow-border"></div>';
    document.body.appendChild(container);

    let currentElement = null;
    let animationFrame = null;
    let lastUpdate = 0;
    const UPDATE_INTERVAL = 50; // 50ms 更新一次位置 (20fps)
    const BORDER_WIDTH = 3;

    // 获取元素圆角（处理各种圆角格式）
    function getElementBorderRadius(el) {
        const style = window.getComputedStyle(el);
        const radius = style.borderRadius;
        
        // 处理 "50% 20px" 等复杂格式
        if (radius.includes(' ')) {
            const parts = radius.split(' ');
            return `${parseFloat(parts[0]) + BORDER_WIDTH}px ${parseFloat(parts[1] || parts[0]) + BORDER_WIDTH}px`;
        }
        
        // 处理百分比
        if (radius.includes('%')) {
            return radius;
        }
        
        // 处理像素值
        const num = parseFloat(radius);
        return `${num + BORDER_WIDTH}px`;
    }

    // 平滑移动效果
    function updateBorderPosition() {
        if (!currentElement) {
            container.style.visibility = 'hidden';
            container.style.opacity = '0';
            return;
        }

        const rect = currentElement.getBoundingClientRect();
        const borderRadius = getElementBorderRadius(currentElement);
        
        // 更新位置和尺寸
        container.style.top = `${rect.top - BORDER_WIDTH}px`;
        container.style.left = `${rect.left - BORDER_WIDTH}px`;
        container.style.width = `${rect.width + BORDER_WIDTH * 2}px`;
        container.style.height = `${rect.height + BORDER_WIDTH * 2}px`;
        container.style.borderRadius = borderRadius;
        container.style.visibility = 'visible';
        container.style.opacity = '1';
    }

    // 鼠标移动处理
    document.addEventListener('mousemove', (e) => {
        // 忽略边框容器自身
        if (e.target === container || e.target === container.firstElementChild) return;
        
        currentElement = e.target;
        
        // 限流更新（每50ms最多更新一次）
        const now = Date.now();
        if (now - lastUpdate > UPDATE_INTERVAL) {
            lastUpdate = now;
            if (animationFrame) cancelAnimationFrame(animationFrame);
            animationFrame = requestAnimationFrame(updateBorderPosition);
        }
    });

    // 窗口变化时更新
    window.addEventListener('resize', () => {
        if (currentElement) {
            if (animationFrame) cancelAnimationFrame(animationFrame);
            animationFrame = requestAnimationFrame(updateBorderPosition);
        }
    });

    // 页面加载完成后初始化
    if (document.readyState !== 'loading') {
        updateBorderPosition();
    } else {
        document.addEventListener('DOMContentLoaded', updateBorderPosition);
    }
})();