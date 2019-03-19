from tornado.options import define, options, parse_command_line
import os

# 命令行参数
define('port', default=8005, type=int, help='port to be bound to.')
parse_command_line()
port = options.port

# 配置
BASE_DIRS = os.path.dirname(__file__)

tornado_option = {
    'debug': False,
    'static_path': os.path.join(BASE_DIRS, 'static'),
    'template_path': os.path.join(BASE_DIRS, 'templates'),
}
