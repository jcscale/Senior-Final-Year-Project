import serial
import time
import tkinter as tk
from PIL import Image, ImageTk
import threading
import numpy as np
import cv2


def quit():
    global running
    running = False
    global root
    root.destroy()


def getSettingValue():
    res = e1.get()
    print(res)


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
    global last_frame
    cap = cv2.VideoCapture(0)
    whT = 320
    confThreshold = 0.5
    nmsThreshold = 0.1

    # LOAD MODEL
    # Coco Names
    classesFile = "coco2.names"
    classNames = []
    with open(classesFile, 'rt') as f:
        classNames = f.read().rstrip('\n').split('\n')
    print(classNames)
    # Model Files
    modelConfiguration = "yolov3-320.cfg"
    modelWeights = "yolov3-320.weights"
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

        indices = cv2.dnn.NMSBoxes(bbox, confs, confThreshold, nmsThreshold)

        for i in indices:
            i = i[0]
            box = bbox[i]
            x, y, w, h = box[0], box[1], box[2], box[3]
            # print(x,y,w,h)
            cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 255), 2)

            cv2.putText(img, f'{classNames[classIds[i]].upper()} {int(confs[i]*100)}%',
                        (x+10, y+30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 255), 2)

            # cv2.putText(img, classNames[classId[i][0]-1].upper(), (box[0]+10, box[1]+30),
            #             cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)

            print(classNames[classIds[i]])

    while True:
        success, img = cap.read()
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


def closeWindow():
    quit()
    root.destroy()


running = False
after_id = None
last_frame = None


root = tk.Tk()
root.protocol("WM_DELETE_WINDOW", closeWindow)
# root.geometry('300x200')
root.title("RVM Software")

video_label = tk.Label()
video_label.pack(expand=True, fill="both")

start_button = tk.Button(root, text="Start", command=start_rec)
start_button.pack(side='top', ipadx=10, padx=10, pady=15)

stop_button = tk.Button(root, text="Stop", command=quit)
stop_button.pack(side='top', ipadx=10, padx=10, pady=15)

setting_button = tk.Button(root, text="settings", command=setting)
setting_button.pack()


root.mainloop()
