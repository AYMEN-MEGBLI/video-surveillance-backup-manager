from typing import Dict, List, Tuple
import os
from dotenv import load_dotenv
import cv2
from ultralytics import YOLO
from datetime import datetime
from functools import cache
from time import sleep
from storage_manager import save_video_details_with_json_file
import locale



locale.setlocale(locale.LC_TIME, 'fr_FR.UTF-8')


# Load the YOLO model once
try:
        model = YOLO("yolov8n.pt")
        print("YOLO model initialized successfully.")
except Exception as e:
        print(f"Error initializing YOLO model: {e}")
names=model.names      
load_dotenv("../../.env")
DetectedObjects = Dict[str, List[Tuple[float, float]]]

@cache
def detect_and_categorize_objects(
    video_path: str= None,
    cap : cv2.VideoCapture= None,
    start_time: int = 0,
    end_time: int = None,
    NB_FRAMES: int = 25,
    humains: bool = True,
    animaux: bool = True,
    vehicules: bool = True,
    autre: bool = False
    ) -> DetectedObjects :

    """
    Fonction qui détecte et catégorise les objets dans une vidéo.
    Args:
    - video_path (str): Chemin de la vidéo à analyser.
    
    Returns:
    - dict: Dictionnaire des catégories d'objets détectées avec les instants de début et de fin ,en ms , de chaque détection.
      DetectedObjects : Dict[str, List[Tuple[float, float]]]
    """
    categorized_objects = {
        "humains": [],
        "animaux": [],
        "vehicules": [],
        "autres": []
    }
    
    classes_to_detect=[]
    classes_to_detect.extend(range(1,9)) if vehicules else None;
    classes_to_detect.append(0) if humains else None;
    classes_to_detect.extend(range(14,24)) if animaux else None;

    assert video_path is not None or cap is not None,  "Erreur: Veuillez spécifier un chemin de vidéo ou un objet de capture vidéo."
    assert start_time >= 0, "Erreur: L'instant de début doit être positif."
    if end_time is not None:
        assert end_time > start_time,   "Erreur: L'instant de fin doit être supérieur à l'instant de début. {} : {}".format(start_time,end_time)
        end_time*=1000
    
    if video_path is not None:
        cap = cv2.VideoCapture(video_path)
    cap.set(cv2.CAP_PROP_POS_MSEC, start_time *1000) # 5 * 1000 (ms)=> 5s
    detect_vehicle_start_time=detect_human_start_time=detect_animal_start_time=detect_other_start_time = None
    no_human_detection_in_frame=no_vehicle_detection_in_frame=no_animal_detection_in_frame =no_other_detection_in_frame = 0
    while cap.isOpened()   :
        success, frame = cap.read()
        if success:  
            current_time = cap.get(cv2.CAP_PROP_POS_MSEC) 
          

            timestamp_sec = float("{:.3f}".format(current_time))            *0.001
            results = model(frame,classes=[classes_to_detect],conf=0.5,verbose=False )
            if autre :
                if len(results[0].boxes.cls)==0  :
                    no_other_detection_in_frame=0
                    if detect_other_start_time  is None :
                        detect_other_start_time = timestamp_sec  
                else:
                    if  detect_other_start_time is not None:
                            no_other_detection_in_frame+=1
                            if no_other_detection_in_frame > NB_FRAMES:
                                categorized_objects["autres"].append((detect_other_start_time, timestamp_sec))
                                detect_other_start_time = None                            
                #verbose=False remove the print of the results 
            for r in results:
                boxes = r.boxes
                for box in boxes: 
                    cls = int(box.cls[0]) 
                    if vehicules :
                        if cls in range(1,9):
                            no_vehicle_detection_in_frame=0
                            if detect_vehicle_start_time is None:
                                detect_vehicle_start_time = timestamp_sec    
                        else:
                            if detect_vehicle_start_time is not None:
                                no_vehicle_detection_in_frame+=1
                                
                                if no_vehicle_detection_in_frame > NB_FRAMES:
                                    categorized_objects["vehicules"].append((detect_vehicle_start_time, timestamp_sec))
                                    detect_vehicle_start_time = None
                    if animaux :
                        if cls in range(14,24):
                            no_animal_detection_in_frame=0
                            if detect_animal_start_time is None:
                                detect_animal_start_time = timestamp_sec      
                        else:
                            if detect_animal_start_time is not None:
                                no_animal_detection_in_frame+=1
                                if no_animal_detection_in_frame > NB_FRAMES:
                                    categorized_objects["animaux"].append((detect_animal_start_time, timestamp_sec)) 
                                    detect_vehicle_start_time = None
                    if humains :
                        if cls == 0 :
                            no_human_detection_in_frame=0
                            if detect_human_start_time is None:
                                detect_human_start_time = timestamp_sec         
                        else:
                            if detect_human_start_time is not None:
                                no_human_detection_in_frame+=1
                                if no_human_detection_in_frame > NB_FRAMES:
                                    categorized_objects["humains"].append((detect_human_start_time, timestamp_sec))
                                    detect_human_start_time = None
            if end_time is not None and current_time  >= end_time  :
                if detect_vehicle_start_time is not None:
                    categorized_objects["vehicules"].append((detect_vehicle_start_time, timestamp_sec))
                    detect_vehicle_start_time = None
                if detect_animal_start_time is not None:
                    categorized_objects["animaux"].append((detect_animal_start_time, timestamp_sec))
                    detect_animal_start_time = None
                if detect_human_start_time is not None:
                    categorized_objects["humains"].append((detect_human_start_time, timestamp_sec))
                    detect_human_start_time = None
                if detect_other_start_time is not None:
                    categorized_objects["autres"].append((detect_other_start_time, timestamp_sec))
                    detect_other_start_time = None
                break
                                
          
           
        else:
            if detect_vehicle_start_time is not None:
                categorized_objects["vehicules"].append((detect_vehicle_start_time, timestamp_sec))
                detect_vehicle_start_time = None
            if detect_animal_start_time is not None:
                categorized_objects["animaux"].append((detect_animal_start_time, timestamp_sec))
                detect_animal_start_time = None
            if detect_human_start_time is not None:
                categorized_objects["humains"].append((detect_human_start_time, timestamp_sec))
                detect_human_start_time = None
            if detect_other_start_time is not None:
                categorized_objects["autres"].append((detect_other_start_time, timestamp_sec))
                detect_other_start_time = None
            break

    if video_path is not None:
        cap.release()
    else :
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
    return categorized_objects

class MyCam:
    def __init__(self, webcam_index=0):
        self.cap = cv2.VideoCapture(webcam_index)
        self.webcam_index=webcam_index
        self.detect_func_ends=True
        self.generate_frames_ends=True
        self.stop_rec=False
        self.on=True
        self.boxes=True
    @staticmethod
    def draw_rec(frame, xyxy, cls,conf, font_scale=0.5, thickness=2):
        x1, y1, x2, y2 = xyxy
        if cls in range(1,9):
            label = "vehicules"
            color=(0, 0, 255)
        elif cls in range(14,24):
            label = "animaux"
            color=(0, 255, 0)
        elif cls == 0:
            label = "humains"
            color=(255, 0, 0)
            
        
        # Draw the bounding box
        cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), color, thickness)
        
        # Calculate the size of the text
        (text_width, text_height), _ = cv2.getTextSize(f"{label} {conf :.2f}%", cv2.FONT_HERSHEY_SIMPLEX, font_scale, thickness)
        
        # Create a filled rectangle for the text background
        cv2.rectangle(frame, (int(x1), int(y1) - text_height - 10), (int(x1) + text_width, int(y1)), color, -1)
        
        # Put the label text on top of the bounding box
        cv2.putText(frame, f"{label} {conf :.2f}%" , (int(x1), int(y1) - 5), cv2.FONT_HERSHEY_SIMPLEX, font_scale, (255, 255, 255), thickness)
        
        return frame
    
    
    @staticmethod    
    def add_timestamp_to_frame( frame, timestamp_text=None, position=(5, 30), font_scale=0.5, font_thickness=1, alpha=0.5):
        if timestamp_text is None:
            timestamp_text =datetime.now().strftime("%A")[:3] + datetime.now().strftime(" %m %Y  %H:%M:%S")
        # Get text size
        (text_width, text_height), _ = cv2.getTextSize(timestamp_text, cv2.FONT_HERSHEY_SIMPLEX, font_scale, font_thickness)
        text_x, text_y = position
        
        # Create overlay for semi-transparent rectangle
        overlay = frame.copy()
        cv2.rectangle(overlay, (text_x, text_y - text_height - 10), (text_x + text_width + 10, text_y + 10), (0, 0, 0), -1)
        
        # Blend the overlay with the original frame
        cv2.addWeighted(overlay, alpha, frame, 1 - alpha, 0, frame)
        
        # Add the timestamp text
        cv2.putText(frame, timestamp_text, (text_x + 5, text_y), cv2.FONT_HERSHEY_SIMPLEX, font_scale, (255, 255, 255), font_thickness, cv2.LINE_AA)
        
        return frame

    def detect_and_categorize_objects_3(self,
                                    NB_FRAMES: int = 5,
                                    humains: bool = True,
                                    animaux: bool = True,
                                    vehicules: bool = True,
                                    ) -> None:
            print("Starting detection and categorization...")
            
            #declaration
            
            #self.openCam()
            categorized_objects = {"humains": [],"animaux": [],"vehicules": []}
            classes_to_detect=[]
            classes_to_detect.extend(range(1,9)) if vehicules else None;
            classes_to_detect.append(0) if humains else None;
            classes_to_detect.extend(range(14,24)) if animaux else None;
            detect_vehicle_start_time=detect_human_start_time=detect_animal_start_time=detect_other_start_time = None
            no_human_detection_in_frame=no_vehicle_detection_in_frame=no_animal_detection_in_frame  = 0
            #------------ Récupérer les propriétés de la vidéo ----------------
            timestamp_sec= 0
            timestamp = datetime.now().strftime("%Y_%m_%d %H_%M_%S")
            # Utilisation du codec H264, largement pris en charge par les navigateurs pour les fichiers MP4
            FOURCC = cv2.VideoWriter_fourcc(*'H264') 
            FPS=10
            FRAME_WIDTH=640
            FRAME_HEIGHT=480
            OUTPUT_PATH= os.path.join("..","..","..","videos-cctv",f"camera_{self.webcam_index} {timestamp}.mp4")
            video_writer = cv2.VideoWriter(OUTPUT_PATH,FOURCC, FPS, (FRAME_WIDTH, FRAME_HEIGHT))
            
            self.stop_rec=False #obliger
            if not self.cap.isOpened():
                print("Error: Webcam could not be opened.")
                return
            
            while self.on :
                self.detect_func_ends=False
                mov_detect=True
                if not self.cap.isOpened():
                    print("Error: Webcam could not be opened.")
                    return
                succes,frame=self.cap.read()
                if succes and not self.stop_rec :
                    if mov_detect:
                        results = model(frame,classes=[classes_to_detect],conf=0.6,verbose=False )
                        for r in results:
                            boxes = r.boxes
                            for box in boxes: 
                                cls = int(box.cls[0])
                                if vehicules :
                                    if cls in range(1,9):
                                        print("vehicules")
                                        no_vehicle_detection_in_frame=0
                                        if detect_vehicle_start_time is None:
                                            detect_vehicle_start_time = timestamp_sec    
                                    else:
                                        if detect_vehicle_start_time is not None:
                                            no_vehicle_detection_in_frame+=1
                                            
                                            if no_vehicle_detection_in_frame > NB_FRAMES:
                                                categorized_objects["vehicules"].append((detect_vehicle_start_time, timestamp_sec))
                                                detect_vehicle_start_time = None
                                if animaux :
                                    if cls in range(14,24):
                                        print("animaux")
                                        no_animal_detection_in_frame=0
                                        if detect_animal_start_time is None:
                                            detect_animal_start_time = timestamp_sec      
                                    else:
                                        if detect_animal_start_time is not None:
                                            no_animal_detection_in_frame+=1
                                            if no_animal_detection_in_frame > NB_FRAMES:
                                                categorized_objects["animaux"].append((detect_animal_start_time, timestamp_sec)) 
                                                detect_vehicle_start_time = None
                                if humains :
                                    if cls == 0 :
                                        print("humains")
                                        no_human_detection_in_frame=0
                                        if detect_human_start_time is None:
                                            detect_human_start_time = timestamp_sec         
                                    else:
                                        if detect_human_start_time is not None:
                                            no_human_detection_in_frame+=1
                                            if no_human_detection_in_frame > NB_FRAMES:
                                                categorized_objects["humains"].append((detect_human_start_time, timestamp_sec))
                                                detect_human_start_time = None
                                if self.boxes:
                                #box.xyxy[0]  # get box coordinates in (left, top, right, bottom) format
                                    frame=MyCam.draw_rec(frame, box.xyxy[0], box.cls,box.conf[0])
                                    
                        frame = MyCam.add_timestamp_to_frame(frame)
                        cv2.imshow("frame",frame)
                        video_writer.write(frame)
                        timestamp_sec +=(1/FPS)
                        if cv2.waitKey(1) & 0xFF == ord('q'):
                            cv2.destroyWindow("frame")
                            

                            video_writer.release()
                            print(f"Saved video: {OUTPUT_PATH}")
                            save_video_details_with_json_file(f"camera_{self.webcam_index} {timestamp}.mp4", categorized_objects, timestamp, timestamp_sec, self.webcam_index)
                            break
                        
                    else: 
                        if detect_vehicle_start_time is not None:
                            categorized_objects["vehicules"].append((detect_vehicle_start_time, timestamp_sec))
                            detect_vehicle_start_time = None
                        if detect_animal_start_time is not None:
                            categorized_objects["animaux"].append((detect_animal_start_time, timestamp_sec))
                            detect_animal_start_time = None
                        if detect_human_start_time is not None:
                            categorized_objects["humains"].append((detect_human_start_time, timestamp_sec))
                            detect_human_start_time = None 
                        video_writer.release()
                        print(f" Saved video: {OUTPUT_PATH}")
                        save_video_details_with_json_file(f"camera_{self.webcam_index} {timestamp}.mp4", categorized_objects, timestamp, timestamp_sec, self.webcam_index)
                        #------------ Récupérer les propriétés de la vidéo ----------------
                        timestamp_sec=0
                        timestamp = datetime.now().strftime("%Y_%m_%d %H_%M_%S")
                        # f"{timestamp_sec:.2f} sec"
                        OUTPUT_PATH= os.path.join("..","..","..","videos-cctv",f"camera_{self.webcam_index} {timestamp}.mp4")
                        video_writer = cv2.VideoWriter(OUTPUT_PATH,FOURCC, FPS, (FRAME_WIDTH, FRAME_HEIGHT))      
                else :
                    if detect_vehicle_start_time is not None:
                        categorized_objects["vehicules"].append((detect_vehicle_start_time, timestamp_sec))
                        detect_vehicle_start_time = None
                    if detect_animal_start_time is not None:
                        categorized_objects["animaux"].append((detect_animal_start_time, timestamp_sec))
                        detect_animal_start_time = None
                    if detect_human_start_time is not None:
                        categorized_objects["humains"].append((detect_human_start_time, timestamp_sec))
                        detect_human_start_time = None 
                    video_writer.release()
                    print(f"Saved video: {OUTPUT_PATH}") 
                    save_video_details_with_json_file(f"camera_{self.webcam_index} {timestamp}.mp4", categorized_objects, timestamp, timestamp_sec, self.webcam_index)
           
                    break
            self.detect_func_ends=True
            #self.destroy()

    def generate_frames(self):
        self.generate_frames_ends=False
        #self.openCam()
        while  self.on and self.cap.isOpened()  :
            succes,frame=self.cap.read()
            if succes :
                
                frame = MyCam.add_timestamp_to_frame(frame)
                if not self.detect_func_ends:
                        cv2.putText(frame,"rec", (580, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7 , (0, 0, 255), 1, cv2.LINE_AA)
                _, buffer = cv2.imencode('.jpg', frame)
                #cv2.imshow("frame2", frame)
                frame = buffer.tobytes()
                if cv2.waitKey(1) & 0xFF == ord('b'):
                    cv2.destroyWindow("frame2")
                    break
                yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        self.generate_frames_ends=True
        #self.destroy()

    def destroy(self):
        
        if self.detect_func_ends and self.generate_frames_ends  :
            self.cap.release()
            cv2.destroyAllWindows()   
    def openCam(self):
        if  not self.cap.isOpened() and not self.generate_frames_ends or not self.detect_func_ends: 
            self.cap = cv2.VideoCapture(self.webcam_index)
            
    def stop_recording(self):
        self.stop_rec=True
    def enable_disable(self):
        if self.on:
            self.on = False
            print("Stopping webcam...")
            sleep(1)
            if self.cap is not None:
                self.cap.release()
                
        else:
            self.on =True
            print("Starting webcam...")
            self.cap = cv2.VideoCapture(self.webcam_index)
            if not self.cap.isOpened():
                print("Error: Webcam could not be opened.")
            else:
                print("Webcam started successfully.")
        
        # Toggle the 'on' flag
        #self.on = not self.on
        print("Camera status:", "Open" if self.cap.isOpened() else "Closed")
            
                