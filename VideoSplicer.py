import tkinter as tk
from tkinter import filedialog, Variable
import ffmpeg

root = tk.Tk()
root.title("FFMPEG Video Splicer")
root.geometry("500x400")



time_slot1 = Variable
time_slot2 = Variable
grab_video_path = ""
render_video_path = ""

def grab_video():
    grab_video_path = filedialog.askopenfilename(filetypes=[("Video Files", "*.mp4")])


def render_video_path():
    render_video_path = filedialog.askdirectory()

tk.Button(root, text="Grab Video", command=grab_video).grid(row=0, column=0, padx=10, pady=10)
tk.Button(root, text="Set Render Path", command=render_video_path).grid(row=0, column=1, padx=10, pady=10)
tk.Label(root, text = "Enter paths in the format of  Hours:Minutes:Seconds").grid(row=1, column=0, padx=10, pady=10)

tk.Label(root, text="Enter first video timestamp").grid(row=2, column=0)
tk.Label(root, text="Enter second video timestamp").grid(row=3, column=0)
time_slot1 = tk.Entry(root)
time_slot2 = tk.Entry(root)

time_slot1.grid(row=2, column=1)
time_slot2.grid(row=3, column=1)


menu = tk.Menu(root)
root.config(menu=menu)
menu.add_cascade(label='Exit', command=root.destroy)

root.mainloop()



root.mainloop()