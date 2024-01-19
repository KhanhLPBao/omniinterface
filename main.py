###---IMPORT LIB---###
import os
import tkinter as Tk
from tkinter import ttk, Menu, filedialog, Frame, Label, Button
from tkinter.messagebox import showerror, showinfo
import random
import socket
import json
import importlib.util           # USE THIS TO IMPORT MODULES
# Import add-on
from Program.reg2server import reg2server
from Program.login import login
from Program.omniengine import matrix_assemble
scriptpath = os.path.dirname(os.path.realpath(__file__))
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
            Tk.Tk.__init__(self)
            screen_width = self.winfo_screenwidth()
            screen_height = self.winfo_screenheight()
            self.geometry(f'1280x800')
            #self.attributes('-fullscreen',True)    
            _titleframe = Tk.Frame(self,
                                height=15,
                                highlightthickness=2,
                                highlightbackground='black')
            _titleframe.pack(fill='both')
            Tk.Label(
                _titleframe,
                text = 'TDG OMNI INTERFACE',
                font = ('Times News Romans',35)
                ).pack()
        login = self.login()
    def login(self):
        _loginframe = Frame(self,
                            height= 45,
                            highlightthickness=2,
                            highlightbackground='white'
                            )
        _loginframe.pack()
        loginframe = login(_loginframe,self.matrix,self.commblock[0],self.serverdir)
        self.mainloop()
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

if __name__ == '__main__':
    from threading import Thread
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

    