import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import shutil
import os

class FileCopyApp:
    def __init__(self, master):
        self.master = master
        self.master.title("File Copy Application")

        # Set the theme
        style = ttk.Style()
        style.theme_use("clam")  # You can try other themes like "vista", "xpnative", etc.

        # Set fixed window size and disable resizing
        self.master.geometry("600x700")
        self.master.resizable(False, False)

        # Center the content
        self.master.grid_rowconfigure(0, weight=1)
        self.master.grid_columnconfigure(0, weight=1)

        # Selected Files
        self.files_label = tk.Label(master, text="Selected Files:", font=("Helvetica", 14), fg="#333")
        self.files_label.grid(row=0, column=0, columnspan=2, pady=(10, 5), sticky="n")

        self.add_files_button = tk.Button(master, text="Add Files", command=self.add_files, bg="#4CAF50", fg="white", font=("Arial", 12))
        self.add_files_button.grid(row=1, column=0, pady=(0, 10), sticky="ew")

        self.clear_files_button = tk.Button(master, text="Clear Files", command=self.clear_files, bg="#FF5733", fg="white", font=("Arial", 12))
        self.clear_files_button.grid(row=2, column=0, pady=(0, 10), sticky="ew")

        # Destinations
        self.destination1_label = tk.Label(master, text="Destination 1:", font=("Helvetica", 14), fg="#333")
        self.destination1_label.grid(row=3, column=0, columnspan=2, pady=(10, 5), sticky="n")

        self.destination1_entry = tk.Entry(master)
        self.destination1_entry.grid(row=4, column=0, pady=(0, 10), sticky="ew", columnspan=2)

        self.clear_dest1_button = tk.Button(master, text="Clear", command=lambda: self.clear_destination(1), bg="#FF5733", fg="white", font=("Arial", 10))
        self.clear_dest1_button.grid(row=4, column=3, pady=(0, 10), sticky="ew")

        self.destination2_label = tk.Label(master, text="Destination 2:", font=("Helvetica", 14), fg="#333")
        self.destination2_label.grid(row=5, column=0, columnspan=2, pady=(10, 5), sticky="n")

        self.destination2_entry = tk.Entry(master)
        self.destination2_entry.grid(row=6, column=0, pady=(0, 10), sticky="ew", columnspan=2)

        self.clear_dest2_button = tk.Button(master, text="Clear", command=lambda: self.clear_destination(2), bg="#FF5733", fg="white", font=("Arial", 10))
        self.clear_dest2_button.grid(row=6, column=3, pady=(0, 10), sticky="ew")

        self.destination3_label = tk.Label(master, text="Destination 3:", font=("Helvetica", 14), fg="#333")
        self.destination3_label.grid(row=7, column=0, columnspan=2, pady=(10, 5), sticky="n")

        self.destination3_entry = tk.Entry(master)
        self.destination3_entry.grid(row=8, column=0, pady=(0, 10), sticky="ew", columnspan=2)

        self.clear_dest3_button = tk.Button(master, text="Clear", command=lambda: self.clear_destination(3), bg="#FF5733", fg="white", font=("Arial", 10))
        self.clear_dest3_button.grid(row=8, column=3, pady=(0, 10), sticky="ew")

        self.add_destination_button = tk.Button(master, text="Add Destination", command=self.add_destination, bg="#4CAF50", fg="white", font=("Arial", 12))
        self.add_destination_button.grid(row=9, column=0, pady=(0, 10), sticky="ew")

        self.clear_destinations_button = tk.Button(master, text="Clear Destinations", command=self.clear_destinations, bg="#FF5733", fg="white", font=("Arial", 12))
        self.clear_destinations_button.grid(row=10, column=0, pady=(0, 10), sticky="ew")

        # Copy and Cut Buttons
        self.copy_button = tk.Button(master, text="Copy Files", command=self.copy_files, bg="#3498db", fg="white", font=("Arial", 12))
        self.copy_button.grid(row=11, column=0, pady=(10, 5), sticky="ew")

        self.cut_button = tk.Button(master, text="Cut Files", command=self.cut_files, bg="#e74c3c", fg="white", font=("Arial", 12))
        self.cut_button.grid(row=12, column=0, pady=(5, 20), sticky="ew")

        # Success Label
        self.success_label = tk.Label(master, text="", font=("Helvetica", 12, "italic"), fg="#27ae60")
        self.success_label.grid(row=13, column=0, columnspan=2, pady=(0, 10), sticky="ew")

        self.selected_files = []
        self.selected_destinations = []




    def add_files(self):
        file_paths = filedialog.askopenfilenames()
        if file_paths:
            self.selected_files = list(file_paths)
            self.files_label.config(text=f"Selected Files: {', '.join(self.selected_files)}")
            self.success_label.config(text="")  # Clear success message when new files are added

    def clear_files(self):
        self.selected_files = []
        self.files_label.config(text="Selected Files:")
        self.success_label.config(text="")  # Clear success message when files are cleared

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
        self.files_label.config(text="Selected Files:")

        self.success_label.config(text=success_message)

    def show_error(self, message):
        messagebox.showerror("Error", message)

if __name__ == "__main__":
    root = tk.Tk()
    app = FileCopyApp(root)
    root.mainloop()
