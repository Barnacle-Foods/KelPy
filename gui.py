# Kelpy gui file
# File created: 7/12/2022
# Author: Chet Russell
# Last edited: 8/3/2022 - Chet Russell

import os
import PySimpleGUI as sg
from core import masker
from core import orthorec
from core import seg
from core import calculate_gsd
from core import clean_masks


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
    while True:  # Event Loop
        
        event, values = newwin.read()
        print(event, values)
        if event == sg.WIN_CLOSED:
            break

        # Running the glint mask generator and the ODM orthomosaic generator
        if event == "Run Orthorectification Independently":
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
                            newwin.perform_long_operation(lambda: masker(values["imgdir"], values["pb"]), end_key="MASKDONE")
                            newwin.read()
                            newwin.perform_long_operation(lambda: orthorec(
                                values["imgdir"],
                                newdir,
                                values["q"],
                                values["crop"],
                                False,
                                values["ft"],
                                False,
                                ),
                                end_key="ORTHDONE"
                            )
                            newwin.read()
                            # ort.update("Orthorectification: DONE")
                        except:
                            # Cleaning up masks in the event of an error
                            clean_masks(values["imgdir"])
                            sg.popup("ERROR 1: Problem processing request.")

        # Running Kelpomatic
        if event == "Run Identification Independently":
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
                                newwin.perform_long_operation(
                                    lambda: 
                                        seg(
                                            values["orthfile"],
                                            values["resdir"],
                                            value,
                                            values["spec"],
                                        ),
                                        end_key="SEGDONE"
                                    )
                                newwin.read()

                            except:
                                # Cleaning up masks in the event of an error
                                sg.popup("ERROR 2: Problem processing request.")
                        else:
                            sg.popup("ERROR: GSD not an integer value.")

        # Running both orthorectification and kelpomatic together
        if event == "Run All":
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
                        newwin.perform_long_operation(lambda: masker(values["imgdir"], values["pb"]), end_key="MASKDONE2")
                        newwin.read()
                        newwin.perform_long_operation(lambda: orthorec(
                                values["imgdir"],
                                newdir,
                                values["q"],
                                values["crop"],
                                False,
                                values["ft"],
                                False,
                                ),
                                end_key="ORTHDONE2"
                        )
                        newwin.read()
                        value = float(calculate_gsd(newdir + "/report.pdf"))
                        newwin.perform_long_operation(
                                    lambda: 
                                        seg(
                                            newdir + "/odm_orthophoto.tif",
                                            newdir,
                                            value,
                                            values["spec"],
                                        ),
                                        end_key="SEGDONE2"
                                    )
                        newwin.read()

                    except:
                        # Cleaning up masks in the event of an error
                        clean_masks(values["imgdir"])
                        sg.popup("ERROR 3: Problem processing request.")

    newwin.close()
