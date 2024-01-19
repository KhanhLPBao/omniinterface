from tkinter.ttk import Frame, Scrollbar
from tkinter import Canvas
class logpanel:
    def __init__(self,master,components,frame : tuple):
        self.item_height = 15
        self.master = master
        self.components = components
        self.components_num = len(self.components)
        self.panel_height = self.components_num * self.item_height
        self.height, self.width = frame
        # canvas 
        self.canvas = Canvas(
            self.master,
            background = 'white',
            scrollregion = (0,0,self.width,self.panel_height))
        self.canvas.pack(expand = True, fill = 'both')
        # display frame
        self.frame = Frame(self.master)
        # scrollbar 
        self.scrollbar = Scrollbar(self, orient = 'vertical', command = self.canvas.yview)
        self.canvas.configure(yscrollcommand = self.scrollbar.set)
        self.scrollbar.place(relx = 1, rely = 0, relheight = 1, anchor = 'ne')
        # events
        self.canvas.bind_all('<MouseWheel>', lambda event: self.canvas.yview_scroll(-int(event.delta / 60), "units"))
        self.bind('<Configure>', self.update_size)
    def update_size(self):
        if self.panel_height >= self.height:
            height = self.panel_height
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