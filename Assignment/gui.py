import tkinter as tk
from tkinter import filedialog
from video_motion_handler import VideoMotionHandler

class MotionGUI:
    def __init__(self):
        # Create the main Tkinter window
        self.root = tk.Tk()
        self.root.title("Select Motion Detection")
        self.root.geometry("900x600")

        # Define the style for buttons
        button_style = {
            "font": ("Arial", 12),
            "bg": "#e0e0e0", 
            "fg": "black",  
            "padx": 20,
            "pady": 10,
            "width": 15 
        }

        # List of button names
        self.buttons = ["Choose Video", "Webcam Motion", "Exit"]

        # Create buttons with specified style
        for button_name in self.buttons:
            button = tk.Button(self.root, text=button_name, command=lambda name=button_name: self.handle_button_click(name), **button_style)
            button.pack(pady=10)

    def handle_button_click(self, button_name):
        if button_name == "Choose Video":
            # Open a file dialog to select a video file
            video_path = self.select_video_file()
            if video_path:
                if video_path.lower().endswith(('.mov', '.mp4')):
                    # Close any existing video handler and initialize a new one with the selected video
                    self.handle_exit()
                    self.video_handler = VideoMotionHandler(video_path)
                else:
                    print("Invalid video format. Please select a .MOV or .mp4 file.")
        elif button_name == "Webcam Motion":
            # Close any existing video handler and initialize a new one with webcam input (0)
            self.handle_exit()
            self.video_handler = VideoMotionHandler(0)
        elif button_name == "Exit":
            # Close the application
            self.handle_exit()

    def select_video_file(self):
        # Open a file dialog to select a video file with specific file types
        file_path = filedialog.askopenfilename(filetypes=[("Video Files", "*.mov;*.mp4")])
        return file_path

    def remove_motion_buttons(self):
        # Remove the "Choose Video" and "Webcam Motion" buttons
        for button_name in ["Choose Video", "Webcam Motion"]:
            for widget in self.root.winfo_children():
                if widget.winfo_class() == "Button" and widget.cget("text") == button_name:
                    widget.destroy()

    def handle_exit(self):
        # Close the main window and exit the application
        self.root.destroy()

    def run(self):
        # Start the main GUI event loop
        self.root.mainloop()
