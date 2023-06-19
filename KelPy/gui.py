# Kelpy gui file
# File created: 7/12/2022
# Author: Chet Russell
# Last edited: 6/19/2023 - Chet Russell

"""
NOTICE: I am aware that a LOT of the code in the mainwin function is spaghetti
code. In the sake of programming time, I had to do what I had to do. Even
though it is spaghetti code, it shouldn't affect runtime, as the nested loops
are just checking user input, the processing steps are inside the final loop.
This will be fixed at a later date, but for now, it works.
"""

import core
import os
import sys
import threading
import PySimpleGUI as sg


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS # type: ignore
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


""" --------------ORTHO FUNCTION THREAD FUNCTION---------------------------
This function allows the masking and orthorectification step to take place 
in one thread, allowing the loading wheel to spin.
------------------------------------------------------------------------ """


def ortho_function_thread(window, imgdir, pb, newdir, q, crop, kmz, ft, exif):
    window.write_event_value("-THREAD START-", "")
    core.masker(imgdir, pb)
    core.orthorec(imgdir, newdir, q, crop, kmz, ft, exif)
    window.write_event_value("-THREAD DONE-", "")


""" --------------SEG FUNCTION THREAD FUNCTION---------------------------
This function allows the segmentation(kelpomatic) step to take place in 
one thread, allowing the loading wheel to spin.
------------------------------------------------------------------------ """


def seg_function_thread(window, ortho, komp, gsd, spec):
    window.write_event_value("-THREAD START-", "")
    core.seg(ortho, komp, gsd, spec)
    window.write_event_value("-THREAD DONE-", "")


""" --------------ALL FUNCTION THREAD FUNCTION---------------------------
This function allows all steps to take place simultaneously in one thread, 
allowing the loading wheel to spin.
------------------------------------------------------------------------ """


def all_function_thread(
    window, imgdir, pb, newdir, q, crop, kmz, ft, exif, ortho, komp, spec
):
    window.write_event_value("-THREAD START-", "")
    core.masker(imgdir, pb)
    core.orthorec(imgdir, newdir, q, crop, kmz, ft, exif)
    value = float(core.calculate_gsd(newdir + "/report.pdf"))
    core.seg(ortho, komp, value, spec)
    window.write_event_value("-THREAD DONE-", "")


""" ------------------------ WINDOW FUNCTION ---------------------------
This function creates the information necessary to make a window.
------------------------------------------------------------------------ """


def window():
    sg.theme("Dark2")
    layout = [
        # Initial Folders
        [
            sg.Text("Image Folder:", font=("Helvetica", 15)),
            sg.FolderBrowse(key="imgdir"),
        ],
        [
            sg.Text("Download To:", font=("Helvetica", 15)),
            sg.FolderBrowse(key="dwndir"),
        ],
        [
            sg.Text("Results Folder Name:"),
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
            sg.Text("GSD (centimeters):"),
            sg.InputText(size=(5, 1), key="gsd"),
            sg.Text("Only required when running independently.", font=("Helvetica", 8)),
        ],
        [
            sg.Text("Species classification:"),
            sg.Combo([True, False], key="spec"),
        ],
        [sg.Button("Run Identification Independently")],
        [sg.Button("Run All", font=("Helvetica", 20))],
    ]

    return sg.Window(
        "KelPy", layout, finalize=True, icon=resource_path("graphics/bull.ico")
    )  # size=(700, 700))


""" ------------------------ MAINWIN FUNCTION ---------------------------
This function uses the information created in the window function and
creates a window.
------------------------------------------------------------------------ """


def mainwin():
    newwin = window()
    loading = False
    while True:  # Event Loop
        event, values = newwin.read(timeout=100) # type: ignore

        if loading == True:
            sg.popup_animated(
                image_source=resource_path("graphics/Wheel.gif"),
                grab_anywhere=False,
                keep_on_top=False,
                message="Processing...",
            )
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

                            threading.Thread(
                                target=ortho_function_thread,
                                args=(
                                    newwin,
                                    values["imgdir"],
                                    values["pb"],
                                    newdir,
                                    values["q"],
                                    values["crop"],
                                    False,
                                    values["ft"],
                                    False,
                                ),
                                daemon=True,
                            ).start()
                            loading = True
                            # ort.update("Orthorectification: DONE")
                        except:
                            # Cleaning up masks in the event of an error
                            loading = False
                            core.clean_masks(values["imgdir"])
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
                        if values["spec"] == "":
                            sg.popup("ERROR: Species value empty.", title="ERROR")
                        else:
                            value = float(values["gsd"])
                            if isinstance(value, float):
                                try:
                                    threading.Thread(
                                        target=seg_function_thread,
                                        args=(
                                            newwin,
                                            values["orthfile"],
                                            values["resdir"],
                                            value,
                                            values["spec"],
                                        ),
                                        daemon=True,
                                    ).start()
                                    loading = True

                                except:
                                    loading = False
                                    # Cleaning up masks in the event of an error
                                    sg.popup("ERROR 2: Problem processing request.")
                            else:

                                sg.popup("ERROR: GSD not an integer value.")

        # Running both orthorectification and kelpomatic together
        elif event == "Run All":
            if values["imgdir"] == "":
                sg.popup("ERROR: No image folder selected.", title="ERROR")
            else:
                if values["dwndir"] == "":
                    sg.popup("ERROR: No results folder selected.", title="ERROR")
                else:
                    if values["spec"] == "":
                            sg.popup("ERROR: Species value empty.", title="ERROR")
                    else:
                        try:
                            # This is the folder that is being created
                            newdir = values["dwndir"] + "/" + values["newdir"]
                            os.mkdir(newdir)
                            # Some multithreading here. Reading between each operation to update gui.
                            threading.Thread(
                                target=all_function_thread,
                                args=(
                                    newwin,
                                    values["imgdir"],
                                    values["pb"],
                                    newdir,
                                    values["q"],
                                    values["crop"],
                                    False,
                                    values["ft"],
                                    False,
                                    newdir + "/odm_orthophoto.tif",
                                    newdir,
                                    values["spec"],
                                ),
                                daemon=True,
                            ).start()
                            loading = True

                        except:
                            # Cleaning up masks in the event of an error
                            loading = False
                            core.clean_masks(values["imgdir"])
                            sg.popup("ERROR 3: Problem processing request.")
        else:
            continue

    newwin.close()
