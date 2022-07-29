import random
import tkinter
import cv2
import threading
import time
import os
import win32com.client
import win32api
import pythoncom
from datetime import datetime

camwidth = 640
camheight = 480
toggle = 1;
recordingIndex = -999

cam_id = 0
user_initial = "SM"

numruns = 3
mindelay = 6
maxdelay = 10

zfish_id = "Z1"
gender = "(blank)"
genotype = "(blank)"
notes = "(blank)"

pre_stimulus_time = 4
pre_reward_time = 4
reward_aversion_time = 4
post_reward_time = 5

run_onset = 0

filename = r'C:\Users\Kanwal\Dropbox\Josephine Zfish\ZF_attention\paradigms.pptx'

now = datetime.now()
nowstr = now.strftime("%Y-%m-%d %H:%M:%S %p")
# new_dir_name = input(str(zfish_id)+nowstr)
# new_dir = pathlib.Path('/Users/nataliaresende/Dropbox/PYTHON/', new_dir_name)
# new_dir.mkdir(parents=True, exist_ok=True)

class VideoRecorder():

    # Video class based on openCV
    def __init__(self, run, paradigm):

        self.open = True
        self.device_index = 0
        self.fps = 20  # fps should be the minimum constant rate at which the camera can
        self.fourcc = "XVID"  # capture images (with no decrease in speed over time; testing is required)
        self.frameSize = (640, 480)  # video formats and sizes also depend and vary according to the camera used
        self.video_filename = zfish_id + "_run_" + str(run) + "_" + paradigm + ".avi"
        self.video_cap = cv2.VideoCapture(self.device_index)
        self.video_writer = cv2.VideoWriter_fourcc(*self.fourcc)
        self.video_out = cv2.VideoWriter(self.video_filename, self.video_writer, self.fps, self.frameSize)
        self.frame_counts = 1
        self.start_time = time.time()
        self.font = cv2.FONT_HERSHEY_PLAIN
        self.tone_marker = cv2.MARKER_STAR
        self.rew_av_marker = cv2.MARKER_DIAMOND
        self.marker_point = (40,20)

    # Video starts being recorded
    def record(self):

        while (self.open == True):
            ret, video_frame = self.video_cap.read()
            cv2.putText(video_frame, str(datetime.now()), (20,40),
                        self.font, 2, (255,255,255), 2, cv2.LINE_AA)
            if (ret == True):
                marker_now = time.time()
                tone_start = marker_now + pre_stimulus_time
                tone_end = marker_now + pre_stimulus_time + 4 #making a variable for tone time
                if tone_start < marker_now < tone_end:
                    cv2.drawMarker(video_frame, self.marker_point, (0,0,255),
                                   self.tone_marker, 40, 2, cv2.LINE_AA)
                self.video_out.write(video_frame)
                self.frame_counts += 1
                time.sleep(0.05)

                gray = cv2.cvtColor(video_frame, cv2.COLOR_BGR2GRAY)
                cv2.imshow('video_frame', gray)
                cv2.waitKey(1)
            else:
                break

    def markerOn(self):
        cv2.drawMarker()

    # Finishes the video recording therefore the thread too
    def stop(self):

        if self.open == True:

            self.open = False
            self.video_out.release()
            self.video_cap.release()
            cv2.destroyAllWindows()

        else:
            pass

    # Launches the video recording function using a thread
    def start(self):
        video_thread = threading.Thread(target=self.record)
        video_thread.start()

def start_PPTrecording(filename):

    paradigm_slides = [['cf', 12], ['dfm', 7], ['ufm', 2]]
    all_runs = [['cf', 0], ['dfm', 0], ['ufm', 0]]

    global fixed_times
    fixed_times = [1, 6000, 1, 4000, 1]
    pythoncom.CoInitialize()
    app = win32com.client.Dispatch("PowerPoint.Application")
    app.Visible = 1
    app.Presentations.Open(FileName=filename)
    app.ActivePresentation.SlideShowSettings.Run()

    # 6-min novel environment test
    novtest_vthread = VideoRecorder('novelenv', 'test')
    novtest_vthread.start()
    time.sleep(15) #change to 360 for true trials
    novtest_vthread.stop()

    #loop through paradigm presentations and record from pre-stimulus to post reward/aversion
    for i in range(numruns):
        this_run = random.choice(paradigm_slides)
        iti = random.randint(mindelay, maxdelay)
        global run_onset
        run_onset = time.time()
        run_now = datetime.now()
        run_nowstr = run_now.strftime("%Y-%m-%d %H:%M:%S %p")

        print('run', i + 1, ':', this_run[0], 'ITI:', iti, "onset:", run_nowstr)

        video_thread = VideoRecorder(i, this_run[0])
        video_thread.start()

        win32api.Sleep((pre_stimulus_time * 1000) + 2000)  # pre-stimulus time
        app.SlideShowWindows(1).View.GotoSlide(this_run[1])  # advance to screen cue
        win32api.Sleep(fixed_times[0])  # fixed 1
        app.SlideShowWindows(1).View.Next()  # play screen cue
        win32api.Sleep(fixed_times[1])  # fixed 2
        app.SlideShowWindows(1).View.Next()  # advance to sound slide
        win32api.Sleep(fixed_times[2])  # fixed 3
        app.SlideShowWindows(1).View.Next()  # play CF/FM
        win32api.Sleep(fixed_times[3])  # fixed 4
        app.SlideShowWindows(1).View.Next()  # advance to black slide
        win32api.Sleep(pre_reward_time * 1000)  # pre-reward interval
        app.SlideShowWindows(1).View.Next()  # advance to video slide
        win32api.Sleep(fixed_times[4])  # fixed 5
        app.SlideShowWindows(1).View.Next()  # start video
        win32api.Sleep(reward_aversion_time * 1000)  # reward/aversion time
        app.SlideShowWindows(1).View.Next()  # advance to black slide

        for y, j in enumerate(all_runs):
            if this_run[0] == j[0]:
                j[1] += 1
            if j[1] == numruns / 3:
                paradigm_slides.pop(y)
                all_runs.pop(y)

        time.sleep(post_reward_time)
        video_thread.stop()
        time.sleep(iti - post_reward_time)

        if len(all_runs) == 0:
            app.SlideShowWindows(1).View.GotoSlide(1)
            pythoncom.CoUninitialize()
            print("Presentation finished.")
            with open("transcript.txt","a+") as wfile:
                wfile.write("Presentation finished.\n")
            break
        with open("transcript.txt","a+") as wfile:
            wfile.write("Filename: "+video_thread.video_filename+"\n\n")


def main_():
    start_PPTrecording(filename)

def tkinter_start():
    top = tkinter.Tk()

    def action():
        global toggle
        toggle *= -1
        if(toggle==-1):
            with open("transcript.txt","a+") as wfile:
                wfile.write("Emergency stop")
            print("Stopped Recording, exiting program")
            cv2.destroyAllWindows()
            os._exit(0)

    B = tkinter.Button(top, text ="Stop Recording", command = action)

    B.pack()
    top.mainloop()

def supermain():
    t1 = threading.Thread(target=main_)
    t2 = threading.Thread(target=tkinter_start)
    t1.start()
    t2.start()
    t1.join()
    t2.join()

def startup():
    
    top1 = tkinter.Tk()
    top1.title("Zfish Interface")
    mainpanel = tkinter.PanedWindow(orient=tkinter.VERTICAL)
    mainpanel.pack(fill=tkinter.BOTH,expand = 1)
    panel1 = tkinter.PanedWindow(mainpanel)
    panel1.pack(fill=tkinter.BOTH, expand=1)

    top1.geometry('368x340')    
    def c():  
        if(os.path.exists("transcript.txt")):   
            os.remove("transcript.txt")   
        with open("transcript.txt", "a+") as wfile:
            wfile.write("DateTime: "+str(datetime.now())+"\n")

            global cam_id    
            if(not(txt.get()=="")):    
                cam_id = int(txt.get())    
                wfile.write("CameraID: "+str(cam_id)+"\n")  
            else:   
                wfile.write("CameraID: 0 DEFAULT\n") 
            global user_initial
            user_initial = txt3.get()
            if(not(txt3.get()=="")):
                wfile.write("User Initials: "+str(user_initial)+"\n")
            else:
                wfile.write("User Initials: (blank)\n")
            global numruns
            if(not(txt4.get()=="")):
                numruns = int(txt4.get())
                wfile.write("Number of Runs/Recordings: "+str(numruns)+"\n")
            else:
                wfile.write("Number of Runs/Recordings: 3 DEFAULT\n")

            global mindelay
            if(not(txt5.get()=="")):
                mindelay = int(txt5.get())
                wfile.write("Min ITI: "+str(mindelay)+" seconds\n")
            else:
                wfile.write("Min ITI: 6 seconds DEFAULT\n")

            global maxdelay
            if(not(txt51.get()=="")):
                maxdelay = int(txt51.get())
                wfile.write("Max ITI: "+str(maxdelay)+" seconds\n")
            else:
                wfile.write("Max ITI: 10 seconds DEFAULT\n")


            global pre_stimulus_time
            if(not(txt52.get()=="")):
                pre_stimulus_time = int(txt52.get())
                wfile.write("Pre-stimulus Time: "+str(pre_stimulus_time)+"\n")
            else:
                wfile.write("Pre_stimulus Time: (blank)\n")

            global pre_reward_time
            if(not(txt53.get()=="")):
                pre_reward_time = int(txt53.get())
                wfile.write("Pre-reward Time: "+str(pre_reward_time)+"\n")
            else:
                wfile.write("Pre-reward Time: (blank)\n")

            global reward_aversion_time
            if(not(txt54.get()=="")):
                reward_aversion_time = int(txt54.get())
                wfile.write("Reward/Aversion Time: "+str(reward_aversion_time)+"\n")
            else:
                wfile.write("Reward/Aversion Time: (blank)\n")


            global zfish_id 
            if(not(txt7.get()=="")):
                zfish_id  = txt7.get()
                wfile.write("Zfish ID: "+str(zfish_id )+"\n")
            else:
                wfile.write("Zfish ID: Z1 DEFAULT\n")           

            global gender
            if(not(txt8.get()=="")):
                gender = txt8.get()
            
                wfile.write("Gender (M/F): "+str(gender)+"\n")
            else:
                wfile.write("Gender (M/F): (blank)\n")  

            global genotype
            if(not(txt9.get()=="")):
                genotype = txt9.get()
            
                wfile.write("Genotype (W/M/T): "+str(genotype)+"\n")
            else:
                wfile.write("Genotype (W/M/T): (blank)\n")

            global notes
            if(not(txt10.get()=="")):
                notes = txt10.get()
            
                wfile.write("Notes: "+str(notes)+"\n")
            else:
                wfile.write("Notes: (blank)\n")
            
            top1.destroy()
            wfile.write("-"*50+"\n")
            return 1
    def val(char):
        if str.isdigit(char) or char == "":
            return True
        else:
            return False

    val1 = (top1.register(val))
    val2 = (top1.register(val))

    txt = tkinter.Entry(top1, validate='all', validatecommand=(val1, '%P'))

    label = tkinter.Label(top1, text="Cam Id:")
    
    panel1.add(label)
    panel1.add(txt)

    panel2 = tkinter.PanedWindow(mainpanel,orient=tkinter.VERTICAL)
    panel2.pack()

    panel3 = tkinter.PanedWindow(panel2,orient=tkinter.HORIZONTAL)
    panel3.pack()
    label3 = tkinter.Label(top1, text="User Initials: ")
    panel3.add(label3)
    txt3 = tkinter.Entry(top1, validate='all') 
    panel3.add(txt3)

    panel4 = tkinter.PanedWindow(panel2,orient=tkinter.HORIZONTAL)
    panel4.pack()
    label4 = tkinter.Label(top1, text="Number of Runs/Recordings: ")
    panel4.add(label4)
    txt4 = tkinter.Entry(top1, validate='all', validatecommand=(val2, '%P')) 
    panel4.add(txt4)

    panel5 = tkinter.PanedWindow(panel2,orient=tkinter.HORIZONTAL)
    panel5.pack()
    label5 = tkinter.Label(top1, text="ITI min (sec): ")
    panel5.add(label5)
    txt5 = tkinter.Entry(top1, validate='all', validatecommand=(val2, '%P')) 
    panel5.add(txt5)

    panel51 = tkinter.PanedWindow(panel2,orient=tkinter.HORIZONTAL)
    panel51.pack()
    label51 = tkinter.Label(top1, text="ITI max (sec): ")
    panel51.add(label51)
    txt51 = tkinter.Entry(top1, validate='all', validatecommand=(val2, '%P')) 
    panel51.add(txt51)
    
    panel52 = tkinter.PanedWindow(panel2,orient=tkinter.HORIZONTAL)
    panel52.pack()
    label52 = tkinter.Label(top1, text="Pre_stimulus Time: ")
    panel52.add(label52)
    txt52 = tkinter.Entry(top1, validate='all') 
    panel52.add(txt52)

    panel53 = tkinter.PanedWindow(panel2,orient=tkinter.HORIZONTAL)
    panel53.pack()
    label53 = tkinter.Label(top1, text="Pre-reward Time: ")
    panel53.add(label53)
    txt53 = tkinter.Entry(top1, validate='all') 
    panel53.add(txt53)

    panel54 = tkinter.PanedWindow(panel2,orient=tkinter.HORIZONTAL)
    panel54.pack()
    label54 = tkinter.Label(top1, text="Reward/Aversion Time: ")
    panel54.add(label54)
    txt54 = tkinter.Entry(top1, validate='all',) 
    panel54.add(txt54)

    panel6 = tkinter.PanedWindow(panel2,orient=tkinter.VERTICAL)
    panel6.pack()
    label6 = tkinter.Label(top1, text="Fish Information: ")
    label6.config(font=("Courier", 24))
    panel6.add(label6)

    panel7 = tkinter.PanedWindow(panel2,orient=tkinter.HORIZONTAL)
    panel7.pack()
    label7 = tkinter.Label(top1, text="Zfish ID: ")
    panel7.add(label7)
    txt7 = tkinter.Entry(top1, validate='all') 
    panel7.add(txt7)

    panel8 = tkinter.PanedWindow(panel2,orient=tkinter.HORIZONTAL)
    panel8.pack()
    label8 = tkinter.Label(top1, text="Gender (M/F): ")
    panel8.add(label8)
    txt8 = tkinter.Entry(top1, validate='all') 
    panel8.add(txt8)

    panel9 = tkinter.PanedWindow(panel2,orient=tkinter.HORIZONTAL)
    panel9.pack()
    label9 = tkinter.Label(top1, text="Genotype (W/M/T): ")
    panel9.add(label9)
    txt9 = tkinter.Entry(top1, validate='all') 
    panel9.add(txt9)

    panel10 = tkinter.PanedWindow(panel2,orient=tkinter.HORIZONTAL)
    panel10.pack()
    label10 = tkinter.Label(top1, text="Notes: ")
    panel10.add(label10)
    txt10 = tkinter.Entry(top1, validate='all') 
    panel10.add(txt10)


    C = tkinter.Button(top1, text ="GO", command = c)
    C.pack(side = tkinter.BOTTOM)
    top1.mainloop()

startup()
supermain()