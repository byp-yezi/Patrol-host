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
        try:
            # 密码连接
            transport = paramiko.Transport((self.host.ip, self.host.port))
            # 密钥连接
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

            exception_ip_list_1 = ['124.71.202.191', '124.71.164.53', '124.71.149.35']
            # 密钥为zjx--prod.pem，但登陆异常的主机
            exception_ip_list_2 = ['121.36.194.73']

            if self.host.password:
                transport.connect(username=self.host.username, password=self.host.password)

            else:
                ssh_key_path = 'D:\\xiaobao\\pem666\\' + self.host.private_key
                if self.host.ip in exception_ip_list_2:

                    ssh.connect(hostname=self.host.ip,
                                port=self.host.port,
                                username=self.host.username,
                                pkey=paramiko.RSAKey.from_private_key_file(ssh_key_path), )

                elif self.host.private_key == 'zjx--prod.pem' or self.host.ip in exception_ip_list_1:
                    ssh.connect(hostname=self.host.ip,
                                port=self.host.port,
                                username=self.host.username,
                                pkey=paramiko.RSAKey.from_private_key_file(ssh_key_path),
                                disabled_algorithms={'pubkeys': ['rsa-sha2-256', 'rsa-sha2-512']})

                else:
                    ssh.connect(hostname=self.host.ip,
                                port=self.host.port,
                                username=self.host.username,
                                pkey=paramiko.RSAKey.from_private_key_file(ssh_key_path), )
            self.transport = transport
            self.ssh = ssh

        except Exception as e:
            print(f"服务器 {self.host.ip} 连接失败，异常退出: {e}")

    # 执行命令
    def exec_command(self, command):
        if self.client is None:
            self.client = paramiko.SSHClient()
            self.client._transport = self.transport
        stdin, stdout, stderr = self.client.exec_command(command)
        data = stdout.read()
        # if len(data) == 0:
        #     print(data.strip())  # 打印正确结果
        #     return data
        if len(data) > 0:
            # print(data.strip())  # 打印正确结果
            return data
        err = stderr.read()
        if len(err) > 0:
            # print(err.strip())  # 打印正确结果
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
