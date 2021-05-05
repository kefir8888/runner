# coding=utf-8

#from tkinter import *
import tkinter as tk
import time
import cv2
import threading
import imutils

from PIL import Image, ImageTk

#self.label = Label (self.master, text = "Controller")
#self.label.pack ()

#self.ip_entry = Entry(self.master, text="enter robot ip")
#self.ip_entry.pack (side=TOP)

#self.ip_button = Button (self.master, text="изменить ip", command = self.change_ip)
#self.ip_button.pack (side=TOP)

#self.wiki_button = Button (self.master, text="Поиск в Википедии", command = self.set_wiki_search)
#self.wiki_button.pack (side=TOP)

#self.close_button = Button (self.master, text = "Close", command = self.join_and_exit)
#self.close_button.pack (side=TOP)

class Main_window:
    def __init__ (self, root, lmain):
        self.root = root
        self.root.title ("Controller")

        self.lmain = lmain
        self.cap = cv2.VideoCapture(0)

        #self.label = Label (self.master, text = "Controller").grid (row=0)
        
        self.ip_entry = tk.Entry(self.root, text="enter robot ip")
        self.ip_entry.pack(side="bottom", fill="both", expand="yes", padx=10, pady=10)
        #self.ip_entry.grid (row=0, column=0)
        
        self.ip_button = tk.Button (self.root, text="Изменить ip", command = self.change_ip, height=3, width = 25)
        #self.ip_button.grid (row=1, column=0)
        self.football_button = tk.Button (self.root, text="Футбол", command = self.set_play_football, height=3, width = 25)
        #self.football_button.grid (row=8, column=0)

        self.football_button = tk.Button (self.root, text="Остановить футбол", command = self.stop_football, height=3, width = 25)
        #self.football_button.grid (row=8, column=1)

        self.close_button = tk.Button (self.root, text = "Закрыть", command = self.join_and_exit, height=3, width = 25)
        #self.close_button.grid (row=7, column=2)

        #self.robot_state = robot_state_

        self.panel = None

        self.stopEvent = threading.Event()
        self.thread = threading.Thread(target=self.videoLoop, args=())
        self.thread.start()
        # set a callback to handle when the window is closed
        #self.root.wm_title("PyImageSearch PhotoBooth")
        self.root.wm_protocol("WM_DELETE_WINDOW", self.join_and_exit)

        #self.idle ()

    def videoLoop(self):
        # DISCLAIMER:
        # I'm not a GUI developer, nor do I even pretend to be. This
        # try/except statement is a pretty ugly hack to get around
        # a RunTime error that Tkinter throws due to threading
        try:
            # keep looping over frames until we are instructed to stop
            while not self.stopEvent.is_set():
                # grab the frame from the video stream and resize it to
                # have a maximum width of 300 pixels
                _, self.frame = self.cap.read()
                self.frame = imutils.resize(self.frame, width=100)

                # OpenCV represents images in BGR order; however PIL
                # represents images in RGB order, so we need to swap
                # the channels, then convert to PIL and ImageTk format
                image = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
                image = Image.fromarray(image)
                image = ImageTk.PhotoImage(image)

                # if the panel is not None, we need to initialize it
                if self.panel is None:
                    self.panel = tk.Label(image=image)
                    self.panel.image = image
                    self.panel.pack(side="left", padx=10, pady=10)

                # otherwise, simply update the panel
                else:
                    self.panel.configure(image=image)
                    self.panel.image = image
        except RuntimeError:
            print("[INFO] caught a RuntimeError")

    def idle (self):
        #self.robot_state.on_idle ()
        
        self.root.after (1000, self.idle)

        # _, frame = self.cap.read()
        # #frame = cv2.flip(frame, 1)
        # cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
        # img = Image.fromarray(cv2image)
        # imgtk = ImageTk.PhotoImage(image=img)
        # self.lmain.imgtk = imgtk
        # self.lmain.configure(image=imgtk)
        # # self.lmain.after(10, show_frame)

        # img = ImageTk.PhotoImage(image=Image.fromarray(cv2image [:300, :300, :]))
        #
        # if self.lmain is None:
        #     self.lmain = tki.Label(image=img)
        #     self.lmain.image = img
        #     self.lmain.pack(side="left", padx=10, pady=10)
        #
        #     # otherwise, simply update the panel
        # else:
        #     print("mlem")
        #     self.lmain.configure(image=img)
        #     self.lmain.image = img


        # self.lmain.imgtk = img
        # self.lmain.configure(image=img)
        # #self.lmain.image = img
        #
        # self.lmain.after(10, show_frame)

        # canvas = tk.Canvas(self.master, width=300, height=300)
        # canvas.pack()
        # canvas.create_image(20, 20, anchor="nw", image=imgtk)

    def join_and_exit (self):
        #self.robot_state.join ()

        self.cap.release()

        self.root.quit ()

    def change_ip (self):
        new_ip = self.ip_entry.get()
        
        print ("new ip is", new_ip)
        
        #self.robot_state.change_ip (new_ip)

    def set_play_football (self):
        print ("changing robot state to play_football")
        command = {"type"           : "state_change",
                   "execution_time" : 0,
                   "contents"       : "playing_football",
                   "parameter"      : None}
        
        self.robot_state.add_commands_to_queue ([command])

    def stop_football (self):
        print ("changing robot state to waiting")
        command = {"type"           : "state_change",
                   "execution_time" : 0,
                   "contents"       : "waiting",
                   "parameter"      : None}
        
        self.robot_state.add_commands_to_queue ([command])

def main():
    root = tk.Tk()
    root.geometry("430x580")

    lmain = tk.Label(root)
    lmain.pack(side="left", padx=10, pady=10)

    GUI = Main_window(root, lmain)

    root.mainloop()

if __name__ == '__main__':
    main()
