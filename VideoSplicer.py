import tkinter as tk
from struct import pack_into
from tkinter import filedialog, StringVar, ttk
import subprocess
from subprocess import PIPE, STDOUT, Popen, STD_INPUT_HANDLE, STD_ERROR_HANDLE
import os
import sys

class VideoSplicerApp(tk.Tk):

    # ------------------------------------------------ CONSTRUCTORS ------------------------------------------------ #

    def __init__(root):
        super().__init__()

        root.constructor_variables()
        root.title("FFMPEG Video Splicer")
        root.geometry(f"{root.width}x{root.height}")
        root.configure(bg='#333333')
        root.constructor_styles()
        root.constuctor_layout()

    def constructor_variables(root):
        root.grab_video_path = StringVar(value="No file selected")
        root.render_video_path = StringVar(value="No folder selected")
        root.time_slot1 = StringVar(value="00:00:00")
        root.time_slot2 = StringVar(value="00:00:00")
        root.output_text = StringVar(value="No issues")
        root.output_file_name = StringVar(value = "Output")
        root.output_text_label = StringVar(value = "Output File Name")

        root.width = 1000
        root.height = 563

        root.BashCommandsRan = [[]]

    def constructor_styles(root):
        style = ttk.Style(root)
        style.theme_use('clam')
        style.configure('TFrame', background='#333333')
        style.configure('TLabel', background='#333333', foreground='#EEE', font=('Segoe UI', 10))
        style.configure('TEntry', fieldbackground='#555', foreground='#EEE', font=('Segoe UI', 10))
        style.configure('TButton', background='#555', foreground='#EEE', font=('Segoe UI', 10, 'bold'), padding=6)
        style.map('TButton', background=[('active', '#666')], foreground=[('active', '#FFF')])
        style.tk.call('tk', 'scaling', 3.0)


    def constuctor_layout(root):

        root.columnconfigure(0, weight=1)
        root.columnconfigure(1, weight=2)

        main_frame = ttk.Frame(root, padding=(20, 15))
        main_frame.grid(sticky="nsew")
        main_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)


        ttk.Button(main_frame, text="Select Video...", command=root.grab_video).grid(row=0, column=0, sticky="ew", padx=5, pady=5)
        ttk.Button(main_frame, text="Output Folder...", command=root.set_render_video_path).grid(row=0, column=1, sticky="ew", padx=5, pady=5)
        ttk.Entry(main_frame, textvariable=root.output_file_name).grid(row=0, column=2, sticky="ew", padx=5, pady=5)
        ttk.Label(main_frame, textvariable=StringVar(value = ".mp4")).grid(row=0, column=3, sticky="ew", padx=5, pady=5)
        ttk.Label(main_frame, textvariable=root.output_text_label).grid(row=1, column=2, sticky="ew", padx=20, pady=2)

        ttk.Label(main_frame, textvariable=root.grab_video_path).grid(row=1, column=0, columnspan=2, sticky="w", padx=5)
        ttk.Label(main_frame, textvariable=root.render_video_path).grid(row=2, column=0, columnspan=2, sticky="w", padx=5, pady=(0,10))

        ttk.Label(main_frame, text = "Enter timestamps in format HH:MM:SS").grid(row=3, column=0, columnspan=2, sticky="w", padx=5, pady=(0,5))

        ttk.Label(main_frame, text="Start time:").grid(row=4, column=0, sticky="e", padx=5, pady=2)
        time_slot1 = ttk.Entry(main_frame, textvariable=root.time_slot1)
        time_slot1.grid(row=4, column=1, sticky="ew", padx=5, pady=2)
        ttk.Label(main_frame, text="End time:").grid(row=5, column=0, sticky="e", padx=5, pady=2)
        time_slot2 = ttk.Entry(main_frame, textvariable=root.time_slot2)
        time_slot2.grid(row=5, column=1, sticky="ew", padx=5, pady=2)

        ttk.Button(main_frame, text="Export Clip", command=root.export).grid(row=6, column=0, columnspan=2, sticky="ew", padx=5, pady=(15,5))
        ttk.Label(main_frame, textvariable=root.output_text).grid(row=7, column=0, sticky="w", padx=5, pady=5)


        menu = tk.Menu(root)
        root.config(menu=menu)
        file_menu = tk.Menu(menu, tearoff=0, bg='#444', fg='#EEE')
        file_menu.add_command(label="Exit", command=root.destroy)
        menu.add_cascade(label="File", menu=file_menu)

        resize_menu = tk.Menu(menu, tearoff=0, bg='#444', fg='#EEE')
        resize_menu.add_command(label=".5x", command=lambda: root.window_scaling(0.5))
        resize_menu.add_command(label="1.0x", command=lambda: root.window_scaling(1.0))
        resize_menu.add_command(label="2.0x", command=lambda: root.window_scaling(2.0))
        resize_menu.add_command(label="3.0x", command=lambda: root.window_scaling(3.0))
        menu.add_cascade(label="Resize", menu=resize_menu)



    # -------------------------------------------------------------------------------------------------------------- #

    def grab_video(root):
        path = (filedialog.askopenfilename(filetypes=[("MP4 Videos", "*.mp4")]))
        if path:
            root.grab_video_path.set(path)
        

    def set_render_video_path(root):
        folder = filedialog.askdirectory()
        if folder:
            root.render_video_path.set(folder)

    def export(root):

        root.check_errors()

        cmd = ["ffmpeg", "-i",root.grab_video_path.get() , "-ss", root.time_slot1.get(), "-to", root.time_slot2.get(), "-c", "copy", (os.path.join(root.render_video_path.get(), root.output_file_name.get()))]
        #Adds the logs of the bash commands that was run for future uses
        root.BashCommandsRan.append(root.execute(cmd))



    #method to write all the lines of terminal output to a list to read for future use in case of bugs
    def execute(root, cmd):
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, universal_newlines=True)
        for line in proc.stdout :
           yield line

        proc.stdout.close()
        return_code = proc.wait()
        if return_code:
            raise subprocess.CalledProcessError(return_code, cmd)


    def check_errors(root):
        #Checks what files are within the selected directory and if there are no errors
        directory = os.listdir(root.render_video_path.get())
        search_string = root.output_file_name.get()

        if not os.path.isfile(root.grab_video_path.get()):
            root.output_text.set("Invalid video file.")
            root.warning_pop("Invalid video file.")
            return

        if not os.path.isdir(root.render_video_path.get()):
            root.output_text.set("Invalid folder path.")
            root.warning_pop("Invalid folder path.")
            return

        if root.time_slot1.get() >= root.time_slot2.get():
            root.output_text.set("End time must start after start time.")
            root.warning_pop("End time must start after start time")
            return

        for fname in directory:
            if os.path.isfile(directory+os.sep+fname) == os.path.isfile(directory.os.sep+root.output_file_name.get()):
                root.output_text.set("File with name already exists.")
                root.warning_pop("File with name already exists.")
                return


    def warning_pop(root, warning):
        window = tk.Toplevel(root)
        window.configure(background = "#FF0000")


        window.title("Warning")
        screenwidth = window.winfo_screenwidth() / 2
        screenheight = window.winfo_screenheight() / 2
        window.geometry("300x200+%d+%d" % (screenwidth, screenheight))
        word_list = warning.split(" ")
        Line1 = ""
        Line2 = ""
        if len(warning) > 30:
            for i in range(len(word_list)):
                if i < len(word_list)/2:
                    Line1 += word_list[i]+" "
                else:
                    Line2 += word_list[i]+" "
        else:
            Line1 = warning

        ttk.Label(window, text=Line1, background = "#FF0000", foreground="#FFFFFF", font=('Segoe UI', 10)).pack(padx=10, pady=5)
        ttk.Label(window, text=Line2, background = "#FF0000", foreground="#FFFFFF", font=('Segoe UI', 10)).pack(padx=10, pady=5)


        ttk.Button(window, text="OK", command=window.destroy).pack(padx = 10, pady = 10)




    def yes_no_window(self, warning):
        window = tk.Toplevel(root)
        window.configure(background="#FF0000")

        window.title("Warning")
        screenwidth = window.winfo_screenwidth() / 2
        screenheight = window.winfo_screenheight() / 2
        window.geometry("300x200+%d+%d" % (screenwidth, screenheight))
        word_list = warning.split(" ")
        Line1 = ""
        Line2 = ""
        if len(warning) > 30:
            for i in range(len(word_list)):
                if i < len(word_list) / 2:
                    Line1 += word_list[i] + " "
                else:
                    Line2 += word_list[i] + " "
        else:
            Line1 = warning

        ttk.Label(window, text=Line1, background="#FF0000", foreground="#FFFFFF", font=('Segoe UI', 10)).pack(padx=10,
                                                                                                              pady=5)
        ttk.Label(window, text=Line2, background="#FF0000", foreground="#FFFFFF", font=('Segoe UI', 10)).pack(padx=10,
                                                                                                              pady=5)

        ttk.Button(window, text="Yes", command=window.destroy).grid(row = 3, column = 0, padx = 5, pady = 5)
        ttk.Button(window, text="No", command=window.destroy and self.warning_pop("Please change the name of the output file")).grid(row = 3, column = 1, padx = 5, pady = 5)


    def window_scaling(root, scale):
        root.tk.call('tk', 'scaling', scale)




if __name__ == "__main__":
    app = VideoSplicerApp()
    app.mainloop()

    
# To add later:
#
#   Replace error text with pop text (Make the error noticable)
#
#   Prevent the whole thing from freezing when splicing a large section. (Loading screen)
#
#   Make resize buttons work
#
#   Have output file name option
#
#   
#
#
# ----------
# Future ideas:
#   
#   Video preview
#   
#   Place sliders on video progress bar instead of typing in exact timeslots
#   
#   make this a subsection of the full a full FFMPEG GUI command list. (like a main menu and this is one of the options)
#   
#   Optimize code for speed
#   
#   
#   