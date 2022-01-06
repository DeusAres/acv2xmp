#!/usr/bin/env python

import PySimpleGUI as sg
import os
import acv2xmp

layout = [
    [
        sg.Column([[ sg.Text(".acv file") ], [ sg.Text("Preset Name") ]]),
        sg.Column([[sg.Input(key='ACV'), sg.FileBrowse(".acv")], [sg.Input(key='NAME')]])
    ],[
        sg.Column([[
                    sg.Button("Convert")
                  ]], justification='right', element_justification='right')
    ],[
        sg.Column([[
                    sg.Text(key='OUT', size = (50, 1))
                  ]], justification='left')
    ]
    
]

window = sg.Window("acv 2 xmp", layout)

while True:
    event, values = window.read()

    if event == sg.WINDOW_CLOSED or event == 'Quit':
        break

    if event ==  "Convert":
        acvFile = values['ACV'].strip('\n').strip(' ')
        if not os.path.exists(acvFile):
            window['OUT'].Update("File error")
            continue

        presetName = values['NAME'].strip('\n').strip(' ')
        if presetName == '':
            window['OUT'].Update("No preset name")
            continue


        fileName = acv2xmp.main(acvFile, presetName)

        window['OUT'].Update("Saved in %s" %fileName)
    
window.close()