#coding=utf-8
import Tkinter as tk
import tkMessageBox
import threading
import pynput
import time
import pyads

# 一些全局变量
INTERVAL = 0.2 # 读取参数间隔 200ms
MINIMIZE = True # 窗口是否为最小化，初始为最小化
SWITCH = False # 窗口是否刚切换了状态
PLC = pyads.Connection(ams_net_port=811) # 通讯端口

# 需要读取的变量，控件显示范围最多7个数字一个小数点
fSystemPrsPV = 0.0
bAdaptPrsRunning = False
fPumpPPVlvCmd = 0.0
fAdaptiveSystemPrsSP = 0.0
bAdaptPrsAccept = False

# 创建root窗口
root = tk.Tk()
root.title("ADS Connection")
root.geometry('600x500+100+50') # 使窗口位于屏幕中央，屏幕为800x600
root.iconify() 
root.overrideredirect(False)  # 隐藏标题栏和边框
check_var = tk.BooleanVar()

def pressF10(key):
    global MINIMIZE, SWITCH
    if key == pynput.keyboard.Key.f10:
        # 使用线程安全的方式更新 Tkinter GUI
        root.after(0, show_window)

def show_window():
    global MINIMIZE, SWITCH
    root.deiconify()
    MINIMIZE = False
    SWITCH = True
    root.attributes("-topmost", True)  # 窗口置顶
    root.attributes("-topmost", False)

def checkAndWriteParameter():
# 检查bAdaptPrsAccept
    global check_var, bAdaptPrsAccept    
    check_var.set(bAdaptPrsAccept)
    result = tkMessageBox.askyesno("确认", "是否确定修改?")
    if result:
        print(result)
        time.sleep(INTERVAL+0.02)
        PLC.write_by_name('MAIN.AdaptiveSystemPrs.bHmiAdaptPrsEnable', not bAdaptPrsAccept, pyads.PLCTYPE_BOOL)
        time.sleep(INTERVAL) # 确保端口open
        bAdaptPrsAccept = PLC.read_by_name('MAIN.AdaptiveSystemPrs.bAdaptPrsAccept', pyads.PLCTYPE_BOOL)
        check_var.set(bAdaptPrsAccept)



# UI界面
class ApplicationUI(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.master = master
        self.pack()
        
        # 使用的图片
        self.exit_image = tk.PhotoImage(file="./source/Exit.gif")
        self.running_f = tk.PhotoImage(file="./source/gray.gif")
        self.running_t = tk.PhotoImage(file="./source/green.gif")
        self.createWidget()
        
    def minimize_window(self):
    # 最小化
        global MINIMIZE, SWITCH
        root.overrideredirect(False) # 不取消会报错
        root.iconify()    
        MINIMIZE = True
        SWITCH = True
        # root.overrideredirect(True) 
    

    def createWidget(self):
    # 创建控件并设置按钮位置
        global fSystemPrsPV
        
        # 退出按钮
        self.quit_bt = tk.Button(self.master, command=self.minimize_window, image=self.exit_image)
        self.quit_bt.place(relx=0.9, rely=0.9, x=-60, y=-60) 
        
        # 校准说明按钮
        
        # 自适应系统压力控件
        self.sys_pressure_title = tk.Label(self.master, text="自适应系统压力") # 标题
        self.sys_pressure_title.place(relx=0.1, rely=0.1, x=-30, y=-35)
        
        self.sys_statement_show = tk.Label(self.master, image=self.running_f) # 机器状态显示
        self.sys_statement_show.place(relx=0.1, rely=0.1, x=-30, y=-6)
        
        self.sys_bAdaptPrsAccept_r = tk.Checkbutton(self.master, variable=check_var, command=checkAndWriteParameter)
        self.sys_bAdaptPrsAccept_r.place(relx=0.1, rely=0.1, x=-13, y=-12)
        
        self.sys_fSystemPrsPV_r = tk.Label(self.master, bg="lightgreen", width=8, text=fSystemPrsPV, anchor=tk.E, relief="solid", bd=1) 
        self.sys_fSystemPrsPV_r.place(relx=0.1, rely=0.1, x=15, y=-10)
        self.sys_fSystemPrsPV_tail = tk.Label(self.master, text="psi", anchor=tk.W)
        self.sys_fSystemPrsPV_tail.place(relx=0.1, rely=0.1, x=77, y=-10)
        
        self.sys_fAdaptiveSystemPrsSP_r = tk.Label(self.master, bg="#D3D3D3", width=8, text=fSystemPrsPV, anchor=tk.E, relief="solid", bd=1) 
        self.sys_fAdaptiveSystemPrsSP_r.place(relx=0.1, rely=0.1, x=15, y=20)
        self.sys_fAdaptiveSystemPrsSP_tail = tk.Label(self.master, text="psi", anchor=tk.W)
        self.sys_fAdaptiveSystemPrsSP_tail.place(relx=0.1, rely=0.1, x=77, y=20)
        
        self.sys_fPumpPPVlvCmd_r = tk.Label(self.master, bg="lightgreen", width=8, text=fPumpPPVlvCmd, anchor=tk.E, relief="solid", bd=1) 
        self.sys_fPumpPPVlvCmd_r.place(relx=0.3, rely=0.1, x=-10, y=-10)
        self.sys_fPumpPPVlvCmd_tail = tk.Label(self.master, text="V", anchor=tk.W)
        self.sys_fPumpPPVlvCmd_tail.place(relx=0.3, rely=0.1, x=52, y=-10)
        

        
        # 压力传感器校准控件
        
        # 系统压力阀校准控件
        
        # 信息区控件
        
        
        
def readParameter(connection): 
# 读取参数
    global SWITCH, fSystemPrsPV, bAdaptPrsRunning, fPumpPPVlvCmd, fAdaptiveSystemPrsSP, bAdaptPrsAccept
    flag = False # 确保窗口切换状态，防止在窗口打开时反复按F10导致多次open
    while True:
        if not MINIMIZE: # 窗口不处于最小化
            if SWITCH and not flag:
                PLC.open() 
                flag = True
                SWITCH = False
            bAdaptPrsRunning = PLC.read_by_name('MAIN.AdaptiveSystemPrs.bAdaptPrsRunning', pyads.PLCTYPE_BOOL) # 第一
            fSystemPrsPV = PLC.read_by_name('MAIN.AdaptiveSystemPrs.fSystemPrsPV', pyads.PLCTYPE_LREAL)
            fPumpPPVlvCmd = PLC.read_by_name('MAIN.AdaptiveSystemPrs.fPumpPPVlvCmd', pyads.PLCTYPE_REAL)
            fAdaptiveSystemPrsSP = PLC.read_by_name('MAIN.AdaptiveSystemPrs.fAdaptiveSystemPrsSP', pyads.PLCTYPE_REAL)
                

            # 获取参数后修改显示
            connection.sys_fSystemPrsPV_r.config(text=fSystemPrsPV)
            if bAdaptPrsRunning:
                connection.sys_statement_show.config(image=connection.running_t)
            else:
                connection.sys_statement_show.config(image=connection.running_f)
            connection.sys_fPumpPPVlvCmd_r.config(text=fPumpPPVlvCmd)
            connection.sys_fAdaptiveSystemPrsSP_r.config(text=fAdaptiveSystemPrsSP)
        if MINIMIZE and SWITCH and flag: # 刚刚最小化
            PLC.close()
            flag = False
            SWITCH = False
        time.sleep(INTERVAL)  # 等待指定的时间间隔



def start_key_listener():
    listener = pynput.keyboard.Listener(on_press=pressF10)
    listener.start()





ADS_connect = ApplicationUI(master=root)

# 键盘监听线程
key_listener_thread = threading.Thread(target=start_key_listener)
key_listener_thread.daemon = True
key_listener_thread.start()

# 读取线程
reading_thread = threading.Thread(target=readParameter, args=(ADS_connect, ))
reading_thread.daemon = True
reading_thread.start()

# 启动界面
root.mainloop()
