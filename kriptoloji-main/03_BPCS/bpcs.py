import numpy as np
from PIL import Image

def message_to_bits(message):
    length = len(message)
    length_bits = format(length, '016b')  # 2 byte length info
    message_bits = ''.join([format(ord(c), '08b') for c in message])
    return length_bits + message_bits

def bits_to_message(bits):
    length = int(bits[:16], 2)
    message_bits = bits[16:16 + (length * 8)]
    message = ''.join([chr(int(message_bits[i:i+8], 2)) for i in range(0, len(message_bits), 8)])
    return message

def calculate_complexity(block):
    vertical = np.sum(block[:, :-1] != block[:, 1:])
    horizontal = np.sum(block[:-1, :] != block[1:, :])
    total = vertical + horizontal
    max_transitions = 2 * block.shape[0] * (block.shape[1] - 1)
    return total / max_transitions

def embed_message(image_path, message, output_path, threshold=0.2):
    img = Image.open(image_path).convert('L')
    img_np = np.array(img)
    height, width = img_np.shape

    bits = message_to_bits(message)
    msg_idx = 0

    flat_img = img_np.flatten()
    bit_planes = [((flat_img >> i) & 1).reshape(height, width) for i in range(8)]

    for plane in range(7, -1, -1):  # From LSB to MSB
        for y in range(0, height, 8):
            for x in range(0, width, 8):
                if msg_idx >= len(bits):
                    break
                block = bit_planes[plane][y:y+8, x:x+8]
                if block.shape != (8,8):
                    continue
                if calculate_complexity(block) >= threshold:
                    part = bits[msg_idx:msg_idx+64]
                    part += '0' * (64 - len(part))  # padding if needed
                    bit_planes[plane][y:y+8, x:x+8] = np.array(list(part), dtype=np.uint8).reshape(8, 8)
                    msg_idx += 64

    if msg_idx < len(bits):
        raise ValueError("Image does not have enough complex blocks to embed the full message.")

    new_img_np = np.zeros_like(flat_img)
    for i in range(8):
        new_img_np += (bit_planes[i].flatten().astype(np.uint8) << i)
    new_img = Image.fromarray(new_img_np.reshape((height, width)))
    new_img.save(output_path)
    print("Message successfully embedded into:", output_path)

def extract_message(image_path, threshold=0.2):
    img = Image.open(image_path).convert('L')
    img_np = np.array(img)
    height, width = img_np.shape

    flat_img = img_np.flatten()
    bit_planes = [((flat_img >> i) & 1).reshape(height, width) for i in range(8)]

    bits = ""
    for plane in range(7, -1, -1):
        for y in range(0, height, 8):
            for x in range(0, width, 8):
                block = bit_planes[plane][y:y+8, x:x+8]
                if block.shape != (8,8):
                    continue
                if calculate_complexity(block) >= threshold:
                    for row in block:
                        bits += ''.join(row.astype(str))
                    if len(bits) >= 16:
                        length = int(bits[:16], 2)
                        total_len = 16 + length * 8
                        if len(bits) >= total_len:
                            return bits_to_message(bits[:total_len])
    return "[No message found]"

# === Example usage ===
if __name__ == "__main__":
    # Step 1: Embed
    embed_message("../kriptoloji.jpg", "Bu gizli bir mesajdir!", "output_embedded.png")

    # Step 2: Extract
    extracted = extract_message("../output_embedded.png")
    print("Extracted message:", extracted)
