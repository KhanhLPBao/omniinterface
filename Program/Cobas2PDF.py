from tkinter import Label, Frame, Entry, Button, Toplevel
from tkinter.filedialog import askopenfilename
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

        #####
        self.master = master
        self.serverlink = serverlink
        #####
        self.workingframe = Frame(self.master, height = 600, width = 800, highlightthickness=2,highlightbackground='black')
        self.workingframe.grid(row = 1, column = 1)
        self.master.grid_rowconfigure(0,weight = 1)
        self.master.grid_rowconfigure(2,weight = 1)       
        self.master.grid_columnconfigure(0,weight = 1)
        self.master.grid_columnconfigure(2,weight = 1)    

        self.font = ("Times News Romans", 15)

        self.input()
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
            command = lambda x = 'Cobas': self.importinfo(x))
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
            command = lambda x = 'Patient': self.importinfo(x))
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
        
        self.timeframe = Frame(
            self.workingframe,
        )
        self.timeframe.grid(
            row = 3,
            column = 1
        )

        self._ngaynhap = Label(
            self.workingframe,
            text = "Ngày tiếp nhận",
            font = self.font,
        )
        self._ngaynhap.grid(
            row = 3,
            column = 0
        )

        self.ngaynhap_ngay = Label(
            self.timeframe,
            text = 'Ngày',
            font = self.font
        ).pack(side='left')

        self.ngaynhap_entry_ngay = Entry(
            self.timeframe,
            width = 3,
            font = self.font
        )
        self.ngaynhap_entry_ngay.pack(side='left')
        
        self.ngaynhap_thang = Label(
            self.timeframe,
            text = 'Tháng',
            font = self.font
        ).pack(side='left')

        self.ngaynhap_entry_thang = Entry(
            self.timeframe,
            width = 3,
            font = self.font
        )
        self.ngaynhap_entry_thang.pack(side='left')

        self.ngaynhap_nam = Label(
            self.timeframe,
            text = 'Năm',
            font = self.font
        ).pack(side='left')

        self.ngaynhap_entry_nam = Entry(
            self.timeframe,
            width = 3,
            font = self.font
        )
        self.ngaynhap_entry_nam.pack(side='left')

        nhaplieu = Button(
            self.workingframe,
            text = "Nhập dữ liệu",
            font = self.font,
            command = self.export
            )
        nhaplieu.grid(
            row = 4,
            column = 0,
            columnspan = 2
        )
    
    def importinfo(self,_filetype):
        _filelink = ''
        widget_type = {
            'Cobas': self._cobasfile,
            'Patient': self._bnfile
            } 
        _importfiletype = {
            'Cobas': [('Cobas result files','*.xml')],
            'Patient': [('Excel 2010 or later','*.xlsx')]
        }
        _filelink = askopenfilename(filetypes = _importfiletype[_filetype])
        widget_type[_filetype].config(text = _filelink)
        self.workingcase[_filetype] = _filelink

    def export(self):
        runningname = self.tenmechay.get()
        receivedday_day = self.ngaynhap_entry_ngay.get()
        receivedday_month = self.ngaynhap_entry_thang.get()
        receivedday_year = self.ngaynhap_entry_nam.get()
        if runningname == "" or self.workingcase['Cobas'] == "" or self.workingcase['Patient'] == "" :
            showerror(title = 'KHÔNG ĐỦ DỮ LIỆU', message= "KHÔNG ĐỦ DỮ LIỆU\nVui lòng điền đủ tên mẻ chạy, chọn file Cobas và bệnh nhân")
        else:
            self.workingcase['Run'] = runningname
            self.workingcase['Rec_day'] = receivedday_day
            self.workingcase['Rec_month'] = receivedday_month
            self.workingcase['Rec_year'] = receivedday_year
            shutil.move(self.workingcase['Cobas'], f'{self.serverlink}/input/')
            shutil.move(self.workingcase['Patient'], f'{self.serverlink}/input/')
            with open(f'{self.serverlink}/listwork/_{self._workingcase}','w') as _work:
                json.dump(self.workingcase,_work)
                _work.close()
            infomsg = f"Tác vụ {self._workingcase} đã đuọc khởi tạo\n-Chương trình: Cobas2PDF - Chuyển kết quả Cobas để ký số\n- Tên mẻ chạy: {self.workingcase['Run']}"
            showinfo(title=f'{self._workingcase} task', message = infomsg)
            slink = self.serverlink
            self.progresspanel = Toplevel()
            self.infor = Label(self.progresspanel,text = "Thông tin đang được xử lý",font = ("Times News Romans", 25))
            self.infor.pack()
            self.checkstatus()
    
    def checkstatus(self):
#        while os.path.isfile(f'{self.serverlink}/output/_{self._workingcase}.kq') == False:
        print('Begin scanning')
        if os.path.isfile(f'{self.serverlink}/output/_{self._workingcase}.kq'):
            self.progresspanel.destroy()
            showinfo
        self.progresspanel.after(5000,self.checkstatus)
