# ADSconnection
在32位windows  xp系统上与twincat2进行本地连接的前端代码，同时记录编写程序在windows xp系统上遇到的问题与解决方案

## 问题1：python版本与py文件打包
windows xp系统与最新版本的python不兼容，根据网上搜索到的内容：windows xp支持python2.7.x和3.4.x版本。但经过测试后python3.4.4无法直接使用，所以我使用了pyhton2.7.18版本。
## 问题1解决方案
python2.7.x并不常用，所以通过anaconda的虚拟环境解决。
安装anaconda，中文官网：https://anaconda.org.cn/anaconda/install/windows/
**构建32位python2.7环境**
进入cmd窗口
```
set CONDA_FORCE_32BIT=1  //切换到32位
conda create --name python27 python=2.7  //创建一个python3.6的环境，命名为python27
conda info --envs  //查看是否添加成功
activate python36  //切换到python3.6环境
python --version  //确认python环境
```
**安装pyinstaller**
注：这一步是必须的，如果不在该环境下安装，还是使用原来的pyinstaller，那么打包的程序仍然为64位
```
pip -V  //再次确认是否为32位的pip
pip install pyinstaller  //安装pyinstaller
```
