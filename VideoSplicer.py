import tkinter as tk
from tkinter import filedialog, StringVar, Variable, ttk
import ffmpeg



class VideoSplicerApp(tk.Tk):

    # ------------------------------------------------ CONSTRUCTORS ------------------------------------------------ #

    def __init__(root):
        super().__init__()
        root.title("FFMPEG Video Splicer")
        root.geometry("600x350")
        root.configure(bg='#333333')
        root.constructor_variables()
        root.constructor_styles()
        root.constuctor_layout()


    def constructor_variables(root):
        root.grab_video_path = StringVar(value="No file selected")
        root.render_video_path = StringVar(value="No file selected")
        root.time_slot1 = StringVar()
        root.time_slot2 = StringVar()

    def constructor_styles(root):
        style = ttk.Style(root)
        style.theme_use('clam')
        # style.configure('TFrame', background='#333333')
        # style.configure('TLabel', background='#333333', foreground='#EEE', font=('Segoe UI', 10))
        # style.configure('TEntry', fieldbackground='#555', foreground='#EEE', font=('Segoe UI', 10))
        # style.configure('TButton', background='#555', foreground='#EEE', font=('Segoe UI', 10, 'bold'), padding=6)
        # style.map('TButton', background=[('active', '#666')], foreground=[('active', '#FFF')])

    def constuctor_layout(root):

        main_frame = ttk.Frame(root, padding=(20, 15))
        main_frame.grid(sticky="nsew")
        main_frame.columnconfigure(1, weight=1)


        ttk.Button(root, text="Grab Video", command=root.grab_video).grid(row=0, column=0, padx=10, pady=10)
        ttk.Button(root, text="Set Render Path", command=root.set_render_video_path).grid(row=0, column=1, padx=10, pady=10)
        ttk.Label(root, text = "Enter paths in the format of  Hours:Minutes:Seconds").grid(row=3, column=0, padx=10, pady=10)

        ttk.Label(root, text="Enter first video timestamp").grid(row=4, column=0)
        ttk.Label(root, text="Enter second video timestamp").grid(row=5, column=0)
        time_slot1 = ttk.Entry(root)
        time_slot2 = ttk.Entry(root)

        time_slot1.grid(row=4, column=1)
        time_slot2.grid(row=5, column=1)


        # ttk.Label(root, textvariable=grab_video_path).grid(row=1, column=0, padx=10, pady=10)
        # ttk.Label(root, textvariable=render_video_path).grid(row=1, column=0, padx=10, pady=10)


        # ttk.Button(root, text="Export", command=export).grid(row=7, column=0, padx=10, pady=10)

        # menu = ttk.Menu(root)
        # root.config(menu=menu)
        # menu.add_cascade(label='Exit', command=root.destroy)




    # -------------------------------------------------------------------------------------------------------------- #
    # time_slot1 = Variable
    # time_slot2 = Variable
    # grab_video_path = ""
    # render_video_path = ""
    # duration = 10 # 10 seconds

    def grab_video(root):
        global grab_video_path
        grab_video_path = (filedialog.askopenfilename(filetypes=[("Video Files", "*.mp4")]))


    def set_render_video_path(root):
        root.render_video_path.set(filedialog.askdirectory())

    # def export():
    #     ffmpeg.input(grab_video_path, ss=0).output('output_file.mp4', t=duration).run()








if __name__ == "__main__":
    app = VideoSplicerApp()
    app.mainloop()