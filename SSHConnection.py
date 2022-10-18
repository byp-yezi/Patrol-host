import sys

import paramiko


class SSHConnection(object):
    def __init__(self, host):
        self.host = host
        self.transport = None
        self.ssh = None
        self.sftp = None
        self.client = None
        # self.connect()

    def connect(self):
        # 密码连接
        transport = paramiko.Transport((self.host.ip, self.host.port))
        # 密钥连接
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        # 密钥为xisland_new.pem，但登陆异常的主机
        exception_ip_list = ['x.x.x.x']

        if self.host.password:
            transport.connect(username=self.host.username, password=self.host.password)
        else:
            if self.host.private_key == 'xxx.pem' and self.host.ip not in exception_ip_list:
                try:
                    ssh.connect(hostname=self.host.ip,
                                port=self.host.port,
                                username=self.host.username,
                                pkey=paramiko.RSAKey.from_private_key_file('D:\\pem\\' + self.host.private_key),
                                disabled_algorithms={'pubkeys': ['rsa-sha2-256', 'rsa-sha2-512']})

                except Exception as e:
                    print(self.host.ip)
                    print(e)
                    print("服务器连接失败，异常退出")
                    sys.exit(-1)

            else:
                try:
                    ssh.connect(hostname=self.host.ip,
                                port=self.host.port,
                                username=self.host.username,
                                pkey=paramiko.RSAKey.from_private_key_file('D:\\pem\\' + self.host.private_key),)

                except Exception as e:
                    print(self.host.ip)
                    print(e)
                    print("服务器连接失败，异常退出")
                    sys.exit(-1)

        self.transport = transport
        self.ssh = ssh

    # 下载
    def download(self, remotepath, localpath):
        if self.sftp is None:
            self.sftp = paramiko.SFTPClient.from_transport(self.transport)
        self.sftp.get(remotepath, localpath)

    # 上传
    def put(self, localpath, remotepath):
        if self.sftp is None:
            self.sftp = paramiko.SFTPClient.from_transport(self.transport)
        self.sftp.put(localpath, remotepath)

    # 执行命令
    def exec_command(self, command):
        if self.client is None:
            self.client = paramiko.SSHClient()
            self.client._transport = self.transport
        stdin, stdout, stderr = self.client.exec_command(command)
        data = stdout.read()
        if len(data) > 0:
            # print data.strip()  # 打印正确结果
            return data
        err = stderr.read()
        if len(err) > 0:
            # print err.strip()  # 输出错误结果
            return err

    # 执行命令
    def private_exec_command(self, command):
        if self.client is None:
            self.client = self.ssh
            # self.client._transport = self.transport
        stdin, stdout, stderr = self.client.exec_command(command)
        data = stdout.read()
        if len(data) > 0:
            # print data.strip()  # 打印正确结果
            return data
        err = stderr.read()
        if len(err) > 0:
            # print err.strip()  # 输出错误结果
            return err

    def close(self):
        if self.transport:
            self.transport.close()
        if self.ssh:
            self.ssh.close()
        if self.client:
            self.client.close()
