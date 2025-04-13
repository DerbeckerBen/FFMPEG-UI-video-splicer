import tkinter as tk
from tkinter import filedialog, StringVar, Variable
import ffmpeg

root = tk.Tk()
root.title("FFMPEG Video Splicer")
root.geometry("640x440")
root.configure(bg='#333333')



time_slot1 = Variable
time_slot2 = Variable
grab_video_path = ""
render_video_path = ""
duration = 10 # 10 seconds

def grab_video():
    global grab_video_path
    grab_video_path = (filedialog.askopenfilename(filetypes=[("Video Files", "*.mp4")]))


def set_render_video_path():
    render_video_path.set(filedialog.askdirectory())

def export():
    ffmpeg.input(grab_video_path, ss=0).output('output_file.mp4', t=duration).run()

tk.Button(root, text="Grab Video", command=grab_video, bg='#333333').grid(row=0, column=0, padx=10, pady=10)
tk.Button(root, text="Set Render Path", command=set_render_video_path).grid(row=0, column=1, padx=10, pady=10)
tk.Label(root, text = "Enter paths in the format of  Hours:Minutes:Seconds").grid(row=3, column=0, padx=10, pady=10)

tk.Label(root, text="Enter first video timestamp").grid(row=4, column=0)
tk.Label(root, text="Enter second video timestamp").grid(row=5, column=0)
time_slot1 = tk.Entry(root)
time_slot2 = tk.Entry(root)

time_slot1.grid(row=4, column=1)
time_slot2.grid(row=5, column=1)


tk.Label(root, textvariable=grab_video_path).grid(row=1, column=0, padx=10, pady=10)
tk.Label(root, textvariable=render_video_path).grid(row=1, column=0, padx=10, pady=10)


tk.Button(root, text="Export", command=export).grid(row=7, column=0, padx=10, pady=10)

menu = tk.Menu(root)
root.config(menu=menu)
menu.add_cascade(label='Exit', command=root.destroy)

root.mainloop()