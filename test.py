import os 
import logging
import subprocess
import shutil
import argparse

interface_dir = '/etc/sysconfig/network-scripts/'
slave_name_1 = ""
slave_name_2 = ""
bond_name = ""
bond_mode = ""
ipaddress = ""
netmask = ""
gateway = ""

LOG = logging.getLogger(__name__)

slave_conf = '''

'''

bond_conf = '''

'''

class Bond(object):
    def __init__(self,conf):
        self.conf = conf
        self.conf.slave_1 = os.path.join(interface_dir, self.conf.slave-1)
        self.conf.slave_2 = os.path.join(interface_dir, self.conf.slave-2)
        self.conf.bond_name = os.path.join(interface_dir, self.conf.name) 
        self.conf.bond_mode = conf.mode
        self.conf.ip = conf.ip
        self.conf.netmask = conf.netmask
        self.conf.gateway = conf.gateway


    def run(self, cmds):
        try:
            LOG.info('Runing cmd: %s', cmds)      #print log
            return subprocess.check_output(cmds)  #return 
        except subprocess.CalledProcessError:
            LOG.exception('Run command failed: %s', cmds)
            shutil.rmtree(self.backup)            #full backup faild ,remove the dir
            return ''

    def write_slave(self):





def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--slave-1', required=True)
    parser.add_argument('--slave-2', required=True)
    parser.add_argument('--name', required=True)
    parser.add_argument('--mode', type=int, default=4, required=True)
    parser.add_argument('--ip', required=True)
    parser.add_argument('--netmask', required=True)
    parser.add_argument('--gateway', required=True)

    conf = parser.parse_args(sys.argv[1:]) 