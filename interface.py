# coding=utf-8

from tkinter import *#Label, Button, Entry
import time
import os

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
    def __init__ (self, master_):
        self.master = master_
        self.master.title ("runner")
        self.label = Label (self.master, text = "runner").grid (row=0)
        
        self.robot_ip = "192.168.31.25"
        
        self.roscore_deploy = False
        
        #IP
        self.ip_entry = Entry(self.master, text="enter robot ip")
        self.ip_entry.grid (row=0, column=0)
        self.ip_button = Button (self.master, text="change ip (now " + str(self.robot_ip) + " )", command = self.change_ip, height=3, width = 25)
        self.ip_button.grid (row=1, column=0)
        
        #ROSCORE
        self.roscore_button = Button (self.master, text="roscore offline", command = self.roscore, height=3, width = 25, bg = "red")
        self.roscore_button.grid (row=8, column=0)

	#TELEOP
        #self.roscore_button = Button (self.master, text="roscore offline", command = self.roscore, height=3, width = 25)
        #self.roscore_button.grid (row=8, column=0)

	#CALIBRATION
        self.calibration_button = Button (self.master, text="calibration offline", command = self.calibration, height=3, width = 25)
        self.calibration_button.grid (row=8, column=1)

	#SCRIPT
        #self.roscore_button = Button (self.master, text="roscore offline", command = self.roscore, height=3, width = 25)
        #self.roscore_button.grid (row=8, column=0)

        self.close_button = Button (self.master, text = "Закрыть", command = self.join_and_exit, height=3, width = 25)
        self.close_button.grid (row=7, column=2)
        
        self.idle ()

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
    	if (self.roscore_deploy == True):
    	    os.system("sshpass -p turtlebot ssh pi@192.168.31.25 pkill -f roslaunch")
    	    
    	    self.calibration_deploy = False
    	    
    	    self.roscore_button.configure(bg = "red")
    	    self.roscore_button.configure(text = "calibration offline")
    	
    	else:
    	    #os.system("sshpass -p turtlebot ssh pi@192.168.31.25 'nohup /home/pi/ros_catkin_ws/src/ros_comm/roslaunch/scripts/roslaunch turtlebot3_bringup turtlebot3_robot.launch > /dev/null 2>&1 &'")
    	    #os.system("sshpass -p turtlebot ssh pi@192.168.31.25 'whoami'")
    	    
    	    #os.system("sshpass -p turtlebot ssh pi@192.168.31.25 'bash -ic 'roslaunch turtlebot3_bringup turtlebot3_robot.launch''")
    	    os.system("sshpass -p turtlebot ssh pi@192.168.31.25 /home/pi/bringup_wrapper.sh")
    	    
    	    
    	    self.calibration_deploy = True
    	    
    	    self.roscore_button.configure(bg = "green")
    	    self.roscore_button.configure(text = "calibration deploy")

    def idle (self):
        self.master.after (1000, self.idle)
        
        self.handle_camera()
    
    def handle_camera(self):
    	pass

    def join_and_exit (self):
        self.master.quit ()

def main():
    root = Tk()
    root.geometry("730x280")

    GUI = Main_window(root)

    root.mainloop()

if __name__ == '__main__':
    main()
