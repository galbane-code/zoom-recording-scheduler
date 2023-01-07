import pyautogui
import time
import os
import sys

def create_task(type: str, name: str, exe_path: str, hour: str):
    task_str= (r'SchTasks /Create /SC {type} /TN "{name}" /TR "{exe_path}" /ST {hour}').format(type=type, name=name, exe_path=exe_path,hour=hour)
    res = os.system(task_str)
    print(res)

def key_press(key: str):
    time.sleep(2)
    if key == "click":
        pyautogui.click()
    else:
        pyautogui.press(key)
    
def press_multiple_keys(keys: list[str]):
    time.sleep(2)
    pyautogui.hotkey(*keys)

params = sys.argv
if len(params) > 1:
    type_key = params[1]
    if type_key == "one key":
        key_press_input = params[2]
        key_press(key_press_input)
    elif type_key == "multiple keys":
        keys_press_input = params[2].split(",")
        press_multiple_keys(keys_press_input)
        
        
