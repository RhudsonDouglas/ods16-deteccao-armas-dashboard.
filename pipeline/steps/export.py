from pathlib import Path
import pandas as pd
from PIL import Image

REQUIRED_COLS = [
    "alert_id","source_id","timestamp","cls","score",
    "bbox_xmin","bbox_ymin","bbox_xmax","bbox_ymax","snapshot_path"
]

def export_outputs(alerts, cfg):
    outdir = Path(cfg["output_dir"])
    snaps = Path(cfg["snapshots_dir"])
    snaps.mkdir(parents=True, exist_ok=True)

    df = pd.DataFrame(alerts)

    snap_paths = []
    for _, row in df.iterrows():
        try:
            im = Image.open(row["source_id"]).convert("RGB")
            box = (int(row["bbox_xmin"]), int(row["bbox_ymin"]), int(row["bbox_xmax"]), int(row["bbox_ymax"]))
            crop = im.crop(box)
            snap_name = f"alert_{int(row['alert_id']):06d}.jpg"
            crop.save(snaps / snap_name, "JPEG", quality=90)
            snap_paths.append(str((snaps / snap_name).as_posix()))
        except Exception:
            snap_paths.append(None)

    df["snapshot_path"] = snap_paths

    missing = set(REQUIRED_COLS) - set(df.columns)
    if missing:
        raise ValueError(f"Colunas obrigatórias ausentes: {missing}")

    if cfg.get("export_parquet", True):
        df.to_parquet(outdir / "alerts.parquet", index=False)
    if cfg.get("export_csv", True):
        df.to_csv(outdir / "alerts.csv", index=False)
