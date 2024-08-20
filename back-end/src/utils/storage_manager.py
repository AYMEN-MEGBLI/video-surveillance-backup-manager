# import sqlite3
import json
import os
from datetime import datetime
from glob import glob
from typing import List, Tuple
from dotenv import load_dotenv
import cv2




"""
def create_table():
    # Connexion à la base de données (ou création si elle n'existe pas)
    conn = sqlite3.connect('videos.db')
    cursor=conn.cursor()
    # Création de la table video_details
    TABLE_QUERY = '''
    CREATE TABLE IF NOT EXISTS video_details (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        path TEXT NOT NULL,
        categorized_objects TEXT,  -- Représentation JSON en tant que chaîne de caractères
        timestamp DATE NOT NULL,    --date de la video
        duration INTEGER NOT NULL,  -- Durée en secondes
        camera INTEGER NOT NULL    -- Identifiant de la caméra
    )
    '''
    cursor.execute(TABLE_QUERY)
    print("table ccccc")

def get_connection():
    return sqlite3.connect('videos.db')

def insert_video_details(path, categorized_objects, timestamp, duration, camera):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO video_details (path, categorized_objects, timestamp, duration, camera)
        VALUES (?, ?, ?, ?, ?)
        ''',
        (path, 
        json.dumps(categorized_objects),  # Conversion de l'objet Python en chaîne JSON
        timestamp,
        duration, 
        camera)
    )
    conn.commit()
    conn.close()

def get_video_details():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM video_details')
    rows = cursor.fetchall()
    conn.close()
    return rows

def close():
    # Plus besoin de fermer manuellement la connexion
    pass
"""
str_to_date = lambda date_string: datetime.strptime(date_string, "%Y_%m_%d   %H_%M_%S").strftime("%d/%m/%Y %H:%M:%S")
get_video_details_from_json_file=lambda : glob(os.path.join("..","..","..","categorized_objects","*.json"))
get_video_details_from_json_file_by_date=lambda date: glob(os.path.join("..","..","..","categorized_objects",f"{date}*.json"))
get_video_details_from_json_file_by_camera= lambda camera : glob(os.path.join("..","..","..","categorized_objects",f"*camera_{camera}*.json"))

def save_video_details_with_json_file(file_name, categorized_objects, timestamp, timestamp_sec, camera):
     with open(os.path.join("..","..","..","categorized_objects",f"{timestamp}.json"),  mode='w', encoding='utf-8' ) as file:
                        a={
                            "file_name":file_name,
                            "date":str_to_date(timestamp),
                            "duration":timestamp_sec,
                            "camera":camera,
                            "categorized_objects":categorized_objects

                        }

                        json.dump(a, file,indent=4)
     print("file saved")




def get_videos_details():
    files=get_video_details_from_json_file()
    videos=[]
    for file in files:
        with open(file, 'r') as f:
            video = json.load(f)
            videos.append(video)
    return videos

def generate_video_chunks( video_path,chunk_size=4096):
    with open(video_path, "rb") as file_object:
        counter = 0
        while True:
            chunk = file_object.read(chunk_size)
            if not chunk:
                print("End of chunks")
                break
            counter = counter + 1
            print("Chunk Counter", counter)
            yield chunk
            
            




def extract_video_segment(video_path: str, 
                          start_time: int = 0,
                          end_time: int = None, 
                          *,
                          categorisation: str | None = None,
                          time_segments: List[Tuple[float, float]] = None) -> None:
    """
    Extrait un segment de vidéo à partir d'un fichier vidéo.
    Args:
    - video_path (str): Chemin de la vidéo source.
    - start_time (int): Instant de début du segment à extraire (en secondes).
    - end_time (int): Instant de fin du segment à extraire (en secondes).
    - categorisation (str | None): Catégorie pour l'enregistrement (facultatif).
    - time_segments (List[Tuple[float, float]]): Liste de paires de temps à extraire (en secondes).
    Returns:
    - None
    """
    load_dotenv("../../.env")
    
    # Vérifier si le fichier vidéo existe
    assert os.path.isfile(video_path), "Erreur: Le fichier vidéo spécifié n'existe pas."
    # Vérifier et ajuster les valeurs de temps
    if end_time is None:
        video_capture = cv2.VideoCapture(video_path)
        end_time = video_capture.get(cv2.CAP_PROP_FRAME_COUNT) / video_capture.get(cv2.CAP_PROP_FPS)
        video_capture.release()
    if start_time < 0 or end_time < 0:
        print("Erreur: Les valeurs de temps doivent être positives.")
        return
    if time_segments is None:
        time_segments = [(start_time, end_time)]
    
    # Créer le répertoire de sortie si nécessaire
    output_directory = os.getenv('OUTPUT_PATH', 'Videos') if categorisation is None else os.path.join(os.getenv('OUTPUT_PATH', 'Videos'), categorisation)
    os.makedirs(output_directory, exist_ok=True)
    
    for segment_start, segment_end in time_segments:
        # Initialiser la capture vidéo
        video_capture = cv2.VideoCapture(video_path)
        
        # Vérifier si la vidéo est ouverte avec succès
        if not video_capture.isOpened():
            print("Erreur: Impossible d'ouvrir la vidéo.")
            return
        if start_time < 0 or end_time < 0:
            print("Erreur: Les valeurs de temps doivent être positives.")
            continue
        if segment_start > segment_end:
            print("Erreur: Le temps de début doit être inférieur au temps de fin.")
            continue
        
        
        # Récupérer les propriétés de la vidéo (FPS, largeur, hauteur)
        fps = video_capture.get(cv2.CAP_PROP_FPS)
        frame_width = int(video_capture.get(cv2.CAP_PROP_FRAME_WIDTH))
        frame_height = int(video_capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
        
        # Calculer le numéro de frame correspondant au temps de début et de fin
        frame_start = int(segment_start * fps)
        frame_end = int(segment_end * fps)
        
        # Vérifier que le temps de début est inférieur au temps de fin
        if frame_start >= frame_end:
           
            print("Erreur: Le temps de début doit être inférieur au temps de fin.")
            return
        
        # Définir le codec et créer l'objet VideoWriter pour enregistrer le segment
        codec = cv2.VideoWriter_fourcc(*'H264')
        output_filename = f'{datetime.now().strftime("%d-%m-%Y(%H-%M-%S)")}_{segment_start}_{segment_end}.mp4'
        output_path = os.path.join(output_directory, output_filename)
        video_writer = cv2.VideoWriter(output_path, codec, fps, (frame_width, frame_height))
        
        # Parcourir les frames jusqu'au temps de début
        for _ in range(frame_start):
            ret, _ = video_capture.read()
            if not ret:
                print("Erreur: Impossible de lire la vidéo.")
                return
        
        # Enregistrer le segment
        for _ in range(frame_start, frame_end):
            ret, frame = video_capture.read()
            if not ret:
                print("Erreur: Impossible de lire la vidéo.")
                return
            video_writer.write(frame)
        
        # Libérer les ressources pour ce segment
        video_capture.release()
        video_writer.release()
        print(f"{output_path} enregistré avec succès dans {output_path}")


