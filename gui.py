from tkinter import *
from tkinter import messagebox, scrolledtext
from PIL import Image, ImageTk
import math
import pyproj
import cv2
import random
import time
import tkinter as tk
import serial
import os
import pymssql
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
from threading import Thread

ser = serial.Serial("/dev/ttyAMA0", 9600)  # 打开串口，波特率9600
conn = pymssql.connect('DESKTOP-OQE2JMU', 'sa', 'weige123', 'test')  # 数据库连接

class Application(Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.WIDTH = 680
        self.HEIGHT = 450
        self.frame = Frame(self.master)
        self.frame.pack()
        self.ws = self.master.winfo_screenwidth()
        self.hs = self.master.winfo_screenheight()
        x = (self.ws / 2) - (self.WIDTH / 2)
        y = (self.hs / 2) - (self.HEIGHT / 2) - 10
        self.master.geometry('%dx%d+%d+%d' % (self.WIDTH, self.HEIGHT, x, y))
        self.backCanvas = Canvas(self.frame, width=self.WIDTH, height=self.HEIGHT)
        self.backPhoto = ImageTk.PhotoImage(
            Image.open("C:\\Users\\csw\\PycharmProjects\\GUI\\gif\\AR.png").resize((self.WIDTH, self.HEIGHT), Image.Resampling.NEAREST))
        self.backCanvas.create_image(self.WIDTH // 2, self.HEIGHT // 2, image=self.backPhoto)
        self.backCanvas.pack()
        self.lableFrameName = Label(self.frame, text='基于增强现实近眼显示的头部定位测姿系统登录', font=('微软雅黑', 20))
        self.lableFrameName.place(x=100, y=30)
        self.labelUserName = Label(self.frame, text='用户名：', font=('微软雅黑', 11))
        self.labelUserName.place(x=290, y=140, anchor='e')
        self.varUserName = StringVar(self.frame, value='')
        self.entryUserName = Entry(self.frame, font=('微软雅黑', 12), width=15, textvariable=self.varUserName)
        self.entryUserName.place(x=300, y=140, anchor='w')
        self.entryUserName.focus_set()
        self.labelPwd = Label(self.frame, text='密码：', font=('微软雅黑', 11))
        self.labelPwd.place(x=290, y=180, anchor='e')
        self.varPwd = StringVar(self.frame, value='')
        self.entryPwd = Entry(self.frame, show='*', font=('微软雅黑', 11), width=15, textvariable=self.varPwd)
        self.entryPwd.place(x=300, y=180, anchor='w')
        self.buttonOk = Button(self.frame, text='登录', font=('微软雅黑', 12), width=8, command=self.login)
        self.buttonOk.place(x=210, y=240)
        self.buttonCancel = Button(self.frame, text='删除', font=('微软雅黑', 12), width=8, command=self.cancel)
        self.buttonCancel.place(x=300, y=240)
        self.buttonRegister = Button(self.frame, text='注册', font=('微软雅黑', 12), width=8, command=self.to_register)
        self.buttonRegister.place(x=390, y=240)
        self.var_confirm_password = StringVar(self.frame, value='')

    def login(self):
        cur = conn.cursor()
        username_value = self.entryUserName.get()
        password_value = self.entryPwd.get()
        sql = 'SELECT count(*) FROM ID WHERE userpwd=%s'
        cur.execute(sql, (username_value + password_value,))
        result1 = cur.fetchone()
        db_have = False
        if result1[0] > 0:
            db_have = True
        if username_value == "":
            messagebox.showwarning(title="用户名不能为空", message="亲，用户名不能为空")
        elif password_value == "":
            messagebox.showwarning(title="密码不能为空", message="亲，密码不能为空")
        elif not db_have:
            result = messagebox.askokcancel(title="该用户不存在", message="该用户不存在，亲，您是否马上去注册？")
            if result:
                self.to_register()
        else:
            sql = 'SELECT username, password FROM ID WHERE userpwd=%s'
            cur.execute(sql, (username_value + password_value,))
            user_data = cur.fetchone()
            if user_data and username_value == user_data[0] and password_value == user_data[1]:
                root0.destroy()
                self.main()
            elif user_data and username_value == user_data[0] and password_value != user_data[1]:
                messagebox.showerror(title="登录失败", message="密码错误")

    def cancel(self):
        self.varUserName.set('')
        self.varPwd.set('')

    def do_register(self):
        cur = conn.cursor()
        register_username_v = self.varUserName.get()
        register_password_v = self.varPwd.get()
        confirm_password_v = self.var_confirm_password.get()
        sql = 'SELECT * FROM ID WHERE username=%s'
        cur.execute(sql, (register_username_v,))
        result1 = cur.fetchone()
        db_have = bool(result1)
        if register_username_v == "":
            messagebox.showwarning(title="注册失败", message="用户名不能为空!")
            return
        elif register_password_v == "":
            messagebox.showwarning(title="注册失败", message="密码不能为空!")
            return
        elif db_have:
            messagebox.showwarning(title="注册失败", message="该用户名已存在")
        elif register_password_v != confirm_password_v:
            messagebox.showwarning(title="两次密码不一致", message="您两次输入的密码不一致啊!")
        elif register_username_v and register_password_v and confirm_password_v == register_password_v:
            sql = 'INSERT INTO ID (username, password, userpwd) VALUES (%s, %s, %s)'
            cur.execute(sql, (register_username_v, register_password_v, register_username_v + register_password_v))
            conn.commit()
            messagebox.showinfo(title="注册成功", message=f"恭喜用户:{register_username_v}注册成功")

    def to_register(self):
        sub_window = Tk()
        sub_window.title("注册界面")
        sub_window.geometry("800x400")
        username_l = Label(sub_window, text="用户名", font="楷体")
        username_l.place(x=271, y=151)
        password_l = Label(sub_window, text="密码", font="楷体")
        password_l.place(x=271, y=201)
        confirm_password_l = Label(sub_window, text="确认密码", font="楷体")
        confirm_password_l.place(x=265, y=251)
        username_entry = Entry(sub_window, width=30, textvariable=self.varUserName)
        username_entry.place(x=351, y=151)
        password_entry = Entry(sub_window, width=30, textvariable=self.varPwd, show="*")
        password_entry.place(x=351, y=201)
        confirm_password_entry = Entry(sub_window, width=30, textvariable=self.var_confirm_password, show="*")
        confirm_password_entry.place(x=351, y=251)
        register_button = Button(sub_window, text="注册", font="楷体", command=self.do_register)
        register_button.place(x=401, y=301)
        sub_window.mainloop()

    def main(self):
        def goto(num):
            root.destroy()
            if num == 1:
                self.one()
            elif num == 2:
                self.two()
        root = Tk()
        root.geometry('300x150+600+200')
        root.title('登录窗口')
        but1 = Button(root, text="测姿", command=lambda: goto(1))
        but1.pack(pady=5)
        but2 = Button(root, text="定位", command=lambda: goto(2))
        but2.pack(pady=5)
        btnQuit = Button(root, text="退出", command=root.destroy)
        btnQuit.pack()
        root.mainloop()

    def one(self):
        def gotomain():
            root.destroy()
            self.main()
        def ini_fun():
            global y0, y1, y2, y3, y4, y5, y6, y7, y8, y9, inter_width, inter_width_entry, slope
            y0_label = tk.Label(root, text='y0').place(x=15, y=550, width=50, height=20)
            y1_label = tk.Label(root, text='y1').place(x=80, y=550, width=50, height=20)
            y2_label = tk.Label(root, text='y2').place(x=145, y=550, width=50, height=20)
            y3_label = tk.Label(root, text='y3').place(x=210, y=550, width=50, height=20)
            y4_label = tk.Label(root, text='y4').place(x=275, y=550, width=50, height=20)
            y5_label = tk.Label(root, text='y5').place(x=340, y=550, width=50, height=20)
            y6_label = tk.Label(root, text='y6').place(x=405, y=550, width=50, height=20)
            y7_label = tk.Label(root, text='y7').place(x=470, y=550, width=50, height=20)
            y8_label = tk.Label(root, text='y8').place(x=535, y=550, width=50, height=20)
            y9_label = tk.Label(root, text='y9').place(x=600, y=550, width=50, height=20)
            slope1_label = tk.Label(root, text='斜率1').place(x=80, y=610, width=50, height=20)
            slope2_label = tk.Label(root, text='斜率2').place(x=145, y=610, width=50, height=20)
            slope3_label = tk.Label(root, text='斜率3').place(x=210, y=610, width=50, height=20)
            slope4_label = tk.Label(root, text='斜率4').place(x=275, y=610, width=50, height=20)
            slope5_label = tk.Label(root, text='斜率5').place(x=340, y=610, width=50, height=20)
            slope6_label = tk.Label(root, text='斜率6').place(x=405, y=610, width=50, height=20)
            slope7_label = tk.Label(root, text='斜率7').place(x=470, y=610, width=50, height=20)
            slope8_label = tk.Label(root, text='斜率8').place(x=535, y=610, width=50, height=20)
            slope9_label = tk.Label(root, text='斜率9').place(x=600, y=610, width=50, height=20)
            inter_width_label = tk.Label(root, text='inter_width:').place(x=100, y=650, width=70, height=20)
            inter_width_entry = tk.Entry(root)
            inter_width_entry.place(x=175, y=650, width=50, height=20)
            inter_width_entry.insert(1, '10')
            slope = ['0.0', '0.0', '0.0', '0.0', '0.0', '0.0', '0.0', '0.0', '0.0', '0.0']
            (y0, y1, y2, y3, y4, y5, y6, y7, y8, y9) = (0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
        def show_y():
            global y0_entry, y1_entry, y2_entry, y3_entry, y4_entry, y5_entry, y6_entry, y7_entry, y8_entry, y9_entry
            global y0, y1, y2, y3, y4, y5, y6, y7, y8, y9, inter_width
            y0_entry = tk.Entry(root)
            y0_entry.place(x=15, y=530, width=50, height=20)
            y0_entry.insert(1, y0)
            y1_entry = tk.Entry(root)
            y1_entry.insert(1, y1)
            y1_entry.place(x=80, y=530, width=50, height=20)
            y2_entry = tk.Entry(root)
            y2_entry.place(x=145, y=530, width=50, height=20)
            y2_entry.insert(1, y2)
            y3_entry = tk.Entry(root)
            y3_entry.place(x=210, y=530, width=50, height=20)
            y3_entry.insert(1, y3)
            y4_entry = tk.Entry(root)
            y4_entry.place(x=275, y=530, width=50, height=20)
            y4_entry.insert(1, y4)
            y5_entry = tk.Entry(root)
            y5_entry.place(x=340, y=530, width=50, height=20)
            y5_entry.insert(1, y5)
            y6_entry = tk.Entry(root)
            y6_entry.place(x=405, y=530, width=50, height=20)
            y6_entry.insert(1, y6)
            y7_entry = tk.Entry(root)
            y7_entry.place(x=470, y=530, width=50, height=20)
            y7_entry.insert(1, y7)
            y8_entry = tk.Entry(root)
            y8_entry.place(x=535, y=530, width=50, height=20)
            y8_entry.insert(1, y8)
            y9_entry = tk.Entry(root)
            y9_entry.place(x=600, y=530, width=50, height=20)
            y9_entry.insert(1, y9)
        def show_slope():
            global slope
            slope1_num = tk.Label(root, text=slope[0], bg='#cccccc').place(x=80, y=590, width=50, height=20)
            slope2_num = tk.Label(root, text=slope[1], bg='#cccccc').place(x=145, y=590, width=50, height=20)
            slope3_num = tk.Label(root, text=slope[2], bg='#cccccc').place(x=210, y=590, width=50, height=20)
            slope4_num = tk.Label(root, text=slope[3], bg='#cccccc').place(x=275, y=590, width=50, height=20)
            slope5_num = tk.Label(root, text=slope[4], bg='#cccccc').place(x=340, y=590, width=50, height=20)
            slope6_num = tk.Label(root, text=slope[5], bg='#cccccc').place(x=405, y=590, width=50, height=20)
            slope7_num = tk.Label(root, text=slope[6], bg='#cccccc').place(x=470, y=590, width=50, height=20)
            slope8_num = tk.Label(root, text=slope[7], bg='#cccccc').place(x=535, y=590, width=50, height=20)
            slope9_num = tk.Label(root, text=slope[8], bg='#cccccc').place(x=600, y=590, width=50, height=20)
        def get_num():
            global y0, y1, y2, y3, y4, y5, y6, y7, y8, y9, inter_width, inter_width_entry
            y0 = int(y0_entry.get())
            y1 = int(y1_entry.get())
            y2 = int(y2_entry.get())
            y3 = int(y3_entry.get())
            y4 = int(y4_entry.get())
            y5 = int(y5_entry.get())
            y6 = int(y6_entry.get())
            y7 = int(y7_entry.get())
            y8 = int(y8_entry.get())
            y9 = int(y9_entry.get())
            inter_width = int(inter_width_entry.get())
        def calculate():
            global y0, y1, y2, y3, y4, y5, y6, y7, y8, y9, inter_width
            get_num()
            x = range(0, inter_width * 10, inter_width)
            y = [y0, y1, y2, y3, y4, y5, y6, y7, y8, y9]
            for k in range(0, 9):
                slope[k] = (y[k + 1] - y[k]) / inter_width
                slope[k] = round(slope[k], 1)
            show_slope()
            f_plot.clear()
            f_plot.plot(x, y)
            f_plot.grid()
            canvs.draw()
        def clear():
            ini_fun()
            show_y()
            show_slope()
        def main2():
            global root, f, f_plot, canvs
            root = tk.Tk()
            root.geometry("670x900+30+30")
            root.title("测姿运作与计算斜率")
            f = Figure(figsize=(6.4, 4.6), dpi=100)
            f_plot = f.add_subplot(111)
            f_plot.grid()
            canvs = FigureCanvasTkAgg(f, root)
            canvs.get_tk_widget().place(x=15, y=15)
            tk.Button(root, text='计算', command=calculate).place(x=500, y=650, width=70, height=30)
            tk.Button(root, text='清空', command=clear).place(x=580, y=650, width=70, height=30)
            tk.Button(root, text='运行', command=lambda: cezi()).place(x=100, y=710, width=100, height=50)
            tk.Button(root, text='返回主窗体', command=gotomain).place(x=100, y=800, width=100, height=50)
            Receive1 = tk.LabelFrame(root, text="接收区", padx=30, pady=5)
            Receive1.place(x=350, y=690)
            Receive_Window1 = scrolledtext.ScrolledText(Receive1, width=20, height=12, padx=30, pady=5, wrap=tk.WORD)
            Receive_Window1.grid()
            toolbar = NavigationToolbar2Tk(canvs, root)
            toolbar.place(x=15, y=475, width=200, height=40)
            y_frame = tk.Frame(root, highlightbackground='gray', highlightthickness=2).place(x=10, y=520, width=650, height=2)
            slope_frame = tk.Frame(root, highlightbackground='gray', highlightthickness=2).place(x=60, y=580, width=600, height=2)
            button_frame = tk.Frame(root, highlightbackground='gray', highlightthickness=2).place(x=60, y=640, width=600, height=2)
            def cezi():
                print("python execute cpp program:")
                os.system("/home/pi/Desktop/kal2/kaltest")
                a = "/home/pi/Desktop/kal2/kaltest"
                if os.path.exists(a):
                    f = os.popen(a)
                    data = f.readlines()
                    f.close()
                    Receive_Window1.insert("end", str(data) + '\n')
                    Receive_Window1.see("end")
            ini_fun()
            show_y()
            show_slope()
            root.mainloop()
        main2()

    def two(self):
        def gotomain():
            root.destroy()
            self.main()
        def lonlat2utm(lon, lat):
            z = int(lon / 6 + 31)
            proj = pyproj.Proj(proj='utm', zone=z, ellps='WGS84')
            return proj(lon, lat), z
        def utm2lonlat(x, y, z):
            proj = pyproj.Proj(proj='utm', zone=z, ellps='WGS84')
            return proj(x, y, inverse=True)
        def insec(p1, r1, p2, r2):
            x, y, R = p1[0], p1[1], r1
            a, b, S = p2[0], p2[1], r2
            d = math.sqrt((abs(a - x)) ** 2 + (abs(b - y)) ** 2)
            if d > (R + S) or d < (abs(R - S)):
                print("没有公共点")
                return None
            elif d == 0 and R == S:
                print("两个圆同心")
                return None
            else:
                A = (R ** 2 - S ** 2 + d ** 2) / (2 * d)
                h = math.sqrt(R ** 2 - A ** 2)
                x2 = x + A * (a - x) / d
                y2 = y + A * (b - y) / d
                x3 = x2 - h * (b - y) / d
                y3 = y2 + h * (a - x) / d
                x4 = x2 + h * (b - y) / d
                y4 = y2 - h * (a - x) / d
                return [x3, y3], [x4, y4]
        def location_trans(p1, r1, p2, r2):
            z1 = lonlat2utm(p1[0], p1[1])
            z2 = lonlat2utm(p2[0], p2[1])
            z = int((z1[1] + z2[1]) / 2)
            C = insec(z1[0], r1, z2[0], r2)
            if C:
                a = utm2lonlat(C[0][0], C[0][1], z)
                b = utm2lonlat(C[1][0], C[1][1], z)
                return a, b
            return None, None
        def location_min(p1, p2, p, r):
            d1 = math.fabs(r - math.sqrt((p[0] - p1[0]) ** 2 + (p[1] - p1[1]) ** 2))
            d2 = math.fabs(r - math.sqrt((p[0] - p2[0]) ** 2 + (p[1] - p2[1]) ** 2))
            return p1 if d1 < d2 else p2
        def location_judg(p1, r1, p2, r2, p3, r3):
            li = []
            z1 = lonlat2utm(p1[0], p1[1])
            z2 = lonlat2utm(p2[0], p2[1])
            z3 = lonlat2utm(p3[0], p3[1])
            z12 = int((z1[1] + z2[1]) / 2)
            z13 = int((z1[1] + z3[1]) / 2)
            z23 = int((z2[1] + z3[1]) / 2)
            z = int((z12 + z13 + z23) / 3)
            C12 = insec(z1[0], r1, z2[0], r2)
            C13 = insec(z1[0], r1, z3[0], r3)
            C23 = insec(z2[0], r2, z3[0], r3)
            if C12:
                m12 = location_min(C12[0], C12[1], z3[0], r3)
                li.append(utm2lonlat(m12[0], m12[1], z12))
            else:
                li.append(None)
            if C13:
                m13 = location_min(C13[0], C13[1], z2[0], r2)
                li.append(utm2lonlat(m13[0], m13[1], z13))
            else:
                li.append(None)
            if C23:
                m23 = location_min(C23[0], C23[1], z1[0], r1)
                li.append(utm2lonlat(m23[0], m23[1], z23))
            else:
                li.append(None)
            if C12 and C13 and C23:
                m = [(m12[0] + m13[0] + m23[0]) / 3, (m12[1] + m13[1] + m23[1]) / 3]
                li.append(utm2lonlat(m[0], m[1], z))
                return li
            elif C12 or C13 or C23:
                li.append(None)
                return li
            else:
                return [None, None, None, None]
        def central_win(win):
            win.resizable(0, 0)
            screenwidth = win.winfo_screenwidth()
            screenheight = win.winfo_screenheight()
            win.update()
            width = win.winfo_width()
            height = win.winfo_height()
            size = '+%d+%d' % ((screenwidth - width) / 2, (screenheight - height) / 2)
            win.geometry(size)
        def gui_start():
            root = tk.Tk()
            root.title("WSG84三点定位系统")
            mainfram = tk.Frame(root, width=800, height=920)
            mainfram.grid_propagate(0)
            mainfram.grid()
            central_win(root)
            labelName = tk.Label(root, text='经度（正E负W）', justify=tk.LEFT).place(x=120, y=20, width=180, height=50)
            labelName = tk.Label(root, text='纬度（正N负S）', justify=tk.LEFT).place(x=300, y=20, width=180, height=50)
            labelName = tk.Label(root, text='位置1:', justify=tk.LEFT).place(x=20, y=70, width=100, height=50)
            labelName = tk.Label(root, text='距离1:', justify=tk.LEFT).place(x=20, y=120, width=100, height=50)
            labelName = tk.Label(root, text='位置2:', justify=tk.LEFT).place(x=20, y=170, width=100, height=50)
            labelName = tk.Label(root, text='距离2:', justify=tk.LEFT).place(x=20, y=220, width=100, height=50)
            labelName = tk.Label(root, text='位置3:', justify=tk.LEFT).place(x=20, y=270, width=100, height=50)
            labelName = tk.Label(root, text='距离3:', justify=tk.LEFT).place(x=20, y=320, width=100, height=50)
            labelName = tk.Label(root, text='12推测点:', justify=tk.LEFT).place(x=20, y=390, width=100, height=50)
            labelName = tk.Label(root, text='13推测点:', justify=tk.LEFT).place(x=20, y=440, width=100, height=50)
            labelName = tk.Label(root, text='23推测点:', justify=tk.LEFT).place(x=20, y=490, width=100, height=50)
            labelName = tk.Label(root, text='中心推测点:', justify=tk.LEFT).place(x=20, y=540, width=100, height=50)
            labelName = tk.Label(root, text='米', justify=tk.LEFT).place(x=300, y=120, width=20, height=50)
            labelName = tk.Label(root, text='米', justify=tk.LEFT).place(x=300, y=220, width=20, height=50)
            labelName = tk.Label(root, text='米', justify=tk.LEFT).place(x=300, y=320, width=20, height=50)
            labelName = tk.Label(root, text='两点定位1:', justify=tk.LEFT).place(x=20, y=630, width=100, height=50)
            labelName = tk.Label(root, text='两点定位2:', justify=tk.LEFT).place(x=20, y=680, width=100, height=50)
            Receive = tk.LabelFrame(root, text="接收区", padx=30, pady=30)
            Receive.place(x=500, y=70)
            Receive_Window = scrolledtext.ScrolledText(Receive, width=20, height=12, padx=30, pady=30, wrap=tk.WORD)
            Receive_Window.grid()
            backPhoto = ImageTk.PhotoImage(Image.open("D:\\Desktop\\earth.png").resize((300, 300), Image.Resampling.NEAREST))
            BackCanvas = Canvas(root, width=300, height=300)
            BackCanvas.create_image(150, 150, image=backPhoto)
            BackCanvas.place(x=500, y=400)
            e1_lon = tk.Entry(mainfram)
            e1_lon.delete(0, tk.END)
            e1_lon.insert(0, 114.304569)
            e1_lon.place(x=120, y=70, width=180, height=50)
            e1_r = tk.Entry(mainfram)
            e1_r.delete(0, tk.END)
            e1_r.insert(0, 300000)
            e1_r.place(x=120, y=120, width=180, height=50)
            e2_lon = tk.Entry(mainfram)
            e2_lon.delete(0, tk.END)
            e2_lon.insert(0, 115.857972)
            e2_lon.place(x=120, y=170, width=180, height=50)
            e2_r = tk.Entry(mainfram)
            e2_r.delete(0, tk.END)
            e2_r.insert(0, 400000)
            e2_r.place(x=120, y=220, width=180, height=50)
            e3_lon = tk.Entry(mainfram)
            e3_lon.delete(0, tk.END)
            e3_lon.insert(0, 116.378517)
            e3_lon.place(x=120, y=270, width=180, height=50)
            e3_r = tk.Entry(mainfram)
            e3_r.delete(0, tk.END)
            e3_r.insert(0, 900000)
            e3_r.place(x=120, y=320, width=180, height=50)
            e1_lat = tk.Entry(mainfram)
            e1_lat.delete(0, tk.END)
            e1_lat.insert(0, 30.593354)
            e1_lat.place(x=300, y=70, width=180, height=50)
            e2_lat = tk.Entry(mainfram)
            e2_lat.delete(0, tk.END)
            e2_lat.insert(0, 28.682976)
            e2_lat.place(x=300, y=170, width=180, height=50)
            e3_lat = tk.Entry(mainfram)
            e3_lat.delete(0, tk.END)
            e3_lat.insert(0, 39.865246)
            e3_lat.place(x=300, y=270, width=180, height=50)
            ex1 = tk.Entry(mainfram, state='readonly')
            ex1.place(x=120, y=390, width=360, height=50)
            ex2 = tk.Entry(mainfram, state='readonly')
            ex2.place(x=120, y=440, width=360, height=50)
            ex3 = tk.Entry(mainfram, state='readonly')
            ex3.place(x=120, y=490, width=360, height=50)
            ex4 = tk.Entry(mainfram, state='readonly')
            ex4.place(x=120, y=540, width=360, height=50)
            ey1 = tk.Entry(mainfram, state='readonly')
            ey1.place(x=120, y=630, width=360, height=50)
            ey2 = tk.Entry(mainfram, state='readonly')
            ey2.place(x=120, y=680, width=360, height=50)
            def dingwei():
                while True:
                    k = 0
                    line = str(str(ser.readline())[2:])
                    if line.startswith('$GPGGA'):
                        line = str(line).split(',')
                        jing = float(line[4][:3]) + float(line[4][3:]) / 60
                        wei = float(line[2][:2]) + float(line[2][2:]) / 60
                        print("经度:", jing)
                        print("纬度:", wei)
                        Receive_Window.insert("end", f"经度:{jing}\n纬度:{wei}\n")
                        Receive_Window.see("end")
                        if jing < 120.2631:
                            img = cv2.imread('1.tif')
                            img = cv2.resize(img, (720, 480))
                            cv2.imshow("img", img)
                            k = cv2.waitKey(0)
                            if k == 5:
                                cv2.destroyAllWindows()
                        if jing > 120.2631:
                            img = cv2.imread('5.tif')
                            img = cv2.resize(img, (720, 480))
                            cv2.imshow("img", img)
                            k = cv2.waitKey(0)
                            if k == 5:
                                cv2.destroyAllWindows()
            def input_judg(e):
                try:
                    s = float(str(e.get()))
                except:
                    e.delete(0, tk.END)
                    e.insert(0, 0)
                    return 0.0
                if e in (e1_lat, e2_lat, e3_lat) and (s < -90 or s > 90):
                    e.delete(0, tk.END)
                    e.insert(0, 0)
                    return 0.0
                elif e in (e1_lon, e2_lon, e3_lon) and (s < -180 or s > 180):
                    e.delete(0, tk.END)
                    e.insert(0, 0)
                    return 0.0
                elif e in (e1_r, e2_r, e3_r) and (s < 0 or s > 400750170):
                    e.delete(0, tk.END)
                    e.insert(0, 0)
                    return 0.0
                return s
            def view(e, s):
                s = str(s)
                e.config(state='normal')
                e.delete(0, tk.END)
                e.insert(0, s)
                e.config(state='readonly')
            def event():
                lat1 = input_judg(e1_lat)
                lon1 = input_judg(e1_lon)
                r1 = input_judg(e1_r)
                lat2 = input_judg(e2_lat)
                lon2 = input_judg(e2_lon)
                r2 = input_judg(e2_r)
                lat3 = input_judg(e3_lat)
                lon3 = input_judg(e3_lon)
                r3 = input_judg(e3_r)
                result = location_judg([lon1, lat1], r1, [lon2, lat2], r2, [lon3, lat3], r3)
                view(ex1, result[0])
                view(ex2, result[1])
                view(ex3, result[2])
                view(ex4, result[3])
            def double(n):
                lat1 = input_judg(e1_lat)
                lon1 = input_judg(e1_lon)
                r1 = input_judg(e1_r)
                lat2 = input_judg(e2_lat)
                lon2 = input_judg(e2_lon)
                r2 = input_judg(e2_r)
                lat3 = input_judg(e3_lat)
                lon3 = input_judg(e3_lon)
                r3 = input_judg(e3_r)
                if n == 1:
                    result = location_trans([lon1, lat1], r1, [lon2, lat2], r2)
                elif n == 2:
                    result = location_trans([lon1, lat1], r1, [lon3, lat3], r3)
                elif n == 3:
                    result = location_trans([lon2, lat2], r2, [lon3, lat3], r3)
                else:
                    result = location_trans([lon1, lat1], r1, [lon2, lat2], r2)
                view(ey1, result[0])
                view(ey2, result[1])
            def clean():
                view(ex1, "")
                view(ex2, "")
                view(ex3, "")
                view(ex4, "")
                view(ey1, "")
                view(ey2, "")
                e1_lon.delete(0, tk.END)
                e1_lon.insert(0, "")
                e2_lon.delete(0, tk.END)
                e2_lon.insert(0, "")
                e3_lon.delete(0, tk.END)
                e3_lon.insert(0, "")
                e1_lat.delete(0, tk.END)
                e1_lat.insert(0, "")
                e2_lat.delete(0, tk.END)
                e2_lat.insert(0, "")
                e3_lat.delete(0, tk.END)
                e3_lat.insert(0, "")
                e1_r.delete(0, tk.END)
                e1_r.insert(0, "")
                e2_r.delete(0, tk.END)
                e2_r.insert(0, "")
                e3_r.delete(0, tk.END)
                e3_r.insert(0, "")
            def start_event():
                t = Thread(target=event)
                t.setDaemon(False)
                t.start()
            def start_clean():
                t = Thread(target=clean)
                t.setDaemon(False)
                t.start()
            def start_double(i):
                t = Thread(target=double, args=(i,))
                t.setDaemon(False)
                t.start()
            def button_event(s):
                if s.keysym in ('C', 'c'):
                    start_event()
                elif s.keysym in ('D', 'd'):
                    start_clean()
            b1 = tk.Button(mainfram, width=30, text="计算123三点定位", command=start_event)
            b1.bind_all('C', button_event)
            b1.bind_all('c', button_event)
            b1.place(x=20, y=590, width=460, height=30)
            b2 = tk.Button(mainfram, width=30, text="清空", command=start_clean)
            b2.bind_all('D', button_event)
            b2.bind_all('d', button_event)
            b2.place(x=20, y=370, width=460, height=30)
            b3 = tk.Button(mainfram, width=30, text="计算12两点定位", command=lambda: start_double(1))
            b3.place(x=20, y=730, width=140, height=50)
            b4 = tk.Button(mainfram, width=30, text="计算13两点定位", command=lambda: start_double(2))
            b4.place(x=180, y=730, width=140, height=50)
            b5 = tk.Button(mainfram, width=30, text="计算23两点定位", command=lambda: start_double(3))
            b5.place(x=340, y=730, width=140, height=50)
            b6 = tk.Button(mainfram, width=30, text="运行", command=lambda: dingwei())
            b6.place(x=20, y=780, width=750, height=50)
            b7 = tk.Button(mainfram, width=30, text="返回主窗体", command=gotomain)
            b7.place(x=20, y=830, width=750, height=50)
            start_event()
            start_double(1)
            root.mainloop()
        gui_start()

root0 = Tk()
root0.title("登录")
app = Application(master=root0)
root0.mainloop()
