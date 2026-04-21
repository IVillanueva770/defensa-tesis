import json
import numpy as np
import cv2
from pathlib import Path

# ── Configuración ──────────────────────────────────────────────────────────────
RENDER_MODE    = 'body+hands'  # 'body' | 'body+hands' | 'full'
CONF_THRESHOLD = 0.3
FPS            = 25
CANVAS_SIZE    = 720           # px en el lado mayor

JSONS_DIR  = Path(__file__).parent / 'jsons'
OUTPUT_DIR = Path(__file__).parent / 'output'

COLORS = [
    (0, 200, 255),   # amarillo-naranja
    (0, 255, 128),   # verde
    (255, 100, 50),  # azul
    (200, 50, 255),  # violeta
]

# ── Conexiones del esqueleto ───────────────────────────────────────────────────
BODY_CONNECTIONS = [
    (0,1),(0,2),(1,3),(2,4),
    (3,5),(4,6),(5,6),
    (5,7),(7,9),(6,8),(8,10),
    (5,11),(6,12),(11,12),
    (11,13),(13,15),(12,14),(14,16),
    (9,91),(10,112),   # muñecas -> raíz de manos
]

FEET_CONNECTIONS = [
    (15,17),(15,18),(15,19),
    (16,20),(16,21),(16,22),
]

FACE_CONNECTIONS = (
    [(23+i, 24+i) for i in range(16)] +         # mandíbula
    [(40+i, 41+i) for i in range(4)] +           # ceja izq
    [(45+i, 46+i) for i in range(4)] +           # ceja der
    [(50+i, 51+i) for i in range(3)] +           # puente nariz
    [(54+i, 55+i) for i in range(4)] +           # base nariz
    [(59+i, 60+i) for i in range(5)] + [(64,59)] +  # ojo izq
    [(65+i, 66+i) for i in range(5)] + [(70,65)] +  # ojo der
    [(71+i, 72+i) for i in range(11)] + [(82,71)] +  # labio ext
    [(83+i, 84+i) for i in range(7)] + [(90,83)]     # labio int
)


def _hand_connections(root):
    conns = []
    # pulgar offset 1 (4 segmentos), luego 4 dedos de 4 segmentos c/u con offset 6,11,16,20
    finger_starts = [1, 6, 11, 16, 20]
    for start in finger_starts:
        conns.append((root, root + start))
        for j in range(3):
            conns.append((root + start + j, root + start + j + 1))
    return conns


LHAND_CONNECTIONS = _hand_connections(91)
RHAND_CONNECTIONS = _hand_connections(112)


def _active_connections():
    conns = BODY_CONNECTIONS + FEET_CONNECTIONS
    if RENDER_MODE in ('body+hands', 'full'):
        conns = conns + LHAND_CONNECTIONS + RHAND_CONNECTIONS
    if RENDER_MODE == 'full':
        conns = conns + FACE_CONNECTIONS
    return conns


ACTIVE_CONNECTIONS = _active_connections()

# ── Helpers ───────────────────────────────────────────────────────────────────

def compute_canvas_params(frames):
    xs, ys = [], []
    for frame in frames:
        for kp_list in frame.values():
            for x, y, s in kp_list:
                if s >= CONF_THRESHOLD:
                    xs.append(x)
                    ys.append(y)

    if not xs:
        return (0, 1), (0, 1), CANVAS_SIZE, CANVAS_SIZE

    pad_x = (max(xs) - min(xs)) * 0.1 or 10
    pad_y = (max(ys) - min(ys)) * 0.1 or 10

    x_range = (min(xs) - pad_x, max(xs) + pad_x)
    y_range = (min(ys) - pad_y, max(ys) + pad_y)

    aspect = (x_range[1] - x_range[0]) / (y_range[1] - y_range[0])
    if aspect >= 1.0:
        W, H = CANVAS_SIZE, max(64, int(CANVAS_SIZE / aspect))
    else:
        W, H = max(64, int(CANVAS_SIZE * aspect)), CANVAS_SIZE

    return x_range, y_range, W, H


def to_canvas(x, y, x_range, y_range, W, H):
    px = int((x - x_range[0]) / (x_range[1] - x_range[0]) * W)
    py = int((y - y_range[0]) / (y_range[1] - y_range[0]) * H)
    return int(np.clip(px, 0, W - 1)), int(np.clip(py, 0, H - 1))


def draw_skeleton(canvas, kp_list, x_range, y_range, W, H, color):
    kps = kp_list  # lista de [x, y, score]
    n   = len(kps)
    radius    = max(3, W // 120)
    thickness = max(2, W // 200)

    for a, b in ACTIVE_CONNECTIONS:
        if a >= n or b >= n:
            continue
        xa, ya, sa = kps[a]
        xb, yb, sb = kps[b]
        if sa < CONF_THRESHOLD or sb < CONF_THRESHOLD:
            continue
        pa = to_canvas(xa, ya, x_range, y_range, W, H)
        pb = to_canvas(xb, yb, x_range, y_range, W, H)
        cv2.line(canvas, pa, pb, color, thickness, cv2.LINE_AA)

    # puntos visibles solo en body+feet (0-22)
    for x, y, s in kps[:23]:
        if s >= CONF_THRESHOLD:
            p = to_canvas(x, y, x_range, y_range, W, H)
            cv2.circle(canvas, p, radius, color, -1, cv2.LINE_AA)


def render_json(json_path: Path, output_path: Path):
    with open(json_path) as f:
        data = json.load(f)

    frames = data['keypoints']

    x_range, y_range, W, H = compute_canvas_params(frames)

    all_ids    = sorted({pid for frame in frames for pid in frame.keys()}, key=lambda x: int(x))
    id_to_color = {pid: COLORS[i % len(COLORS)] for i, pid in enumerate(all_ids)}

    # intentar mp4v, fallback a XVID+avi
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out    = cv2.VideoWriter(str(output_path), fourcc, FPS, (W, H))
    if not out.isOpened():
        output_path = output_path.with_suffix('.avi')
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        out = cv2.VideoWriter(str(output_path), fourcc, FPS, (W, H))

    for frame in frames:
        canvas = np.zeros((H, W, 3), dtype=np.uint8)
        for pid in sorted(frame.keys(), key=lambda x: int(x)):
            draw_skeleton(canvas, frame[pid], x_range, y_range, W, H, id_to_color[pid])
        out.write(canvas)

    out.release()
    print(f"  -> {output_path.name}  ({len(frames)} frames, {W}x{H}px, {len(all_ids)} persona/s)")


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    OUTPUT_DIR.mkdir(exist_ok=True)

    json_files = sorted(JSONS_DIR.glob('*.json'))
    if not json_files:
        print("No se encontraron archivos JSON en", JSONS_DIR)
        return

    print(f"Modo: {RENDER_MODE}  |  Conf. threshold: {CONF_THRESHOLD}  |  FPS: {FPS}")
    print(f"Procesando {len(json_files)} archivo/s...\n")

    for jp in json_files:
        print(f"{jp.name}")
        render_json(jp, OUTPUT_DIR / (jp.stem + '.mp4'))

    print(f"\nListo. Videos guardados en: {OUTPUT_DIR}")


if __name__ == '__main__':
    main()
