import os
import time
import tkinter
from tkinter import ttk, Label, Entry, StringVar, Button, RAISED, FLAT


class Timer:
    def __init__(self, parent):
        root.geometry("280x100")
        root.title("Таймер выключения пк")
        root.resizable(width=False, height=False)
        self.displaying_counting = Label(root, text="осталось", font=("Arial bold", 14))
        self.displaying_counting.place(x=0, y=60)


        self.lbl_sec = Label(root, text="сек", font=("Arial bold", 14))
        self.lbl_sec.place(x=135, y=0)
        self.lbl_min = Label(root, text="мин", font=("Arial bold", 14))
        self.lbl_min.place(x=80, y=0)
        self.lbl_hour = Label(root, text="час", font=("Arial bold", 14))
        self.lbl_hour.place(x=30, y=0)

        self.entry_seconds = Entry(parent, width=2)
        self.entry_seconds.place(x=120, y=5)
        self.entry_minutes = Entry(parent, width=2)
        self.entry_minutes.place(x=65, y=5)
        self.entry_hours = Entry(parent, width=4)
        self.entry_hours.place(x=5, y=5)

        self.imput_str_sec = StringVar()
        self.imput_str_min = StringVar()
        self.imput_str_hour = StringVar()

        callback = root.register(self.only_numeric_input_less_than_60)
        callback_hours = root.register(self.only_numeric_input)
        self.entry_seconds.configure(validate="key", validatecommand=(callback, "%P"), textvariable=self.imput_str_sec)
        self.entry_minutes.configure(validate="key", validatecommand=(callback, "%P"), textvariable=self.imput_str_min)
        self.entry_hours.configure(validate="key", validatecommand=(callback_hours, "%P"), textvariable=self.imput_str_hour)

        self.imput_str_sec.trace_variable("w", self.entry_set_call)
        self.imput_str_min.trace_variable("w", self.entry_set_call)
        self.imput_str_hour.trace_variable("w", self.entry_set_call)

        btn = Button(root, text="начать отсчет", command=self.clicked_start, relief=RAISED, overrelief=FLAT)
        btn.place(x=10, y=30)
        btn2 = Button(root, text="stop", command=self.stop_countdown, relief=RAISED, overrelief=FLAT)
        btn2.place(x=100, y=30)


    def logic(self, seconds, minutes, hours):
        "responsible for the countdown and turns off the computer"
        seconds = int(seconds)
        minutes = int(minutes)
        hours = int(hours)

        s = time.strftime("%S", time.localtime())
        m = time.strftime("%M", time.localtime())
        h = time.strftime("%H", time.localtime())
        day = time.strftime("%d", time.localtime())

        sec_at_the_end = seconds + int(s)
        min_at_the_end = minutes + int(m)
        hour_at_the_end = hours + int(h)
        day_at_the_end = day
        day_at_the_end = int(day_at_the_end)

        while True:
            if sec_at_the_end > 60:
                sec_at_the_end -= 60
                min_at_the_end += 1
            if min_at_the_end > 60:
                min_at_the_end -= 60
                hour_at_the_end += 1
            if hour_at_the_end > 24:
                hour_at_the_end -= 24
                day_at_the_end += 1
            else:
                break

        old_s = int(s)
        self.stop_flag = True
        self.off_pc_flag = False
        if self.stop_flag == True:
            while True:

                if seconds <= 0 and minutes > 0:
                    seconds = 60
                    minutes -= 1
                if minutes <= 0 and hours > 0:
                    minutes = 60
                    hours -= 1

                s = time.strftime("%S", time.localtime())
                m = time.strftime("%M", time.localtime())
                h = time.strftime("%H", time.localtime())
                day = time.strftime("%d", time.localtime())

                s = int(s)
                m = int(m)
                h = int(h)
                day = int(day)

                if s > old_s:
                    seconds -= 1
                old_s = s

                res = "осталось {}".format(hours) + "час {}".format(minutes) + "мин {}".format(int(seconds)) + "сек"
                self.displaying_counting.after(100, self.displaying_counting.configure(text=res))
                if sec_at_the_end <= s and min_at_the_end <= m and hour_at_the_end <= h and day_at_the_end <= day and  self.off_pc_flag == True:
                    self.displaying_counting.configure(text="конец")
                    os.system('shutdown -s')
                    break

                if self.stop_flag == False:
                    self.displaying_counting.configure(text="осталось")
                    break
                self.off_pc_flag = True
                root.update()


    def clicked_start(self):
        "logic buttom and displaying a countdown"
        seconds = self.entry_seconds.get()
        minutes = self.entry_minutes.get()
        hours = self.entry_hours.get()

        if seconds == "":
            seconds = 0
        if minutes == "":
            minutes = 0
        if hours == "":
            hours = 0

        self.logic( seconds, minutes, hours)
        root.update()


    def entry_set_call(self, name, index, mode):
        "prohibits entering more than 2 digits, for hours 4"
        sec = self.imput_str_sec.get()
        min = self.imput_str_min.get()
        hour = self.imput_str_hour.get()
        if len(sec) > 2:
            self.imput_str_sec.set(sec[:-1])
        if len(min) > 2:
            self.imput_str_min.set(min[:-1])
        if len(hour) > 4:
            self.imput_str_hour.set(hour[:-1])


    def only_numeric_input(self, P):
        "prohibits entering not numbers"
        if P.isdigit() or P == "" :
            return True
        return False

    def only_numeric_input_less_than_60(self,P):
        "prohibits entering letters and numbers greater than 59. for seconds and minutes"
        if P.isdigit() and int(P) < 60 or P == "" :
            return True
        return False


    def stop_countdown(self):
        "no explanation is required"
        self.stop_flag = False


if __name__ == "__main__":
    root = tkinter.Tk()
    timer = Timer(root)
    root.mainloop()



