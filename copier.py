import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import shutil
import os

class SelectedFilesWindow:
    def __init__(self, master, selected_files, on_close):

        self.master = master
        self.selected_files = selected_files
        self.on_close = on_close

        self.top = tk.Toplevel(self.master)
        self.top.title("Selected Files")

        # Set the fixed window size
        self.top.geometry("600x400")
        self.top.resizable(False, False)


        self.label = tk.Label(self.top, text="Selected Files:", font=("Helvetica", 14), fg="#333")
        self.label.pack(pady=(10, 5))

        self.scrollbar = tk.Scrollbar(self.top, orient="vertical")
        self.listbox = tk.Listbox(self.top, selectmode=tk.MULTIPLE, font=("Arial", 12), yscrollcommand=self.scrollbar.set)
        self.listbox.pack(pady=(0, 10), fill="both", expand=True)
        self.scrollbar.config(command=self.listbox.yview)
        self.scrollbar.pack(side="right", fill="y")

        for file_path in selected_files:
            self.listbox.insert(tk.END, file_path)

        self.close_button = tk.Button(self.top, text="Close", command=self.close_window_and_clear, bg="#3498db", fg="white", font=("Arial", 12))
        self.close_button.pack(pady=(5, 10), fill="both", expand=True)
        self.on_close = on_close  # Store the callback function

        self.delete_button = tk.Button(self.top, text="Delete", command=self.delete_selected_files, bg="#e74c3c", fg="white", font=("Arial", 12))
        self.delete_button.pack(pady=(5, 10), fill="both", expand=True)

    def close_window_and_clear(self):
        self.top.destroy()
        self.on_close()

    def delete_selected_files(self):
        selected_indices = self.listbox.curselection()
        for index in reversed(selected_indices):
            self.listbox.delete(index)
            del self.selected_files[index]



class FileCopyApp:
    def __init__(self, master):
        self.master = master
        self.master.title("File Copy Application")

        self.selected_destinations = []

        # Set the theme
        style = ttk.Style()
        style.theme_use("clam")  # You can try other themes like "vista", "xpnative", etc.

        # Set fixed window size and disable resizing
        self.master.geometry("420x700")
        self.master.resizable(False, False)

        # Create a canvas with a vertical scrollbar
        self.canvas = tk.Canvas(master)
        self.scrollbar = tk.Scrollbar(master, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        # Pack the canvas and scrollbar
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        # Create a frame inside the canvas
        self.frame = tk.Frame(self.canvas)

        # Add the frame to the canvas window
        self.canvas.create_window((0, 0), window=self.frame, anchor="nw")

        # Bind the frame to the scrollbar
        self.frame.bind("<Configure>", self.on_frame_configure)

        # Center the content
        self.master.grid_rowconfigure(0, weight=1)
        self.master.grid_columnconfigure(0, weight=1)

        # Selected Files
        self.files_frame = tk.Frame(self.frame)
        self.files_frame.pack(side="top", fill="both", expand=True)

        self.add_files_button = tk.Button(self.files_frame, text="Add Files", command=self.add_files, bg="#4CAF50", fg="white", font=("Arial", 12),width=43)
        self.add_files_button.grid(row=1, column=0, pady=(10, 5), sticky="ew")

        self.clear_files_button = tk.Button(self.files_frame, text="Clear Files", command=self.clear_files, bg="#FF5733", fg="white", font=("Arial", 12),width=43)
        self.clear_files_button.grid(row=2, column=0, pady=(0, 10), sticky="ew")

        self.selected_files_window = None  # Reference to the selected files window

        # Destinations
        self.destination1_label = tk.Label(self.frame, text="Destination 1:", font=("Helvetica", 14), fg="#333")
        self.destination1_label.pack(side="top", pady=(10, 5), anchor="w")

        self.destination1_entry = tk.Entry(self.frame)
        self.destination1_entry.pack(side="top", pady=(0, 10), fill="both", expand=True)

        self.clear_dest1_button = tk.Button(self.frame, text="Clear", command=lambda: self.clear_destination(1), bg="#FF5733", fg="white", font=("Arial", 10))
        self.clear_dest1_button.pack(side="top", pady=(0, 10), fill="both", expand=True)

        self.destination2_label = tk.Label(self.frame, text="Destination 2:", font=("Helvetica", 14), fg="#333")
        self.destination2_label.pack(side="top", pady=(10, 5), anchor="w")

        self.destination2_entry = tk.Entry(self.frame)
        self.destination2_entry.pack(side="top", pady=(0, 10), fill="both", expand=True)

        self.clear_dest2_button = tk.Button(self.frame, text="Clear", command=lambda: self.clear_destination(2), bg="#FF5733", fg="white", font=("Arial", 10))
        self.clear_dest2_button.pack(side="top", pady=(0, 10), fill="both", expand=True)

        self.destination3_label = tk.Label(self.frame, text="Destination 3:", font=("Helvetica", 14), fg="#333")
        self.destination3_label.pack(side="top", pady=(10, 5), anchor="w")

        self.destination3_entry = tk.Entry(self.frame)
        self.destination3_entry.pack(side="top", pady=(0, 10), fill="both", expand=True)

        self.clear_dest3_button = tk.Button(self.frame, text="Clear", command=lambda: self.clear_destination(3), bg="#FF5733", fg="white", font=("Arial", 10))
        self.clear_dest3_button.pack(side="top", pady=(0, 10), fill="both", expand=True)

        self.add_destination_button = tk.Button(self.frame, text="Add Destination", command=self.add_destination, bg="#4CAF50", fg="white", font=("Arial", 12))
        self.add_destination_button.pack(side="top", pady=(0, 10), fill="both", expand=True)

        self.clear_destinations_button = tk.Button(self.frame, text="Clear Destinations", command=self.clear_destinations, bg="#FF5733", fg="white", font=("Arial", 12))
        self.clear_destinations_button.pack(side="top", pady=(0, 10), fill="both", expand=True)

        # Copy and Cut Buttons
        self.copy_button = tk.Button(self.frame, text="Copy Files", command=self.copy_files, bg="#3498db", fg="white", font=("Arial", 12))
        self.copy_button.pack(side="top", pady=(10, 5), fill="both", expand=True)

        self.cut_button = tk.Button(self.frame, text="Cut Files", command=self.cut_files, bg="#e74c3c", fg="white", font=("Arial", 12))
        self.cut_button.pack(side="top", pady=(5, 20), fill="both", expand=True)

        # Success Label
        self.success_label = tk.Label(self.frame, text="", font=("Helvetica", 12, "italic"), fg="#27ae60")
        self.success_label.pack(side="top", pady=(0, 10), fill="both", expand=True)

        # Developer Information
        self.developer_label = tk.Label(self.frame, text="Developed By arcTech (2024) pilot applications association with AI", font=("Arial", 10), fg="#333")
        self.developer_label.pack(side="bottom", pady=(10, 5), anchor="w")

        self.selected_files_window = None  # Added for tracking the SelectedFilesWindow instance
        self.selected_files = []
        self.selected_destinations = []  #

    def close_selected_files_window(self):
        if self.selected_files_window:
            self.selected_files_window = None
            self.clear_files()

    def on_frame_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def add_files(self):
        file_paths = filedialog.askopenfilenames()
        if file_paths:
            self.selected_files = list(file_paths)
            self.success_label.config(text="")  # Clear success message when new files are added

            # Open a new window to display selected files
            self.selected_files_window = SelectedFilesWindow(self.master, self.selected_files, self.close_selected_files_window)


    def clear_files(self):
        self.selected_files = []
        self.success_label.config(text="")  # Clear success message when files are cleared

        # Close the selected files window if it is open
        if self.selected_files_window:
            self.selected_files_window.close_window_and_clear()


    def close_selected_files_window(self):
        self.selected_files_window = None

    def add_destination(self):
        destination_path = filedialog.askdirectory()
        if destination_path:
            self.selected_destinations.append(destination_path)

            # Display selected destinations in entry fields
            self.display_destinations()

    def clear_destination(self, index):
        if 1 <= index <= len(self.selected_destinations):
            self.selected_destinations.pop(index - 1)
            self.display_destinations()

    def display_destinations(self):
        entries = [self.destination1_entry, self.destination2_entry, self.destination3_entry]
        for i, entry in enumerate(entries):
            if i < len(self.selected_destinations):
                entry.delete(0, tk.END)
                entry.insert(0, self.selected_destinations[i])
            else:
                entry.delete(0, tk.END)

    def clear_destinations(self):
        self.selected_destinations = []
        self.display_destinations()
        self.success_label.config(text="")  # Clear success message when destinations are cleared

    def copy_files(self):
        if not self.selected_files:
            self.show_error("No Files selected. Please add Files.")
            return

        if not self.selected_destinations:
            self.show_error("No destinations selected. Please add at least one destination.")
            return

        success_message = "Files successfully copied to:\n"
        for source_path in self.selected_files:
            for destination in self.selected_destinations:
                try:
                    if os.path.exists(destination):
                        destination_path = os.path.join(destination, os.path.basename(source_path))
                        if os.path.exists(destination_path):
                            raise FileExistsError(f"File/Folder already exists at destination: {destination}")

                        if os.path.isdir(source_path):
                            shutil.copytree(source_path, destination_path)
                            print(f"Folder copied to {destination}")
                        else:
                            shutil.copy(source_path, destination)
                            print(f"File copied to {destination}")

                        success_message += f"- {destination}\n"
                except FileExistsError as fe:
                    self.show_error(str(fe))
                    return
                except Exception as e:
                    print(f"Error copying file/folder to {destination}: {e}")

        self.success_label.config(text=success_message)

    def cut_files(self):
        if not self.selected_files:
            self.show_error("No Files selected. Please add Files.")
            return

        if not self.selected_destinations:
            self.show_error("No destinations selected. Please add at least one destination.")
            return

        success_message = "Files successfully moved to:\n"
        for source_path in self.selected_files:
            for destination in self.selected_destinations:
                try:
                    if os.path.exists(destination):
                        destination_path = os.path.join(destination, os.path.basename(source_path))
                        if os.path.exists(destination_path):
                            raise FileExistsError(f"File/Folder already exists at destination: {destination}")

                        if os.path.isdir(source_path):
                            shutil.move(source_path, destination_path)
                            print(f"Folder moved to {destination}")
                        else:
                            shutil.move(source_path, destination)
                            print(f"File moved to {destination}")

                        success_message += f"- {destination}\n"
                except FileExistsError as fe:
                    self.show_error(str(fe))
                    return
                except Exception as e:
                    print(f"Error moving file/folder to {destination}: {e}")

        # Clear the selected files after a successful move
        self.selected_files = []

        self.success_label.config(text=success_message)

    def show_error(self, message):
        messagebox.showerror("Error", message)

if __name__ == "__main__":
    root = tk.Tk()
    app = FileCopyApp(root)
    root.mainloop()
