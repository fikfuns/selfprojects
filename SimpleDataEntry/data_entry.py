#!/usr/bin/env python
# coding: utf-8

# In[24]:


import PySimpleGUI as sg
import pandas as pd
# Add some color to the window

sg.theme('DarkTeal9')
excel_file = 'dataentry.xlsx'
df = pd.read_excel(excel_file)

layout = [
    [sg.Text('Fill the data plz: ')],
    [sg.Text('Name', size=(15,1)), sg.InputText(key='Name')],
    [sg.Text('Gender', size=(15,1)),
        sg.InputCombo(['Male', 'Female'], key='Gender', size=(20, 1))],
    [sg.Text('Age', size=(15,1)), sg.InputText(key='Age')],
    [sg.Text('Place of Birth', size=(15,1)), sg.InputText(key='Birthplace')],
    [sg.Text('Date Collected', size=(15,1)), sg.InputText(key='Date Collected')],
    [sg.Text('Test Code', size=(15,1)), sg.InputText(key='Test Code')],
    [sg.Submit(), sg.Button('Clear'), sg.Exit()]
]

window = sg.Window('The DataEntrynator 3000', layout)


def clear_input():
    for key in values:
        window[key]('')
    return None



while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Exit':
        break
    if event == 'Clear':
        clear_input()
    if event == 'Submit':
        df = df.append(values, ignore_index=True)
        # Only works if keyName == ColumnName 100% match
        df.to_excel(excel_file, index=False)
        sg.popup('Data saved!')
        clear_input()     
window.close()


# In[ ]:




