import logging, threading, inspect, sys
from colorama import init, Fore, Style  # Windows系统需安装：pip install colorama

# 初始化colorama（Windows系统支持ANSI颜色）
init(autoreset=True)

# 定义不同日志级别的颜色
LEVEL_COLORS = {
    'DEBUG': Fore.CYAN,    # 青色
    'INFO': Fore.GREEN,     # 绿色
    'WARNING': Fore.YELLOW, # 黄色
    'ERROR': Fore.RED,      # 红色
    'CRITICAL': Fore.MAGENTA # 品红色（深红）
}

# 自定义带颜色的日志格式化器
class ColoredFormatter(logging.Formatter):
    def format(self, record):
        # 给日志级别添加颜色，其他字段保持默认
        level_name = record.levelname
        color = LEVEL_COLORS.get(level_name, Fore.WHITE)  # 默认白色
        record.levelname = f"{color}{level_name}{Style.RESET_ALL}"  # 重置颜色避免影响后续输出
        return super().format(record)

# 配置日志基础设置
logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.handlers.clear()  # 清除默认处理器

# 创建控制台处理器并绑定带颜色的格式化器
console_handler = logging.StreamHandler(sys.stdout)
formatter = ColoredFormatter(
    '%(asctime)s - %(filename)s - Thread:%(threadName)s - Line:%(lineno)d - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)


logging.log = lambda level, msg: logger.log(
    getattr(logging, level.upper(), logging.INFO),
    msg,
    extra={
        'lineno': inspect.currentframe().f_back.f_lineno,
        'filename': inspect.currentframe().f_back.f_code.co_filename.split('/')[-1],  # 只显示文件名（不含路径）
        'threadName': threading.current_thread().name
    }
)