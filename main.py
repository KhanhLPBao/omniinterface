###---IMPORT LIB---###
import os
import tkinter as Tk
from tkinter import ttk, Menu, filedialog, Frame, Label, Button, Canvas
from tkinter.messagebox import showerror, showinfo
import random
import socket
import json
import importlib.util           # USE THIS TO IMPORT MODULES
# Import add-on
from Program import mainframework
from Program.reg2server import reg2server
from Program.login import login
from Program.omniengine import matrix_assemble, exportlc, importlc, encode, decode,sendrequest
from Program import mainframework,logpanel
from threading import Thread
scriptpath = os.path.dirname(os.path.realpath(__file__))
ultilityframe_height = 250
reduce_factor = 0.9

logpanel = logpanel.logpanel
#menubar = mainframework.menubar
class startup(Tk.Tk):
    def __init__(initboard):
        Tk.Tk.__init__(initboard)
        initboard.geometry(f'400x200')  
        try:
            os.remove(f'{scriptpath}/completed.txt')
        except:
            pass
        with open(f'{scriptpath}/completed.txt','w') as startup_status:
            startup_status.write('0')
        connectlabel = Label(initboard.master, 
        text = 'CONNECTING TO SERVER...',
        font = ('Times News Romans',20))
        connectlabel.pack()
        initboard.startup_clear()
    def startup_clear(initboard):
        with open(f'{scriptpath}/completed.txt') as startup_status:
            startup_status_bin = startup_status.read()
            if startup_status_bin == '1':
                initboard.destroy()
        initboard.after(1000,initboard.startup_clear)
        initboard.mainloop()
class main(Tk.Tk):
    def __init__(self):   
        connected = self.connection()   
        print('main - connected =',connected)   
        if connected == 0:
            print('main - Begin frame construction') 
            self.logsectioncleared = True
            self.token = self.commblock[0]
            exportlc(scriptpath,self.token,f'Successfully established connection to host with token {self.token}','log')
            exportlc(scriptpath,self.token,'','cache')
            Tk.Tk.__init__(self)
            self.screen_width = int(self.winfo_screenwidth()*reduce_factor)
            self.screen_height = int(self.winfo_screenheight()*reduce_factor)
            self.w = self.screen_width
            self.h = self.screen_height
            self.geometry(f'{self.screen_width}x{self.screen_height}')
            self._titleframe, self.mainframe, self.ultilityframe, self.functionalframe, self.logframe = self.frameconstruct()
            self.title_init()
            self.menuinit()
            self.login()
            self.mainloop()
    def frameconstruct(self):
        #self.attributes('-fullscreen',True)    
        _titleframe = Frame(self,
                            height=15,
                            highlightthickness=2,
                            highlightbackground='black')
        _titleframe.pack(fill='both')
        mainframe = Frame(
            self,
            height = self.screen_height-15-ultilityframe_height,
            highlightthickness=2
        )
        mainframe.pack_propagate(False)
        mainframe.pack(fill='both')
        ultilityframe = Frame(
            self,
            height = ultilityframe_height,
            highlightthickness=2,
            highlightbackground='black'
        )
        ultilityframe.pack_propagate(False)
        ultilityframe.pack(fill='both')
        functionalframe = Frame(
            ultilityframe,
            height = ultilityframe_height,
            width = int(self.w*0.2),
            highlightthickness=1,
            highlightbackground='black'
        )
        functionalframe.pack_propagate(False)
        functionalframe.pack(side='left')

        logframe = Frame(
            ultilityframe,
            height = ultilityframe_height,
            width = int(self.w*0.8),
            highlightthickness=1
        )
        logframe.pack_propagate(False)
        logframe.pack(side='left')

        return [_titleframe,
            mainframe,
            ultilityframe,
            functionalframe,
            logframe]

    def title_init(self):
        Tk.Label(
            self._titleframe,
            text = 'TDG OMNI INTERFACE',
            font = ('Times News Romans',35)
            ).pack()

    def account_import(self):
        if os.path.isfile(f'{scriptpath}/cache/__session{self.token}'):
            self.accountname = decode(open(f'{scriptpath}/cache/__session{self.token}'),self.matrix)
            if '<DECODE ERROR>' in self.accountname:
                showerror(title = 'SOMETHING IS WRONG', message = 'ERROR! NO INFORMATION ABOUT LOGIN SESSION FOUND, PLEASE RESTARTED THE PROGRAM')
                quit()
    def login(self):
        _loginframe = Frame(self.mainframe,
                            height= 45,
                            highlightthickness=2,
                            highlightbackground='white'
                            )
        _loginframe.pack()
        login(_loginframe,self.matrix,self.commblock[0],self.serverdir,scriptpath)         

    def quit(self):
        self.destroy()            
    def connection(self):
        import shutil
        with open(f'{scriptpath}/configure.json') as _temp_file:
            serverconfig = json.load(_temp_file)
        self.serverdir = serverconfig['serverdir']
        self.reg2serverinfo = reg2server(self.serverdir,0).connect()
        if type(self.reg2serverinfo) is dict:     #Request success!
            self.commblock = [self.reg2serverinfo['connection token'],self.reg2serverinfo['encoded matrix'].split('\t')]   
            self.matrix = matrix_assemble(self.commblock[1])
            with open(f'{scriptpath}/completed.txt','w') as startup_status:
                startup_status.write('1')
            with open(f'{scriptpath}/token.txt','w') as token:
                token.write(self.commblock[0])
            return 0
        else:
            showerror(title='SERVER NOT RESPONSE', message='ERROR! Received no responses from server, please check category serverlink or increased response time')
            exit(1)
    def logarea(self):
        previous = importlc(scriptpath,self.token,'cache')
        def update():
            now = importlc(scriptpath,self.token,'log')
            if now.split('\n')[-1] == previous.split('\n')[-1]:
                return '0'
            else:
                exportlc(scriptpath,self.token,previous + now,'cache')
                return now.split('\n')
        n = update()
        if type(n) is list:
            if self.logsectioncleared is True:
                pass
            else:
                self.logframe.destroy()
                self.logframe = self.logframecreated()
                self.logframe.pack_propagate(False)
                self.logframe.pack(side='left', expand = True)
            self.logsectioncleared = False    
            self.logsection = logpanel(self.logframe,n,(ultilityframe_height,int(self.w*0.8)),self.token, scriptpath)
        self.after(1000,self.logarea)

    def menuinit(self):
        menuframe = Menu(self)
        self.menu = mainframework.menubar.menubar(menuframe, scriptpath, self.serverdir, self.token, self.matrix, True)
        self['menu'] = menuframe  



if __name__ == '__main__':
    if os.path.isfile(f'{scriptpath}/configure.json') == False:
        while True:
            serverconfig = filedialog.askdirectory(title="Chọn đường đẫn đến thư mục của server")
            if serverconfig == "":
                showerror("NO SERVER INTERFACE FOUND", "PROGRAM CANNOT RUN ALONE!!!")
                exit(1)
            else:
                with open(f'{scriptpath}/configure.json','w') as confg:
                    json.dump({"serverdir":f"{serverconfig}"},confg)
                    confg.close()
                break
    s = Thread(target=startup).start()
    Thread(target=main).start()

    