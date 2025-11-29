import logging
import threading
import sys
import subprocess
try:
    from colorama import init, Fore, Style  # Windows系统需安装：pip install colorama
except ImportError:
    subprocess.run(["pip","install","colorama"])

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
        # 给日志级别添加颜色，其他字段保持默认（logging自动收集）
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

# 修复：移除extra中的内置字段，让logging自动收集
def custom_log(level, msg):
    # 转换日志级别（默认INFO）
    level_num = getattr(logging, level.upper(), logging.INFO)
    # 直接调用logger.log，logging会自动收集filename、lineno、threadName
    logger.log(level_num, msg)

# 替换默认的logging.log为自定义函数（避免lambda的帧信息问题）
logging.log = custom_log