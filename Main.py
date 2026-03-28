import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox

import csv

paths_of_files_list = []
combined_data = []
headers_seen = []
picked_headers = []


def files_selection():
    global paths_of_files_list
    headers_seen.clear()
    picked_headers.clear()
    paths_of_files = filedialog.askopenfilenames(filetypes=[("CSV files", "*.csv")])
    if not paths_of_files:
        headers_display.config(state=tk.NORMAL)
        headers_display.delete("1.0", tk.END)
        headers_display.config(state=tk.DISABLED)
        picked_headers_display.config(state=tk.NORMAL)
        picked_headers_display.delete("1.0", tk.END)
        picked_headers_display.config(state=tk.DISABLED)
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
                picked_headers_display.config(state=tk.NORMAL)
                picked_headers_display.delete("1.0", tk.END)
                picked_headers_display.config(state=tk.DISABLED)

def on_header_click(event):
    index = headers_display.index(f"@{event.x},{event.y}")
    line_start = headers_display.index(f"{index} linestart")
    line_end = headers_display.index(f"{index} lineend")
    clicked_line = headers_display.get(line_start, line_end)
    clicked_header = clicked_line.strip(",").strip()

    if clicked_header not in picked_headers:
        picked_headers.append(clicked_header)
    else:
        picked_headers.remove(clicked_header)
    picked_headers_display.config(state=tk.NORMAL)
    picked_headers_display.delete("1.0", tk.END)
    picked_headers_display.insert(tk.END, ",\n".join(picked_headers))
    picked_headers_display.config(state=tk.DISABLED)





def start_combining():
        global paths_of_files_list
        combined_data.clear()
        if not paths_of_files_list:
            messagebox.showinfo("CSV Combiner", "Please select the files you want to combine first before attempting to combine them!")
            return
        if picked_headers:
            headers = [f.strip() for f in picked_headers]
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

picked_headers_display_frame = tk.Frame(window)
picked_headers_display_frame.pack()
picked_headers_display = tk.Text(picked_headers_display_frame, height=5, width=50, wrap=tk.WORD)
picked_headers_display.pack(side=tk.LEFT)
scrollbar = tk.Scrollbar(picked_headers_display_frame, command=picked_headers_display.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
picked_headers_display.config(yscrollcommand=scrollbar.set)
picked_headers_display.config(state=tk.DISABLED)


tk.Label(window).pack()
tk.Button(window, text="3- Start Combining!", command=start_combining).pack()




window.mainloop()