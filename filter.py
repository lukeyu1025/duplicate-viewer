import csv
import os
import tkinter as tk
from tkinter import filedialog, ttk

DEFAULT_OUTPUT_FILENAME = "filtered_duplicate_files.csv"

def filter_csv():
    input_csv = filedialog.askopenfilename(title="Select CSV File to Filter", filetypes=[("CSV files", "*.csv")])
    if input_csv:
        default_output_path = os.path.join(os.path.dirname(input_csv), DEFAULT_OUTPUT_FILENAME)
        output_csv = filedialog.asksaveasfilename(title="Save Filtered CSV As", defaultextension=".csv", initialfile=DEFAULT_OUTPUT_FILENAME, initialdir=os.path.dirname(input_csv), filetypes=[("CSV files", "*.csv")])
        if output_csv:
            filter_and_save_csv(input_csv, output_csv)
            root.destroy()  # Close the Tkinter window once filtering is completed

def filter_and_save_csv(input_csv, output_csv):
    desired_formats = ['.jpg', '.jpeg', '.png', '.mp4', '.mov']

    with open(input_csv, mode='r', newline='', encoding='utf-8') as infile:
        with open(output_csv, mode='w', newline='', encoding='utf-8') as outfile:
            reader = csv.reader(infile)
            writer = csv.writer(outfile)
            header = next(reader)
            header[1] = "File Name"  # Change header for file name
            writer.writerow(header)  # Write modified header row
            for row in reader:
                if any(row[1].lower().endswith(format.lower()) for format in desired_formats):
                    # Change file path to file name
                    row[1] = os.path.basename(row[1])
                    writer.writerow(row)

    print(f"Filtered CSV has been saved to {output_csv}.")

def main():
    global root
    root = tk.Tk()
    root.title("CSV Filter")
    root.geometry("300x150")

    select_button = ttk.Button(root, text="Select CSV File", command=filter_csv)
    select_button.pack(pady=20)

    root.mainloop()

if __name__ == "__main__":
    main()
