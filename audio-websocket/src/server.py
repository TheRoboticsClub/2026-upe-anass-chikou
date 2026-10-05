import asyncio
import numpy as np
import torch
from faster_whisper import WhisperModel
from websockets.asyncio.server import serve

# Code taken from and inspired by [DialoStack](https://github.com/aquintan4/DialoStack)
class SpeechToText:
    def __init__(self):
        self.sample_rate = 16000
        self.language = "es"
        self.model_size = "base"
        self.vad_threshold = 0.5
        self.grace_period = 0.5
        self.max_phrase_secs = 3.0

        self.chunk_size = 512
        self.max_silence = int(self.grace_period * self.sample_rate / self.chunk_size)
        self.max_phrase_chunks = int(
            self.max_phrase_secs * self.sample_rate / self.chunk_size
        )
        self.min_phrase_chunks = 5

        self.load_silero_model()
        self.load_whisper_model()

    def load_silero_model(self) -> None:
        self.silero_model, _ = torch.hub.load(
            repo_or_dir="snakers4/silero-vad", model="silero_vad", trust_repo=True
        )

    def load_whisper_model(self) -> None:
        self.whisper = WhisperModel(
            self.model_size, device="cpu", compute_type="int8", cpu_threads=4
        )

    async def processMessage(self, websocket) -> None:
        phrase = []
        silence = 0
        vad_buffer = np.array([], dtype=np.float32)

        try:
            async for message in websocket:
                if type(message) == bytes:
                    audio_chunk = np.frombuffer(message, dtype=np.float32)
                    vad_buffer = np.concatenate((vad_buffer, audio_chunk))

                    # Silero needs 512 chunks
                    while len(vad_buffer) >= self.chunk_size:
                        chunk = vad_buffer[:self.chunk_size]
                        vad_buffer = vad_buffer[self.chunk_size:]

                        tensor_chunk = torch.from_numpy(chunk.flatten()).float()
                        speech_prob = self.silero_model(tensor_chunk, self.sample_rate).item()
                        is_voice = speech_prob > self.vad_threshold

                        if is_voice:
                            phrase.append(chunk)
                            silence = 0
                        elif phrase:
                            # Silence after talking
                            phrase.append(chunk)
                            silence += 1

                        if silence > self.max_silence and phrase:
                          await self.flush_phrase(websocket, phrase)                        
                          phrase = []
                          silence = 0
                        if len(phrase) > self.max_phrase_chunks:
                          await self.flush_phrase(websocket, phrase)                        
                          phrase = []
                          silence = 0
                      
                elif type(message) == str:
                    if message == "Stop":
                      await self.flush_phrase(websocket, phrase)
                      vad_buffer = np.array([], dtype=np.float32)
                      
                      phrase = []
                      silence = 0
                    else:
                      print(f"Recibido: {message}")
                else:
                    print(f"Tipo desconocido: {type(message)}")

        except Exception as ex:
            print(f"Error: {ex}")

    
    async def flush_phrase(self, websocket, chunks: list[np.ndarray]) -> None:
        if len(chunks) <= self.min_phrase_chunks:
            return

        audio = np.concatenate(chunks).flatten()
        await self.transcribe_audio(websocket, audio)
                       
    async def transcribe_audio(self, websocket, audio: np.ndarray) -> None:
        print(f"Duracion frase: {len(audio) / self.sample_rate}")

        def obtain_text() -> str:
            segments, _ = self.whisper.transcribe(
                audio,
                language=self.language,
                beam_size=3,
                temperature=0.0,
                condition_on_previous_text=False
            )

            return "".join(segment.text for segment in segments).strip()

        text = await asyncio.to_thread(obtain_text)

        if text:
            print(f"\nTranscripción: {text}")
            await websocket.send(text)


async def main():
    speech_text = SpeechToText()
    print("Servidor WebSocket inicializado...")
    server = await serve(speech_text.processMessage, "localhost", 8765)
    await server.serve_forever()


if __name__ == "__main__":
    asyncio.run(main())