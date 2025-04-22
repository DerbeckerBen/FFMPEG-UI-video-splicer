import tkinter as tk

class ResizableApp:
    def __init__(self, root):
        self.root = root
        self.root.attributes('-fullscreen', True)

        self.base_width = 800
        self.base_height = 600

        self.button = tk.Button(root, text="Click Me", font=("Arial", 20))
        self.button.pack(expand=True, fill='both')

        self.root.bind("<Configure>", self.on_resize)

    def on_resize(self, event):
        w_scale = event.width / self.base_width
        h_scale = event.height / self.base_height
        scale = min(w_scale, h_scale)
        
        # Resize font
        new_font_size = int(20 * scale)
        self.button.config(font=("Arial", new_font_size))

if __name__ == "__main__":
    root = tk.Tk()
    app = ResizableApp(root)
    root.mainloop()
