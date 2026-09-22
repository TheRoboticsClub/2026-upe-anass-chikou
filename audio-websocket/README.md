# Audio WebSocket
 
Programa de prueba para grabar audio desde el navegador, enviarlo a un servidor Python vía WebSocket y transcribirlo a texto con Whisper.
 
## Instalación y uso
 
1. **Instala `ffmpeg`** (si no lo tienes ya):
   
  - **Windows** (con `winget`):
```powershell
     winget install ffmpeg
```
  - **Linux / WSL**:
```bash
     sudo apt update
     sudo apt install ffmpeg
```
 
2. **Instala las dependencias de Python:**
```bash
   pip install websockets openai-whisper
```
 
3. **Arranca el servidor:**
```bash
   python server.py
```
  (En Linux/WSL puede que se necesite usar `python3` en vez de `python`)
 
  Deberías ver `Servidor WebSocket inicializado...` en la terminal.
 
4. **Abre `index.html`** en el navegador.
5. **Pulsa "Grabar audio"** y concede permiso de micrófono si el navegador lo solicita.
6. **Pulsa "Parar audio"** cuando termines de grabar.
7. En el directorio del proyecto encontrarás `audio.webm`, y la transcripción aparecerá tanto en la terminal del servidor como en la página web.

 
## Notas
 
- La primera vez que se ejecuta el servidor, Whisper descarga el modelo (`base`, `small`, etc.) automáticamente, esto puede tardar unos segundos o minutos.
- Si `ffmpeg` no está instalado correctamente, Whisper no podrá procesar el audio y dará error al transcribir.