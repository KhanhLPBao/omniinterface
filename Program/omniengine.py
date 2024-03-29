def matrix_assemble(matrixblock:list):
    ran_elements = {
        'source_str_lower':'abcdefghijklmnopqrstuvwxyz',
        'source_str_UPPER':'ABCDEFGHIJKLMNOPQRSTUVWXYZ',
        'source_str_number':'0123456789',
        'source_str_symbol':'-*~:+^.[]<>?=#',
        'source_endline': '|',
        'source_space':' '
    }  
    allrdchar = ''.join(itemchar for chargroup, itemchar in ran_elements.items())
    ran_source = ('').join([_a for __a,_a in ran_elements.items()])
    matrix_combination = [
        f'{_d}{_e}' for (_n,_b) in ran_elements.items() \
            for (_n,_c) in ran_elements.items() \
            for _d in _b for _e in _c
    ]
    assembled = {}
    for comidx, comb in enumerate(matrix_combination):
        assembled[comb] = matrixblock[comidx]
    return assembled
def encode(matrix:dict,strin):
    stroutput = []
    strinput = ''.join(r + '|' for r in strin.split('\n'))
    
    i = 0
    while i != len(strinput) - 1:
        try:
            strexport = matrix[f'{strinput[i]}{strinput[i+1]}']
        except:
            strexport = '##ERROR##'#        finally:
        stroutput.append(strexport)
        i += 1
    return ''.join(stroutput)
def decode(encodedstr:str,matrix:dict):
    out = encodedstr
    ##<< Decryp encoded str >>##
    alphabet = {e:o for o,e in matrix.items()}
    out_block = [out[i:i+4] for i in range(0, len(out),4)]
    str_decoded = [alphabet[block] for block in out_block]
    ##<< Begin to match decypted str >>##
    output = ''
    for blockpos, decode_block in enumerate(str_decoded):
        if blockpos == 0:
            output += decode_block[0]
        elif blockpos == len(str_decoded) - 1:
            break
        if decode_block[1] == str_decoded[blockpos+1][0]:
            output += decode_block[1]
        else:
            output += '<DECODE ERROR>'
    output = output.replace('|','\n')
    return output
def block_analysis(commfile):
    with open(commfile) as _req:
        req = [_a.rstrip() for _a in _req.readlines()]
    req_index = {
        'title': req.index('<title>'),
        '/title': req.index('</title>'),
        'registry': req.index('<registry>'),
        '/registry': req.index('</registry>'),
        'input': req.index('<input>'),
        '/input': req.index('</input>'),
        'output': req.index('<output>'),
        '/output': req.index('</output>')
    }
    title = str(req[req_index['title'] + 1])
    reg = req[req_index['registry']+1:req_index['/registry']]
    inp = req[req_index['input']+1:req_index['/input']]
    out = str(req[req_index['output']+1:req_index['/output']])
    return [title,reg,inp,out]
def debug(mod,exportstr,exporttype=None):
    from datetime import datetime
    from tkinter import filedialog
    from tkinter.messagebox import showerror,showinfo
    now = datetime.now()
    strexport = f'At {now}\tModule {mod} exported contents:\n{"="*12}\n<BEGIN REPORT>\nexportstr\n<END REPORT>\n{"="*12}'
    match exporttype:
        case 'file':
            filesave = filedialog.asksaveasfilename(
                title = "Select location to save log files",
                filetypes = (('LOG',"*.log*"))
                )
            try:
                if os.path.isfile(filesave):
                    with open(filesave,'a') as logfile:
                        logfile.write(f'\n{strexport}')
                else:
                    with open(filesave,'w') as logfile:
                        logfile.write(f'\n{strexport}')     
            except PermissionError:
                showerror(title = 'ERROR!', message = 'Permission denied, automatically output to terminal instead')    
                print(strexport)
        case 'panel':
            showinfo(title = 'Debug message',message=strexport)
        case None:
            print(strexport)