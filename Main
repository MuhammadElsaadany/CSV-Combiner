import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox

import csv

selected_paths = []
combined_data = []
seen = []
picked = []


def files_selection():
    global selected_paths
    seen.clear()
    picked.clear()
    paths = filedialog.askopenfilenames(filetypes=[("CSV files", "*.csv")])
    if not paths:
        fields_display.config(state=tk.NORMAL)
        fields_display.delete("1.0", tk.END)
        fields_display.config(state=tk.DISABLED)
        fields_picked_display.config(state=tk.NORMAL)
        fields_picked_display.delete("1.0", tk.END)
        fields_picked_display.config(state=tk.DISABLED)
        amount_var.set("Files Selected = " + str(len(paths)) + " File/s")
        messagebox.showinfo("CSV Combiner", "Please select the files you want to combine!")
    else:
        amount_var.set("Files Selected = " + str(len(paths)) + " File/s")
        selected_paths = paths
        for i in selected_paths:
            with open(i, mode="r", encoding="utf-8-sig") as file:
                reader = csv.DictReader(file)
                for field in reader.fieldnames:
                    if field not in seen:
                        seen.append(field)
                fields_display.config(state=tk.NORMAL)
                fields_display.delete("1.0", tk.END)
                fields_display.insert(tk.END,",\n".join(seen), "clickable")
                fields_display.tag_config("clickable", foreground="blue", underline=True)
                fields_display.tag_bind("clickable", "<Button-1>", on_field_click)
                fields_display.config(state=tk.DISABLED)
                fields_picked_display.config(state=tk.NORMAL)
                fields_picked_display.delete("1.0", tk.END)
                fields_picked_display.config(state=tk.DISABLED)

def on_field_click(event):
    index = fields_display.index(f"@{event.x},{event.y}")
    line_start = fields_display.index(f"{index} linestart")
    line_end = fields_display.index(f"{index} lineend")
    clicked_line = fields_display.get(line_start, line_end)
    clicked_field = clicked_line.strip(",").strip()

    if clicked_field not in picked:
        picked.append(clicked_field)
    else:
        picked.remove(clicked_field)
    fields_picked_display.config(state=tk.NORMAL)
    fields_picked_display.delete("1.0", tk.END)
    fields_picked_display.insert(tk.END, ",\n".join(picked))
    fields_picked_display.config(state=tk.DISABLED)





def start_combining():
        global selected_paths
        combined_data.clear()
        if not selected_paths:
            messagebox.showinfo("CSV Combiner", "Please select the files you want to combine first before attempting to combine them!")
            return
        if picked:
            fields = [f.strip() for f in picked]
        else:
            messagebox.showinfo("CSV Combiner", "Please select fields to combine!")
            return
        for i in selected_paths:
            with open(i, mode="r", encoding="utf-8-sig") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    combined_row = {}
                    for field in fields:
                        if field in row:
                            combined_row[field] = row[field]
                    if combined_row:
                        combined_data.append(combined_row)
        final_file_path = filedialog.asksaveasfilename(title="Save your CSV file",defaultextension=".csv",filetypes=[("CSV files", "*.csv"), ("All files", "*.*")])
        if not final_file_path:
            return
        with open(final_file_path, mode='w', newline='', encoding="utf-8-sig") as finalfile:
            writer = csv.DictWriter(finalfile, fieldnames=fields)
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
tk.Label(window, text="Total Field Names In These Files:").pack()

fields_display_frame = tk.Frame(window)
fields_display_frame.pack()
fields_display = tk.Text(fields_display_frame, height=5, width=50, wrap=tk.WORD)
fields_display.pack(side=tk.LEFT)
scrollbar = tk.Scrollbar(fields_display_frame, command=fields_display.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
fields_display.config(yscrollcommand=scrollbar.set)
fields_display.config(state=tk.DISABLED)

tk.Label(window, text="2- Click The Blue Field Names You Want To Combine (click again to remove!):").pack()

fields_picked_display_frame = tk.Frame(window)
fields_picked_display_frame.pack()
fields_picked_display = tk.Text(fields_picked_display_frame, height=5, width=50, wrap=tk.WORD)
fields_picked_display.pack(side=tk.LEFT)
scrollbar = tk.Scrollbar(fields_picked_display_frame, command=fields_picked_display.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
fields_picked_display.config(yscrollcommand=scrollbar.set)
fields_picked_display.config(state=tk.DISABLED)


tk.Label(window).pack()
tk.Button(window, text="3- Start Combining!", command=start_combining).pack()




window.mainloop()