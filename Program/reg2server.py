import random
import os
import socket
from time import sleep
from tkinter.messagebox import showerror, showinfo
class reg2server:
    def __init__(self, serverdir:str,confirm_bin):
        self.rd_elements = {
            'char':'abcdefghijklmnopqrstuvwxyz',
            'num':'0123456789',
        }          
        rdlog = ''.join(random.choice(self.rd_elements['num']) for _ in range(4))
        self.allstr = "".join([_a for _i,_a in self.rd_elements.items()])
        self.scriptpath = os.path.realpath(__file__).replace('\\main.py','')
        self.hostname = socket.gethostname()
        self.request_seq = random.choice(self.rd_elements['num'][1:]) +\
             ''.join(random.choice(self.rd_elements['num']) for _ in range(9))
        self.serverdir = serverdir
        if confirm_bin == 0:  
            try:
                requestconfirm = self.request_mamanger()
                if type(requestconfirm) is dict:
                    showerror(title = 'ERROR!', message = f'Encountered error:\n{requestconfirm}')
                    return 1
                else:
                    encodematrix = self.getmatrix(requestconfirm)
                    self.reg2serveroutput = {
                        'connection token': requestconfirm,
                        'encoded matrix': self.matrixblock,
                    } 
            except KeyboardInterrupt:
                return 1
        else:
            pass
    def connect(self):
        return self.reg2serveroutput
    def seq_generator(self):        
        pos_rd_num = [str(x) for x in range(10)]
        request_coord = []
        
        for i in range(10):
            request_coord.append([0,0])
        for i in range(10):
            _seq = self.request_seq[i]
            _pos = int(random.choice(''.join(pos_rd_num))) 
            pos_rd_num.remove(str(_pos))
            _c1 = request_coord[_pos]
            _c1[1] = _seq
            request_coord[_pos] = _c1
            _c2 = request_coord[i]
            _c2[0] = _pos
            request_coord[i] = _c2
        request_gr = {}
        request_str = []
        rdseq = "".join(random.choice(self.allstr) for _ in range(random.randint(5,10)))
        for pos, seq in request_coord:
            request_str.append(f'{pos}{seq}')
        return {
            'rdstring_title':rdseq,
            'sequence_block':"   ".join(request_str),
            "ignite_sequence": self.request_seq,
            'output': ''.join(random.choice(self.allstr) for _ in range(random.randint(15,300)))
        }
    def codeblock_request(self,blocktitle,titleseq,registryseq,inputseq,outputseq):
        titleline = titleseq
        registryline = ''.join(registryseq)
        inputline = '\n'.join(inputseq)
        outputline = outputseq
        requestblock = [
            '<title>',
            titleline,
            '</title>','<registry>',
            registryline,
            '</registry>','<input>',
            inputline,
            '</input>','<output>',
            outputline,
            '</output>',
            '<END>'
        ]
        try:
            with open(f'{self.serverdir}/interface_request/{self.hostname}_{blocktitle}.request','w') as request:
                request.write('\n'.join(requestblock))
            return 0
        except PermissionError:
            return 3
        except Exception as ex:
            showerror(title='ERROR',message='ERROR! THE FOLLOWING LOGS ARE RECORDED\n' + '-'*18 + '\n' + str(ex))  
            return 1
    def loginblock_request(self,blocktitle,titleseq,registryseq,inputseq,outputseq):
        titleline = titleseq
        registryline = registryseq
        inputline = inputseq
        outputline = outputseq
        requestblock = [
            '<title>',
            titleline,
            '</title>','<registry>',
            registryline,
            '</registry>','<input>',
            inputline,
            '</input>','<output>',
            outputline,
            '</output>',
            '<END>'
        ]
        try:
            with open(f'{self.serverdir}/interface_request/{self.hostname}_{blocktitle}.login','w') as request:
                request.write('\n'.join(requestblock))
            return 0
        except PermissionError:
            return 3
        except Exception as ex:
            showerror(title='ERROR',message='ERROR! THE FOLLOWING LOGS ARE RECORDED\n' + '-'*18 + '\n' + str(ex))  
            return 1
    def request_mamanger(self):
        def block_decode(responseblock:list):
            realblock = str(responseblock[0][:10])
            return realblock
        def response_check(filename):
            pendingcount = 1
            pendingcountmax = 60
            while os.path.isfile(f'{self.serverdir}/interface_request/{filename}.request') is True and pendingcount <= pendingcountmax:
                pendingcount += 1
                sleep(1)
            if pendingcount > pendingcountmax and os.path.isfile(f'{self.serverdir}/interface_request/{filename}.request'):
                resout = {'Pending timed out': False}
                return resout
            waitcount = 1
            wait_countmax = 30
            while os.path.isfile(f'{self.serverdir}/interface_response/{filename}.response') is False and waitcount <= wait_countmax:
                waitcount += 1
                sleep(1)
            if waitcount > wait_countmax and os.path.isfile(f'{self.serverdir}/interface_response/{filename}.response') is False:
                resout = {'Request timed out': False}
            else:   
                reswrite_waiting = 1
                reswrite_waitingmax = 15
                while reswrite_waiting <= reswrite_waitingmax:
                    with open(f'{self.serverdir}/interface_response/{filename}.response') as response:
                        response = [_r.rstrip() for _r in response.readlines()]
                        if response[-1] != '<END>':
                            sleep(1)
                            reswrite_waiting += 1
                        else:
                            break      
                if reswrite_waiting > reswrite_waitingmax:
                    resout = {'Response file invalid': False}
                else:
                    serverrestitle = response[response.index('<title>')+1:response.index('</title>')][0]
                    seq_decoded = block_decode(response[response.index('<registry>')+1:response.index('</registry>')])
                    resout = {
                            'seq length': int(f'{serverrestitle[0]}{serverrestitle[-1]}') == 10,
                            'seq returned': seq_decoded == initseq['ignite_sequence']
                        }
            return resout 

        initseq = self.seq_generator()
        request_send = self.codeblock_request(initseq['rdstring_title'],'Connecting',initseq['sequence_block'],[''],initseq['output'])
        match request_send:
            case 0:
                server_comm_title = f'{self.hostname}_{initseq["rdstring_title"]}'
                serverseq = response_check(server_comm_title)
                if False in [response_results for rescategory, response_results in serverseq.items()]:
                    request_send2 = self.codeblock_request(initseq['rdstring_title'],'Connecting',initseq['sequence_block'],[''],'1')
                    match request_send2:
                        case 0:
                            serverseq2 = response_check(server_comm_title)
                            if False in [response_results for rescategory, response_results in serverseq.items()]:
                                return 1
                            else:
                                request_send2 = self.codeblock_request(initseq['rdstring_title'],'Requesting',initseq['sequence_block'],[''],'0')
                                match request_send2:
                                    case 0:
                                        os.remove(server_comm_title + '.response')
                                        return initseq['rdstring_title']
                                    case other:
                                        return 1
                        case other:
                            return 1
                else:
                    os.remove(f'{self.serverdir}/interface_response/{server_comm_title}.response')
                    return initseq['rdstring_title']
            case other:
                return 1
    def getmatrix(self,requestblock):
        filename = f'{self.serverdir}/interface_response/{self.hostname}_{requestblock}'
        matrix_waiting = 1
        matrix_waitingmax = 60
        while os.path.isfile(f'{filename}.seq') is False and matrix_waiting <= matrix_waitingmax:
            matrix_waiting += 5
            sleep(5)
            
        waiting_results = [matrix_waiting > matrix_waitingmax, os.path.isfile(f'{filename}.seq')]
        if waiting_results[1] is False:
            showerror('ERROR! Server returned no certificate')
            return 1
        else:
            while True:
                with open(f'{filename}.certificate') as cert:
                    cert = [_z.rstrip() for _z in cert]
                if cert[-1] == '<END>':
                    break
                elif len(cert) == 0:
                    pass
            self.matrixblock = cert[cert.index('<output>')+1:cert.index('</output>')][0]
            return 0

