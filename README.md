# 基于paramiko实现的自动化运维工具

本应用是基于paramiko实现，通过SSH连接主机并批量执行命令，节省运维人员的大量人力，由于是使用SSH连接，所以使用的是无代理的方式，目前支持密码登录和秘钥登录。

## 1、部署：

```
pip install paramiko
pip install xlrd
pip install xlwt

注：最新版本的xlrd，在用pandas导入xlsx格式文件时，会报格式不支持的错误。
解决方法：直接退回到1.2.0版本

pip uninstall xlrd
pip install xlrd==1.2.0

```

## 2、使用方法
### 在host.xls文件中填入主机信息主机IP、SSH端口、主机用户名、主机密码、主机密钥、执行命令的文件名
###密码登录填密码，密钥登录填密钥
例如：

|      IP       | Port | UserName | Password | Private_key |    CMD_File     |      |
| :-----------: | :--: | :------: | :------: | :---------: | :-------------: | ---- |
| 192.168.1.109 |  22  |   root   |   1234   |   xxx.pem   | linux_check.xls |      |
| 192.168.1.110 |  22  |   root   |   1234   |   xxx.pem   | linux_check.xls |      |

### 在CMD文件夹下新建执行命令的文件，填入执行的命令、返回结果的正则表达式、返回结果的描述，可参照下列格式：

| CMD                                      | CMD_RE |   Desc   |      |
| :--------------------------------------- | :----: | :------: | ---- |
| idle_cpu=\`top -bn1 -i &#124; grep 'id' &#124; awk -F ',' '{print $4}' &#124; awk '{print $1}'\`;used_cpu=\`echo "100 $idle_cpu" &#124; awk '{printf("%0.1f\n",$1-$2)}'\`;awk 'BEGIN{printf"%.2f%\n",('$used_cpu')}' |   .*   |  cpu使用率  |      |
| sum=\`free -m &#124; grep Mem &#124; awk '{print $2}'\`;use=\`free -m &#124; grep Mem &#124; awk '{print $3}'\`;awk 'BEGIN{printf"%.2f%\n",('$use'/'$sum')*100}' |   .*   |  内存使用率   |      |
| df -h / &#124; awk 'NR==2 {print $5}'    |   .*   | /文件系统使用率 |      |

如果不需要通过正则表达式来筛选返回值，则填入 `.*`表示取所有内容

### 运行main.py，生成out.xls文件，如果按照上述的例子执行，则返回的结果格式如下所示：

|      IP       | cpu使用率 | 内存使用率  | /文件系统使用率 |      |
| :-----------: | :----: | :----: | :------: | ---- |
| 192.168.1.109 |  28%   | 76.54% |   0.27   |      |
| 192.168.1.110 |  52%   | 72.52% |   0.01   |      |
