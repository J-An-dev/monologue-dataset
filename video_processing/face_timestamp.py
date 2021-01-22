import face_recognition
import cv2
import numpy as np

# Load some sample pictures and learn how to recognize them.
image = face_recognition.load_image_file("obama.png")
face_encoding = face_recognition.face_encodings(image)[0]

known_faces = [face_encoding]

# Initialize some variables
frame_size = 112
mrgn = 150




def ms2hms(ms):
    seconds = round((ms / 1000) % 60, 3)
    seconds2 = int(seconds)
    ms3 = "%03d" % ((seconds - seconds2) * 1000)
    seconds2 = "%02d" % seconds2
    minutes = (ms / (1000 * 60)) % 60
    minutes = int(minutes)
    minutes = "%02d" % minutes
    hours = (ms / (1000 * 60 * 60)) % 24
    hours = int(hours)
    hours = "%02d" % hours
    hms = str(hours)+':'+str(minutes)+':'+str(seconds2)+'.'+str(ms3)  ## format: HH:MM:SS.mmm
    return(hms)


def face_timestamp(videofile):
    video = cv2.VideoCapture(videofile)
    total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    i = 0
    state = None
    get_first_face = False

    face_locations = []
    face_encodings = []
    frames = []

    OUT_W = []
    OUT_H = []
    X = []
    Y = []
    ss = []
    t = []
    first_frame = 0

    while i < total_frames:
        print("%d / %d" % (i, total_frames))

        ret, frame = video.read()
        if not ret:
            break

        time = int(video.get(cv2.CAP_PROP_POS_MSEC))
        if first_frame == 1 or np.any(frame[0]):
            first_frame = 1
            i = i + 75  ## recognize every 3s
            for j in range(75):
                _, tmp_frame = video.read()
            face_locations = face_recognition.face_locations(frame)
            face_encodings = face_recognition.face_encodings(frame, face_locations)

            if face_locations != []:
                match = face_recognition.compare_faces(known_faces, face_encodings, tolerance=0.5)
                if match[0] == True:
                    for (top, right, bottom, left) in face_locations:
                        # face = frame[top - (mrgn + 15):bottom + (mrgn - 15), left - mrgn:right + mrgn]
                        out_w = str((right + mrgn) - (left - mrgn))
                        out_h = str((bottom + mrgn) - (top - mrgn))
                        x = str(left - mrgn)
                        y = str(top - (mrgn+10))
                        if not get_first_face:
                            OUT_W.append(out_w)
                            OUT_H.append(out_h)
                            X.append(x)
                            Y.append(y)
                            ss.append(time)
                            get_first_face = True
                            state = 1
                            continue
                        
                        # if abs(int(X[-1]) - int(x)) > 80 and state == 1:
                        #     OUT_W.append(out_w)
                        #     OUT_H.append(out_h)
                        #     X.append(x)
                        #     Y.append(y)
                        #     t.append(time)
                        #     ss.append(time)
                        #     state = 2
                        
                        if abs(int(X[-1]) - int(x)) > 50 and abs(int(X[-1]) - int(x)) < 200 and abs(int(y[-1]) - int(y)) < 80 and state == 1:
                            OUT_W.append(out_w)
                            OUT_H.append(out_h)
                            X.append(x)
                            Y.append(y)
                            t.append(time)
                            ss.append(time)
                            state = 1
                            continue

                        # if abs(int(X[-1]) - int(x)) > 200 and abs(int(y[-1]) - int(y)) < 100 and state == 2:
                        #     OUT_W.append(out_w)
                        #     OUT_H.append(out_h)
                        #     X.append(x)
                        #     Y.append(y)
                        #     t.append(time)
                        #     ss.append(time)
                        #     state = 2
                        #     continue

                        if state == 3:
                            OUT_W.append(out_w)
                            OUT_H.append(out_h)
                            X.append(x)
                            Y.append(y)
                            ss.append(time)
                            state = 1
                            continue
                else:
                    if state == 1:
                        state = 3
                        t.append(time)
                        continue

            else:
                if state == 1:
                    state = 3
                    t.append(time)
                    continue

        else:
            i = i + 1



    if len(ss) > len(t):
        t.append(time - 1200)
        if t[-1] == 0:
            t[-1] = (total_frames - 30) * 40

    for i in range(len(ss)):
        ss[i] = ms2hms(ss[i])
        t[i] = ms2hms(t[i])

    return OUT_W, OUT_H, X, Y, ss, t









