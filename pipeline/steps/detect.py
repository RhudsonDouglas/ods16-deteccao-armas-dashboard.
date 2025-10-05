from ultralytics import YOLO
from PIL import Image
import numpy as np

def run_inference(frames, cfg):
    model = YOLO(cfg.get("model_name", "yolov8n.pt"))
    conf = float(cfg.get("confidence_threshold", 0.4))
    results = []
    for path in frames:
        img = Image.open(path).convert("RGB")
        arr = np.array(img)
        pred = model.predict(arr, conf=conf, verbose=False)[0]
        dets = []
        for b in pred.boxes:
            x1, y1, x2, y2 = map(float, b.xyxy[0].tolist())
            cls = int(b.cls[0].item())
            score = float(b.conf[0].item())
            dets.append({
                "source_path": str(path),
                "bbox": (x1, y1, x2, y2),
                "cls": cls,
                "score": score
            })
        results.append({"source": str(path), "detections": dets})
    return results
