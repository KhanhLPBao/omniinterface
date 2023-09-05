import os
import sys
pathtoscript = os.path.dirname(__file__)
sys.path.append(f'{pathtoscript}/dependencies/')
from distutils.core import setup
import dependencies.py2exe

setup(
    name = 'TDG Omni Interface',
    windows = [
        {
            'script':f'{pathtoscript}/TDGOmniInterface.py'
        }
    ],
    options = {
        'py2exe':{
            'packages':['tkinter','os','time','sys','json','inspect'],
            'bundle_files':1,
            'compressed': False
        }
    },
    zipfile = None,
    console = [
        {
            'script':f'{pathtoscript}/TDGOmniInterface.py',
            }
            ]
)
