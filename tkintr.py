import tkinter as tk
from datetime import datetime, timedelta
import os
from keypress import create_task
import uuid
import json

input_keys = {True: "one key", False: "multiple keys"}
fields = 'Zoom Link', "Zoom Start Hour"
now = datetime.now()
cwd = os.getcwd()
entries = []
btn_entries_name_to_time = {}
btn_entries_name_to_entry = {}
config_data = {}
with open("config.json") as json_file:
    config_data = json.load(json_file)
    

record_program_path = config_data["record_program_path"]

def create_python_task_bat(specific_exe_path, python_exe_param,
                           python_exe_second_param = None, btn_name=""):

    file_name = specific_exe_path.replace(".py","") + btn_name  + ".bat"
    with open(file_name, "w+") as f:
        if  python_exe_second_param == None:
            f.write('@echo off!\npython "{exe}" "{python_exe_param}"\nexit'.format(
                                                                        exe=cwd + "\\" + specific_exe_path,
                                                                        python_exe_param= python_exe_param))
        else:
            f.write('@echo off!\npython "{exe}" "{python_exe_param}" "{python_exe_second_param}"\nexit'.format(
                                                                        exe=cwd + "\\" + specific_exe_path,
                                                                        python_exe_param= python_exe_param,
                                                                        python_exe_second_param=python_exe_second_param))
    return cwd + "\\" +  file_name

def fetch():
    entries_without_last  = entries.copy()
    entries_without_last.pop(0)
    dict_fields_values = {}
    for entry in entries_without_last:
        dict_fields_values[entry[0]] = entry[1].get()
    zoom_hour = datetime.strptime(dict_fields_values["Zoom Start Hour"],"%H:%M") + timedelta(minutes=1)
    myuuid = uuid.uuid4()
    
    """ 
    create a task for the recording program to start
    """
    create_task("ONCE", "record_temp_task_" + myuuid.hex, record_program_path,dict_fields_values["Zoom Start Hour"])
    """ 
    create a task for the zoom link to launch to start
    """
    zoom_link_bat = create_python_task_bat("link.py", dict_fields_values["Zoom Link"])
    create_task("ONCE", "zoom_temp_task" + myuuid.hex, zoom_link_bat, zoom_hour.strftime('%H:%M'))

    """ 
    create a task for the recording btn's
    """
    for btn_entry_name in btn_entries_name_to_entry.keys():
        bat_name = create_btn_tasks_bat(btn_entry_name, btn_entries_name_to_entry[btn_entry_name].get())
        create_task("ONCE", btn_entry_name + myuuid.hex, bat_name, btn_entries_name_to_time[btn_entry_name].get())
    

def create_btn_tasks_bat(btn_name, btn_to_push):
    is_single_btn = ',' not in btn_to_push
    current_btn_bat = create_python_task_bat("keypress.py", 
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
    entries.append((btn_name + "btn",ent))
    btn_entries_name_to_entry[btn_name] = ent
    row = tk.Frame(root)
    lab = tk.Label(row, width=25, text=btn_name +  " time of execution", anchor='w')
    ent = tk.Entry(row)
    row.pack(side=tk.TOP, fill=tk.X, padx=8, pady=5)
    lab.pack(side=tk.LEFT)
    ent.pack(side=tk.RIGHT, expand=tk.YES, fill=tk.X)
    entries.append((btn_name + "time",ent))
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
                command=(lambda e=entries: fetch()))
b1.pack(side=tk.LEFT, padx=0, pady=0)

b3 = tk.Button(row, text='Add',  command=(lambda e=entries: add_form_entries(root)))
b3.pack(side=tk.LEFT, padx=5, pady=0)

lab = tk.Label(row, width=7, text="btn name", anchor='w')
lab.pack(side=tk.LEFT ,padx=10, pady=0)  
btn_ent = tk.Entry(row)
btn_ent.pack(side=tk.RIGHT)

entries.append(row)
makeform(root, fields)
root.title("Zoom Recorder")
root.iconbitmap(r'videocamera.ico')
root.bind('<Return>')
root.mainloop()
