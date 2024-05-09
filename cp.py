import tkinter as tk
from tkinter import ttk, filedialog
import os
import duplicates as dup
import csv

def list_duplicates_in_folder():
    global folder_path
    folder_path = filedialog.askdirectory(title="Select Folder to Find Duplicates")
    if folder_path:
        select_csv_location("duplicate_files.csv")

def select_csv_location(default_csv_name):
    global folder_path
    if folder_path:
        csv_path = filedialog.asksaveasfilename(defaultextension=".csv", initialfile=default_csv_name, filetypes=[("CSV files", "*.csv")], title="Save CSV File As")
        if csv_path:
            save_duplicates_to_csv(folder_path, csv_path)

def save_duplicates_to_csv(folder_path, csv_path):
    duplicates_info = dup.list_all_duplicates(folder_path, to_csv=False, fastscan=True)
    with open(csv_path, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Hash', 'File Name', 'File Path'])  # Write header row
        for hash_value, file_list in duplicates_info.items():
            for file_name in file_list:
                # Get the full file path
                file_path = os.path.join(folder_path, file_name)
                # Write hash value, file name, and file path to CSV
                writer.writerow([hash_value, file_name, file_path])
    print(f"Duplicate files information has been saved to {csv_path}.")

def main():
    root = tk.Tk()
    root.title("Select Folder to Find Duplicates")

    root.geometry("400x200")  # Set the size of the window

    list_duplicates_in_folder()  # Start the process by asking the user to select a folder

    root.mainloop()

if __name__ == "__main__":
    main()
