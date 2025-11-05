from PIL import Image
import numpy as np


def text_to_bits(text):
    return ''.join(f'{ord(c):08b}' for c in text)


def bits_to_text(bits):
    chars = [bits[i:i + 8] for i in range(0, len(bits), 8)]
    return ''.join(chr(int(b, 2)) for b in chars)


def hide_message_with_mask(img_path, message, channel='B', output_img='hidden.png', output_mask='mask.png'):
    img = Image.open(img_path).convert('RGB')
    arr = np.array(img)
    h, w, _ = arr.shape

    ch_idx = 'RGB'.index(channel)
    flat = arr[:, :, ch_idx].flatten()

    bitstring = text_to_bits(message)
    if len(bitstring) > flat.size:
        raise ValueError(f"Message too long. Max bits: {flat.size}, required: {len(bitstring)}")

    changed_mask = np.zeros(flat.shape, dtype=np.uint8)

    for i, bit in enumerate(bitstring):
        orig_bit = flat[i] & 1
        new_bit = int(bit)
        if orig_bit != new_bit:
            flat[i] = (flat[i] & 0xFE) | new_bit
            changed_mask[i] = 255  # mark change

    arr[:, :, ch_idx] = flat.reshape(h, w)

    Image.fromarray(arr).save(output_img)

    mask_arr = np.zeros_like(arr)
    mask_arr[:, :, ch_idx] = changed_mask.reshape(h, w)
    Image.fromarray(mask_arr).save(output_mask)

    print(f"Hidden message in {output_img}")
    print(f"Mask showing changed bits saved to {output_mask}")


def extract_message(img_path, message_length, channel='B'):
    img = Image.open(img_path).convert('RGB')
    arr = np.array(img)
    flat = arr[:, :, 'RGB'.index(channel)].flatten()
    bits = ''.join(str(flat[i] & 1) for i in range(message_length * 8))
    return bits_to_text(bits)


hide_message_with_mask('assets_main/coffee.png', 'Secret message', channel='B',
                       output_img='assets_main/coffee_hidden.png',
                       output_mask='assets_main/coffee_mask.png')
msg = extract_message('assets_main/coffee_hidden.png', message_length=14, channel='B')
print(msg)
