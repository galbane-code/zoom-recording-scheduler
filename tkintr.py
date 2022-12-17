import tkinter as tk
from datetime import datetime, timedelta
import os
from keypress import create_task
import uuid

input_keys = {True: "one key", False: "multiple keys"}
fields = 'Python Path','Zoom Link','Stop Recording Btn','Day', "Zoom Start Hour", "Recording Start Hour","Recording Stop Hour",'Recording Path','Recording Btn'
now = datetime.now()
cwd = os.getcwd()
days_list = ['sunday','monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday']
days_in_command = ['SUN','MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT']
entries = []

def create_python_task_bat(python_exe_path, specific_exe_path, python_exe_param, python_exe_second_param = None):
    file_name = specific_exe_path.replace(".py","") + "_.bat"
    with open(file_name, "w+") as f:
        if  python_exe_second_param == None:
            f.write('@echo off!\n"{python_exe_path}" "{exe}" "{python_exe_param}"\npause'.format(python_exe_path=python_exe_path,
                                                                        exe=cwd + "\\" + specific_exe_path,
                                                                        python_exe_param= python_exe_param))
        else:
            f.write('@echo off!\n"{python_exe_path}" "{exe}" "{python_exe_param}" "{python_exe_second_param}"\npause'.format(python_exe_path=python_exe_path,
                                                                        exe=cwd + "\\" + specific_exe_path,
                                                                        python_exe_param= python_exe_param,
                                                                        python_exe_second_param=python_exe_second_param))
    return cwd + "\\" + file_name

def fetch(entries):
    dict_fields_values = {entry[0]: entry[1].get() for i,entry in enumerate(entries)}
    dict_days_to_days_command = {days_list[i]: days_in_command[i] for i in range(len(days_list))}
    zoom_hour = datetime.strptime(dict_fields_values["Zoom Start Hour"],"%H:%M") + timedelta(minutes=2)
    dict_fields_values["Day"] = dict_days_to_days_command[dict_fields_values["Day"]]
    

    myuuid = uuid.uuid4()
    """ 
    create a task for the recording program to start
    """
    create_task("ONCE", "record_temp_task_" + myuuid.hex, dict_fields_values["Recording Path"], dict_fields_values["Day"],zoom_hour.strftime('%H:%M'))
    """ 
    create a task for the zoom link to launch to start
    """
    zoom_link_bat = create_python_task_bat(dict_fields_values["Python Path"], "link.py", dict_fields_values["Zoom Link"])
    create_task("ONCE", "zoom_temp_task" + myuuid.hex, zoom_link_bat, dict_fields_values["Day"], dict_fields_values["Zoom Start Hour"])
    """ 
    create a bat file for the start recording program btn
    """
    recording_btn_status = ',' not in dict_fields_values["Recording Btn"]
    click_start_record = create_python_task_bat(dict_fields_values["Python Path"], "keypress.py", 
                                                input_keys[recording_btn_status],dict_fields_values["Recording Btn"])
    """ 
    create a bat file for the stop recording program btn
    """
    recording_stop_btn_status = ',' not in dict_fields_values["Stop Recording Btn"]
    click_stop_record = create_python_task_bat(dict_fields_values["Python Path"], "keypress.py", 
                                                input_keys[recording_stop_btn_status],dict_fields_values["Stop Recording Btn"])
    """ 
    create a task for the recording btn's
    """
    create_task("ONCE", "record_temp_task_start_click" + myuuid.hex, click_start_record, dict_fields_values["Day"],dict_fields_values["Recording Start Hour"])
    create_task("ONCE", "record_temp_task_stop_click" + myuuid.hex, click_stop_record, dict_fields_values["Day"],dict_fields_values["Recording Stop Hour"])

def add_form_entries(root):
    btn_name = btn_ent.get()
    btn_ent.delete(0,len(btn_name))
    row = tk.Frame(root)
    lab = tk.Label(row, width=25, text=btn_name, anchor='w')
    ent = tk.Entry(row)
    row.pack(side=tk.TOP, fill=tk.X, padx=8, pady=5)
    lab.pack(side=tk.LEFT)
    ent.pack(side=tk.RIGHT, expand=tk.YES, fill=tk.X)
    entries.append(ent)
    row = tk.Frame(root)
    lab = tk.Label(row, width=25, text=btn_name +  " time of execution", anchor='w')
    ent = tk.Entry(row)
    row.pack(side=tk.TOP, fill=tk.X, padx=8, pady=5)
    lab.pack(side=tk.LEFT)
    ent.pack(side=tk.RIGHT, expand=tk.YES, fill=tk.X)
    entries.append(ent)


def makeform(root, fields):
    for field in fields:
        row = tk.Frame(root)
        lab = tk.Label(row, width=25, text=field, anchor='w')
        ent = tk.Entry(row)
        row.pack(side=tk.TOP, fill=tk.X, padx=8, pady=5)
        lab.pack(side=tk.LEFT)
        ent.pack(side=tk.RIGHT, expand=tk.YES, fill=tk.X)
        entries.append((field, ent))
    


root = tk.Tk()
row = tk.Frame(root)
row.pack(side=tk.TOP, fill=tk.X, padx=8, pady=5)

b1 = tk.Button(row, text='Show',
                command=(lambda e=entries: fetch(e)))
b1.pack(side=tk.LEFT, padx=0, pady=0)

b3 = tk.Button(row, text='Add',  command=(lambda e=entries: add_form_entries(root)))
b3.pack(side=tk.LEFT, padx=5, pady=0)

lab = tk.Label(row, width=7, text="btn name", anchor='w')
lab.pack(side=tk.LEFT ,padx=10, pady=0)  
btn_ent = tk.Entry(row)
btn_ent.pack(side=tk.RIGHT)

entries.append(row)
makeform(root, fields)
root.bind('<Return>', (lambda event, e=entries: fetch(e)))   
root.mainloop()
