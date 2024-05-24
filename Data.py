class Data(object):
    def __init__(self, ip, port, desc, data):
        self.ip = ip
        self.port = port  # 添加端口属性
        # 执行命令的描述
        self.desc = desc
        # 执行命令返回的结果
        self.data = data
