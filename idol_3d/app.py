import os
import json
import time
import shutil
import requests
from flask import Flask, request, jsonify, send_file, Response

app = Flask(__name__)

OPTIONS_PATH = "/data/options.json"
OUTPUT_DIR = "/data/outputs"
HA_WWW_DIR = "/config/www/idol_out"
BASE_URL = "https://speridlabs-idol.hf.space"

os.makedirs(OUTPUT_DIR, exist_ok=True)
try:
    os.makedirs(HA_WWW_DIR, exist_ok=True)
except Exception:
    pass


def get_options():
    if os.path.exists(OPTIONS_PATH):
        try:
            with open(OPTIONS_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {
        "hf_token": "",
        "default_mode": "real",
        "default_gaussians": 262144
    }


HTML_PAGE = """<!DOCTYPE html>
<html lang="pl">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Speridlabs Idol 3D - Home Assistant</title>
  <style>
    :root {
      --bg: #111111;
      --card: #1c1c1c;
      --text: #e1e1e1;
      --accent: #03a9f4;
      --accent-hover: #0288d1;
      --border: #2c2c2c;
    }
    * { box-sizing: border-box; }
    body, html {
      margin: 0; padding: 0; width: 100%; height: 100%;
      background: var(--bg); color: var(--text);
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
      display: flex; flex-direction: row; overflow: hidden;
    }
    #sidebar {
      width: 350px; min-width: 310px; background: var(--card);
      border-right: 1px solid var(--border); padding: 20px;
      display: flex; flex-direction: column; gap: 15px; overflow-y: auto; z-index: 10;
    }
    h2 { margin: 0; font-size: 18px; display: flex; align-items: center; gap: 8px; color: #fff; }
    .field { display: flex; flex-direction: column; gap: 6px; font-size: 13px; }
    label { color: #aaa; font-weight: 500; }
    input[type="file"], select, input[type="number"] {
      background: #262626; border: 1px solid var(--border); color: var(--text);
      padding: 9px 10px; border-radius: 6px; font-size: 13px; width: 100%;
    }
    #dropzone {
      border: 2px dashed #444; border-radius: 8px; padding: 18px;
      text-align: center; cursor: pointer; transition: 0.2s; background: #161616;
    }
    #dropzone:hover, #dropzone.dragover { border-color: var(--accent); background: #1a242b; }
    #preview { max-width: 100%; max-height: 160px; border-radius: 6px; display: none; margin: 10px auto 0; object-fit: contain; }
    button {
      background: var(--accent); color: #fff; border: none; padding: 12px;
      border-radius: 6px; font-size: 14px; font-weight: 600; cursor: pointer; transition: 0.2s;
    }
    button:hover:not(:disabled) { background: var(--accent-hover); }
    button:disabled { opacity: 0.5; cursor: not-allowed; }
    #status {
      font-size: 13px; padding: 10px; border-radius: 6px;
      background: #222; border: 1px solid var(--border); min-height: 42px; line-height: 1.4;
    }
    .actions { display: flex; gap: 8px; }
    .btn-secondary {
      background: #2c2c2c; color: #fff; text-decoration: none; text-align: center;
      padding: 10px; border-radius: 6px; font-size: 13px; flex: 1; font-weight: 500;
      border: 1px solid #3d3d3d;
    }
    .btn-secondary:hover { background: #383838; }
    #viewer-container { flex: 1; position: relative; height: 100%; background: #0a0a0a; }
    canvas { width: 100%; height: 100%; display: block; }
    #viewer-hint {
      position: absolute; bottom: 14px; right: 16px; background: rgba(0,0,0,0.65);
      padding: 6px 12px; border-radius: 6px; font-size: 12px; color: #999; pointer-events: none;
    }
    @media (max-width: 768px) {
      body { flex-direction: column; overflow-y: auto; }
      #sidebar { width: 100%; border-right: none; border-bottom: 1px solid var(--border); }
      #viewer-container { min-height: 60vh; }
    }
  </style>
</head>
<body>
  <div id="sidebar">
    <h2>Speridlabs Idol 3D</h2>

    <div id="dropzone" onclick="document.getElementById('fileInput').click()">
      <div id="drop-text">Kliknij lub przeciągnij zdjęcie tutaj (JPG/PNG)</div>
      <img id="preview" alt="Podgląd" />
      <input type="file" id="fileInput" accept="image/*" style="display:none" />
    </div>

    <div class="field">
      <label for="mode">Tryb wycinania i kadrowania</label>
      <select id="mode">
        <option value="real" __SEL_REAL__>Fotografia (Real - margines 1.7x)</option>
        <option value="synthetic" __SEL_SYNTH__>Render / AI (Synthetic - margines 1.2x)</option>
      </select>
    </div>

    <div class="field">
      <label for="gaussians">Liczba punktów (Gaussians)</label>
      <select id="gaussians">
        <option value="32768">32 768 (Szybki / ~0.4 MB)</option>
        <option value="65536">65 536 (Lekki / ~0.8 MB)</option>
        <option value="262144" selected>262 144 (Domyślny / ~3.2 MB)</option>
        <option value="524288">524 288 (Wysoki / ~6.1 MB)</option>
        <option value="1048576">1 048 576 (Maksymalny / ~12.2 MB)</option>
      </select>
    </div>

    <div class="field">
      <label for="seed">Seed</label>
      <input type="number" id="seed" value="42" />
    </div>

    <button id="genBtn" onclick="generate3D()" disabled>Wygeneruj obiekt 3D</button>

    <div id="status">Wybierz zdjęcie, aby rozpocząć. Jeśli w folderze jest już model, wyświetli się obok.</div>

    <div class="actions" id="downloadBox" style="display:none;">
      <a id="dlPly" class="btn-secondary" href="latest.ply" download="idol_model.ply">Pobierz .PLY</a>
    </div>
  </div>

  <div id="viewer-container">
    <div id="viewer-hint">LPM: obrót | PPM: przesunięcie | Rolka: zoom</div>
  </div>

  <script type="module">
    import * as SPLAT from "https://cdn.jsdelivr.net/npm/gsplat@latest";

    const container = document.getElementById("viewer-container");
    const scene = new SPLAT.Scene();
    const camera = new SPLAT.Camera();
    const renderer = new SPLAT.WebGLRenderer();
    container.appendChild(renderer.canvas);
    const controls = new SPLAT.OrbitControls(camera, renderer.canvas);

    function resize() {
      renderer.setSize(container.clientWidth, container.clientHeight);
    }
    window.addEventListener("resize", resize);
    resize();

    let animRunning = false;
    function startRenderLoop() {
      if (animRunning) return;
      animRunning = true;
      const frame = () => {
        controls.update();
        renderer.render(scene, camera);
        requestAnimationFrame(frame);
      };
      requestAnimationFrame(frame);
    }

    window.loadSplatModel = async function(url) {
      try {
        scene.reset();
        await SPLAT.PLYLoader.LoadAsync(url, scene);
        startRenderLoop();
        document.getElementById("downloadBox").style.display = "flex";
      } catch (err) {
        console.log("Brak poprzedniego modelu lub błąd ładowania:", err);
      }
    };

    window.loadSplatModel("latest.ply?t=" + Date.now());
  </script>

  <script>
    const fileInput = document.getElementById("fileInput");
    const preview = document.getElementById("preview");
    const dropzone = document.getElementById("dropzone");
    const genBtn = document.getElementById("genBtn");
    const statusEl = document.getElementById("status");
    let selectedFile = null;

    fileInput.addEventListener("change", (e) => {
      if (e.target.files.length > 0) handleFile(e.target.files[0]);
    });

    dropzone.addEventListener("dragover", (e) => {
      e.preventDefault();
      dropzone.classList.add("dragover");
    });
    dropzone.addEventListener("dragleave", () => dropzone.classList.remove("dragover"));
    dropzone.addEventListener("drop", (e) => {
      e.preventDefault();
      dropzone.classList.remove("dragover");
      if (e.dataTransfer.files.length > 0) handleFile(e.dataTransfer.files[0]);
    });

    function handleFile(file) {
      selectedFile = file;
      const reader = new FileReader();
      reader.onload = (e) => {
        preview.src = e.target.result;
        preview.style.display = "block";
        document.getElementById("drop-text").textContent = file.name;
        genBtn.disabled = false;
      };
      reader.readAsDataURL(file);
    }

    async function generate3D() {
      if (!selectedFile) return;
      genBtn.disabled = true;
      statusEl.textContent = "Wysyłanie zdjęcia do klastra ZeroGPU (Speridlabs Idol)...";

      const formData = new FormData();
      formData.append("image", selectedFile);
      formData.append("mode", document.getElementById("mode").value);
      formData.append("gaussians", document.getElementById("gaussians").value);
      formData.append("seed", document.getElementById("seed").value);

      const t0 = Date.now();
      try {
        const res = await fetch("generate", {
          method: "POST",
          body: formData
        });
        const data = await res.json();
        if (!res.ok || data.error) {
          throw new Error(data.error || "Błąd serwera API");
        }
        const elapsed = ((Date.now() - t0) / 1000).toFixed(1);
        statusEl.textContent = `Gotowe w ${elapsed} s! Ładowanie modelu 3D do przeglądarki...`;
        const plyUrl = "latest.ply?t=" + Date.now();
        document.getElementById("dlPly").href = plyUrl;
        await window.loadSplatModel(plyUrl);
        statusEl.textContent = `Obiekt 3D wygenerowany (${elapsed} s). Zapisano też w /config/www/idol_out/latest.ply.`;
      } catch (err) {
        statusEl.textContent = "Błąd: " + err.message;
      } finally {
        genBtn.disabled = false;
      }
    }
  </script>
</body>
</html>
"""


@app.route("/", methods=["GET"])
def index():
    opts = get_options()
    mode = opts.get("default_mode", "real")
    html = HTML_PAGE.replace("__SEL_REAL__", "selected" if mode == "real" else "")
    html = html.replace("__SEL_SYNTH__", "selected" if mode == "synthetic" else "")
    return Response(html, mimetype="text/html")


@app.route("/latest.ply", methods=["GET"])
def get_latest_ply():
    latest_file = os.path.join(OUTPUT_DIR, "latest.ply")
    if not os.path.exists(latest_file):
        return jsonify({"error": "Brak wygenerowanego modelu"}), 404
    return send_file(latest_file, mimetype="application/octet-stream", as_attachment=False)


@app.route("/generate", methods=["POST"])
def generate():
    if "image" not in request.files:
        return jsonify({"error": "Nie przesłano pliku obrazu."}), 400

    img_file = request.files["image"]
    mode = request.form.get("mode", "real")
    gaussians = int(request.form.get("gaussians", 262144))
    seed = int(request.form.get("seed", 42))

    opts = get_options()
    hf_token = opts.get("hf_token", "").strip()

    headers = {}
    if hf_token:
        headers["Authorization"] = f"Bearer {hf_token}"

    temp_img = os.path.join(OUTPUT_DIR, "input_upload.jpg")
    img_file.save(temp_img)

    try:
        with open(temp_img, "rb") as f:
            up_res = requests.post(
                f"{BASE_URL}/gradio_api/upload",
                headers=headers,
                files={"files": (img_file.filename or "image.jpg", f, img_file.mimetype or "image/jpeg")},
                timeout=60
            )
        up_res.raise_for_status()
        uploaded_path = up_res.json()[0]

        payload = {
            "data": [
                {"path": uploaded_path, "meta": {"_type": "gradio.FileData"}},
                mode,
                seed,
                gaussians
            ]
        }
        call_res = requests.post(
            f"{BASE_URL}/gradio_api/call/generate",
            headers={**headers, "Content-Type": "application/json"},
            json=payload,
            timeout=30
        )
        call_res.raise_for_status()
        event_id = call_res.json()["event_id"]

        stream_res = requests.get(
            f"{BASE_URL}/gradio_api/call/generate/{event_id}",
            headers=headers,
            stream=True,
            timeout=180
        )
        stream_res.raise_for_status()

        ply_url = None
        last_event = ""
        for line in stream_res.iter_lines(decode_unicode=True):
            if not line:
                continue
            if line.startswith("event:"):
                last_event = line[6:].strip()
            elif line.startswith("data:"):
                data_str = line[5:].strip()
                if last_event == "error":
                    raise RuntimeError(f"ZeroGPU API Error: {data_str}")
                try:
                    parsed = json.loads(data_str)
                    if isinstance(parsed, list) and len(parsed) > 0:
                        first_item = parsed[0]
                        if isinstance(first_item, dict) and ("url" in first_item or "path" in first_item):
                            ply_url = first_item.get("url") or f"{BASE_URL}/gradio_api/file={first_item['path']}"
                            break
                except Exception:
                    continue

        if not ply_url:
            raise RuntimeError("API nie zwróciło ścieżki do pliku .ply (sprawdź limit ZeroGPU lub poprawność tokena HF).")

        dl_res = requests.get(ply_url, headers=headers, timeout=120)
        dl_res.raise_for_status()

        latest_ply = os.path.join(OUTPUT_DIR, "latest.ply")
        with open(latest_ply, "wb") as out_f:
            out_f.write(dl_res.content)

        if os.path.exists("/config"):
            os.makedirs(HA_WWW_DIR, exist_ok=True)
            timestamp_name = f"idol_{int(time.time())}.ply"
            shutil.copy(latest_ply, os.path.join(HA_WWW_DIR, "latest.ply"))
            shutil.copy(latest_ply, os.path.join(HA_WWW_DIR, timestamp_name))

        return jsonify({"status": "ok"})

    except Exception as e:
        return jsonify({"error": str(e)}), 500
