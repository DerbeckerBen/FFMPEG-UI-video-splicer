import tkinter as tk
from tkinter import filedialog, StringVar, Variable, ttk
import ffmpeg
import subprocess

class VideoSplicerApp(tk.Tk):

    # ------------------------------------------------ CONSTRUCTORS ------------------------------------------------ #

    def __init__(root):
        super().__init__()
        root.title("FFMPEG Video Splicer")
        root.geometry("1200x700")
        root.configure(bg='#333333')
        root.constructor_variables()
        root.constructor_styles()
        root.constuctor_layout()


    def constructor_variables(root):
        root.grab_video_path = StringVar(value="No file selected")
        root.render_video_path = StringVar(value="No folder selected")
        root.time_slot1 = StringVar()
        root.time_slot2 = StringVar()

    def constructor_styles(root):
        style = ttk.Style(root)
        style.theme_use('clam')
        style.configure('TFrame', background='#333333')
        style.configure('TLabel', background='#333333', foreground='#EEE', font=('Segoe UI', 10))
        style.configure('TEntry', fieldbackground='#555', foreground='#EEE', font=('Segoe UI', 10))
        style.configure('TButton', background='#555', foreground='#EEE', font=('Segoe UI', 10, 'bold'), padding=6)
        style.map('TButton', background=[('active', '#666')], foreground=[('active', '#FFF')])

    def constuctor_layout(root):

        root.columnconfigure(0, weight=1)
        root.columnconfigure(1, weight=2)

        main_frame = ttk.Frame(root, padding=(20, 15))
        main_frame.grid(sticky="nsew")
        main_frame.columnconfigure(1, weight=1)


        ttk.Button(main_frame, text="Select Video...", command=root.grab_video).grid(row=0, column=0, sticky="ew", padx=5, pady=5)
        ttk.Button(main_frame, text="Output Folder...", command=root.set_render_video_path).grid(row=0, column=1, sticky="ew", padx=5, pady=5)

        ttk.Label(main_frame, textvariable=root.grab_video_path).grid(row=1, column=0, columnspan=2, sticky="w", padx=5)
        ttk.Label(main_frame, textvariable=root.render_video_path).grid(row=2, column=0, columnspan=2, sticky="w", padx=5, pady=(0,10))

        ttk.Label(main_frame, text = "Enter timestamps in format HH:MM:SS").grid(row=3, column=0, columnspan=2, sticky="w", padx=5, pady=(0,5))

        ttk.Label(main_frame, text="Start time:").grid(row=4, column=0, sticky="e", padx=5, pady=2)
        ttk.Entry(main_frame, textvariable=root.time_slot1).grid(row=4, column=1, sticky="ew", padx=5, pady=2)
        ttk.Label(main_frame, text="End time:").grid(row=5, column=0, sticky="e", padx=5, pady=2)
        ttk.Entry(main_frame, textvariable=root.time_slot2).grid(row=5, column=1, sticky="ew", padx=5, pady=2)

        ttk.Button(main_frame, text="Export Clip", command=root.export).grid(row=6, column=0, columnspan=2, sticky="ew", padx=5, pady=(15,5))

        menu = tk.Menu(root)
        root.config(menu=menu)
        file_menu = tk.Menu(menu, tearoff=0, bg='#444', fg='#EEE')
        file_menu.add_command(label="Exit", command=root.destroy)
        menu.add_cascade(label="File", menu=file_menu)


    # -------------------------------------------------------------------------------------------------------------- #

    def grab_video(root):
        path = (filedialog.askopenfilename(filetypes=[("MP4 Videos", "*.mp4")]))
        if path:
            root.grab_video_path.set(path)
        


    def set_render_video_path(root):
        root.render_video_path.set(filedialog.askdirectory())
        folder = filedialog.askdirectory()
        if folder:
            root.render_video_path.set(folder)

    def export(root):
        str_timeslot1 = str(root.time_slot1).split(":")
        str_timeslot2 = str(root.time_slot2).split(":")
        timeslot1 = 0
        timeslot2 = 0
        for i in range(len(str_timeslot1)): timeslot1 += int(str_timeslot1[i]) * 60 ^ (2 - i)
        for i in range(len(str_timeslot1)): timeslot2+=int(str_timeslot2[i])*60^(2-i)

        cmd = ["ffmpeg", "-i", "-ss", timeslot1, "-to", timeslot2, "-c:v", "copy", "-c:a", "copy", "output.mp4"]
        subprocess.run(cmd)








if __name__ == "__main__":
    app = VideoSplicerApp()
    app.mainloop()