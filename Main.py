import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox

import csv

paths_of_files_list = []
combined_data = []
headers_seen = []
headers_picked = []


def files_selection():
    global paths_of_files_list
    headers_seen.clear()
    headers_picked.clear()
    paths_of_files = filedialog.askopenfilenames(filetypes=[("CSV files", "*.csv")])
    if not paths_of_files:
        headers_display.config(state=tk.NORMAL)
        headers_display.delete("1.0", tk.END)
        headers_display.config(state=tk.DISABLED)
        headers_picked_display.config(state=tk.NORMAL)
        headers_picked_display.delete("1.0", tk.END)
        headers_picked_display.config(state=tk.DISABLED)
        amount_var.set("Files Selected = " + str(len(paths_of_files)) + " File/s")
        messagebox.showinfo("CSV Combiner", "Please select the files you want to combine!")
    else:
        amount_var.set("Files Selected = " + str(len(paths_of_files)) + " File/s")
        paths_of_files_list = paths_of_files
        for i in paths_of_files_list:
            with open(i, mode="r", encoding="utf-8-sig") as file:
                reader = csv.DictReader(file)
                for header in reader.fieldnames:
                    if header not in headers_seen:
                        headers_seen.append(header)
                headers_display.config(state=tk.NORMAL)
                headers_display.delete("1.0", tk.END)
                headers_display.insert(tk.END,",\n".join(headers_seen), "clickable")
                headers_display.tag_config("clickable", foreground="blue", underline=True)
                headers_display.tag_bind("clickable", "<Button-1>", on_header_click)
                headers_display.config(state=tk.DISABLED)
                headers_picked_display.config(state=tk.NORMAL)
                headers_picked_display.delete("1.0", tk.END)
                headers_picked_display.config(state=tk.DISABLED)

def on_header_click(event):
    index = headers_display.index(f"@{event.x},{event.y}")
    line_start = headers_display.index(f"{index} linestart")
    line_end = headers_display.index(f"{index} lineend")
    clicked_line = headers_display.get(line_start, line_end)
    clicked_header = clicked_line.strip(",").strip()

    if clicked_header not in headers_picked:
        headers_picked.append(clicked_header)
    else:
        headers_picked.remove(clicked_header)
    headers_picked_display.config(state=tk.NORMAL)
    headers_picked_display.delete("1.0", tk.END)
    headers_picked_display.insert(tk.END, ",\n".join(headers_picked))
    headers_picked_display.config(state=tk.DISABLED)





def start_combining():
        global paths_of_files_list
        combined_data.clear()
        if not paths_of_files_list:
            messagebox.showinfo("CSV Combiner", "Please select the files you want to combine first before attempting to combine them!")
            return
        if headers_picked:
            headers = [f.strip() for f in headers_picked]
        else:
            messagebox.showinfo("CSV Combiner", "Please select column headers to combine!")
            return
        for i in paths_of_files_list:
            with open(i, mode="r", encoding="utf-8-sig") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    combined_row = {}
                    for header in headers:
                        if header in row:
                            combined_row[header] = row[header]
                    if combined_row:
                        combined_data.append(combined_row)
        final_file_path = filedialog.asksaveasfilename(title="Save your CSV file",defaultextension=".csv",filetypes=[("CSV files", "*.csv"), ("All files", "*.*")])
        if not final_file_path:
            return
        with open(final_file_path, mode='w', newline='', encoding="utf-8-sig") as finalfile:
            writer = csv.DictWriter(finalfile, fieldnames=headers)
            writer.writeheader()
            writer.writerows(combined_data)
        messagebox.showinfo("CSV Combiner", "Done! CSV Files Combined Successfully!")

window = tk.Tk()
window.title("CSV Combiner")
window.resizable(True, True)
window.minsize(500, 500)

amount_var = tk.StringVar(value= "Files Selected = " + str(0) + " File/s")

tk.Label(window, text="\n" + "1- Select CSV Files To Combine" + "\n" + "l" + "\n" + "l" + "\n" + "V").pack()
tk.Label(window).pack()
tk.Button(window, text="1- Select Files", command=files_selection).pack()
tk.Label(window).pack()
tk.Label(window, textvariable=amount_var).pack()

tk.Label(window).pack()
tk.Label(window).pack()
tk.Label(window, text="Total Column Headers In These Files:").pack()

headers_display_frame = tk.Frame(window)
headers_display_frame.pack()
headers_display = tk.Text(headers_display_frame, height=5, width=50, wrap=tk.WORD)
headers_display.pack(side=tk.LEFT)
scrollbar = tk.Scrollbar(headers_display_frame, command=headers_display.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
headers_display.config(yscrollcommand=scrollbar.set)
headers_display.config(state=tk.DISABLED)

tk.Label(window, text="2- Click The Blue Column Headers You Want To Combine (click again to remove!):").pack()

headers_picked_display_frame = tk.Frame(window)
headers_picked_display_frame.pack()
headers_picked_display = tk.Text(headers_picked_display_frame, height=5, width=50, wrap=tk.WORD)
headers_picked_display.pack(side=tk.LEFT)
scrollbar = tk.Scrollbar(headers_picked_display_frame, command=headers_picked_display.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
headers_picked_display.config(yscrollcommand=scrollbar.set)
headers_picked_display.config(state=tk.DISABLED)


tk.Label(window).pack()
tk.Button(window, text="3- Start Combining!", command=start_combining).pack()




window.mainloop()