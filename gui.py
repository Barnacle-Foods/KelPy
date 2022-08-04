# Kelpy gui file
# File created: 7/12/2022
# Author: Chet Russell
# Last edited: 8/3/2022 - Chet Russell

import os
import threading
import PySimpleGUI as sg
from core import masker
from core import orthorec
from core import seg
from core import calculate_gsd
from core import clean_masks

def ortho_function_thread(window, imgdir, pb, newdir, q, crop, kmz, ft, exif):
    window.write_event_value('-THREAD START-', '')
    masker(imgdir, pb)
    orthorec(imgdir, newdir, q, crop, kmz, ft, exif)
    window.write_event_value('-THREAD DONE-', '')

def seg_function_thread(window, ortho, komp, gsd, spec):
    window.write_event_value('-THREAD START-', '')
    seg(ortho, komp, gsd, spec)
    window.write_event_value('-THREAD DONE-', '')

def all_function_thread(window, imgdir, pb, newdir, q, crop, kmz, ft, exif, ortho, komp, spec):
    window.write_event_value('-THREAD START-', '')
    masker(imgdir, pb)
    orthorec(imgdir, newdir, q, crop, kmz, ft, exif)
    value = float(calculate_gsd(newdir + "/report.pdf"))
    seg(ortho, komp, value, spec)
    window.write_event_value('-THREAD DONE-', '')

""" ------------------------ WINDOW FUNCTION ---------------------------
This function creates the information necessary to make a window.
------------------------------------------------------------------------ """


def window():
    sg.theme("Default")
    layout = [
        # Initial Folders
        [
            sg.Text("Image Folder:", font=("Helvetica", 15)),
            sg.FolderBrowse(key="imgdir"),
        ],
        [
            sg.Text("Results Folder:", font=("Helvetica", 15)),
            sg.FolderBrowse(key="dwndir"),
        ],
        [
            sg.Text("Folder Name:"),
            sg.InputText(size=(15, 1), key="newdir"),
        ],
        [sg.Text("")],
        # Orthorectification options
        [sg.Text("Orthorectification", font=("Helvetica", 20))],
        [
            sg.Text("Pixel Buffer (for glint masking):"),
            sg.Combo([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10], default_value=5, key="pb"),
        ],
        [
            sg.Text("Quality:"),
            sg.Combo(
                ["ultra", "high", "medium", "low", "lowest"],
                default_value="high",
                key="q",
            ),
        ],
        [
            sg.Text("Crop:"),
            sg.Combo([0, 1, 2, 3, 4, 5], default_value=0, key="crop"),
            # sg.Text("This setting has the tendency to crop out water areas, use with caution.")
        ],
        # WORK IN PROGRESS
        # [
        #    sg.Text("Generate KMZ (Google Earth) render:"),
        #    sg.Combo([True, False],default_value='False',key='kmz')
        # ],
        [
            sg.Text("Feature-type algorithm:"),
            sg.Combo(["sift", "akaze", "hahog", "orb"], default_value="sift", key="ft"),
        ],
        # WORK IN PROGRESS
        # [
        #    sg.Text("Use EXIF:"),
        #    sg.Combo([True, False],default_value=True,key='exif')
        # ],
        [
            sg.Button("Run Orthorectification Independently"),
        ],
        [sg.Text("")],
        # Kelpomatic options
        [sg.Text("Kelp Identification (Kelpomatic)", font=("Helvetica", 20))],
        [
            sg.Text("Orthomosaic File:"),
            sg.FileBrowse(key="orthfile"),
            sg.Text("Only required when running independently.", font=("Helvetica", 8)),
        ],
        [
            sg.Text("Results Folder:"),
            sg.FolderBrowse(key="resdir"),
            sg.Text("Only required when running independently.", font=("Helvetica", 8)),
        ],
        [
            sg.Text("GSD:"),
            sg.InputText(size=(5, 1), key="gsd"),
            sg.Text("Only required when running independently.", font=("Helvetica", 8)),
        ],
        [
            sg.Text("Species classification (default value false):"),
            sg.Combo([True, False], default_value=False, key="spec"),
        ],
        [sg.Button("Run Identification Independently")],
        [sg.Button("Run All", font=("Helvetica", 20))],
    ]

    return sg.Window("Kelpy", layout, finalize=True)  # size=(700, 700))


""" ------------------------ MAINWIN FUNCTION ---------------------------
This function uses the information created in the window function and
creates a window.
------------------------------------------------------------------------ """


def mainwin():
    newwin = window()
    loading = False
    while True:  # Event Loop
        event, values = newwin.read(timeout=100)

        #sg.popup_animated("C:/Users/matt/Documents/imagery_project/UUjhE.gif")
        if loading == True:
            sg.popup_animated("C:/Users/matt/Documents/imagery_project/UUjhE.gif")
        else:
            sg.popup_animated(image_source=None)
        if event == sg.WIN_CLOSED:
            break
        elif event == "-THREAD DONE-":
            loading = False
        elif event == "-THREAD START-":
            loading = True

        # Running the glint mask generator and the ODM orthomosaic generator
        elif event == "Run Orthorectification Independently":
            if values["imgdir"] == "":
                sg.popup("ERROR: No image folder selected.", title="ERROR")
            else:
                if values["dwndir"] == "":
                    sg.popup("ERROR: No results folder selected.", title="ERROR")
                else:
                    if values["newdir"] == "":
                        sg.popup("ERROR: No name for results.", title="ERROR")
                    else:
                        try:
                            newdir = values["dwndir"] + "/" + values["newdir"]
                            os.mkdir(newdir)
                            
                            threading.Thread(target=ortho_function_thread, args=(newwin, values["imgdir"], values["pb"], values["newdir"], values["q"], values["crop"], False, values["ft"], False,), daemon=True).start()
                            loading = True
                            # ort.update("Orthorectification: DONE")
                        except:
                            # Cleaning up masks in the event of an error
                            loading = False
                            clean_masks(values["imgdir"])
                            sg.popup("ERROR 1: Problem processing request.")

        # Running Kelpomatic
        elif event == "Run Identification Independently":
            if values["orthfile"] == "":
                sg.popup("ERROR: No orthomosaic file selected.", title="ERROR")
            else:
                if values["resdir"] == "":
                    sg.popup("ERROR: No results folder selected.", title="ERROR")
                else:
                    if values["gsd"] == "":
                        sg.popup("ERROR: GSD value empty.", title="ERROR")
                    else:
                        value = float(values["gsd"])
                        if isinstance(value, float):
                            try:
                                threading.Thread(target=seg_function_thread, args=(newwin, values["orthfile"], values["resdir"], value, values["spec"],), daemon=True).start()
                                loading = True

                            except:
                                # Cleaning up masks in the event of an error
                                sg.popup("ERROR 2: Problem processing request.")
                        else:
                            loading = False
                            sg.popup("ERROR: GSD not an integer value.")

        # Running both orthorectification and kelpomatic together
        elif event == "Run All":
            if values["imgdir"] == "":
                sg.popup("ERROR: No image folder selected.", title="ERROR")
            else:
                if values["dwndir"] == "":
                    sg.popup("ERROR: No results folder selected.", title="ERROR")
                else:
                    try:
                        # This is the folder that is being created
                        newdir = values["dwndir"] + "/" + values["newdir"]
                        os.mkdir(newdir)
                        # Some multithreading here. Reading between each operation to update gui.
                        threading.Thread(target=all_function_thread, args=(newwin, values["imgdir"], values["pb"], values["newdir"], values["q"], values["crop"], False, values["ft"], False, newdir + "/odm_orthophoto.tif", newdir, values["spec"],), daemon=True).start()
                        loading = True

                    except:
                        # Cleaning up masks in the event of an error
                        loading = False
                        clean_masks(values["imgdir"])
                        sg.popup("ERROR 3: Problem processing request.")
        else:
            continue
        
    
    newwin.close()
