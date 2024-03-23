import tkinter as tk


def create_window(download_callback):
    window = tk.Tk()
    window.title("Soyjak Downloader")
    window.minsize(width=300, height=300)

    button = tk.Button(window, text="Download", command=download_callback)
    button.pack()

    window.mainloop()
