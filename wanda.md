### 1. 迁移虚拟机
将compute04上的虚拟机迁移到其他计算节点。预计花费20~40分钟

操作建议：
- 提前规划内存交大的虚拟机的目标计算节点
- 页面操作为宜，监控迁移状态、调整迁移更方便
- 实时查看迁移完成情况，对迁移周期较长的机器，使用`nova live-migration-force-complete <server> <migration>`(以向客户报备)
- 监控其他计算节点内存使用情况，及时调整内存交大的虚拟机的目标计算节点
### 2. 将compute4节点隔离
操作建议：
- 页面操作
- 将升级节点设置单独AZ
### 3. 上传内核rpm包
`kernel-3.10.0-862.14.4.el7.x86_64.rpm`
### 4. 内核升级
`yum install kernel-3.10.0-862.14.4.el7.x86_64.rpm`
### 5. 修改grub(默认不需要修改)
修改grub，设置新内核为默认启动内核
```
# 备份原grub文件
cp /etc/default/grub ~

# 修改grub
vim /etc/default/grub
GRUB_DEFAULT=0  #修改为0

# 生成新的内核配置
grub2-mkconfig -o /boot/grub2/grub.cfg
```
### 6. 重启验证
重启后，使用`uname -sr`命令验证启动内核是否为升级目标内核
### 7. 检查compute4节点服务
页面检查计算节点状态，底层容器状态检查，各个服务状态检查
创建虚拟机
