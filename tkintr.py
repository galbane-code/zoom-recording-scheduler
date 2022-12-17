import tkinter as tk
from datetime import datetime, timedelta
import os
from keypress import create_task
import uuid

input_keys = {True: "one key", False: "multiple keys"}
fields = 'Python Path','Zoom Link', "Zoom Start Hour",'Recording Path'
now = datetime.now()
cwd = os.getcwd()
days_list = ['sunday','monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday']
days_in_command = ['SUN','MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT']
entries = []
btn_entries_name_to_time = {}
btn_entries_name_to_entry = {}

def create_python_task_bat(python_exe_path, specific_exe_path, python_exe_param, python_exe_second_param = None, btn_name=""):
    file_name = specific_exe_path.replace(".py","") + btn_name  + "_.bat"
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
    create a task for the recording btn's
    """
    for btn_entry_name in btn_entries_name_to_entry.key():
        bat_name = create_btn_tasks_bat(btn_entry_name, btn_entries_name_to_entry[btn_entry_name].get(), dict_fields_values["Python Path"])
        create_task("ONCE", btn_entry_name + myuuid.hex, bat_name, btn_entries_name_to_time[btn_entry_name])
    

def create_btn_tasks_bat(btn_name, btn_to_push, python_path):
    is_single_btn = ',' not in btn_to_push
    current_btn_bat = create_python_task_bat(python_path, "keypress.py", 
                                                input_keys[is_single_btn], btn_to_push, btn_name)
    return current_btn_bat


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
    btn_entries_name_to_entry[btn_name] = ent
    row = tk.Frame(root)
    lab = tk.Label(row, width=25, text=btn_name +  " time of execution", anchor='w')
    ent = tk.Entry(row)
    row.pack(side=tk.TOP, fill=tk.X, padx=8, pady=5)
    lab.pack(side=tk.LEFT)
    ent.pack(side=tk.RIGHT, expand=tk.YES, fill=tk.X)
    entries.append(ent)
    btn_entries_name_to_time[btn_name] = ent

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

b1 = tk.Button(row, text='Start',
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
