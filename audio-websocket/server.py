import asyncio
import whisper

from websockets.asyncio.server import serve

model = whisper.load_model("small")

async def processMessage(websocket):
  async for message in websocket:
    try:
      
      if type(message) == bytes:
        filename = "audio.webm"
        print(f"Recibido audio: {len(message)} bytes...")
        with open(filename, "wb") as audio_file:
          audio_file.write(message)
        
        result = await asyncio.to_thread(model.transcribe, filename, language="es")
        print(result["text"])
        
        await websocket.send(result["text"])
      elif type(message) == str:
        print("Recibido: ", message)
      else:
        print(f"Tipo desconocido: {type(message)}")
    except Exception as ex:
      print(f"Error: {ex}")

async def main():
  print("Servidor WebSocket inicializado...")
  server = await serve(processMessage, "localhost", 8765)
  await server.serve_forever()


if __name__ == "__main__":
  asyncio.run(main())