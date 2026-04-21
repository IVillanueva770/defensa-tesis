"""
Overlay de esqueletos sobre videos originales.

Para ajustar la alineacion de cada video, editá el dict TRANSFORMS abajo.
Parametros por video:
  flip_h  : espejado horizontal (bool)
  flip_v  : espejado vertical (bool)
  rotate  : rotacion en grados, sentido horario (0 / 90 / 180 / 270)
  scale   : factor de escala sobre el mapeo base (1.0 = sin cambio)
  tx      : desplazamiento horizontal en pixeles del video final (+ = derecha)
  ty      : desplazamiento vertical en pixeles del video final (+ = abajo)
  alpha   : opacidad del esqueleto sobre el video (0.0 - 1.0)
"""

import json
import numpy as np
import cv2
from pathlib import Path

# ── Transformaciones por video ────────────────────────────────────────────────
TRANSFORMS = {
    '62866_3': dict(flip_h=True, flip_v=False, rotate=90, scale=0.8, tx=-44, ty=0, alpha=0.85),
    '62876_2': dict(flip_h=False, flip_v=True, rotate=270, scale=1.0,  tx=-125, ty=0,  alpha=0.85),
    '62908_1': dict(flip_h=False, flip_v=True, rotate=270, scale=1.0,  tx=70,   ty=0,  alpha=0.85),
    '63176_3': dict(flip_h=False, flip_v=True, rotate=270, scale=0.82, tx=40,   ty=20, alpha=0.85),
    '79235_2': dict(flip_h=False, flip_v=True, rotate=270, scale=1.0,  tx=15,   ty=0,  alpha=0.85),
    '79540_1': dict(flip_h=False, flip_v=True, rotate=270, scale=0.85, tx=-75,  ty=80, alpha=0.85),
}

# ── Config general ────────────────────────────────────────────────────────────
CONF_THRESHOLD = 0.3
RENDER_MODE    = 'body+hands'   # 'body' | 'body+hands' | 'full'

JSONS_DIR   = Path(__file__).parent / 'jsons'
VIDEOS_DIR  = Path(__file__).parent / 'videos_input'
OUTPUT_DIR  = Path(__file__).parent / 'output_overlay'

COLORS = [
    (0, 220, 255),
    (0, 255, 128),
    (255, 100, 50),
    (200, 50, 255),
]

# ── Conexiones (igual que render_skeletons.py) ────────────────────────────────
BODY_CONNECTIONS = [
    (0,1),(0,2),(1,3),(2,4),
    (3,5),(4,6),(5,6),
    (5,7),(7,9),(6,8),(8,10),
    (5,11),(6,12),(11,12),
    (11,13),(13,15),(12,14),(14,16),
    (9,91),(10,112),
]
FEET_CONNECTIONS = [(15,17),(15,18),(15,19),(16,20),(16,21),(16,22)]
FACE_CONNECTIONS = (
    [(23+i, 24+i) for i in range(16)] +
    [(40+i, 41+i) for i in range(4)] +
    [(45+i, 46+i) for i in range(4)] +
    [(50+i, 51+i) for i in range(3)] +
    [(54+i, 55+i) for i in range(4)] +
    [(59+i, 60+i) for i in range(5)] + [(64,59)] +
    [(65+i, 66+i) for i in range(5)] + [(70,65)] +
    [(71+i, 72+i) for i in range(11)] + [(82,71)] +
    [(83+i, 84+i) for i in range(7)] + [(90,83)]
)
def _hand_connections(root):
    conns = []
    for start in [1, 6, 11, 16, 20]:
        conns.append((root, root + start))
        for j in range(3):
            conns.append((root + start + j, root + start + j + 1))
    return conns
LHAND_CONNECTIONS = _hand_connections(91)
RHAND_CONNECTIONS = _hand_connections(112)

def active_connections():
    c = BODY_CONNECTIONS + FEET_CONNECTIONS
    if RENDER_MODE in ('body+hands', 'full'):
        c += LHAND_CONNECTIONS + RHAND_CONNECTIONS
    if RENDER_MODE == 'full':
        c += FACE_CONNECTIONS
    return c

ACTIVE_CONNECTIONS = active_connections()

# ── Transformacion de coordenadas ─────────────────────────────────────────────

def compute_kp_bounds(frames):
    """Bounding box global de los keypoints con score suficiente."""
    xs, ys = [], []
    for frame in frames:
        for kp_list in frame.values():
            for x, y, s in kp_list:
                if s >= CONF_THRESHOLD:
                    xs.append(x); ys.append(y)
    return min(xs), max(xs), min(ys), max(ys)


def transform_point(x, y, kp_bounds, video_W, video_H, t):
    """Mapea un punto de espacio keypoint al espacio del video segun el transform t."""
    x_min, x_max, y_min, y_max = kp_bounds
    kp_w = x_max - x_min or 1
    kp_h = y_max - y_min or 1

    # 1. Normalizar a [0, 1]
    nx = (x - x_min) / kp_w
    ny = (y - y_min) / kp_h

    # 2. Flip
    if t['flip_h']: nx = 1.0 - nx
    if t['flip_v']: ny = 1.0 - ny

    # 3. Rotar (sentido horario)
    r = t['rotate'] % 360
    if r == 90:
        nx, ny = ny, 1.0 - nx
    elif r == 180:
        nx, ny = 1.0 - nx, 1.0 - ny
    elif r == 270:
        nx, ny = 1.0 - ny, nx

    # 4. Mapeo base: fit con aspect ratio preservado, centrado en el video
    kp_aspect = kp_w / kp_h
    if r in (90, 270):
        kp_aspect = 1.0 / kp_aspect   # el bounding box giro
    vid_aspect = video_W / video_H

    if kp_aspect > vid_aspect:
        fit_w = video_W
        fit_h = video_W / kp_aspect
    else:
        fit_h = video_H
        fit_w = video_H * kp_aspect

    ox = (video_W - fit_w) / 2
    oy = (video_H - fit_h) / 2

    # 5. Aplicar scale (centrado en el video)
    s = t['scale']
    px = nx * fit_w * s + ox + (fit_w * (1 - s) / 2) + t['tx']
    py = ny * fit_h * s + oy + (fit_h * (1 - s) / 2) + t['ty']

    return int(np.clip(px, -9999, 9999)), int(np.clip(py, -9999, 9999))


# ── Dibujo ────────────────────────────────────────────────────────────────────

def draw_skeleton_on_frame(canvas, kp_list, kp_bounds, W, H, color, transform):
    n = len(kp_list)
    radius    = max(3, W // 120)
    thickness = max(2, W // 200)

    def tp(i):
        x, y, s = kp_list[i]
        return transform_point(x, y, kp_bounds, W, H, transform), s

    for a, b in ACTIVE_CONNECTIONS:
        if a >= n or b >= n:
            continue
        pa, sa = tp(a)
        pb, sb = tp(b)
        if sa < CONF_THRESHOLD or sb < CONF_THRESHOLD:
            continue
        cv2.line(canvas, pa, pb, color, thickness, cv2.LINE_AA)

    for i, (x, y, s) in enumerate(kp_list[:23]):
        if s >= CONF_THRESHOLD:
            p, _ = tp(i)
            cv2.circle(canvas, p, radius, color, -1, cv2.LINE_AA)


# ── Pipeline principal ────────────────────────────────────────────────────────

def overlay_video(stem, transform):
    json_path  = JSONS_DIR / f'{stem}.json'
    video_path = next(VIDEOS_DIR.glob(f'x {stem}*.mp4'), None)

    if not json_path.exists():
        print(f'  [!] JSON no encontrado: {json_path.name}'); return
    if video_path is None:
        print(f'  [!] Video no encontrado para {stem}'); return

    with open(json_path) as f:
        data = json.load(f)
    frames = data['keypoints']

    cap = cv2.VideoCapture(str(video_path))
    W   = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    H   = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)

    kp_bounds = compute_kp_bounds(frames)

    all_ids    = sorted({pid for fr in frames for pid in fr.keys()}, key=lambda x: int(x))
    id_to_color = {pid: COLORS[i % len(COLORS)] for i, pid in enumerate(all_ids)}

    out_path = OUTPUT_DIR / f'{stem}_overlay.mp4'
    fourcc   = cv2.VideoWriter_fourcc(*'mp4v')
    out      = cv2.VideoWriter(str(out_path), fourcc, fps, (W, H))
    if not out.isOpened():
        out_path = out_path.with_suffix('.avi')
        out = cv2.VideoWriter(str(out_path), cv2.VideoWriter_fourcc(*'XVID'), fps, (W, H))

    alpha = transform['alpha']

    for frame_idx, frame_kp in enumerate(frames):
        ret, orig = cap.read()
        if not ret:
            break

        skeleton_layer = np.zeros_like(orig)
        for pid in sorted(frame_kp.keys(), key=lambda x: int(x)):
            draw_skeleton_on_frame(
                skeleton_layer, frame_kp[pid], kp_bounds, W, H,
                id_to_color[pid], transform
            )

        # Blend: donde hay esqueleto (no negro), mezclar con alpha
        mask = skeleton_layer.any(axis=2)
        blended = orig.copy()
        blended[mask] = cv2.addWeighted(orig, 1 - alpha, skeleton_layer, alpha, 0)[mask]

        out.write(blended)

    cap.release()
    out.release()
    n_json = len(frames)
    print(f'  -> {out_path.name}  ({n_json} frames, {W}x{H}px)')


def main():
    OUTPUT_DIR.mkdir(exist_ok=True)

    # Para arrancar, procesar solo 62866_3. Descomenta los otros cuando esten calibrados.
    to_process = [
        '62866_3',
        '62876_2',
        '62908_1',
        '63176_3',
        '79235_2',
        '79540_1',
    ]

    print(f'Modo: {RENDER_MODE}  |  Conf: {CONF_THRESHOLD}\n')
    for stem in to_process:
        print(stem)
        overlay_video(stem, TRANSFORMS[stem])

    print(f'\nListo. Videos en: {OUTPUT_DIR}')


if __name__ == '__main__':
    main()
