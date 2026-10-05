// https://developer.chrome.com/blog/audio-worklet
// https://developer.mozilla.org/en-US/docs/Web/API/Web_Audio_API/Using_AudioWorklet

let audioStream = null, audioContext = null, audioSource = null, audioWorklet = null

const ws = new WebSocket("ws://localhost:8765");
const playBtn = document.querySelector("#btn-play");
const stopBtn = document.querySelector("#btn-stop");
const test = document.querySelector("#test");

ws.addEventListener("open", () => {
  console.log("Conectado...");
});

ws.addEventListener("message", (ev) => {
  console.log(`Mensaje recibido: ${ev.data}`);
  test.textContent = test.textContent + "\n" + ev.data;
});

ws.addEventListener("error", (ev) => {
  console.error(`Error: ${ev}`);
});

ws.addEventListener("close", (event) => {
  console.log(`Conexión cerrada\nCódigo: ${event.code}\nRazón: ${event.reason}`);
});

async function startAudio() {
  audioStream = await navigator.mediaDevices.getUserMedia({ audio: true });

  audioContext = new AudioContext({ sampleRate: 16000 });
  await audioContext.audioWorklet.addModule("worklet.js");
  audioSource = audioContext.createMediaStreamSource(audioStream);

  // AudioWorletNode - audio crudo (HTPPS)
  audioWorklet = new AudioWorkletNode(audioContext, "audio-worklet");
  audioSource.connect(audioWorklet);
  audioWorklet.port.onmessage = (ev) => {
    if (ws.readyState === WebSocket.OPEN) {
      ws.send(ev.data);
    }
  }

  playBtn.disabled = true;
  stopBtn.disabled = false;
}

async function stopAudio() {
  if (ws.readyState === WebSocket.OPEN) {
    ws.send("Stop"); // Lo hacemos para que no se corte la frase al final de repente
  }
  
  if (audioWorklet) {
    audioWorklet.port.onmessage = null;
    audioWorklet.disconnect();
    audioWorklet = null;
  }

  if (audioSource) {
    audioSource.disconnect();
    audioSource = null;
  }

  if (audioStream) {
    audioStream.getTracks().forEach(track => track.stop());
    audioStream = null;
  }

  if (audioContext) {
    await audioContext.close();
    audioContext = null;
  }

  playBtn.disabled = false;
  stopBtn.disabled = true;
}

playBtn.addEventListener("click", startAudio);
stopBtn.addEventListener("click", stopAudio);