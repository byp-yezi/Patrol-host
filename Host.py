class Host(object):
    def __init__(self, ip, port, username, password, private_key, cmd, cmd_re, desc):
        self.ip = ip
        self.port = port
        self.username = username
        self.password = password
        self.private_key = private_key
        # 执行命令
        self.cmd = cmd
        # 执行命令结果使用的正则表达式
        self.cmd_re = cmd_re
        # 执行命令的描述
        self.desc = desc
