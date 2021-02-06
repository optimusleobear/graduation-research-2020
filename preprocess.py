import subprocess
import os
from shutil import copy, copytree, rmtree
from tkinter import *
import tkinter.filedialog

def micb():
    filenames = tkinter.filedialog.askopenfilenames()
    prepro_folder = 'MicB/temp/'

    if len(filenames) != 0:
        string_filename = ""
        for i in range(0, len(filenames)):
            copy(filenames[i], prepro_folder)
            string_filename += str(filenames[i]) + "\n"
        os.chdir('MicB')
        command = '! python run.py --input_folder temp \
              --output_folder output \
              --GPU 0'
        subprocess.call(command, shell=True)

        source_path = os.path.abspath(r'output')
        target_path = os.path.abspath(r'../preprocessed')
        if os.path.exists(target_path):
            rmtree(target_path)
        elif os.path.exists(target_path):
            os.makedirs(target_path)
        copytree(source_path, target_path)

        # remove cache
        os.chdir('temp')
        subprocess.call('rm -rf *', shell=True)
        os.chdir('../output')
        subprocess.call('rm -rf *', shell=True)
        os.chdir('..')

        os.chdir('..')

        lb.config(text="File(s) has been processed:\n" + string_filename)
        print('\033[1;33;44mFiles has been saved to preprocessed folder.\033[0m')
    else:
        lb.config(text="ERROR 404: No file is selected.")

root = Tk()
lb = Label(root, text='')
lb.pack()
btn = Button(root, text="Select file", command=micb)
btn.pack()
root.mainloop()
