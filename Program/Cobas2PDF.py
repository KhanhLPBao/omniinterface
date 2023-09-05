from tkinter import Label, Frame, Entry, Button, Toplevel
from tkinter.filedialog import askopenfile
from tkinter.messagebox import showerror, showinfo
import shutil
import string
import random
import json
import os
outputdir = ''
class main:
    def __init__(self,master,serverlink):
        self._workingcase = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(8))
        self.workingcase = {}
        with open(f'{serverlink}/listwork/_{self.workingcase}','w') as _work:
            _work.close()
        #####
        self.master = master
        self.serverlink = serverlink
        #####
        self.workingframe = Frame(self.master, height = 600, width = 800)
        self.workingframe.grid(row = 1, column = 1)
        self.master.grid_rowconfigure(0,weight = 1)
        self.master.grid_rowconfigure(2,weight = 1)       
        self.master.grid_columnconfigure(0,weight = 1)
        self.master.grid_columnconfigure(2,weight = 1)    

        self.font = ("Times News Romans", 15)

    def input(self):
        _tenmechay = Label(
            self.workingframe,
            text = "Tên mẻ chạy",
            font = self.font)
        _tenmechay.grid(
            row = 0, 
            column = 0)
        
        self.tenmechay = Entry(
            self.workingframe,
            width = 25,
            font = self.font)
        self.tenmechay.grid(
            row = 0,
            column = 1)
        
        cobasfile = Button(
            self.workingframe,
            text = 'Chọn file kết quả\nHPV Cobas',
            font = self.font,
            command = self.importinfo('Cobas'))
        cobasfile.grid(
            row = 1,
            column = 0)

        self._cobasfile = Label(
            self.workingframe,
            text = "",
            font = self.font,
            width = 35)
        self._cobasfile.grid(
            row = 1,
            column = 1)

        bnfile = Button(
            self.workingframe,
            text = 'Chọn file excel thông tin bệnh nhân',
            font = self.font,
            command = self.importinfo('Patient'))
        bnfile.grid(
            row = 2,
            column = 0
        )

        self._bnfile = Label(
            self.workingframe,
            text = "",
            font = self.font
        )
        self._bnfile.grid(
            row = 2,
            column =1
            )
        
        nhaplieu = Button(
            self.workingframe,
            text = "Nhập dữ liệu",
            font = self.font,
            command = self.export
            )
        nhaplieu.grid(
            row = 3,
            column = 0,
            columnspan = 2
        )
    
    def importexcel(self,_filetype):
        match _filetype:
            case 'Cobas':
                _filelink = askopenfile(title = "Chọn", mode = 'r', filetypes=[('Cobas result files','*.xml')])
                self.workingcase['Cobas'] = _filelink
                self._cobasfile.config(text = "_filelink")
            case 'Patient':
                _filelink = askopenfile(title = "Chọn", mode = 'r', filetypes=[('Excel','*.xlsx')])
                self.workingcase['Patient'] = _filelink            
                self._bnfile.config(text = _filelink)

    def export(self):
        runningname = self.tenmechay.get()
        if runningname == "" or self.workingcase['Cobas'] == "" or self.workingcase['Patient'] == "" :
            showerror(title = 'KHÔNG ĐỦ DỮ LIỆU', message= "KHÔNG ĐỦ DỮ LIỆU\nVui lòng điền đủ tên mẻ chạy, chọn file Cobas và bệnh nhân")
        else:
            self.workingcase['Run'] = runningname
            shutil.move(self.workingcase['Cobas'], f'{self.serverlink}/input/')
            shutil.move(self.workingcase['Patient'], f'{self.serverlink}/input/')
            with open(f'{self.serverlink}/listwork/_{self._workingcase}','w') as _work:
                json.dump(self.workingcase,_work)
                _work.close()
            infomsg = f"Tác vụ {self._workingcase} đã đuọc khởi tạo\n-Chương trình: Cobas2PDF - Chuyển kết quả Cobas để ký số\n- Tên mẻ chạy: {self.workingcase['Run']}"
            showinfo(title=f'{self._workingcase} task', message = infomsg)
            slink = self.serverlink
            progresspanel = Toplevel()
            self.infor = Label(progresspanel,text = "Thông tin đang được xử lý",font = ("Times News Romans", 25))
            self.infor.pack()
            progresspanel.after(5000,checkstatus)
            wkc = self._workingcase
            def checkstatus(wkc):
                import time
                if os.path.isfile(f'{slink}/output/_{wkc}.kq'):
                    self.info.config(text = "Đã chuyển đổi xong\nVui lòng vào thư mục xuất để lấy kết quả")
                    exitbutton = Button(progresspanel, text = "OK", command = progresspanel.destroy())