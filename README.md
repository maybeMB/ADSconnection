# 编写在32位windows xp上与twincat2本地连接的python2.7程序中遇到的问题汇总（持续施工中）
记录编写程序时在windows xp系统上遇到的问题与解决方案

## 问题1：python版本与py文件打包
windows xp系统与最新版本的python不兼容，根据网上搜索到的内容：windows xp支持python2.7.x和3.4.x版本。但经过测试后python3.4.4无法直接使用，所以我使用了pyhton2.7.18版本。py文件的打包使用的是pyinstaller
### 问题1解决方案
python2.7.x并不常用，所以通过anaconda的虚拟环境解决。
安装anaconda，中文官网：https://anaconda.org.cn/anaconda/install/windows/

**构建32位python2.7环境**

进入cmd窗口
```
set CONDA_FORCE_32BIT=1  //切换到32位
conda create --name python27 python=2.7  //创建一个python3.6的环境，命名为python27
conda info --envs  //查看是否添加成功
activate python27  //切换到python2.7环境
python --version  //确认python环境
```
**安装pyinstaller**

注：这一步与上面是相连的，如果不在该环境下安装，还是使用原来的pyinstaller，那么打包的程序仍然为64位
```
conda install pyinstaller  //安装pyinstaller,若出现报错可使用: pip install pyinstaller
```
**使用pyinstaller将py文件打包成exe文件**

```
cd  (file_path) //进入需要打包文件的路径
activate python27 //必须要进入此虚拟环境，否则打包出来的是系统默认python环境
pyinstaller -F --hidden-import=pynput.keyboard._win32 --hidden-import=pynput.mouse._win32 connect.py //关于--hidden-import属性在问题3中会说明
```

## 问题2：pyads版本问题（这会导致打包后的exe文件缺少pyads中一些库）
在虚拟环境中应该使用
```
conda install pyads //或 pip install pyads
```
但是此方法安装的pyads是使用python3环境的   请查看：https://pypi.org/project/pyads/ 这也导致在后续pyinstaller对代码文件打包后运行exe文件会出现pyads.structs模块不存在的报错。
我先是在使用pyinstaller时加入了--hidden-import=pynput.pyads.structs参数，但没有用。
然后我在/Lib/site-packages/PyInstaller/hooks中写了hook文件，同样无用。最后才发现是pyads的版本问题，保险起见我将hook文件一并上传
### 问题2解决方案
pyads手动安装3.1.3：https://pypi.org/project/pyads/3.1.3/ 或下载我的pyads-3.1.3.tar.gz包

## 问题3：pyinstaller打包后的exe文件缺少库
pyinstaller打包后的exe文件缺少pynput.keyboard和pynput.mouse库，
### 问题3解决方案
在pyinstaller打包时加入--hidden-import=pynput.keyboard._win32 --hidden-import=pynput.mouse._win32参数

## 问题4：pynput功能异常
pynput检测指定按键或鼠标的功能在win10上正常但是在xp系统上无法运行
### 问题4解决方案
这需要修改python中的lib/pynput/_util/win32.py文件，若使用anaconda，路径为：adaconda(anaconda安装路径)/envs/python27(虚拟环境名称)/Lib/site-packages/lib/pynput/_util/win32.py（可参考：https://github.com/moses-palmer/pynput/pull/508/commits/563e92b906bd03d1c7d92f15a533754cab6bdc1a ）或下载我的win32.py文件（pynput版本1.7.7）

## 问题5：pyads使用typing问题
typing是python3.5才出现的标准包，python2.7使用需要安装typing包。
### 问题5解决方案
在**python27虚拟环境**下安装typing
```
conda install typing //或用pip
```

## 问题6：Tkinter在非主线程中更新导致程序错误
Tkinter组件在非主线程中使用config函数更新会报错
### 问题6解决方案
使用tk.after(0, 函数名)函数，将界面更新的内容全部放入after调用的函数中

## 问题7：使用Tkinter创建隐藏标题栏的窗口，打开窗口时大小发生变化
Tkinter创建隐藏标题栏的窗口，设置为 geometry('666x460+61+73') 。 启动程序时打开的窗口大小正常，但最小化再打开后窗口尺寸变大，变为 682x499 ，超过设置的尺寸
### 问题6解决方案
暂无
