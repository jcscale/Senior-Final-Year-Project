from tkinter.constants import N, NE, W
import serial
import time
import tkinter as tk
from tkinter import Label, ttk
from PIL import Image, ImageTk
import threading
import numpy as np
import cv2
import psutil


def quit():
    global running
    running = False
    global root

    # cap.release()

    root.quit()
    # for widget in frame1.winfo_children():
    #     widget.destroy()


def stop():
    try:
        cap.release()
        cv2.destroyAllWindows()
        start_button.config(state="normal")
        stop_button.config(state="disabled")
        e1.config(state="normal")
        e2.config(state="normal")
        e3.config(state="normal")
        e4.config(state="normal")

    except NameError:
        # cap.release()
        # cv2.destroyAllWindows()
        start_button.config(state="normal")
        stop_button.config(state="disabled")
        e1.config(state="normal")
        e2.config(state="normal")
        e3.config(state="normal")
        e4.config(state="normal")


def getSettingValue():
    global res1
    global res2
    global res3

    res1 = e1.get()
    res2 = e2.get()
    res3 = e3.get()

    print(res1, res2, res3)
    # return res1, res2, res3


def setting():
    top = tk.Toplevel()
    top.title('Settings')

    # global video
    # global port
    # global baud

    videoCapture = tk.Label(top, text="Video Capture").grid(row=0)
    serialPort = tk.Label(top, text="Port").grid(row=1)
    baudRate = tk.Label(top, text="Baud Rate").grid(row=2)

    v1 = tk.StringVar(root, value=0)
    v2 = tk.StringVar(root, value='COM3')
    v3 = tk.StringVar(root, value='9600')

    global e1, e2, e3

    e1 = tk.Entry(top, textvariable=v1)
    e2 = tk.Entry(top, textvariable=v2)
    e3 = tk.Entry(top, textvariable=v3)

    e1.grid(row=0, column=1)
    e2.grid(row=1, column=1)
    e3.grid(row=2, column=1)

    settingBtn = tk.Button(
        top, text="OK", command=getSettingValue)
    settingBtn.grid(row=3, column=1)

    # if top.destroy:
    #     video = int(e1.get())
    #     print(video)


def start():

    # webcam = tk.Toplevel()
    # webcam.title('Web Camera')
    global last_frame

    # Arduino
    # arduino = serial.Serial('COM3', 9600)
    # time.sleep(2)

    global cap

    vid = e1.get()

    port = e2.get()
    rate = e3.get()

    algo = e4.get()
    if algo == "yolov3-320":
        cfg = "yolov3-320.cfg"
        weights = "yolov3-320.weights"
    else:
        cfg = "yolov3-tiny.cfg"
        weights = "yolov3-tiny.weights"
    print(cfg)
    print(weights)

    # Arduino
    # arduino = serial.Serial(port, int(rate))
    # time.sleep(2)

    print(type(vid), type(port), type(rate))
    print(vid, port, rate)

    cap = cv2.VideoCapture(int(vid))
    whT = 320
    confThreshold = 0.5
    nmsThreshold = 0.1

    prev_frame_time = 0

    # LOAD MODEL
    # Coco Names
    classesFile = "coco.names"
    classNames = []
    with open(classesFile, 'rt') as f:
        classNames = f.read().rstrip('\n').split('\n')
    # print(classNames)
    # Model Files
    modelConfiguration = cfg
    modelWeights = weights
    net = cv2.dnn.readNetFromDarknet(modelConfiguration, modelWeights)
    net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
    net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)

    def findObjects(outputs, img):
        hT, wT, cT = img.shape
        bbox = []
        classIds = []
        confs = []
        for output in outputs:
            for det in output:
                scores = det[5:]
                classId = np.argmax(scores)
                confidence = scores[classId]
                if confidence > confThreshold:
                    w, h = int(det[2]*wT), int(det[3]*hT)
                    x, y = int((det[0]*wT)-w/2), int((det[1]*hT)-h/2)
                    bbox.append([x, y, w, h])
                    classIds.append(classId)
                    confs.append(float(confidence))

        indices = cv2.dnn.NMSBoxes(
            bbox, confs, confThreshold, nmsThreshold)

        for i in indices:
            i = i[0]
            box = bbox[i]
            x, y, w, h = box[0], box[1], box[2], box[3]
            # print(x,y,w,h)

            if classNames[classIds[i]] == 'bottle':

                cv2.rectangle(img, (x, y), (x+w, y+h), (0, 225, 0), 2)

                cv2.putText(img, f'{classNames[classIds[i]].upper()} {int(confs[i]*100)}%',
                            (x+10, y+30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 225, 0), 2)

                # cv2.putText(img, classNames[classId[i][0]-1].upper(), (box[0]+10, box[1]+30),
                #             cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)

                # print(classNames[classIds[i]])

                # arduino.write(b'1')

            elif classNames[classIds[i]] != 'bottle':
                classNames[classIds[i]] = 'not bottle'
                cv2.rectangle(img, (x, y), (x+w, y+h), (0, 0, 225), 2)

                cv2.putText(img, f'{classNames[classIds[i]].upper()}',
                            (x+10, y+30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 225), 2)

                # cv2.putText(img, classNames[classId[i][0]-1].upper(), (box[0]+10, box[1]+30),
                #             cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)

                # print(classNames[classIds[i]])
                # arduino.write(b'2')

    while True:
        success, img = cap.read()

        gray = img
        # resizing the frame size according to our need
        gray = cv2.resize(gray, (500, 300))
        font = cv2.FONT_HERSHEY_SIMPLEX
        # time when we finish processing for this frame
        new_frame_time = time.time()

        fps = 1/(new_frame_time-prev_frame_time)
        prev_frame_time = new_frame_time
        fps = int(fps)
        message4.config(text=fps)
        message5.config(text=f"{psutil.cpu_percent()} %")
        # cv2.putText(gray, fps, (7, 70), font, 3, (100, 255, 0), 3, cv2.LINE_AA)

        blob = cv2.dnn.blobFromImage(
            img, 1 / 255, (whT, whT), [0, 0, 0], 1, crop=False)
        net.setInput(blob)
        layersNames = net.getLayerNames()
        outputNames = [(layersNames[i[0] - 1])
                       for i in net.getUnconnectedOutLayers()]
        outputs = net.forward(outputNames)
        findObjects(outputs, img)
        last_frame = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))

        # cv2.imshow('Image', img)
        # cv2.waitKey(1)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


def update_frame():
    if last_frame is not None:
        tk_img = ImageTk.PhotoImage(master=video_label, image=last_frame)
        video_label.config(image=tk_img)
        video_label.tk_img = tk_img

    if running:
        root.after(10, update_frame)


def start_rec():
    global running

    running = True
    thread = threading.Thread(target=start, daemon=True)
    thread.start()
    update_frame()

    start_button.config(state="disabled")
    stop_button.config(state="normal")
    e1.config(state="disabled")
    e2.config(state="disabled")
    e3.config(state="disabled")
    e4.config(state="disabled")


def closeWindow():
    quit()
    root.destroy()


running = False
after_id = None
last_frame = None


def raise_frame(frame):
    frame.tkraise()


###################### MAIN ######################
root = tk.Tk()
root.protocol("WM_DELETE_WINDOW", closeWindow)
# root.geometry('300x200')
root.title("RVM Software")


frame1 = tk.LabelFrame(root, text='Camera')
frame2 = tk.LabelFrame(root, text='Message')

for frame in (frame1, frame2):
    frame.grid(row=0, column=0, sticky='nsew')

frame3 = tk.LabelFrame(root, text='Configurations')
frame3.grid(row=2, column=0, sticky='nsew')


###################### PERFORMANCE  ######################

frame4 = tk.LabelFrame(root, text='Performance')
frame4.grid(row=1, column=0, sticky='nsew')
fpsLabel = tk.Label(frame4, text="FPS:").pack(side="left", padx=5, pady=5)
message4 = tk.Label(frame4, text=0)
message4.pack(side="left", padx=5, pady=5)
cpuLabel = Label(frame4, text="CPU:").pack(side="left", padx=5, pady=5)
message5 = Label(frame4, text=f"{psutil.cpu_percent()} %")
message5.pack(side="left", padx=5, pady=5)


video_label = tk.Label(frame1)
video_label.pack(expand=True, fill="both")

message = tk.Label(
    frame2, text='Make sure that this computer is connected to the Arduino before pressing "Start" button').pack()

message2 = tk.Label(frame1, text="Plastic Bottle Detection")
message2.pack()


global e1, e2, e3

###################### VIDEO CAPTURE ######################


videoCapture = tk.Label(frame3, text="Video Capture").pack(
    side="left", padx=5, pady=5)
v1 = tk.IntVar(frame3, value=0)
# e1 = tk.Entry(frame3, textvariable=v1)
# e1.pack(side="left", padx=5, pady=5)

e1 = ttk.Combobox(frame3, width=27, textvariable=v1, state="readonly")
e1['values'] = (
    0, 1, 2, 3, 4, 5, 6, 7, 8, 9
)
e1.pack(side="left", padx=5, pady=5)
e1.current(0)


###################### SERIAL PORT ######################


serialPort = tk.Label(frame3, text="Port").pack(side="left", padx=5, pady=5)
v2 = tk.StringVar(frame3, value='COM3')
e2 = tk.Entry(frame3, textvariable=v2)
e2.pack(side="left", padx=5, pady=5)


###################### BAUD RATE ######################

baudRate = tk.Label(frame3, text="Baud Rate").pack(side="left", padx=5, pady=5)
v3 = tk.StringVar(frame3, value='9600')
# e3 = tk.Entry(frame3, textvariable=v3)
# e3.pack(side="left", padx=5, pady=5)

e3 = ttk.Combobox(frame3, width=27, textvariable=v3, state="readonly")
e3['values'] = (
    300, 600, 1200, 2400, 4800, 9600, 14400, 19200, 28800, 31250, 38400, 57600, 115200
)
e3.pack(side="left", padx=5, pady=5)
e3.current(5)


###################### ALGORITHM ######################

algorithm = tk.Label(frame3, text="Algorithm").pack(
    side="left", padx=5, pady=5)
v4 = tk.StringVar(frame3, value="yolov3-320")
e4 = ttk.Combobox(frame3, width=27, textvariable=v4, state="readonly")
e4['values'] = (
    "yolov3-320", "yolov3-tiny"
)
e4.pack(side="left", padx=5, pady=5)
e4.current(0)


###################### BUTTONS ######################


start_button = tk.Button(frame3, text="Start", command=lambda: [
                         start_rec(), raise_frame(frame1)])
start_button.pack(side='left', expand=True, fill="both", padx=5, pady=5)

# restart_button = tk.Button(root, text="Restart", command=start_rec)
# restart_button.pack(side='left', expand=True, fill="both", padx=5, pady=5)

stop_button = tk.Button(frame3, text="Stop",
                        command=lambda: [raise_frame(frame2), stop()])
stop_button.pack(side='left', expand=True, fill="both", padx=5, pady=5)

stop_button.config(state="disabled")

ext_button = tk.Button(frame3, text="Exit", command=quit)
ext_button.pack(side='left', expand=True, fill="both", padx=5, pady=5)

# setting_button = tk.Button(root, text="settings", command=setting)
# setting_button.pack(side='left', expand=True, fill="both", padx=5, pady=5)


root.mainloop()
