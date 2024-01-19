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
from Program.reg2server import reg2server
from Program.login import login
from Program.omniengine import matrix_assemble
from threading import Thread
scriptpath = os.path.dirname(os.path.realpath(__file__))
ultilityframe_height = 250
reduce_factor = 0.9
class startup(Tk.Tk):
    def __init__(self):
        Tk.Tk.__init__(self)
        self.geometry(f'400x200')  
        with open(f'{scriptpath}/completed.txt','w') as startup_status:
            startup_status.write('0')
        connectlabel = Label(self.master, 
        text = 'CONNECTING TO SERVER...',
        font = ('Times News Romans',20))
        connectlabel.pack()
        self.startup_clear()
    def startup_clear(self):
        with open(f'{scriptpath}/completed.txt') as startup_status:
            startup_status_bin = int(startup_status.read())
            if startup_status_bin == 1:
                self.destroy()
        self.after(1000,self.startup_clear)
        self.mainloop()
class main(Tk.Tk):
    def __init__(self):   
        connected = self.connection()      
        if connected == 0:
            self.token = self.commblock[0]
            self.exportlc(f'Successfully established connection to host with token {self.token}','log')
            self.exportlc('','cache')
            Tk.Tk.__init__(self)
            screen_width = int(self.winfo_screenwidth()*reduce_factor)
            screen_height = int(self.winfo_screenheight()*reduce_factor)
            self.w = screen_width
            self.h = screen_height
            self.geometry(f'{screen_width}x{screen_height}')
            #self.attributes('-fullscreen',True)    
            _titleframe = Frame(self,
                                height=15,
                                highlightthickness=2,
                                highlightbackground='black')
            _titleframe.pack(fill='both')
            Tk.Label(
                _titleframe,
                text = 'TDG OMNI INTERFACE',
                font = ('Times News Romans',35)
                ).pack()
            self.mainframe = Frame(
                self,
                height = screen_height-15-ultilityframe_height,
                highlightthickness=2,
                highlightbackground='blue'
            )
            self.mainframe.pack_propagate(False)
            self.mainframe.pack(fill='both')
            ultilityframe = Frame(
                self,
                height = ultilityframe_height,
                highlightthickness=2,
                highlightbackground='yellow'
            )
            ultilityframe.pack_propagate(False)
            ultilityframe.pack(fill='both')
            self.logframe = Frame(
                ultilityframe,
                height = ultilityframe_height-2,
                width = int(self.w*0.8),
                highlightthickness=4,
                highlightbackground='red'
            )
            self.logframe.pack_propagate(False)
            self.logframe.pack(side='left')
            self.functionalframe = Frame(
                ultilityframe,
                height = ultilityframe_height-2,
                width = int(self.w*0.2),
                highlightthickness=4,
                highlightbackground='green'
            )
            self.functionalframe.pack_propagate(False)
            self.functionalframe.pack(side='left')
            
            self.login()
            self.logpanel()
            self.mainloop()
    def exportlc(self,content,filetype):
        with open(f'{scriptpath}/{filetype}/{self.token}','w') as o:
            o.write(content)
    def importlc(self,token,filetype):
        filerequested = f'{scriptpath}/{filetype}/{token}'
        if os.path.isfile(filerequested):
            with open(filerequested) as _o:
                o = _o.read()
                return o
        else:
            return False
    def login(self):
        _loginframe = Frame(self.mainframe,
                            height= 45,
                            highlightthickness=2,
                            highlightbackground='white'
                            )
        _loginframe.pack()
        loginframe = login(_loginframe,self.matrix,self.commblock[0],self.serverdir)
        #self.mainloop()
    
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
            print('Init success!')
            with open(f'{scriptpath}/completed.txt','w') as startup_status:
                startup_status.write('1')
            with open(f'{scriptpath}/token.txt','w') as token:
                token.write(self.commblock[0])
            return 0
        else:
            showerror(title='SERVER NOT RESPONSE', message='ERROR! Received no responses from server, please check category serverlink or increased response time')
            exit(1)
    def logpanel(self):
        logfont = ('Arial','15')
        previous = self.importlc(self.token,'cache')

        n = update()
        logpanel = Canvas(
            self.logframe,
            background = 'white',
            scrollregion = (0,0,self.w,self.h)
            )
        if type(n) is str:
            Label(logpanel,text = n,background = 'white', font = logfont).pack(side='top', anchor='nw')
        logpanel.pack(expand = True, fill = 'both')
        logpanel.after(2000,update)
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

    