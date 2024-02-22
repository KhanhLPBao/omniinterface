"""
menubar format at json:
{
    Level 1:{
              Level 2: Program (lvl 3):scriptname|Program (lvl 3):scriptname|Program (lvl 3):scriptname
              OR
              Level : scriptname
                            
                        }
}
"""
import tkinter as Tk
import importlib
class menubar:
    def __init__(self,menuframe,scriptdir,serverdir,token,matrix,init):  ##Initiation
        from os.path import isfile
        from os import remove
        import socket
        from tkinter import Menu
        ## < Import value > ##
        self.Menu = Menu
        self.hostname = socket.gethostname()

        self.matrix = matrix
        self.token = token
        self.scriptdir = scriptdir
        self.serverdir = serverdir

        self.menufile = f'{scriptdir}/config/menu'
        self.fontmenu = ("Times News Romans",13)
        self.menu_lvl1 = {}
        self.menu_lvl2 = {}
        self.menu_lvl3 = {}
        
        self.menubar = self.Menu(menuframe)
        #menuframe.config(menu=self.menubar)
        self.menu_init(init)
    def menu_init(self,state):
        from os.path import isfile
        if state:
            if isfile(self.menufile):
                print('mainframework.menubar - Importing config')
                menu_bin = self.menuconfig(self.hostname,'import')
                if menu_bin == 0:
                    self.construct(self.menuimport)
                else:
                    self.menuconfig(self.hostname,'request running program')
            else:
                print('mainframework.menubar - Config not found, requesting...')
                self.menuconfig(self.hostname,'request running program')
        ## < Menu construct engine > ##
    def rootmenu(self,name):
        print('Begin construction of lvl1 menu',name)
        menutask = self.rootlvl1.add_cascade(
            label = name,
            menu = self.menubar,
            font = self.fontmenu
        )
        return menutask
    def branchmenu(self,menu,name,menutype,root,extra):
        print('Begin the construction of menu',name,'on',menu)
        match menutype:
            case "self":
                sectiontask = menu.add_command(
                    label = name,
                    font = self.fontmenu,
                    command = extra,
                    state = 'disabled'
                )
                return sectiontask
            case "cascade":
                sectiontask = menu.add_command(
                    label = section,
                    menu = root,
                    font = self.fontmenu
                )
                return sectiontask
        
    def construct(self,menu_data):
        import json
        self.rootlvl1 = self.Menu(self.menubar)
        for rootname, rootcontent in menu_data.items():   #lvl 1 MENU
            self.menu_lvl1[rootname] = self.rootmenu(rootname)
            self.rootlvl2 = self.Menu(self.rootlvl1)
            for branchname, branchcontent in rootcontent.items():
                for branchtype, extraconfig in [b_.split(':') for b_ in branchcontent.split('|')]:
                    self.menu_lvl2[f'{rootname}.{branchname}'] = self.branchmenu(
                        self.rootlvl2,
                        branchname,
                        branchtype,
                        self.menu_lvl1[rootname],
                        extraconfig
                        )
                    if branchtype == 'cascade':
                        self.branch = Menu(
                            self.menu_lvl2[f'{rootname}.{branchname}'],
                            tearoff = 0
                        )
                        for infolvl3 in extraconfig.split("|"):
                            sub_branchname, sub_branchprog = infolvl3.split(':')
                            self.menu_lvl3[f'{rootname}.{branchname}.{sub_branchname}'] = self.branchmenu(
                                self.branch,
                                sub_branchname,
                                'cascade',
                                self.menu_lvl2[f'{rootname}.{branchname}'],
                                sub_branchprog
                                )
        ## < Menu configuration > ##
    def menuconfig(self,hostname,requesttype,extra = None):
        import os
        import json
        try:
            from Program.omniengine import encode, decode, sendrequest, block_analysis
        except:
            
            spec = importlib.util.spec_from_file_location("module.name","K:\\source\\omniinterface\\Program\\omniengine.py")
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            encode = module.encode
            decode = module.decode
            sendrequest = module.sendrequest
            block_analysis = module.block_analysis
        hostname = hostname  
        def request_management(blocktitle,regval,inpval,outval,**kwargs):
            rqs = sendrequest(self.serverdir,hostname,self.token,blocktitle,regval,inpval,outval)
            repeat = False
            response = []
            nowait_value = ''
            nowait_bool = kwargs['nowait']
            try:
                if nowait_bool:
                    nowait_value = '--nowait'
            except:
                nowait_value = ''
            print(rqs)
            while rqs != 0:
                if repeat:
                    return 'error_2'    #Error 2: No response file found
                    break
                else:
                    repeat = True
                    rqs = sendrequest(self.serverdir,hostname,self.token,blocktitle,regval,inpval,outval,nowait_value)            
            return 0
        def checkvalue(importvalue):
            v = importvalue
            valuetype = type(v)
            while valuetype is list:
                v = v[0]
                valuetype = type(v)
            return v
            # Scan for types
        match requesttype:
            case 'import':
                if os.path.isfile(self.menufile):
                    self.menuimport = json.load(
                        open(self.menufile)
                        )
                    return 0
                else:
                    return 1
            case 'create':
                with open(self.menufile,'w') as menu:
                    menu.close()
                return 0
            case 'export':
                with open(self.menufile,'w') as menu:
                    menu.write(extra)
                return 0
            case 'request user permission':
                # Request for user's permission to unlock certain functions, and also including functions imported from server
                
                accname = open(f'{self.scriptdir}\\cache\\__session{self.t}').read()
                r = request_management('Permission request',accname,self.token,'')
                if r == 0:
                    resaccname = checkvalue(block_analysis(f'{self.serverdir}/interface_response/{hostname}_{self.token}.response')[-2])
                    if resaccname == decode(accname,self.matrix):
                        response = checkvalue(block_analysis(f'{self.serverdir}/interface_response/{hostname}_{self.token}.response')[-1])
                        return response
                    else:
                        return 'error_1'    #Error 1: Account's name not matched
                else:
                    return r
            case 'request running program':
                # Request for user's permission to unlock certain functions, and also including functions imported from server
                # Extra = [prog1]|[prog2]|...
                # prog is program's name, including root and branch name if neccessary
                import os
                import shutil
                print('mainframework.menubar.menuconfig.checkvalue - Sending request')
                r = request_management('Menu_request',hostname,extra,'',nowait=True)
                if r == 0:
                    count_ = 0
                    maxcount = 30
                    found = False
                    fileresponse = f'{self.serverdir}/interface_response/{hostname}_{self.token}.response'
                    while count_ <= maxcount:
                        if os.path.isfile(fileresponse):
                            found = True
                            break
                        else:
                            print('mainframework.menubar.menuconfig.checkvalue - waiting...',count_ + 1,'/',maxcount,end='\r')
                            count_ += 1
                    if found:
                        print('mainframework.menubar.menuconfig.checkvalue - found response!')
                        shutil.move(fileresponse,f'{self.scriptdir}/config/menu')
                        return 0
                    else:
                        print('mainframework.menubar.menuconfig.checkvalue - Timed out!')
                        return 2
                else:
                    return 1
                del encode, decode, sendrequest, block_analysis
            case 'adjust':
                # Configuration: [configname1]:[val changed to]|[configname2]:[val changed to]
                import json
                source = json.load(open(self.menufile))
                response = ''
                for conf in extra.split('|'):
                    b = source
                    val, adj = conf.split(':')
                    val_lvl = val.split('.')
                    end = False
                    for v in val_lvl:
                        if val in b[v]:
                            end = True
                            source[v][val] = adj
                            break
                    if end:
                        response += f'{val}_done|'
                    else:
                        response += f'{val}_error|'
                        b = source[v]
                with open(self.menufile,'w') as menuconfigexport:
                    json.dump(source,menuconfigexport)
                return response
    def setmenupermission(self):
        from os.path import isfile
        from Program.omniengine import decode,encode
        status = {
            0:'disabled',
            1:'active'
            }
        filesession = f'cache/__session{self.token}'
        if isfile(filesession):
            with open(filesession) as s:
                id = s.read()
            permission = self.menuconfig(self.hostname,'request user permission')
            if 'error' not in permission:
                permission_decoded = decode(permission, self.matrix).split(',')
                for codename in permission_decoded:
                    conf = codename.split(':')
                    elements = conf[0].split('.')
                    level = len(elements)
                    match level:
                        case 1:
                            self.menu_lvl1[conf[0]].entryconfig(codename, state = status[conf[1]])
                        case 2:
                            self.menu_lvl2[conf[0]].entryconfig(elements[-1], state = status[conf[1]])
                        case 3:
                            self.menu_lvl2[conf[0]].entryconfig(elements[-1], state = status[conf[1]])
        else:
            return 1

if __name__ == '__main__':
    import tkinter as Tk
    import json

    with open("K:\\source\\omniinterface\\Program\\matrix.json") as debugmatrix:
        debugmatrix = json.load(debugmatrix)
    root = Tk.Tk()
    
    menubar(
        root,
        "K:\\source\\omniinterface",
        "K:\\source\\debug",
        'test',
        debugmatrix,
        True
    )