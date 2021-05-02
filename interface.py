# coding=utf-8

from tkinter import *#Label, Button, Entry
import time

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
    def __init__ (self, master_, robot_state_):
        self.master = master_
        self.master.title ("Controller")

        #self.label = Label (self.master, text = "Controller").grid (row=0)
        
        self.ip_entry = Entry(self.master, text="enter robot ip")
        self.ip_entry.grid (row=0, column=0)
        
        self.ip_button = Button (self.master, text="Изменить ip", command = self.change_ip, height=3, width = 25)
        self.ip_button.grid (row=1, column=0)
        self.football_button = Button (self.master, text="Футбол", command = self.set_play_football, height=3, width = 25)
        self.football_button.grid (row=8, column=0)

        self.football_button = Button (self.master, text="Остановить футбол", command = self.stop_football, height=3, width = 25)
        self.football_button.grid (row=8, column=1)

        self.close_button = Button (self.master, text = "Закрыть", command = self.join_and_exit, height=3, width = 25)
        self.close_button.grid (row=7, column=2)

        self.robot_state = robot_state_
        
        self.idle ()

    def idle (self):
        self.robot_state.on_idle ()
        
        self.master.after (1000, self.idle)

    def join_and_exit (self):
        #self.robot_state.join ()
        self.master.quit ()

    def change_ip (self):
        new_ip = self.ip_entry.get()
        
        print ("new ip is", new_ip)
        
        self.robot_state.change_ip (new_ip)

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
    root = Tk()
    root.geometry("730x580")

    GUI = Main_window(root, robot_state)

    root.mainloop()

if __name__ == '__main__':
    main()
