import tkinter as tk
from tkinter import ttk, filedialog, StringVar
import ffmpeg

class VideoSplicerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("FFMPEG Video Splicer")
        self.configure(bg='#333333')
        self.geometry("600x350")
        self._create_variables()
        self._create_styles()
        self._build_layout()

    def _create_variables(self):
        self.grab_video_path = StringVar(value="No file selected")
        self.render_video_path = StringVar(value="No folder selected")
        self.time_slot1 = StringVar()
        self.time_slot2 = StringVar()
        self.duration = 10  # fallback duration

    def _create_styles(self):
        style = ttk.Style(self)
        style.theme_use('clam')
        style.configure('TFrame', background='#333333')
        style.configure('TLabel', background='#333333', foreground='#EEE', font=('Segoe UI', 10))
        style.configure('TEntry', fieldbackground='#555', foreground='#EEE', font=('Segoe UI', 10))
        style.configure('TButton',
                        background='#555', foreground='#EEE',
                        font=('Segoe UI', 10, 'bold'),
                        padding=6)
        style.map('TButton',
                  background=[('active', '#666')],
                  foreground=[('active', '#FFF')])

    def _build_layout(self):
        # make columns expand
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=2)

        main_frame = ttk.Frame(self, padding=(20, 15))
        main_frame.grid(sticky="nsew")
        main_frame.columnconfigure(1, weight=1)

        # Row 0: Buttons
        ttk.Button(main_frame, text="Select Video...", command=self.grab_video).grid(row=0, column=0, sticky="ew", padx=5, pady=5)
        ttk.Button(main_frame, text="Output Folder...", command=self.set_render_video_path).grid(row=0, column=1, sticky="ew", padx=5, pady=5)

        # Row 1: Paths Display
        ttk.Label(main_frame, textvariable=self.grab_video_path).grid(row=1, column=0, columnspan=2, sticky="w", padx=5)
        ttk.Label(main_frame, textvariable=self.render_video_path).grid(row=2, column=0, columnspan=2, sticky="w", padx=5, pady=(0,10))

        # Row 3: Instructions
        ttk.Label(main_frame, text="Timestamps format: HH:MM:SS").grid(row=3, column=0, columnspan=2, sticky="w", padx=5, pady=(0,5))

        # Row 4–5: Time inputs
        ttk.Label(main_frame, text="Start time:").grid(row=4, column=0, sticky="e", padx=5, pady=2)
        ttk.Entry(main_frame, textvariable=self.time_slot1).grid(row=4, column=1, sticky="ew", padx=5, pady=2)

        ttk.Label(main_frame, text="End time:").grid(row=5, column=0, sticky="e", padx=5, pady=2)
        ttk.Entry(main_frame, textvariable=self.time_slot2).grid(row=5, column=1, sticky="ew", padx=5, pady=2)

        # Row 6: Export button
        ttk.Button(main_frame, text="Export Clip", command=self.export).grid(row=6, column=0, columnspan=2, sticky="ew", padx=5, pady=(15,5))

        # Menu
        menu = tk.Menu(self, bg='#333333', fg='#EEE')
        file_menu = tk.Menu(menu, tearoff=0, bg='#444', fg='#EEE')
        file_menu.add_command(label="Exit", command=self.destroy)
        menu.add_cascade(label="File", menu=file_menu)
        self.config(menu=menu)

    def grab_video(self):
        path = filedialog.askopenfilename(filetypes=[("MP4 Videos", "*.mp4")])
        if path:
            self.grab_video_path.set(path)

    def set_render_video_path(self):
        folder = filedialog.askdirectory()
        if folder:
            self.render_video_path.set(folder)

    def export(self):
        start = self.time_slot1.get()
        end = self.time_slot2.get()
        try:
            # calculate duration if both provided
            if start and end:
                fmt = "%H:%M:%S"
                import datetime
                t1 = datetime.datetime.strptime(start, fmt)
                t2 = datetime.datetime.strptime(end, fmt)
                delta = (t2 - t1).total_seconds()
                if delta <= 0:
                    raise ValueError("End must be after start")
                duration = delta
            else:
                duration = self.duration

            input_kwargs = {'ss': start} if start else {}
            out_path = f"{self.render_video_path.get()}/clip.mp4"
            (
                ffmpeg
                .input(self.grab_video_path.get(), **input_kwargs)
                .output(out_path, t=duration)
                .run(overwrite_output=True)
            )
            tk.messagebox.showinfo("Done", f"Saved clip to:\n{out_path}")
        except Exception as e:
            tk.messagebox.showerror("Error", str(e))


if __name__ == "__main__":
    app = VideoSplicerApp()
    app.mainloop()
