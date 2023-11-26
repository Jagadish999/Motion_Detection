import os
import cv2
from tkinter import *
from PIL import Image, ImageTk
import numpy as np
from datetime import datetime

import cvlib
from cvlib.object_detection import draw_bbox

class VideoMotionHandler:
    def __init__(self, vidPath):
        # Create the main Tkinter window
        self.root = Tk()
        self.root.geometry("700x740")
        self.root.configure(bg="black")
        self.vidPath = vidPath
        self.motionFrame = []  # Initialize a list to store frames with motion detected
        self.exitTracker = False

        element_style = {
            "font": ("Arial", 16),
            "bg": "black",
            "fg": "white",
        }

        print("Webcam Motion button clicked!")

        # Create a title label
        if self.vidPath == 0:

            label_title = Label(self.root, text="Webcam Motion Detection", font=("times new roman", 30, "bold"), bg="black", fg="red")

        else:
            label_title = Label(self.root, text="Video Motion Detection", font=("times new roman", 30, "bold"), bg="black", fg="red")
        label_title.pack()

        # Create a label frame for displaying the webcam feed
        f1 = LabelFrame(self.root, bg="red")
        f1.pack()
        L1 = Label(f1, bg="red")
        L1.pack()

        # Open the video source (file or webcam)
        cap = cv2.VideoCapture(self.vidPath)

        # Create an "Exit" button
        exit_button = Button(self.root, text="Exit", **element_style)
        exit_button.pack(pady=10)
        exit_button.config(command=self.exit_button_click)

        frames = []  # Initialize a list to store frames

        while True:
            ret, frame = cap.read()
            if ret:
                # Resize and convert the frame
                frame = cv2.resize(frame, dsize=(600, 400))
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                normalFrame = frame
                frames.append(frame)

                #code from lecture slide from frame_diff to eroded_diff
                if len(frames) > 1:
                    first_frame_to_float = np.float32(frames[len(frames) -1])
                    second_frame_to_float = np.float32(frames[len(frames) -2])

                    frame_diff = (first_frame_to_float - second_frame_to_float) ** 2
                    frame_diff_allchannel = np.sum(frame_diff, axis=2)

                    thresholded_diff = frame_diff_allchannel > 500

                    k_r = cv2.getStructuringElement(cv2.MORPH_ERODE, (5, 5))
                    eroded_diff = cv2.morphologyEx(np.float32(thresholded_diff), cv2.MORPH_RECT, k_r)

                    img = Image.fromarray((eroded_diff * 255).astype(np.uint8))
                    img = ImageTk.PhotoImage(image=img)

                    if eroded_diff.mean() * 10000 > 10:
   
                        bbox, labels, conf = cvlib.detect_common_objects(frame)
                        frame = draw_bbox(frame, bbox, labels, conf)

                        self.motionFrame.append(frame)  # Add frames with motion to the list

                        frame_pil = Image.fromarray(frame)

                        showAbleImg = ImageTk.PhotoImage(image=frame_pil)

                        L1.config(image=showAbleImg)
                        L1.image = showAbleImg
                    else:

                        normalFrame = ImageTk.PhotoImage(Image.fromarray(normalFrame))
                        L1.config(image=normalFrame)
                        L1.image = normalFrame

                else:
                    normalFrame = ImageTk.PhotoImage(Image.fromarray(normalFrame))
                    L1.config(image=normalFrame)
                    L1.image = normalFrame

                self.root.update()
            else:
                # When the video ends, save frames as images and create a video
                self.exitTracker = True
                self.save_frames_as_images(self.motionFrame)
                self.save_video(self.motionFrame)
                break

        cap.release()

    def save_frames_as_images(self, motionFrame):
        # Create a folder to save images
        now = datetime.now()
        folder_name = now.strftime("%Y%m%d%H%M%S") + "Images"
        folder_path = os.path.join("motion_details", "Images", folder_name)
        os.makedirs(folder_path, exist_ok=True)

        for i, frame in enumerate(motionFrame):
            frame_filename = os.path.join(folder_path, f"frame_{i}.png")
            cv2.imwrite(frame_filename, cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))

    def save_video(self, motionFrame):
        # Create a folder to save videos
        now = datetime.now()
        folder_name = now.strftime("%Y%m%d%H%M%S") + "Videos"
        folder_path = os.path.join("motion_details", "Videos", folder_name)
        os.makedirs(folder_path, exist_ok=True)

        video_filename = os.path.join(folder_path, now.strftime("%Y%m%d%H%M%S") + ".avi")

        frame_width = motionFrame[0].shape[1]
        frame_height = motionFrame[0].shape[0]

        out = cv2.VideoWriter(video_filename, cv2.VideoWriter_fourcc(*'XVID'), 20.0, (frame_width, frame_height))

        for frame in motionFrame:
            out.write(frame)

        out.release()

    def exit_button_click(self):
        # Save frames as images and create a video before exiting

        if self.exitTracker == False:
            self.save_frames_as_images(self.motionFrame)
            self.save_video(self.motionFrame)
        self.root.destroy()  # Close the main window
