# Barnacle imagery project gui file
# File created: 7/12/2022
# Author: Chet Russell
# Last edited: 7/25/2022 - Chet Russell

from tkinter import W
import PySimpleGUI as sg
from main import masker
from main import orthorec
from main import seg
from main import calculate_gsd

sg.theme('Default')

layout = [
    # Initial Folders
    [
        sg.Text("Image Folder:", font=("Helvetica", 15)),
        sg.FolderBrowse(key='imgdir')
    ],
    [
        sg.Text("Results Folder:", font=("Helvetica", 15)),
        sg.FolderBrowse(key='dwndir')
    ],
    [sg.Text('')],
    
    # Orthorectification options
    [sg.Text("Orthorectification", font=("Helvetica", 20), key='ort')],
    [   
        sg.Text("Pixel Buffer (for glint masking):"),
        sg.Combo([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10],default_value=5,key='pb')
    ],
    [   
        sg.Text("Quality:"),
        sg.Combo(['ultra', 'high', 'medium', 'low', 'lowest'],default_value='high',key='q')
    ],
    [
        sg.Text("Crop:"),
        sg.Combo([0, 1, 2, 3, 4, 5],default_value=0,key='crop'),
        #sg.Text("This setting has the tendency to crop out water areas, use with caution.")
    ],
    [
        sg.Text("Generate KMZ (Google Earth) render:"),
        sg.Combo([True, False],default_value='False',key='kmz')
    ],
    [
        sg.Text("Feature-type algorithm:"),
        sg.Combo(['sift', 'akaze', 'hahog', 'orb'],default_value='sift',key='ft'),
    ],

    # WORK IN PROGRESS
    #[
    #    sg.Text("Use EXIF:"),
    #    sg.Combo([True, False],default_value=True,key='exif')
    #],

    [sg.Button("Run Orthorectification Independently"), sg.Text("This will take a while. Be patient.")],
    [sg.Text('')],

    # Kelpomatic options
    [sg.Text("Kelp Identification (Kelpomatic)", font=("Helvetica", 20), key='ki')],
    [
        sg.Text("Orthomosaic File:"),
        sg.FileBrowse(key='orthfile')
    ],
    [
        sg.Text("Results Folder:"),
        sg.FolderBrowse(key='resdir')
    ], 
    [sg.Text('GSD:'), sg.InputText(size=(5, 1), key='gsd')], 

    # WORK IN PROGRESS
    #[
    #    sg.Text("Species classification:"),
    #    sg.Combo([True, False],default_value='False',key='spec')
    #],

    [sg.Button("Run Identification Independently")],
    [sg.Button("Run All", font=("Helvetica", 20))]
]

window = sg.Window('Kelpy', layout,size=(700, 700))
ort = window['ort']
ki = window['ki']

while True:  # Event Loop
    event, values = window.read()
    print(event, values)
    if event == sg.WIN_CLOSED:
        break

    # Running the glint mask generator and the ODM orthomosaic generator
    if event == 'Run Orthorectification Independently':
        if values['imgdir'] == '':
            sg.popup('ERROR: No image folder selected.', title='ERROR')
        else:
            if values['dwndir'] == '':
                sg.popup('ERROR: No results folder selected.', title='ERROR')
            else:
                masker(values['imgdir'], values['pb'])
                orthorec(values['imgdir'], values['dwndir'], values['q'], values['crop'], values['kmz'], values['ft'], False)
                ort.update('Orthorectification: DONE')

    # Running Kelpomatic
    if event == 'Run Identification Independently':
        if values['orthfile'] == '':
            sg.popup('ERROR: No orthomosaic file selected.', title='ERROR')
        else: 
            if values['resdir'] == '':
                sg.popup('ERROR: No results folder selected.', title='ERROR')
            else:
                if values['gsd'] == '':
                    sg.popup('ERROR: GSD value empty.', title='ERROR')
                else:
                    try:
                        value = float(values['gsd'])
                        ki.update('Identification (Kelpomatic): DONE')
                        sg.popup(seg(values['orthfile'], values['resdir'], value, False), title='results')

                    except:
                        sg.popup('ERROR: GSD not an integer value.')

    # Running together
    if event == 'Run All':
        if values['imgdir'] == '':
            sg.popup('ERROR: No image folder selected.', title='ERROR')
        else:
            if values['dwndir'] == '':
                sg.popup('ERROR: No results folder selected.', title='ERROR')
            else:
                try:
                    masker(values['imgdir'], values['pb'])
                    orthorec(values['imgdir'], values['dwndir'], values['q'], values['crop'], values['kmz'], values['ft'], False)
                    value = float(calculate_gsd(values['dwndir'] + '/report.pdf'))
                    sg.popup(seg(values['dwndir'] + '/odm_orthophoto.tif', values['dwndir'], value, False), title='results')

                except:
                    sg.popup('ERROR: Problem processing request.')
                
window.close()