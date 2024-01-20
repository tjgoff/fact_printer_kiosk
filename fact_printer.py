import os
import platform
import random
import win32print
import keyboard


#initial setup    
quotes_file = "quotes.txt"
facts_file = "facts.txt"
buffer_file = "buffer.txt" #holds content to be printed


#Key presses drive the app
def on_key_event(e):
    if e.event_type == keyboard.KEY_DOWN:
        if e.name == "f":
            print("Print a fact!")
            file_name = facts_file
        elif e.name == "q":
            print("Print a quote!")
            file_name = quotes_file
        elif e.name == "esc":
            print("Esc: closing time!")
            return
        else:
            print("Unrecognized key/command: ", e.name)
            return
        
        text_to_print = get_random_entry(file_name)
        write_text_to_file(text_to_print, buffer_file)
        print("Print:", text_to_print)
        send_file_to_printer(buffer_file)


#utilities
def send_file_to_printer(file_name):
    system_platform = get_os()
    #print("System platform: ", system_platform)
    current_directory = os.getcwd()
    full_file_path = os.path.join(current_directory, file_name)
    
    if system_platform == "Mac" or system_platform == "Linux":
        os.system("lpr -P printer_name " + full_file_path) #TODO: replace "printer_name"
    elif system_platform == "Windows":
        print_file_on_windows(full_file_path)


def get_os():
    if platform.system() == "Darwin":
        return "Mac"
    return platform.system() # "Linux" or "Windows" (hopefully)
    

def print_file_on_windows(file_path):
    try:
        with open(file_path, 'r') as file:
            file_contents = file.read()
        
        default_printer = win32print.GetDefaultPrinter()
        printer_handle = win32print.OpenPrinter(default_printer)
        job_handle = win32print.StartDocPrinter(printer_handle, 1, ("Print Job", None, "RAW"))
        win32print.WritePrinter(printer_handle, file_contents.encode('utf-8'))
        win32print.EndDocPrinter(printer_handle)
        win32print.ClosePrinter(printer_handle)
        print(f"File '{file_path}' sent to printer")

    except Exception as e:
        print(f"Error sending file to printer: {e}")


def get_random_entry(file_path):
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
            file.close()
            
        if not lines:
            print("File is empty.")
            return
            
        return (random.choice(lines)).strip() # remove trailing newline character
            
    except FileNotFoundError:
        print(f"File not found: {file_path}")
    except Exception as e:
        print(f"An error occurred: {e}")


def write_text_to_file(text, file_path, mode="w"):
    with open(file_path, mode) as file:
        file.write(text)
    file.close()



if __name__ == "__main__":
    keyboard.hook(on_key_event)
    print("Press [f] key for a fact, or press [q] key for a quote.  Press [esc] key to end program")

    # Keep the program running until "esc" to close
    keyboard.wait('esc')
    