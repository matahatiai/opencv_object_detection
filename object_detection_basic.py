import cv2
from cvzone.HandTrackingModule import HandDetector
thres = 0.45 # Threshold to detect object

cap = cv2.VideoCapture(1)
cap.set(3,1280)
cap.set(4,720)
cap.set(10,70)

classNames= ['person','bicycle','car','motorcycle','airplane','bus','train','truck','boat','traffic light','fire hydrant','street sign','stop sign','parking meter','bench','bird','cat','dog','horse','sheep','cow','elephant','bear','zebra','giraffe','hat','backpack','umbrella','shoe','eye glasses','handbag','tie','suitcase','frisbee','skis','snowboard','sports ball','kite','baseball bat','baseball glove','skateboard','surfboard','tennis racket','bottle','plate','wine glass','cup','fork','knife','spoon','bowl','banana','apple','sandwich','orange','broccoli','carrot','hot dog','pizza','donut','cake','chair','couch','potted plant','bed','mirror','dining table','window','desk','toilet','door','tv','laptop','mouse','remote','keyboard','cell phone','microwave','oven','toaster','sink','refrigerator','blender','book','clock','vase','scissors','teddy bear','hair drier','toothbrush','hair brush']

configPath = 'ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt'
weightsPath = 'frozen_inference_graph.pb'

net = cv2.dnn_DetectionModel(weightsPath,configPath)
net.setInputSize(320,320)
net.setInputScale(1.0/ 127.5)
net.setInputMean((127.5, 127.5, 127.5))
net.setInputSwapRB(True)

hand_detector = HandDetector(detectionCon=0.5, maxHands=1)

while True:
    success,img = cap.read()

    try :
        img = hand_detector.findHands(img, draw=True)
        #hand_detector.findPosition(img)
        #myHandType = hand_detector.handType()
    except Exception as e :
        print(e)

    classIds, confs, bbox = net.detect(img,confThreshold=thres)
    print(classIds,bbox)
    if len(classIds) != 0:
        for classId, confidence,box in zip(classIds.flatten(),confs.flatten(),bbox):
            try :

                cv2.rectangle(img,box,color=(0,255,0),thickness=2)
                cv2.putText(img,classNames[classId-1].upper(),(box[0]+10,box[1]+30),
                cv2.FONT_HERSHEY_COMPLEX,1,(0,255,0),2)
                cv2.putText(img,str(round(confidence*100,2)),(box[0]+200,box[1]+30),
                cv2.FONT_HERSHEY_COMPLEX,1,(0,255,0),2)
            except Exception as e :
                print(e)

    cv2.imshow("Output",img)
    cv2.waitKey(1)