import argparse
import os
import yaml
from steps.load import load_inputs
from steps.detect import run_inference
from steps.postprocess import postprocess
from steps.export import export_outputs

def main():
    parser = argparse.ArgumentParser(description="Pipeline offline ODS16")
    parser.add_argument("--config", required=True, help="caminho do config.yaml")
    args = parser.parse_args()

    with open(args.config, "r", encoding="utf-8") as f:
        cfg = yaml.safe_load(f)

    os.makedirs(cfg["output_dir"], exist_ok=True)
    os.makedirs(cfg["snapshots_dir"], exist_ok=True)

    frames = load_inputs(cfg)              # 1) Entrada
    detections = run_inference(frames, cfg) # 2) Inferência
    alerts = postprocess(detections, cfg)   # 3) Pós-processamento
    export_outputs(alerts, cfg)             # 4) Exportação

if __name__ == "__main__":
    main()
