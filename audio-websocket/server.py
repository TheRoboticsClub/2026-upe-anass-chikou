#!/usr/bin/env python

"""Echo server using the asyncio API."""

import asyncio
from websockets.asyncio.server import serve

async def processMessage(websocket):
  async for message in websocket:
    if type(message) == bytes:
      print(f"Recibido audio: {len(message)} bytes...")
      with open("audio.webm", "wb") as audio_file:
        audio_file.write(message)
    elif type(message) == str:
      print("Recibido: ", message)
    else:
      print(f"Tipo desconocido: {type(message)}")
    await websocket.send("Mensaje recibido por el servidor")

async def main():
  print("Servidor WebSocket inicializado...")
  server = await serve(processMessage, "localhost", 8765)
  await server.serve_forever()


if __name__ == "__main__":
  asyncio.run(main())