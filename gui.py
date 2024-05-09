import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk, ExifTags
import os
import csv
import pyautogui
from collections import defaultdict

class DuplicateViewer(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Duplicate Viewer")
        self.geometry("800x600")
        self.selected_csv_file = None
        self.duplicate_files = []
        self.current_piece_index = 0

        self.select_csv_button = ttk.Button(self, text="Select CSV File", command=self.select_csv_file)
        self.select_csv_button.pack(pady=20)

        self.canvas = tk.Canvas(self)
        self.canvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.image_frame = ttk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.image_frame, anchor="nw")

        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollbar.pack(side="right", fill="y")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.bind("<Configure>", self.on_canvas_configure)
        self.image_frame.bind("<Configure>", self.on_frame_configure)

        self.canvas.bind_all("<MouseWheel>", self.on_mousewheel)

    def on_canvas_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def on_frame_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    def select_csv_file(self):
        csv_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")], title="Select CSV File")
        if csv_path:
            self.selected_csv_file = csv_path
            self.load_duplicate_files()

    def load_duplicate_files(self):
        self.duplicate_files = []
        hash_files_map = defaultdict(list)
        with open(self.selected_csv_file, mode='r', encoding='utf-8') as file:
            next(file)  # Skip header row
            for row in file:
                hash_value, file_name, file_path = row.strip().split(',')
                hash_files_map[hash_value].append((file_name, file_path))

        for files_with_same_hash in hash_files_map.values():
            self.duplicate_files.append(files_with_same_hash)

        self.show_piece()

    def show_piece(self):
        # Clear previous images and labels
        for widget in self.image_frame.winfo_children():
            widget.destroy()
    
        if not self.duplicate_files:
            return
    
        # Get current piece of duplicate files
        current_files = self.duplicate_files[self.current_piece_index]
    
        # Show files side by side
        for file_info in current_files:
            img_frame = ttk.Frame(self.image_frame)
            img_frame.pack(side=tk.TOP)
    
            file_path = file_info[1]
            if file_path.lower().endswith(('.jpg', '.jpeg', '.png')):
                try:
                    # Load image
                    img = Image.open(file_path)
                    img = self.rotate_image(img)
                    img = img.resize((200, 200), Image.BICUBIC)
                    img = ImageTk.PhotoImage(img)
                    label_img = ttk.Label(img_frame, image=img)
                    label_img.image = img
                    label_img.pack(side=tk.LEFT, padx=10, pady=10)
    
                    # Display filename and file location
                    file_label = ttk.Label(img_frame, text=file_info[0] + '\n\n' + file_info[1], wraplength=200)
                    file_label.pack(side=tk.LEFT, padx=10, pady=10)
    
                    # Button for opening folder
                    open_folder_button = ttk.Button(img_frame, text="Open Folder", command=lambda path=file_path: self.open_file_location(path))
                    open_folder_button.pack(side=tk.LEFT, padx=(0, 10), pady=10)
                except (OSError, Image.UnidentifiedImageError) as e:
                    # Display error message
                    error_label = ttk.Label(img_frame, text="Error: Unable to open image", wraplength=200)
                    error_label.pack(side=tk.LEFT, padx=10, pady=10)
                    print(f"Error: Unable to open image {file_path}")
            elif file_path.lower().endswith(('.mp4', '.mov')):
                # Load video icon
                video_icon_path = os.path.join(os.path.dirname(__file__), 'video_icon.png')
                video_icon = Image.open(video_icon_path)
                video_icon = video_icon.resize((200, 200), Image.BICUBIC)
                video_icon = ImageTk.PhotoImage(video_icon)
                label_video_icon = ttk.Label(img_frame, image=video_icon)
                label_video_icon.image = video_icon
                label_video_icon.pack(side=tk.LEFT, padx=10, pady=10)
    
                # Display filename and file location as a clickable link
                file_label = ttk.Label(img_frame, text=file_info[0] + '\n'+ file_info[1], wraplength=200, cursor="hand2", foreground="blue")
                file_label.pack(side=tk.LEFT, padx=10, pady=10)
                file_label.bind("<Button-1>", lambda event, path=file_path: self.open_file_location(path))


    def rotate_image(self, img):
        try:
            for orientation in ExifTags.TAGS.keys():
                if ExifTags.TAGS[orientation] == 'Orientation':
                    break
            exif = dict(img._getexif().items())

            if exif[orientation] == 3:
                img = img.rotate(180, expand=True)
            elif exif[orientation] == 6:
                img = img.rotate(270, expand=True)
            elif exif[orientation] == 8:
                img = img.rotate(90, expand=True)
        except (AttributeError, KeyError, IndexError):
            # Cases: image don't have getexif
            pass
        return img

    def open_file_location(self, path):
        print("Opening folder containing the file:", path)
        try:
            folder_path, file_name = os.path.split(path)
            os.startfile(os.path.dirname(path))
            pyautogui.press('down')  # Navigate down to the first file in the folder
            pyautogui.typewrite(file_name)  # Type the file name to select it
            #pyautogui.press('enter')  # Press Enter to open the file
        except Exception as e:
            messagebox.showerror("Error", f"Unable to open folder: {e}")



def main():
    app = DuplicateViewer()
    app.mainloop()

if __name__ == "__main__":
    main()

