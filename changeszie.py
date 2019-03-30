# C:\Users\17732\Desktop\毕设数据\AD_20180514_171054_tread.dat
#coding=utf-8  
from tkinter import * 
import numpy as np  
from scipy import interpolate  
import pylab as pl
import matplotlib.pyplot as plt
from scipy.interpolate import spline
import math
import struct 
import cx_Oracle
import tkinter.font
import matplotlib

zhfont1 = matplotlib.font_manager.FontProperties(fname='C:\Windows\Fonts\simkai.ttf')
  
class WidgetsDemo:  
    def __init__(self):  
        window = Tk()                 # 创建一个窗口  
        window.title("踏面状态检测")  # 设置标题  
          
        frame1 = Frame(window)        # 创建一个框架  
        frame1.pack()                 # 将框架frame1放置在window中  
          
        self.v1 = IntVar()  
        # 创建一个复选框，如果选中则self.v1为1,否则为0,当点击cbtBold时，触发processCheckbutton函数  
        cbtBold = Checkbutton(frame1,text="全选",variable=self.v1,
                              command=self.processCheckbutton)  
          
        self.v2 = IntVar()  
        # 创建两个单选按钮，放置在frame1中，按钮文本是分别是数据波形和踏面转态模拟，  
        # 当rbRed按钮被选中时self.v2为1,当rbYellow按钮被选中时，self.v2为2，按钮被点击时触发processRadiobutto函数  
        rbRed = Radiobutton(frame1,text="数据波形",
                            variable=self.v2,value=1, 
                            command=self.processRadiobutton)  
        rbYellow = Radiobutton(frame1,text="踏面状态模拟",  
                               variable=self.v2,value=2,  
                               command=self.processRadiobutton)  
        # grid布局  
        cbtBold.grid(row=1,column=1)  
        rbRed.grid(row=1,column=2)  
        rbYellow.grid(row=1,column=4)  

        framede = Frame(window)
        framede.pack()

        self.v3 = IntVar()  
        # 创建两个单选按钮，放置在frame1中，按钮文本是分别是数据波形和踏面转态模拟，  
        # 当rbRed按钮被选中时self.v2为1,当rbYellow按钮被选中时，self.v2为2，按钮被点击时触发processRadiobutto函数  
        rb1 = Radiobutton(framede,text="选取10000个测量点",
                            variable=self.v3,value=1, 
                            command=self.processdegreebutton)  
        rb5 = Radiobutton(framede,text="选取50000个测量点",  
                               variable=self.v3,value=2,  
                               command=self.processdegreebutton)  
        rb10 = Radiobutton(framede,text="选取100000个测量点",  
                               variable=self.v3,value=3,  
                               command=self.processdegreebutton)
        # grid布局  
        rb1.grid(row=1,column=1)  
        rb5.grid(row=1,column=2)  
        rb10.grid(row=1,column=3)  
          
        frame2 = Frame(window)   # 创建框架frame2  
        frame2.pack()            # 将frame2放置在window中  
          
          
        label = Label(frame2,text="输入检测数据路径: ")   # 创建标签  
        self.name = StringVar()  
        # 创建Entry，内容是与self.name关联  
        entryName = Entry(frame2, font=3,textvariable=self.name)  
        # 创建按钮，点击按钮时触发processButton函数  
        btGetName = Button(frame2,text="确认检测", 
                           command=self.processButton)  
          
        # 创建消息  
        message = Message(frame2,text="demo only!")  
          
        # grid布局  
        label.grid(row=1,column=1)  
        entryName.grid(row=1,column=2)  
        btGetName.grid(row=1,column=3)  
        message.grid(row=1,column=4)  
        

        frame3 = Frame(window,height=10,width=90)
        frame3.pack()

        upload_to_oracle = Button(frame3,text="确认上传",command=self.upload)  

        upload_to_oracle.grid(row=1,column=2)
        # 创建格式化文本，并放置在window中
        global text  
        text = Text(window,height=15,width=70)  
        text.pack()
        text.tag_config('tag1',foreground='red',font=('verdana',20,'bold'))
        text.tag_config('tag3',font=(1))  
        text.insert(END,"注意：\n",'tag1')
        text.insert(END,"用户可根据需求选择相应的结果类型。\n")
        text.insert(END,"选择全选时将展示踏面状态模拟图和测量数据波形。\n")  
        text.insert(END,"图形会以新界面显示。\n")  
          
        # 监测事件直到window被关闭  
        window.mainloop()  
    
    #读取文件
    def xshow(self,filename):  
        if self.v3.get() == 1:
            number = 10000
        if self.v3.get() == 2:
            number = 50000
        if self.v3.get() == 3:
            number = 100000
        f = open(filename, "rb")  
        pic = []  
        for i in range(number):    
            data = f.read(4)  
            elem = struct.unpack("f", data)[0]  
            pic.append(elem)
        # print(pic)  
        f.close()
        return pic  
    #将路径保存到数据库中
    def upload(self):
        conn_str = 'gsx/123456@//127.0.0.1:1521/xe'
        db = cx_Oracle.connect(conn_str)
        # # print(db.version)
        sql = "insert into abrpath values(' "+ 'C:\\Users\\17732\\Desktop\\毕设数据\\abrarray\\abrdata.txt' + "')" 
        # print(sql)
        cursor_oracle = db.cursor()
        cursor_oracle.execute(sql)
        db.commit()
        print("保存成功")
        text.insert(END,"保存成功\n",'tag3') 

    #获取测量数据
    def gettestdata(self):
        path = self.name.get()
        pic = self.xshow(path)
        a = pic[88:]
        global dat1
        dat = []
        N = len(a)
        for i in range(N):
            if i%8==1:
                dat.append(a[i])
        dat.insert(0,10.528277803783812e-41)
        dat.append(10.528277803783812e-41)
        dat1 = []
        for i in range(0,len(dat)):
            dat1.append(dat[i]*math.pow(10,41))
        # print(dat)
        return dat

    #获取标准轮数据
    def getstadata(self):
        path = self.name.get()
        pic = self.xshow(path)
        a = pic[88:]
        sta = []
        global sta1
        N = len(a)
        for i in range(N):
            if i%8==6:
                sta.append(a[i])
        sta.insert(0,10.528277803783812e-41)
        sta.append(10.528277803783812e-41)
        sta1 = []
        for i in range(0,len(sta)):
            sta1.append(sta[i]*math.pow(10,41))
        return sta
        

    # 复选框点击按钮函数  
    def processCheckbutton(self):
        print("选择全选")
        text.insert(END,"已选择：全选\n",'tag3')

    def buildfile(self,dat):
        fp = open("C:\\Users\\17732\\Desktop\\毕设数据\\abrarray\\abrdata.txt",'w')
        for item in range(0,len(dat)):
            fp.write(str(dat[item]))
        fp.close
        
      
    # 单选按钮点击函数  
    def processRadiobutton(self):
        if self.v2.get() == 1:
            print ("选择数据波形")
            text.insert(END,"已选择：数据波形\n",'tag3')

        elif self.v2.get() == 2:
            print("选择踏面转态模拟")
            text.insert(END,"已选择：踏面状态模拟\n",'tag3')
        print(self.v2.get())

    #数据量选择函数
    def processdegreebutton(self):
        if self.v3.get() == 1:
            print ("10000个测量点")
            text.insert(END,"已选择：10000个测量点\n",'tag3')

        elif self.v3.get() == 2:
            print("50000个测量点")
            text.insert(END,"已选择：50000个测量点\n",'tag3')

        elif self.v3.get() == 3:
            print("100000个测量点")
            text.insert(END,"已选择：100000个测量点\n",'tag3')
        print(self.v2.get())
      
    # Get Name按钮点击函数  
    def processButton(self): 
        #选择全选时触发的函数 
        if self.v1.get() == 1:
            dat = self.gettestdata()
            sta = self.getstadata()
            # print(dat[:100])
            # print(sta[:100])
            wornlist = []
            newdata = []
            for i in range(0,len(dat)):
                newdata.append(sta[i]-dat[i])
                wornlist.append(abs(newdata[i]))
            worn = min(wornlist[1:len(wornlist)-1])
            # print(wornlist)
            # print(worn)
            # print(newdata)
            for i in range(0,len(newdata)):
                newdata[i] = newdata[i]+worn
                newdata[i] = newdata[i]*math.pow(10,41)
            maxabr = abs(min(newdata[1:len(newdata)-1]))
            sumabr = abs(sum(newdata[1:len(newdata)-1]))
            avrabr = sumabr/(len(newdata)-2)
            worn1 = worn*math.pow(10,41)
            worn1 = format(worn1,'0.2f')
            maxabr1 = maxabr*math.pow(10,1)
            maxabr1 = format(maxabr1,'0.2f')
            avrabr1 = avrabr*math.pow(10,1)
            avrabr1 = format(avrabr1,'0.2f')

            # print(maxabr)
            text.insert(END,"磨损量为",'tag3')
            text.insert(END, worn*math.pow(10,41),'tag3')
            text.insert(END,"mm\n",'tag3')
            text.insert(END,"最大擦伤深度为",'tag3')
            text.insert(END, maxabr*math.pow(10,1),'tag3')
            text.insert(END,"mm\n",'tag3')
            text.insert(END,"平均擦伤深度为",'tag3')
            text.insert(END, avrabr*math.pow(10,1),'tag3')
            text.insert(END,"mm\n",'tag3')
            # print(sta)
            # print(dat)
            # print(newdata)
            x = np.linspace(0,len(dat1)-1,len(dat1))
            y = np.array(dat1)
            # plt.plot(x,y,'r')

            x_t = np.linspace(0,len(sta1)-1,len(sta1))
            y_t = np.array(sta1)
            n = len(dat)
            x_new = []
            y_new = []
            x_new1 = []
            y_new1 = []
            for i in range(1,n+1):
                rx = (9.15-worn+newdata[i-1])*math.cos((2*i*math.pi)/n)
                x_new.append(rx)
                ry = (9.15-worn+newdata[i-1])*math.sin((2*i*math.pi)/n)
                y_new.append(ry)
                rx1 = 9.15*math.cos((2*i*math.pi)/n)
                x_new1.append(rx1)
                ry1 = 9.15*math.sin((2*i*math.pi)/n)
                y_new1.append(ry1)
            # print(x_new)
            # print(y_new)
            xnew = np.array(x_new)
            ynew = np.array(y_new)
            xnew1 = np.array(x_new1)
            ynew1 = np.array(y_new1)
            plt.subplot(121)
            font1 = {'family' : 'Times New Roman',  
            'weight' : 'normal',  
            'size'   : 15,  
            }  
            plt.scatter(xnew,ynew,c='red',s=1,label="Tested Tread state simulation",alpha=0.6)
            plt.scatter(xnew1,ynew1,c='blue',s=1,label="Standard Tread state simulation",alpha=0.6)
            plt.title("Tread state simulation",fontsize = 20)
            plt.text(1, -10.8, 'wear amount =' + str(worn1) + 'mm\n' + 'max abrasion amount =' + str(maxabr1) + 'mm\n' + 'average abrasion amount =' + str(avrabr1) + 'mm',fontsize=13,bbox=dict(boxstyle="round",facecolor='yellow',alpha=0.4))
            plt.legend(prop=font1,loc='upper right')
            plt.axis('equal')
            plt.subplot(122)             
            plt.plot(x,y,'r', label="tested wheel")
            plt.plot(x_t,y_t,'b', label="standard wheel")
            plt.xlabel('test point',fontsize=15)
            plt.ylabel('distance/mm',fontsize=15)
            plt.text(1000, 4, 'wear amount =' + str(worn1) + 'mm\n' + 'max abrasion amount =' + str(maxabr1) + 'mm\n' + 'average abrasion amount =' + str(avrabr1) + 'mm',fontsize=15,bbox=dict(boxstyle="round",facecolor='yellow',alpha=0.4))
            plt.title( 'Test Data',fontsize=20)
            plt.legend(prop=font1,loc='upper right')
            pl.show()
            self.buildfile(dat)

        #选择数据波形时触发的函数
        elif self.v2.get() == 1:
            dat = self.gettestdata()
            sta = self.getstadata()
            # print(dat[:100])
            # print(sta[:100])
            wornlist = []
            newdata = []
            for i in range(0,len(dat)):
                newdata.append(sta[i]-dat[i])
                wornlist.append(abs(newdata[i]))
            worn = min(wornlist[1:len(wornlist)-1])
            # print(wornlist)
            # print(worn)
            # print(newdata)
            for i in range(0,len(newdata)):
                newdata[i] = newdata[i]+worn
                newdata[i] = newdata[i]*math.pow(10,41)
            maxabr = abs(min(newdata[1:len(newdata)-1]))
            sumabr = abs(sum(newdata[1:len(newdata)-1]))
            avrabr = sumabr/(len(newdata)-2)
            worn1 = worn*math.pow(10,41)
            worn1 = format(worn1,'0.2f')
            maxabr1 = maxabr*math.pow(10,1)
            maxabr1 = format(maxabr1,'0.2f')
            avrabr1 = avrabr*math.pow(10,1)
            avrabr1 = format(avrabr1,'0.2f')

            # print(maxabr)
            text.insert(END,"磨损量为",'tag3')
            text.insert(END, worn*math.pow(10,41),'tag3')
            text.insert(END,"mm\n",'tag3')
            text.insert(END,"最大擦伤深度为",'tag3')
            text.insert(END, maxabr*math.pow(10,1),'tag3')
            text.insert(END,"mm\n",'tag3')
            text.insert(END,"平均擦伤深度为",'tag3')
            text.insert(END, avrabr*math.pow(10,1),'tag3')
            text.insert(END,"mm\n",'tag3')
            # print(sta)
            # print(dat)
            # print(newdata)
            x = np.linspace(0,len(dat1)-1,len(dat1))
            y = np.array(dat1)
            # plt.plot(x,y,'r')

            x_t = np.linspace(0,len(sta1)-1,len(sta1))
            y_t = np.array(sta1)
            font1 = {'family' : 'Times New Roman',  
            'weight' : 'normal',  
            'size'   : 15,  
            }  
            plt.plot(x,y,'r', label="tested wheel")
            plt.plot(x_t,y_t,'b', label="standard wheel")
            plt.xlabel('test point',fontsize=15)
            plt.ylabel('distance/mm',fontsize=15)
            plt.text(800, 4, 'wear amount =' + str(worn1) + 'mm\n' + 'max abrasion amount =' + str(maxabr1) + 'mm\n' + 'average abrasion amount =' + str(avrabr1) + 'mm',fontsize=15,bbox=dict(boxstyle="round",facecolor='yellow',alpha=0.4))
            plt.title( 'Test Data',fontsize=20)
            plt.legend(prop=font1,loc='upper right')
            pl.show()
            self.buildfile(dat)


        #选择踏面状态模拟时触发的函数
        elif self.v2.get() == 2:
            dat = self.gettestdata()
            sta = self.getstadata()
            # print(dat[:100])
            # print(sta[:100])
            wornlist = []
            newdata = []
            for i in range(0,len(dat)):
                newdata.append(sta[i]-dat[i])
                wornlist.append(abs(newdata[i]))
            worn = min(wornlist[1:len(wornlist)-1])
            # print(wornlist)
            # print(worn)
            # print(newdata)
            for i in range(0,len(newdata)):
                newdata[i] = newdata[i]+worn
                newdata[i] = newdata[i]*math.pow(10,41)
            maxabr = abs(min(newdata[1:len(newdata)-1]))
            sumabr = abs(sum(newdata[1:len(newdata)-1]))
            avrabr = sumabr/(len(newdata)-2)
            worn1 = worn*math.pow(10,41)
            worn1 = format(worn1,'0.2f')
            maxabr1 = maxabr*math.pow(10,1)
            maxabr1 = format(maxabr1,'0.2f')
            avrabr1 = avrabr*math.pow(10,1)
            avrabr1 = format(avrabr1,'0.2f')

            # print(maxabr)
            text.insert(END,"磨损量为",'tag3')
            text.insert(END, worn*math.pow(10,41),'tag3')
            text.insert(END,"mm\n",'tag3')
            text.insert(END,"最大擦伤深度为",'tag3')
            text.insert(END, maxabr*math.pow(10,1),'tag3')
            text.insert(END,"mm\n",'tag3')
            text.insert(END,"平均擦伤深度为",'tag3')
            text.insert(END, avrabr*math.pow(10,1),'tag3')
            text.insert(END,"mm\n",'tag3')
            # print(sta)
            # print(dat)
            # print(newdata)
            n = len(dat)
            x_new = []
            y_new = []
            x_new1 = []
            y_new1 = []
            for i in range(1,n+1):
                rx = (9.15-worn+newdata[i-1])*math.cos((2*i*math.pi)/n)
                x_new.append(rx)
                ry = (9.15-worn+newdata[i-1])*math.sin((2*i*math.pi)/n)
                y_new.append(ry)
                rx1 = 9.15*math.cos((2*i*math.pi)/n)
                x_new1.append(rx1)
                ry1 = 9.15*math.sin((2*i*math.pi)/n)
                y_new1.append(ry1)
            # print(x_new)
            # print(y_new)
            xnew = np.array(x_new)
            ynew = np.array(y_new)
            xnew1 = np.array(x_new1)
            ynew1 = np.array(y_new1)
            font1 = {'family' : 'Times New Roman',  
            'weight' : 'normal',  
            'size'   : 15,  
            }  
            plt.scatter(xnew,ynew,c='red',s=1,label="Tested Tread state simulation",alpha=0.6)
            plt.scatter(xnew1,ynew1,c='blue',s=1,label="Standard Tread state simulation",alpha=0.6)
            plt.title("Tread state simulation",fontsize = 20)
            plt.text(10, -7.5, 'wear amount =' + str(worn1) + 'mm\n' + 'max abrasion amount =' + str(maxabr1) + 'mm\n' + 'average abrasion amount =' + str(avrabr1) + 'mm',fontsize=15,bbox=dict(boxstyle="round",facecolor='yellow',alpha=0.4))
            plt.legend(prop=font1,loc='upper right')
            plt.axis('equal')
            pl.show()
            self.buildfile(dat)
      
WidgetsDemo() 