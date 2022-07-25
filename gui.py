# Barnacle imagery project gui file
# File created: 7/12/2022
# Author: Chet Russell
# Last edited: 7/25/2022 - Chet Russell

import PySimpleGUI as sg
from main import masker
from main import orthorec
from main import seg

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
    
    # Glint Masking options
    [sg.Text("Glint Masking", font=("Helvetica", 20), key='gm')],
    [   
        sg.Text("Pixel Buffer:"),
        sg.Combo([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10],default_value=5,key='pb')
    ],
    [sg.Button("Run Glint Masker Independently")],
    [sg.Text('')],
    
    # Orthorectification options
    [sg.Text("Orthorectification", font=("Helvetica", 20), key='ort')],
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
    [sg.Button("Run", font=("Helvetica", 20))]
]

window = sg.Window('Kelpy', layout,size=(700, 700))
gm = window['gm']
ort = window['ort']
ki = window['ki']

while True:  # Event Loop
    event, values = window.read()
    print(event, values)
    if event == sg.WIN_CLOSED:
        break

    # Running the glint masker
    if event == 'Run Glint Masker Independently':
        if values['imgdir'] == '':
            sg.popup('ERROR: No image folder selected.')
        else:
            masker(values['imgdir'], values['pb'])
            gm.update('Glint Masking: DONE')

    # Running the ODM orthomosaic generator
    if event == 'Run Orthorectification Independently':
        if values['imgdir'] == '':
            sg.popup('ERROR: No image folder selected.')
        else:
            if values['dwndir'] == '':
                sg.popup('ERROR: No results folder selected.')
            else:
                orthorec(values['imgdir'], values['dwndir'], values['q'], values['crop'], values['kmz'], values['ft'], values['exif'])
                ort.update('Orthorectification: DONE')

    # Running Kelpomatic
    if event == 'Run Identification Independently':
        if values['orthfile'] == '':
            sg.popup('ERROR: No orthomosaic file selected.')
        else: 
            if values['resdir'] == '':
                sg.popup('ERROR: No results folder selected.')
            else:
                if values['gsd'] == '':
                    sg.popup('ERROR: GSD value empty.')
                else:
                    try:
                        value = float(values['gsd'])
                        ki.update('Identification (Kelpomatic): DONE')
                        sg.popup(seg(values['orthfile'], values['resdir'], value, False))
                    except:
                        sg.popup('ERROR: GSD not an integer value.')

window.close()