class AudioProcessor extends AudioWorkletProcessor {
  constructor() {
    super();
    this.buffer = new Float32Array(512);
    this.offset = 0;
  }

  process(inputs, outputs, parameters) {
    const input = inputs[0];
    if (!input || !input[0]) return true;
    const channelData = input[0]; // 128 muestras

    this.buffer.set(channelData, this.offset);
    this.offset += channelData.length;

    if (this.offset >= 512) {
      this.port.postMessage(this.buffer.slice());
      this.buffer = new Float32Array(512);
      this.offset = 0;
    }
    
    return true;
  }
}

registerProcessor("audio-worklet", AudioProcessor);