import os
import sys
import tkinter as Tk
from tkinter import ttk
from tkinter import Menu
from tkinter import filedialog
from tkinter.messagebox import showerror, showinfo
import json

pathtoscript = os.path.dirname(__file__)
class maingui(Tk.Tk):
    def __init__(self):
        self.masterconfig = json.load(open(f'{pathtoscript}/configure.json'))
        ### Folder cua may chu ###
        self.serverdir = self.masterconfig['serverdir']
        ##########################
        Tk.Tk.__init__(self)
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        self.geometry(f'{screen_width}x{screen_height}')
        self.attributes('-fullscreen',True)       

        _titleframe = Tk.Frame(self,
                               height=15,
                               highlightthickness=2,
                               highlightbackground='black')
        
        Tk.Label(_titleframe,text = 'TDG OMNI INTERFACE', font = ('Times News Romans',35)).pack()
        _titleframe.pack(fill='both')

        self.mainframe = Tk.Frame(self,
                                  height=(screen_height-125),
                                  highlightthickness=2,highlightbackground='black')
        self.mainframe.pack(expand=True,fill='both')

        self.utilityframe = Tk.Frame(self,
                                     height=(100),
                                     width = screen_width,
                                     highlightthickness=2,
                                     highlightbackground='black',
                                     relief='raised')         
        self.utilityframe.pack(side='bottom')  

        self.mainmenu = Menu(self)
        self.config(menu=self.mainmenu)

        self.section_file = Menu(
            self.mainmenu,
            tearoff = 0
        )
        self.mainmenu.add_cascade(label="File",
                                  menu=self.section_file) 
        self.section_file.add_command(label = 'Sign up',
                                      command = self.signup)
        self.section_file.add_command(label = 'Logout')
        self.section_file.add_command(label = 'Quit',
                                      command = self.quit)    
        self.section_file.entryconfig("Logout", state="disabled")

        self.section_program = Menu(
            self.mainmenu,
            tearoff = 0
        )
        self.mainmenu.add_cascade(label="Program",
                                  menu=self.section_program)
        try:            
            with open(f'{self.serverdir}/programindex.json') as _prog_idx:
                self.prog_idx = json.load(_prog_idx)
                _prog_idx.close()
            for prog in self.prog_idx["Program"]:
                self.section_program.add_command(label = prog)
                self.section_program.entryconfig(prog, state = 'disabled')
        except FileNotFoundError:
            showerror('NO SERVERDIR DETECTED','FOUND NO TRACE OF SERVER DIRECTORY')
            exit(1)
        self._panel = {'File':self.section_file,'Program': self.section_program}

        self.login()
        
    def login(self):
        loginframe = Tk.Frame(self.mainframe,
                              height=300,
                              width=500,
                              highlightthickness=1,
                              highlightbackground='black') 
        loginframe.pack(pady=300,
                        expand=True)  
        loginframe.columnconfigure(200,
                                   weight=3)
        loginframe.columnconfigure(300,
                                   weight=1)
        _title = Tk.Label(loginframe,
                          text = 'VUI LÒNG ĐĂNG NHẬP ĐỂ SỬ DỤNG CÁC CHỨC NĂNG',font=('Times News Romans',15))
        _title.grid(column=0,
                    row = 0,
                    columnspan=2)
        _acc = Tk.Label(loginframe,
                        text='Tên tài khoản',font=('Times News Romans',15),
                        height=1, width=15,
                        highlightthickness=1, highlightbackground='black')
        _acc.grid(column=0,
                  row=1,
                  stick='nwse')
        self.acc = Tk.Entry(loginframe,
                            width=35, font=('Times News Romans',15))
        self.acc.grid(column=1,
                      row=1)
        _pwd = Tk.Label(loginframe,
                        text='Mật khẩu',font=('Times News Romans',15),
                        height=1,width=15,
                        highlightthickness=1,highlightbackground='black')
        _pwd.grid(column=0,
                  row=2,
                  stick='nwse')
        self.pwd = Tk.Entry(loginframe,
                            width=35,
                            font = ('Times News Romans', 15),
                            show='*'
                            )
        self.pwd.grid(column=1,
                      row=2)
        _button = Tk.Button(loginframe,
                            text = 'ĐĂNG NHẬP', font=('Times News Romans',20),
                            command = self.logincheck)
        _button.grid(column=0,
                     row=3,
                     columnspan=2)

        self.failed_login = 0

    def logincheck(self):
        import time
        import random

        self.acc_name = self.acc.get()
        acc_pwd = ''.join(format(i, '08b') for i in bytearray(self.pwd.get(), encoding ='utf-8'))
        try:
            print(self.acc_name.encode("utf-8").hex())
            with open(f'{self.serverdir}/account/{self.acc_name.encode("utf-8").hex()}') as acc_info:
                compare = bin(acc_pwd == json.load(acc_info)['pwd'])
                acc_info.close()
        except:
            compare = bin(False)
        time.sleep(random.uniform(0.6,2.3))
        del time
        del random
        loginresonse = {bin(True):self.loginsuccess, bin(False):self.loginfailed}
        loginresonse[compare]()
        
    def loginsuccess(self):
        for _w in self.mainframe.winfo_children():
            _w.destroy()
        self.mainmenu.add_command(label=f'Welcome {self.acc_name}')  
        self.section_file.entryconfig("Logout", state="active")
        self.accpermopen(self.acc_name)
    
    def loginfailed(self):
        print(self.failed_login)
        if self.failed_login < 5:
            showerror('LOGIN FAILED', f'Username and passworld not match with server\' data\nYou have {5 - self.failed_login} times left')
        else:
            showerror('LOGIN FAILED', 'Encountered to much failed login, anti timing-attack activated.\nProgram will shut down')
            exit(1)

    def accpermopen(self,account):
        with open(f'{self.serverdir}/account/{account.encode("utf-8").hex()}') as acc_info:
            acc_perm = json.load(acc_info)['perm']
            acc_info.close()
            all_opt = [_o for _o in acc_perm]
            if all_opt[0] == 'All':
                _alltask = [(bat,t) for bat in self.prog_idx if bat != "File" for t in self.prog_idx[bat]  ]
                for _task,_opt in _alltask:
                    self._panel[_task].entryconfig(_opt,state='active')
            else:
                _alltask = [o for x in all_opt for o in acc_perm[x]]
                for _opt in _alltask:
                    if int(permallowed) == 1:
                        self._panel[_opt].entryconfig(opt,state='active')
    
    def signup(self):
        def check():
            import os
            ipacc = acc.get()
            pwd1 = pwd.get()
            pwd2 = pwd_entry.get()

            if os.path.isfile(f'{self.serverdir}/account/{ipacc.encode("utf-8").hex()}'):
                showerror('ACCOUNT EXISTS', 'ACCOUNT ALREADY EXISTS ON SERVER\' DATABASE')
            else:
                if hash(pwd1) == hash(pwd2):
                    account = {}
                    account['perm'] = []
                    account['pwd'] = ''.join(format(i, '08b') for i in bytearray(pwd1, encoding ='utf-8'))
                    with open(f'{self.serverdir}/account/{ipacc.encode("utf-8").hex()}','w') as newacc:
                        json.dump(account,newacc)
                        newacc.close()
                    showinfo('REGISTRATION SUCCESS','ACCOUNT HAVE BEEN REGISTRATED\nContact moderators and administrators for perm setup')
                    for _w in self.mainframe.winfo_children():
                        _w.destroy()
                    self.login()
                else:
                    showerror('PASSWORDS NOT MATCHED', 'HASH COMPARE FAILED DUE TO PASSWORDS NOT MATCHED.\nPLEASE REENTER PASSWORDS')

        for _w in self.mainframe.winfo_children():
            _w.destroy()
        self.mainframe.columnconfigure(100,weight = 1)
        self.mainframe.columnconfigure(400,weight = 3)        

        Tk.Label(
            self.mainframe,
            text = 'ĐĂNG KÝ TÀI KHOẢN',
            font = ('Times News Romans', 20)
            ).grid(columnspan = 2,
            padx = 200)
        _acc = Tk.Label(
            self.mainframe,
            text = 'TÊN TÀI KHOẢN',
            font = ('Times News Romans', 15)
            ).grid(column = 0,
                   row = 1,
                   padx = 200)
        acc = Tk.Entry(
            self.mainframe,
            width = 50,
            font = ('Times News Romans', 15)
            )
        acc.grid(
            column = 1,
            row = 1,
            padx = 100
        )

        _pwd = Tk.Label(
            self.mainframe,
            text = 'MẬT KHẨU',
            font = ('Times News Romans', 15)
            ).grid(column = 0,
                   row = 2
                   )
        
        pwd = Tk.Entry(
            self.mainframe,
            width = 50,
            font = ('Times News Romans', 15),
            show = '*'
            )
        pwd.grid(
            column = 1,
            row = 2,
            padx = 100
            )    
        _pwd_entry = Tk.Label(
            self.mainframe,
            text = 'NHẬP LẠI MẬT KHẨU',
            font = ('Times News Romans', 15)
            ).grid(column = 0,
                   row = 3,
                   padx = 100)
        pwd_entry = Tk.Entry(
            self.mainframe,
            width = 50,
            font = ('Times News Romans', 15),
            show = '*'
            )
        pwd_entry.grid(
            column = 1,
            row = 3,
            )    

        finallization = Tk.Button(
            self.mainframe,
            text = 'ĐĂNG KÝ',
            font = ('Times News Romans', 25),
            command = check)
        finallization.grid(
            column = 0,
            row = 4,
            columnspan = 2,
            padx = 100
<<<<<<< HEAD:main.py
            )
       
if __name__ == '__main__':
    if os.path.isfile(f'{pathtoscript}/configure.json') == False:
        while True:
            serverd = filedialog.askdirectory(title="Chọn đường đẫn đến thư mục của server")
            if serverd == "":
                showerror("NO SERVER INTERFACE FOUND", "PROGRAM CANNOT RUN ALONE!!!")
            else:
                break
        with open(f'{pathtoscript}/configure.json','w') as confg:
            json.dump({"serverdir":f"{serverd}"},confg)
            confg.close()

        
    run = maingui()
    run.mainloop()
=======
            )
>>>>>>> f26dc6952aff21825ab515fa778cbcae71413677:TDGOmniInterface.py
