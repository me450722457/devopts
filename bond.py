# -*- coding:utf-8 -*-
import os
import os.path
import re
import time

dir1 = "/etc/sysconfig/network-scripts/"
interface_name_1 = ""
interface_name_2 = ""
bond_name = ""
bond_mode = ""
ipaddress = ""
netmask = ""
gateway = ""


def update_eth(interface_name):
    file_data = ""
    line_list = []
    with open(("%sifcfg-%s") % (dir1, interface_name)) as f:
        for i in f:
            line_list.append(i)
    for j in line_list:
        if re.search('^ONBOOT', j):
            file_data += "ONBOOT=yes\n"
        elif re.search('^BOOTPROTO', j):
            file_data += "BOOTPROTO=none\n"
        elif re.search("^NM_CONTROLLED", j):
            file_data += "NM_CONTROLLED=no\n"
        elif re.search("^UUID", j):
            file_data += "# %s" % j
        elif re.search("^IPADDR", j):
            file_data += "# %s" % j
        elif re.search("^NETMASK", j):
            file_data += "# %s" % j
        elif re.search("^GATEWAY", j):
            file_data += "# %s" % j
        elif re.search("DNS", j):
            file_data += "# %s" % j
        else:
            file_data += j  # 其它内容原封不动添加到字符串
    file_data = file_data.strip()
    os.system(('echo "%s" > "%sifcfg-%s"') % (file_data,dir1,interface_name))

