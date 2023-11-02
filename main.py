import time

import paramiko
import xlrd
import re

from Data import Data
from Host import Host
from SSHConnection import SSHConnection
from WriteDataToExcel import WriteDataToExcel


# 读取主机列表
def read_host_list(filename):
    host_list = []
    # 批量读取主机列表
    workbook = xlrd.open_workbook(filename)  # 打开Excel文件
    sheet = workbook.sheet_by_index(0)  # 获取第一个工作表
    for i in range(1, sheet.nrows):
        ip = sheet.cell(i, 0).value  # 读取IP地址
        port = int(sheet.cell(i, 1).value)  # 读取端口号并转换为整数
        username = sheet.cell(i, 2).value  # 读取用户名

        # 读取密码
        password_cell = sheet.cell(i, 3)
        if password_cell.ctype == xlrd.XL_CELL_NUMBER:  # 检查单元格类型是否为数字
            password = str(int(password_cell.value))
        else:
            password = str(password_cell.value)

        private_key = str(sheet.cell(i, 4).value)  # 读取私钥
        cmd_file = sheet.cell(i, 5).value  # 读取命令文件名

        # 读取命令文件
        cmd, cmd_re, desc = read_cmd_file("CMD/" + cmd_file)

        host = Host(ip, port, username, password, private_key, cmd, cmd_re, desc)
        host_list.append(host)

    return host_list


# 读取命令文件
def read_cmd_file(filename):
    cmd = []
    cmd_re = []
    desc = []
    workbook_cmd = xlrd.open_workbook(filename)
    sheet_cmd = workbook_cmd.sheet_by_index(0)

    for i in range(1, sheet_cmd.nrows):
        cmd.append(sheet_cmd.cell(i, 0).value)
        cmd_re_value = sheet_cmd.cell(i, 1).value
        cmd_re.append(cmd_re_value if cmd_re_value else None)
        desc.append(sheet_cmd.cell(i, 2).value)

    return cmd, cmd_re, desc


# 执行命令并获取结果
def execute_commands(host, password):
    conn = SSHConnection(host)
    conn.connect()
    data = []
    desc = []

    try:
        for i in range(len(host.cmd)):
            cmd_result = None  # 存储命令执行结果的变量，初始化为 None

            if password:
                cmd_result = conn.exec_command(host.cmd[i])
            else:
                cmd_result = conn.private_exec_command(host.cmd[i])

            if cmd_result is not None:
                return_value = cmd_result.decode('utf-8')
            else:
                return_value = ""

            re_str = re.search(host.cmd_re[i], return_value)
            if re_str:
                re_str = re_str.group()
            else:
                re_str = ""

            data.append(re_str)
            desc.append(host.desc[i])

    except paramiko.SSHException as e:
        print(f"主机 {host.ip} SSH 执行命令失败: {e}")
    except Exception as e:
        print(f"发生了其他异常: {e}")

    conn.close()
    return Data(host.ip, desc, data)


# 主函数
def main():
    host_list = read_host_list("host.xls")  # 读取主机列表
    data_list = []  # 存储执行结果的列表

    # 逐个主机执行命令并获取结果
    for host in host_list:
        data_list.append(execute_commands(host, host.password))

    # 创建WriteDataToExcel实例并写入Excel数据
    write_excel = WriteDataToExcel()
    write_excel.write_data_to_excel(data_list)

    print("脚本执行完毕")
    # time.sleep(2)


if __name__ == "__main__":
    main()
