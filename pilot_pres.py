import cv2
import time
import threading
import random
import tkinter
import os
import win32com.client
import win32api

camwidth = 640
camheight = 480
toggle = 1;
recordingIndex_ = -999

cam_id = 0
user_initials = "SM"
numruns = 1
mindelay = 5
maxdelay = 10

fishID = "Z1"
gender = "(blank)"
status = "(blank)"
notes = "(blank)"

pre_stimulus_time = "blank"
pre_reward_time = "blank"
reward_aversion_time = "blank"

def tkinter_start():
    top = tkinter.Tk()

    def action():
        global toggle
        toggle *= -1
        if (toggle == -1):
            with open("transcript.txt", "a+") as wfile:
                wfile.write("Emergency stop")
            print("Stopped Recording, exiting program")
            cv2.destroyAllWindows()
            os._exit(0)

    B = tkinter.Button(top, text="Stop Recording", command=action)

    B.pack()
    top.mainloop()


def startup():
    top1 = tkinter.Tk()
    top1.title("Zfish Interface")
    mainpanel = tkinter.PanedWindow(orient=tkinter.VERTICAL)
    mainpanel.pack(fill=tkinter.BOTH, expand=1)
    panel1 = tkinter.PanedWindow(mainpanel)
    panel1.pack(fill=tkinter.BOTH, expand=1)

    top1.geometry('368x329')

    def c():
        if (os.path.exists("transcript.txt")):
            os.remove("transcript.txt")
        with open("transcript.txt", "a+") as wfile:
            import datetime
            wfile.write("DateTime: " + str(datetime.datetime.now()) + "\n")

            # global cam_id
            # if (not (txt.get() == "")):
            #     cam_id = int(txt.get())
            #     wfile.write("CameraID: " + str(cam_id) + "\n")
            # else:
            #     wfile.write("CameraID: 0 DEFAULT\n")

            global user_initials
            user_initials = txt3.get()
            if (not (txt3.get() == "")):
                wfile.write("User Initials: " + str(user_initials) + "\n")
            else:
                wfile.write("User Initials: (noname)\n")

            global numruns
            if (not (txt4.get() == "")):
                numruns = int(txt4.get())
                wfile.write("Number of Runs/Recordings: " + str(numruns) + "\n")
            else:
                wfile.write("Number of Runs/Recordings: 1 DEFAULT\n")

            global mindelay
            if (not (txt5.get() == "")):
                mindelay = int(txt5.get())
                wfile.write("Min ITI: " + str(mindelay) + " seconds\n")
            else:
                wfile.write("Min ITI: 5 seconds DEFAULT\n")

            global maxdelay
            if (not (txt51.get() == "")):
                maxdelay = int(txt51.get())
                wfile.write("Max ITI: " + str(maxdelay) + " seconds\n")
            else:
                wfile.write("Max ITI: 10 seconds DEFAULT\n")

            global pre_stimulus_time
            if (not (txt52.get() == "")):
                pre_stimulus_time = int(txt52.get())
                wfile.write("Pre-Stimulus Time: " + str(pre_stimulus_time) + " seconds\n")
            else:
                wfile.write("Pre-Stimulus Time: (blank)\n")

            global pre_reward_time
            if (not (txt53.get() == "")):
                pre_reward_time = int(txt53.get())
                wfile.write("Pre-Reward Time: " + str(pre_reward_time) + " seconds\n")
            else:
                wfile.write("Pre-Reward Time: (blank)\n")

            global reward_aversion_time
            if (not (txt54.get() == "")):
                reward_aversion_time = int(txt54.get())
                wfile.write("Reward/Aversion Time: " + str(reward_aversion_time) + " seconds\n")
            else:
                wfile.write("Reward/Aversion Time: (blank)\n")

            global fishID
            fishID = txt7.get()
            if (not (txt7.get() == "")):
                wfile.write("Fish ID: " + str(fishID) + "\n")
            else:
                wfile.write("Fish ID: (noname)\n")

            global gender
            gender = txt8.get()
            if (not (txt8.get() == "")):
                wfile.write("Gender (M/F): " + str(gender) + "\n")
            else:
                wfile.write("Gender (M/F): (blank)\n")

            global status
            status = txt9.get()
            if (not (txt9.get() == "")):
                wfile.write("Status (W/M/T): " + str(status) + "\n")
            else:
                wfile.write("Status (W/M/T): (blank)\n")

            global notes
            notes = txt10.get()
            if (not (txt10.get() == "")):
                wfile.write("Notes: " + str(notes) + "\n")
            else:
                wfile.write("Notes: (nonotes)\n")

            top1.destroy()
            wfile.write("-" * 50 + "\n")
            return 1

    def val(char):
        if str.isdigit(char) or char == "":
            return True
        else:
            return False

    #val1 = (top1.register(val))
    val2 = (top1.register(val))

    # txt = tkinter.Entry(top1, validate='all', validatecommand=(val1, '%P'))
    #
    # label = tkinter.Label(top1, text="Cam Id:")
    #
    # panel1.add(label)
    # panel1.add(txt)
    panel2 = tkinter.PanedWindow(mainpanel, orient=tkinter.VERTICAL)

    panel2.pack()

    panel3 = tkinter.PanedWindow(panel2, orient=tkinter.HORIZONTAL)
    panel3.pack()
    label3 = tkinter.Label(top1, text="User Initials: ")
    panel3.add(label3)
    txt3 = tkinter.Entry(top1, validate='all')
    panel3.add(txt3)

    panel4 = tkinter.PanedWindow(panel2, orient=tkinter.HORIZONTAL)
    panel4.pack()
    label4 = tkinter.Label(top1, text="Number of Runs/Recordings: ")
    panel4.add(label4)
    txt4 = tkinter.Entry(top1, validate='all', validatecommand=(val2, '%P'))
    panel4.add(txt4)

    panel5 = tkinter.PanedWindow(panel2, orient=tkinter.HORIZONTAL)
    panel5.pack()
    label5 = tkinter.Label(top1, text="ITI min (sec): ")
    panel5.add(label5)
    txt5 = tkinter.Entry(top1, validate='all', validatecommand=(val2, '%P'))
    panel5.add(txt5)

    panel51 = tkinter.PanedWindow(panel2, orient=tkinter.HORIZONTAL)
    panel51.pack()
    label51 = tkinter.Label(top1, text="ITI max (sec): ")
    panel51.add(label51)
    txt51 = tkinter.Entry(top1, validate='all', validatecommand=(val2, '%P'))
    panel51.add(txt51)

    panel52 = tkinter.PanedWindow(panel2, orient=tkinter.HORIZONTAL)
    panel52.pack()
    label52 = tkinter.Label(top1, text="Pre-Stimulus Time: ")
    panel52.add(label52)
    txt52 = tkinter.Entry(top1, validate='all')
    panel52.add(txt52)

    panel53 = tkinter.PanedWindow(panel2, orient=tkinter.HORIZONTAL)
    panel53.pack()
    label53 = tkinter.Label(top1, text="Pre-Reward Time: ")
    panel53.add(label53)
    txt53 = tkinter.Entry(top1, validate='all')
    panel53.add(txt53)

    panel54 = tkinter.PanedWindow(panel2, orient=tkinter.HORIZONTAL)
    panel54.pack()
    label54 = tkinter.Label(top1, text="Reward/Aversion Time: ")
    panel54.add(label54)
    txt54 = tkinter.Entry(top1, validate='all', )
    panel54.add(txt54)

    panel6 = tkinter.PanedWindow(panel2, orient=tkinter.VERTICAL)
    panel6.pack()
    label6 = tkinter.Label(top1, text="Fish Information: ")
    label6.config(font=("Courier", 24))
    panel6.add(label6)

    panel7 = tkinter.PanedWindow(panel2, orient=tkinter.HORIZONTAL)
    panel7.pack()
    label7 = tkinter.Label(top1, text="Fish ID: ")
    panel7.add(label7)
    txt7 = tkinter.Entry(top1, validate='all')
    panel7.add(txt7)

    panel8 = tkinter.PanedWindow(panel2, orient=tkinter.HORIZONTAL)
    panel8.pack()
    label8 = tkinter.Label(top1, text="Gender (M/F): ")
    panel8.add(label8)
    txt8 = tkinter.Entry(top1, validate='all')
    panel8.add(txt8)

    panel9 = tkinter.PanedWindow(panel2, orient=tkinter.HORIZONTAL)
    panel9.pack()
    label9 = tkinter.Label(top1, text="Status (W/M/T): ")
    panel9.add(label9)
    txt9 = tkinter.Entry(top1, validate='all')
    panel9.add(txt9)

    panel10 = tkinter.PanedWindow(panel2, orient=tkinter.HORIZONTAL)
    panel10.pack()
    label10 = tkinter.Label(top1, text="Notes: ")
    panel10.add(label10)
    txt10 = tkinter.Entry(top1, validate='all')
    panel10.add(txt10)

    C = tkinter.Button(top1, text="GO", command=c)
    C.pack(side=tkinter.BOTTOM)
    top1.mainloop()


def advanceSlides(ind, the_run, app, f_times):
    if (toggle == 1):
        index = -999
        if (os.path.exists("recordingIndex.txt")):

            with open("recordingIndex.txt") as rfile:
                for line in rfile:
                    index = int(line)
        else:
            index = 0
            with open("recordingIndex.txt", "a+") as wfile:
                wfile.write(str(0))
        global recordingIndex_
        recordingIndex_ = index + 1
        with open("transcript.txt", "a+") as wfile2:
            wfile2.write("Run # " + str(ind + 1) + ":" + the_run[0] + "\n")

        win32api.Sleep((pre_stimulus_time * 1000) + 2000)  # pre-stimulus time
        app.SlideShowWindows(1).View.GotoSlide(the_run[1])  # advance to screen cue
        #win32api.Sleep(f_times[0])  # fixed 1
        #app.SlideShowWindows(1).View.Next()  # play screen cue
        #win32api.Sleep(f_times[1])  # fixed 2
        #app.SlideShowWindows(1).View.Next()  # advance to sound slide
        #win32api.Sleep(f_times[2])  # fixed 3
        #app.SlideShowWindows(1).View.Next()  # play CF/FM
        win32api.Sleep(f_times[3])  # fixed 4
        app.SlideShowWindows(1).View.Next()  # advance to black slide
        win32api.Sleep(pre_reward_time * 1000)  # pre-reward interval
        app.SlideShowWindows(1).View.Next()  # advance to video slide
        win32api.Sleep(f_times[4])  # fixed 5
        app.SlideShowWindows(1).View.Next()  # start video
        win32api.Sleep(reward_aversion_time * 1000)  # reward/aversion time
        app.SlideShowWindows(1).View.Next()  # advance to black slide


def main_():

    path = r'C:\Users\josep\anaconda3\envs\ZF_attention_project\pilot_paradigms.pptx'

    global paradigm_slides
    paradigm_slides = [['reward', 2], ['aversion', 6]]
    global all_runs
    all_runs = [['reward', 0], ['aversion', 0]]

    global x
    x = win32com.client.Dispatch("PowerPoint.Application")
    x.Visible = 1
    x.Presentations.Open(FileName=path)
    x.ActivePresentation.SlideShowSettings.Run()

    fixed_times = [1, 1000, 1, 2000, 1]
    index = -999

    for i in range(numruns):
        this_run = random.choice(paradigm_slides)
        iti = random.randint(mindelay, maxdelay)

        print('run', i + 1, ':', this_run[0], 'ITI:', iti)
        advanceSlides(i, this_run, x, fixed_times)

        for y, j in enumerate(all_runs):
            if this_run[0] == j[0]:
                j[1] += 1
            if j[1] == numruns / 2:
                paradigm_slides.pop(y)
                all_runs.pop(y)

        time.sleep(iti)

        if len(all_runs) == 0:
            x.SlideShowWindows(1).View.GotoSlide(1)
            print("Presentation finished.")
            break

    with open("transcript.txt", "a+") as wfile:
        wfile.write("Session end")
    os._exit(0)


def supermain():
    t1 = threading.Thread(target=main_)
    t2 = threading.Thread(target=tkinter_start)
    t1.start()
    t2.start()
    t1.join()
    t2.join()


startup()


supermain()