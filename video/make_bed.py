from math import sin, pi
from pathlib import Path
import wave

rate = 44100
seconds = 12
path = Path("public/ambient-bed.wav")
path.parent.mkdir(parents=True, exist_ok=True)

with wave.open(str(path), "w") as stream:
    stream.setnchannels(2)
    stream.setsampwidth(2)
    stream.setframerate(rate)
    for i in range(rate * seconds):
        t = i / rate
        fade = min(1.0, t / 1.5, (seconds - t) / 1.5)
        pad = 0.032 * (sin(2 * pi * 110 * t) + 0.55 * sin(2 * pi * 164.81 * t))
        shimmer = 0.009 * sin(2 * pi * 329.63 * t + sin(t * 0.7))
        sample = max(-1.0, min(1.0, (pad + shimmer) * fade))
        value = int(sample * 32767)
        stream.writeframesraw(value.to_bytes(2, "little", signed=True) * 2)

print(path)
