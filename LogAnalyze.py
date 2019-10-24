#coding:utf-8
__author__ = 'zhangxd18'
import sys
import os
import codecs
import re
import Tkinter
import tkMessageBox
import tkFileDialog

#reload(sys)
#sys.setdefaultencoding("utf8")
#sys.setdefaultencoding("gbk")
#sys.setdefaultencoding("gb2312")
#sys.setdefaultencoding("gb18030")

def analyze(logPath, configPath):
    analyzeFile = '%s-Analyze.log'%logPath.split('/')[-1]
    count = 0
    regularExpression = False
    if radioValue.get() == 2:
        regularExpression = True
    with open(analyzeFile, 'w') as flog:
        para = "\t regularExpression = %d\n---------------------------------------------------\n\n"%regularExpression
        print para
        flog.write(para)
    
    logFile = open(logPath, "rb")
    logLines = logFile.readlines()
    logFile.close()
    
    configFile = open(configPath, "rb")
    configLines = configFile.readlines()
    configFile.close()
        
    for i, logLine in enumerate(logLines):
        #print i
        
        for j, configLine in enumerate(configLines):
            configLine = configLine.strip()
            if configLine == '' or configLine.startswith('//') or configLine.startswith('#') or configLine.upper().startswith('REM'):
                #print 'Skip line[%d]:%s\r\n'%(j+1, configLine)
                continue
            
            para = None
            if regularExpression == False:
                if logLine.find(configLine) != -1:
                    para = '\t [%d] %s\r\n %s'%(i+1, configLine, logLine)
            else:
                matchObj = re.search(configLine+'(.*)', logLine, re.M|re.I)
                if matchObj:
                    para = '\t [%d] %s\r\n %s'%(i+1, configLine, logLine)
                
            if para != None:
                print para
                with open(analyzeFile, 'a+') as flog:
                    flog.write(para)
                count = count+1
                continue
                
    
    para = "total count = %d\n\n"%count
    print para
    with open(analyzeFile, 'a+') as flog:
        flog.write(para)
        

def select_log_path():
    path = tkFileDialog.askopenfilename()
    logFilePath.set(path)
    
def select_config_path():
    path = tkFileDialog.askopenfilename()
    configFilePath.set(path)
    
def start_analyze():
    print logFilePath.get(), configFilePath.get()
    print "Any line start with '#' or '//' or 'REM' int the config file means comment!!!"
    analyze(logFilePath.get(), configFilePath.get())
    tkMessageBox.showinfo('tips', '分析结束')
    
if "__main__" == __name__:
    #print sys.argv[1]
    
    root = Tkinter.Tk()
    logFilePath = Tkinter.StringVar()
    configFilePath = Tkinter.StringVar()
    radioValue = Tkinter.IntVar()
    # set函数是设置单选框中的初始值，set的参数和Radiobutton组件中的value比较，如果存在相同的情况，则为初始值
    radioValue.set(1)
    
    #root.withdraw()
    Tkinter.Label(root, text = '日志文件：').grid(row = 0, column = 0)
    Tkinter.Entry(root, textvariable = logFilePath).grid(row = 0, column = 1)
    Tkinter.Button(root, text = '文件选择', command = select_log_path).grid(row = 0, column = 2)

    Tkinter.Label(root, text = '配置文件：').grid(row = 1, column = 0)
    Tkinter.Entry(root, textvariable = configFilePath).grid(row = 1, column = 1)
    Tkinter.Button(root, text = '文件选择', command = select_config_path).grid(row = 1, column = 2)
    
    Tkinter.Radiobutton(root, variable = radioValue, text = "普通模式", value = 1).grid(row = 2, column = 0)
    Tkinter.Radiobutton(root, variable = radioValue, text = "正则模式", value = 2).grid(row = 2, column = 1)
    Tkinter.Button(root, text = '开始分析', command = start_analyze).grid(row = 2, column = 2)
    
    root.mainloop()




