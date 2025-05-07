import wave
import numpy as np

def text_to_bits(text):
    return ''.join(f'{ord(c):08b}' for c in text)

def bits_to_text(bits):
    chars = [chr(int(bits[i:i+8], 2)) for i in range(0, len(bits), 8)]
    return ''.join(chars)

def embed_message_in_audio(audio_path, message, output_path, delta=5):
    with wave.open(audio_path, 'rb') as audio:
        params = audio.getparams()
        frames = audio.readframes(params.nframes)
        audio_data = np.frombuffer(frames, dtype=np.int16).copy()

    message_bits = text_to_bits(message)
    if len(message_bits) > len(audio_data):
        raise ValueError("Mesaj sığmıyor!")

    for i, bit in enumerate(message_bits):
        for j in range(3):
            idx = i * 3 + j
            if idx >= len(audio_data):
                break
            audio_data[idx] = np.clip(audio_data[idx] + (delta if bit == '1' else -delta), -32768, 32767)


    with wave.open(output_path, 'wb') as out:
        out.setparams(params)
        out.writeframes(audio_data.tobytes())

    print(f"Mesaj gömüldü: {output_path}")

def extract_message_from_audio(original_path, modified_path, message_bit_length, delta=5):
    with wave.open(original_path, 'rb') as orig, wave.open(modified_path, 'rb') as mod:
        orig_data = np.frombuffer(orig.readframes(orig.getnframes()), dtype=np.int16)
        mod_data = np.frombuffer(mod.readframes(mod.getnframes()), dtype=np.int16)

    bits = ''
    for i in range(message_bit_length):
        votes = []
        for j in range(3):
            idx = i * 3 + j
            if idx >= len(orig_data):
                break
            diff = mod_data[idx] - orig_data[idx]
            if diff >= delta:
                votes.append('1')
            elif diff <= -delta:
                votes.append('0')
        bits += max(set(votes), key=votes.count) if votes else '0'

    return bits_to_text(bits)

if __name__ == "__main__":
    original_file = 'C:/Users/nurda/Downloads/kriptoloji-main/kriptoloji-main/8s_audio.wav'
    output_file = "8s_audio_with_message.wav"
    message = input("Gizlenecek mesaj: ")

    bit_count = len(text_to_bits(message))

    embed_message_in_audio(original_file, message, output_file, delta=10)
    extracted = extract_message_from_audio(original_file, output_file, bit_count, delta=10)

    print("Çıkarılan mesaj:", extracted)