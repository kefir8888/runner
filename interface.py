# coding=utf-8

import numpy as np
import tkinter as tk
import time
import os

import threading
import imutils

import cv2

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

def order_points(pts):
    rect = np.zeros((4, 2), dtype="float32")
    s = pts.sum(axis=1)

    min_ind = np.argmin(s)
    max_ind = np.argmax(s)

    rect[0] = pts[min_ind]
    rect[2] = pts[max_ind]

    inds = [_ for _ in range(4)]
    inds.remove(min_ind)
    inds.remove(max_ind)

    #print(inds)

    without = np.array ([pts[i] for i in inds])

    diff = np.diff(without, axis=1)

    #print(without)

    rect[1] = without[np.argmin(diff)]
    rect[3] = without[np.argmax(diff)]

    return rect

def get_transform(pts):
    rect = order_points(pts)

    (tl, tr, br, bl) = rect

    widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
    widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
    maxWidth = max(int(widthA), int(widthB))

    heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
    heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
    maxHeight = max(int(heightA), int(heightB))

    dst = np.array([
        [0, 0],
        [maxWidth - 1, 0],
        [maxWidth - 1, maxHeight - 1],
        [0, maxHeight - 1]], dtype="float32")

    M = cv2.getPerspectiveTransform(rect, dst)

    return (M, (maxWidth, maxHeight))

def apply_transform(image, transform):
    warped = cv2.warpPerspective(image, transform[0], transform[1])

    return warped


class Main_window:
    def __init__ (self, root, lmain):
        self.root = root
        self.lmain = lmain
        self.cap = cv2.VideoCapture(2)
        
        self.points = np.array([[15, 255], [256, 149], [535, 193], [330, 340]])
        self.transform = get_transform(self.points)
        
        #self.root.title ("runner")
        #self.label = tk.Label (self.root, text = "runner").grid (row=0)
        
        self.robot_ip = "192.168.31.25"
        
        self.roscore_deploy = False
        self.calibration_deploy = False
        self.script_deploy = False
        
        #IP
        self.ip_entry = tk.Entry(self.root, text="enter robot ip")
        #self.ip_entry.grid (row=0, column=0)
        self.ip_button = tk.Button (self.root, text="change ip (now " + str(self.robot_ip) + " )", command = self.change_ip, height=3, width = 25)
        self.ip_entry.pack(side="bottom", expand="no", padx=10, pady=10)
        #self.ip_button.grid (row=1, column=0)
        
        #ROSCORE
        self.roscore_button = tk.Button (self.root, text="roscore offline", command = self.roscore, height=3, width = 25, bg = "red")
        self.roscore_button.pack(side="bottom", expand="no", padx=10, pady=10)
        #self.roscore_button.grid (row=8, column=0)

	#TELEOP
        #self.roscore_button = Button (self.master, text="roscore offline", command = self.roscore, height=3, width = 25)
        #self.roscore_button.grid (row=8, column=0)

	#CALIBRATION
        self.calibration_button = tk.Button (self.root, text="calibration offline", command = self.calibration, height=3, width = 25)
        self.calibration_button.pack(side="bottom", expand="no", padx=10, pady=10)
        #self.calibration_button.grid (row=8, column=1)

	#SCRIPT
        self.script_button = tk.Button (self.root, text="script offline", command = self.script, height=3, width = 25)
        self.script_button.pack(side="bottom", padx=10, pady=10)
        
        self.close_button = tk.Button (self.root, text = "Закрыть", command = self.join_and_exit, height=3, width = 25)
        self.close_button.pack(side="bottom", expand="no", padx=10, pady=10)
        #self.close_button.grid (row=7, column=2)
        
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
                #self.frame = imutils.resize(self.frame, width=400)

                # OpenCV represents images in BGR order; however PIL
                # represents images in RGB order, so we need to swap
                # the channels, then convert to PIL and ImageTk format
                image = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
                warped = apply_transform(image, self.transform)
                
                img_sh = image.shape
                warped_resized = cv2.resize(warped, (img_sh[1], img_sh[0]))
                
                concat = np.concatenate((image, warped_resized), axis=1)
                
                #img = Image.fromarray(warped)
                #img = Image.fromarray(image)
                img = Image.fromarray(concat)
                
                image = ImageTk.PhotoImage(img)

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


    def change_ip (self):
        new_ip = self.ip_entry.get()
        
        #print ("new ip is", new_ip)
        
        self.robot_ip = new_ip
        self.roscore_button.configure(text = "change ip (now " + str(self.robot_ip) + " )")

    def roscore(self):
    	if (self.roscore_deploy == True):
    	    os.system("pkill -f roscore")
    	    
    	    self.roscore_deploy = False
    	    
    	    self.roscore_button.configure(bg = "red")
    	    self.roscore_button.configure(text = "roscore offline")
    	
    	else:
    	    os.system("nohup roscore > /dev/null 2>&1 &")
    	    
    	    self.roscore_deploy = True
    	    
    	    self.roscore_button.configure(bg = "green")
    	    self.roscore_button.configure(text = "roscore deploy")

    def calibration(self):
    	if (self.calibration_deploy == True):
    	    os.system("sshpass -p turtlebot ssh pi@192.168.31.25 pkill -f roslaunch")
    	    
    	    self.calibration_deploy = False
    	    
    	    self.calibration_button.configure(bg = "red")
    	    self.calibration_button.configure(text = "calibration offline")
    	
    	else:
    	    #os.system("sshpass -p turtlebot ssh pi@192.168.31.25 'nohup /home/pi/ros_catkin_ws/src/ros_comm/roslaunch/scripts/roslaunch turtlebot3_bringup turtlebot3_robot.launch > /dev/null 2>&1 &'")
    	    #os.system("sshpass -p turtlebot ssh pi@192.168.31.25 'whoami'")
    	    
    	    #os.system("sshpass -p turtlebot ssh pi@192.168.31.25 'bash -ic 'roslaunch turtlebot3_bringup turtlebot3_robot.launch''")
    	    os.system("sshpass -p turtlebot ssh -i pi@192.168.31.25 /home/pi/bringup_wrapper.sh")
    	    
    	    
    	    self.calibration_deploy = True
    	    
    	    self.calibration_button.configure(bg = "green")
    	    self.calibration_button.configure(text = "calibration deploy")

    def script(self):
    	if (self.script_deploy == True):
    	    os.system("pkill -f main_3wrobot_ros.py")
    	    
    	    self.script_deploy = False
    	    
    	    self.script_button.configure(bg = "red")
    	    self.script_button.configure(text = "calibration offline")
    	
    	else:
    	    os.system("python3 /home/aidalab/cruzhochki/rcognita/main_3wrobot_ros.py --init_x 2 --init_y 2 --init_alpha 3.14 --dt 0.1 --Nactor 8 --pred_step_size 9 --mode 3")
    	    
    	    self.script_deploy = True
    	    
    	    self.script_button.configure(bg = "green")
    	    self.script_button.configure(text = "script deploy")

    def idle (self):
        self.master.after (1000, self.idle)
        
        self.handle_camera()
    
    def handle_camera(self):
    	pass

    def join_and_exit (self):
        self.cap.release()
        
        self.root.quit ()

def main():
    root = tk.Tk()
    root.geometry("1530x1080")

    lmain = tk.Label(root)
    lmain.pack(side="left", padx=10, pady=10)

    GUI = Main_window(root, lmain)

    root.mainloop()

if __name__ == '__main__':
    main()
