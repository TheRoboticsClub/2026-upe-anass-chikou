class AudioProcessor extends AudioWorkletProcessor {
  constructor() {
    super();
  }

  process(inputs, outputs, parameters) {
    // [0] primera entrada, solo tenemos el micrófono 
    // [0] segunda entrada, canal de audio (mono, estéreo)
    const channelData = inputs[0][0];
    if (inputs && channelData) {
      this.port.postMessage(channelData.slice());
    }

    return true;
  }
}

registerProcessor("audio-worklet", AudioProcessor);