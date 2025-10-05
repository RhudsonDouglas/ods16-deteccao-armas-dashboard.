from pathlib import Path

def load_inputs(cfg):
    input_dir = Path(cfg["input_dir"])
    # Exemplo simples: coleciona imagens .jpg/.png (se tiver vídeos, depois a gente extrai frames com OpenCV)
    frames = sorted(list(input_dir.glob("*.jpg"))) + sorted(list(input_dir.glob("*.png")))
    return frames
