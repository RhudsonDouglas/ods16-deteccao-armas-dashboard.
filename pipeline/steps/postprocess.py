import itertools

def postprocess(detections, cfg):
    # Se precisar, implemente NMS adicional aqui usando cfg["iou_threshold"]
    alerts = []
    counter = itertools.count(1)
    for item in detections:
        for d in item["detections"]:
            alerts.append({
                "alert_id": next(counter),
                "source_id": d["source_path"],
                "timestamp": None,  # preencha se tiver metadados
                "cls": d["cls"],
                "score": d["score"],
                "bbox_xmin": d["bbox"][0],
                "bbox_ymin": d["bbox"][1],
                "bbox_xmax": d["bbox"][2],
                "bbox_ymax": d["bbox"][3],
                "snapshot_path": None  # será preenchido na exportação
            })
    return alerts
