import pandas as pd

REQUIRED = {
    "alert_id","source_id","timestamp","cls","score",
    "bbox_xmin","bbox_ymin","bbox_xmax","bbox_ymax","snapshot_path"
}

def test_minimum_schema():
    df = pd.DataFrame([{
        "alert_id": 1, "source_id": "data/img.jpg", "timestamp": None,
        "cls": 0, "score": 0.9,
        "bbox_xmin": 0, "bbox_ymin": 0, "bbox_xmax": 10, "bbox_ymax": 10,
        "snapshot_path": "snapshots/alert_000001.jpg"
    }])
    assert REQUIRED.issubset(df.columns)
