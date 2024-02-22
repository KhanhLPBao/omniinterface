from tkinter import ttk,Frame,Button,Label,Entry
from tkinter.messagebox import showerror, showinfo
import os
import socket
from Program.reg2server import reg2server
from Program.omniengine import debug,block_analysis,encode,decode,matrix_assemble, exportlc
from time import sleep
hostname = socket.gethostname()
class login:
    def __init__(self, section, matrix, logintoken,serverdir,scriptpath):
        self.master = section
        self.token = logintoken
        self.matrix = matrix
        self.serverdir = serverdir
        self.scriptpath = scriptpath
        loginframe = Frame(self.master,
                            height=60,
                            width=120)
        loginframe.pack()
        loginframe.columnconfigure(0,weight = 50)
        loginframe.columnconfigure(1,weight = 10)
        loginframe.columnconfigure(2,weight = 10)
        loginframe.columnconfigure(3,weight = 50)
        Label(loginframe,text = 'LOGIN').grid(row = 0, column = 0, columnspan = 3)
        _ID = Label(loginframe,
                    text = 'ID').grid(row = 1, column = 0)
        _passwd = Label(loginframe,
                    text = 'Password').grid(row = 2, column = 0)
        self.ID = Entry(loginframe, 
                    width = 35,
                    font=('Times News Romans',15))
        self.ID.grid(row = 1, column = 1, columnspan = 2)
        self.passwd = Entry(loginframe,
                        width=35,
                        font = ('Times News Romans', 15),
                        show='*'
                        )
        self.passwd.grid(row = 2, column = 1, columnspan = 2)
        self.loginbutton = Button(loginframe, text = 'LOGIN',command = self.login)
        self.loginbutton.grid(row = 3, column = 1)
        self.exitbutton = Button(loginframe, text = 'EXIT',command = self.exit)
        self.exitbutton.grid(row = 3, column = 2)
    def exit(self):
        #exit(1)
        #self.master.destroy()
        quit()
    def login(self):
        id = encode(self.matrix,self.ID.get())
        pwd = encode(self.matrix,self.passwd.get())  
        reg2server(self.serverdir,1).loginblock_request(
            self.token,
            'LOGIN',
            id,
            pwd,
            ''
        )
        self.frameswitch('disable')
        log = self.login_manager()
        if str(log) == "['0']": #Login complete
            showinfo(title = 'LOGIN COMPLETE',message = 'LOGIN COMPLETED! WELCOMETO TDG OMNI INTERFACE')
            self.master.destroy()
            exportlc(self.scriptpath, self.token,'Login completed','log')
            with open(f'{self.scriptpath}/cache/__session{self.token}','w') as cache:
                cache.write(id)
            with open(f'{self.scriptpath}/cache/{self.token}_logged','w') as logged:
                logged.write('1')
            return 0
        elif str(log) == '1':
            showerror(title = 'SOME SHARK INSIDE THE NETWORK!', message = 'ERROR! CANNOT CONNECTED TO SERVER')
            self.frameswitch('normal')
            exportlc(self.scriptpath, self.token,'No responses from server','lol')
            return 1
        else:
            showerror(title = 'SERVER SAYS NO!', message = f'SERVER RETURNED ERROR: {str(log)}')
            self.frameswitch('normal')
            exportlc(self.scriptpath, self.token,'Encountered error: Login Mismatch','lol')
            return 1
    def login_manager(self):
        fileresponse = f'{self.serverdir}\\interface_response\\{hostname}_{self.token}.response'
        count = 0
        countmax = 15
        found = 0
        while found == 0 and count <= countmax:
            count += 1
            if os.path.isfile(fileresponse):
                c = 0
                while c == 0:
                    with open(fileresponse) as _r:
                        r = _r.read()
                    if '<END>' in r:
                        c = 1
                        responseblock = block_analysis(fileresponse)
                        if responseblock[0] == 'login response':
                            accepted = responseblock[-1]
                            fount = 1
                            os.remove(fileresponse)
                            return accepted
            sleep(1)
        if found == 0:
            return 1
    def frameswitch(self,status):
        self.ID.config(state = status)
        self.passwd.config(state = status)
        self.loginbutton.config(state = status)