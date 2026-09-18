# Audio WebSocket

Programa de prueba para grabar audio desde el navegador y enviarlo a un servidor Python vía WebSocket.

## Requisitos

- Python con la librería [`websockets`](https://websockets.readthedocs.io/) instalada:
  ```
  pip install websockets
  ```

## Uso

1. **Arrancar el servidor:**
   ```
   python server.py
   ```

2. **Abre `index.html`** en el navegador.

3. **Pulsa "Grabar audio"** y concede permiso de micrófono si el navegador lo solicita.

4. **Pulsa "Parar audio"** cuando termines de grabar.

5. En el directorio del proyecto encontrarás `audio.webm` listo para escuchar.