import cv2
import json
import os
import numpy as np

BASE = r"C:\Users\Ignacio Villanueva\Desktop\Defensa de tesis"
JSON_BASE = os.path.join(BASE, "jsons keypoints", "ohp_poses")
OUT_DIR = os.path.join(BASE, "keypoint_videos")
os.makedirs(OUT_DIR, exist_ok=True)

# COCO 17 skeleton connections (índices 0-16)
SKELETON = [
    (0, 1), (0, 2),           # nariz → ojos
    (1, 3), (2, 4),           # ojos → orejas
    (5, 6),                   # hombros
    (5, 7), (7, 9),           # brazo izquierdo
    (6, 8), (8, 10),          # brazo derecho
    (5, 11), (6, 12),         # hombros → caderas
    (11, 12),                 # caderas
    (11, 13), (13, 15),       # pierna izquierda
    (12, 14), (14, 16),       # pierna derecha
]

# Colores por segmento corporal (BGR)
SEG_COLORS = {
    "head":  (0, 255, 255),    # amarillo
    "arm_l": (0, 165, 255),    # naranja
    "arm_r": (255, 100, 0),    # azul
    "torso": (0, 255, 0),      # verde
    "leg_l": (180, 0, 255),    # violeta
    "leg_r": (255, 0, 180),    # rosa
}

def seg_color(i, j):
    pair = tuple(sorted([i, j]))
    if pair in [(0,1),(0,2),(1,3),(2,4)]:
        return SEG_COLORS["head"]
    if pair in [(5,7),(7,9)]:
        return SEG_COLORS["arm_l"]
    if pair in [(6,8),(8,10)]:
        return SEG_COLORS["arm_r"]
    if pair in [(5,6),(5,11),(6,12),(11,12)]:
        return SEG_COLORS["torso"]
    if pair in [(11,13),(13,15)]:
        return SEG_COLORS["leg_l"]
    if pair in [(12,14),(14,16)]:
        return SEG_COLORS["leg_r"]
    return (255, 255, 255)

def select_main_person(frame_kps):
    """Elige la persona con más keypoints con confianza > 0.3."""
    best_id, best_count = None, -1
    for pid, kps in frame_kps.items():
        count = sum(1 for kp in kps[:17] if kp[2] > 0.3)
        if count > best_count:
            best_count = count
            best_id = pid
    return frame_kps.get(best_id, []) if best_id else []

def transform_kps(kps, w, h):
    """Los JSON landscape (480x270) fueron generados con ejes transpuestos vs OpenCV."""
    if w > h:  # landscape: transponer x↔y
        return [[kp[1], kp[0], kp[2]] for kp in kps]
    return kps  # cuadrado: coordenadas directas

def draw_pose(frame, kps, conf_thresh=0.25):
    if not kps:
        return frame
    kps17 = kps[:17]
    # Dibujamos huesos
    for i, j in SKELETON:
        if i >= len(kps17) or j >= len(kps17):
            continue
        xi, yi, ci = kps17[i]
        xj, yj, cj = kps17[j]
        if ci > conf_thresh and cj > conf_thresh:
            color = seg_color(i, j)
            cv2.line(frame, (int(xi), int(yi)), (int(xj), int(yj)), color, 2)
    # Dibujamos puntos
    for idx, (x, y, c) in enumerate(kps17):
        if c > conf_thresh:
            cv2.circle(frame, (int(x), int(y)), 5, (255, 255, 255), -1)
            cv2.circle(frame, (int(x), int(y)), 5, (0, 0, 0), 1)
    return frame

def process_video(video_path, json_path, out_path, label):
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"  ERROR abriendo video: {video_path}")
        return False

    fps = cap.get(cv2.CAP_PROP_FPS) or 30
    w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    writer = cv2.VideoWriter(out_path, fourcc, fps, (w, h))

    with open(json_path) as f:
        data = json.load(f)
    frames_kps = data["keypoints"]

    frame_idx = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        if frame_idx < len(frames_kps):
            kps = select_main_person(frames_kps[frame_idx])
            kps = transform_kps(kps, w, h)
            frame = draw_pose(frame, kps)

        # Label en esquina
        cv2.rectangle(frame, (5, 5), (len(label)*11 + 15, 32), (0, 0, 0), -1)
        cv2.putText(frame, label, (10, 24),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 200), 2)
        writer.write(frame)
        frame_idx += 1

    cap.release()
    writer.release()
    return True

VIDEOS_TO_PROCESS = [
    # (video_file, json_subfolder, json_name, label)
    (r"videos correctos\x 79235_2.mp4",  "correct",      "79235_2.json",  "Tecnica Correcta"),
    (r"videos correctos\x 79540_1.mp4",  "correct",      "79540_1.json",  "Tecnica Correcta"),
    (r"videos error codo\x 62866_3.mp4", "elbows_error", "62866_3.json",  "Error de Codos"),
    (r"videos error codo\x 62876_2.mp4", "elbows_error", "62876_2.json",  "Error de Codos"),
    (r"videos error rodilla\x 62908_1.mp4", "knees_error", "62908_1.json", "Error de Rodillas"),
    (r"videos error rodilla\x 63176_3.mp4", "knees_error", "63176_3.json", "Error de Rodillas"),
]

for video_rel, json_sub, json_name, label in VIDEOS_TO_PROCESS:
    video_path = os.path.join(BASE, video_rel)
    json_path  = os.path.join(JSON_BASE, json_sub, json_name)
    base_name  = json_name.replace(".json", "")
    out_name   = f"{json_sub}_{base_name}_kp.mp4"
    out_path   = os.path.join(OUT_DIR, out_name)

    print(f"Procesando: {video_rel}")
    if not os.path.exists(video_path):
        print(f"  VIDEO NO ENCONTRADO: {video_path}")
        continue
    if not os.path.exists(json_path):
        print(f"  JSON NO ENCONTRADO: {json_path}")
        continue

    ok = process_video(video_path, json_path, out_path, label)
    if ok:
        print(f"  OK -> {out_path}")
