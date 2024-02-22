import tkinter as Tk
from tkinter.ttk import Frame, Scrollbar, Label, Style
from tkinter import Canvas
class logpanel:
    def __init__(self,master,components,frame : tuple,token,scriptpath):
        self.s = Style()
        self.s.configure('My.TFrame', background='red')
        self.logfont = ('Arial','15')
        self.item_height = 50
        self.master = master
        self.components = components
        self.components_num = len(self.components)
        self.token = token
        self.scriptpath = scriptpath
        self.panel_height = self.components_num * self.item_height
        self.height, self.width = frame
        self.logsection = None
        # canvas 
        self.canvas = Canvas(
            self.master,
            background = 'white',
            scrollregion = (0,0,self.width,self.panel_height))
        self.canvas.pack(expand = True, fill = 'both', side = 'top')
        # display frame
        self.frame = Frame(
            self.master,
            )
        for item in self.components:
            self.create_item(item).pack(
                expand = True,
                fill = 'both')
        # scrollbar 
        self.scrollbar = Scrollbar(self.master, orient = 'vertical', command = self.canvas.yview)
        self.scrollbar.place(relx = 1, rely = 0, relheight = 1, anchor = 'ne')

        # events
        self.canvas.bind_all('<MouseWheel>', lambda event: self.canvas.yview_scroll(-int(event.delta / 60), "units"))
        self.master.bind('<Configure>', self.update_size)
    def update_size(self,event):
        if self.panel_height >= self.height:
            height = self.panel_height
            print('Exceed',self.height,self.panel_height)
            self.canvas.bind_all('<MouseWheel>', lambda event: self.canvas.yview_scroll(-int(event.delta / 60), "units"))
            self.scrollbar.place(relx = 1, rely = 0, relheight = 1, anchor = 'ne')

        else:
            height = self.height
            self.canvas.unbind_all('<MouseWheel>')
            self.scrollbar.place_forget()
        self.canvas.create_window(
            (0,0), 
            window = self.frame, 
            anchor = 'nw', 
            width = self.width, 
            height = height
        )
    def create_item(self,item):
        frame = Frame(
            self.frame,
            style = 'My.TFrame',
            height = self.item_height
        )
        Label(frame, text = item, font = self.logfont).pack(
            side='top',
            anchor='nw')
        return frame