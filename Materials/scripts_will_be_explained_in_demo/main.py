from PIL import Image
import numpy as np


def text_to_bits(text):
    return ''.join(f'{ord(c):08b}' for c in text)


def bits_to_text(bits):
    return ''.join(chr(int(bits[i:i + 8], 2)) for i in range(0, len(bits), 8))


def hide_message_with_mask(img_path, message, channel='R', bit_position=0,
                           output_img='hidden.png', output_mask='mask.png'):
    img = Image.open(img_path).convert('RGB')
    arr = np.array(img)
    h, w, _ = arr.shape

    ch_idx = 'RGB'.index(channel)
    flat = arr[:, :, ch_idx].flatten()

    bitstring = text_to_bits(message)
    if len(bitstring) > flat.size:
        raise ValueError("Message too large for image.")

    changed_mask = np.zeros_like(flat, dtype=np.uint8)

    bit_mask = 1 << bit_position
    clear_mask = (~bit_mask) & 0xFF

    for i, bit in enumerate(bitstring):
        bit_val = (int(bit) << bit_position) & 0xFF
        original = flat[i]

        new = (flat[i] & clear_mask) | bit_val

        if new != original:
            changed_mask[i] = 255

        flat[i] = new

    arr[:, :, ch_idx] = flat.reshape(h, w)

    Image.fromarray(arr).save(output_img)

    mask_img = np.zeros_like(arr)
    mask_img[:, :, ch_idx] = changed_mask.reshape(h, w)
    Image.fromarray(mask_img).save(output_mask)

    print(f"Message embedded into {channel} channel at bit position {bit_position}.")
    print(f"Output image: {output_img}")
    print(f"Change mask: {output_mask}")


def extract_message(img_path, message_length, channel='R', bit_position=0):
    img = Image.open(img_path).convert('RGB')
    arr = np.array(img)

    ch_idx = 'RGB'.index(channel)
    flat = arr[:, :, ch_idx].flatten()

    bits = ''.join(str((flat[i] >> bit_position) & 1) for i in range(message_length * 8))
    return bits_to_text(bits)


# Example:
hide_message_with_mask(
    'assets_main/bluesky.jpg',
    "there is no way a bee should be able to fly."
    "Its wings are too small to get its fat "
    "little body off the ground."
    "The bee, of course, flies anyway because bees "
    "don't care what humans think is impossible."
    "Yellow, black. Yellow, black. Yellow, black. Yellow, black."
    "Ooh, black and yellow!"
    "there is no way a bee should be able to fly."
    "Its wings are too small to get its fat "
    "little body off the ground."
    "The bee, of course, flies anyway because bees "
    "don't care what humans think is impossible."
    "Yellow, black. Yellow, black. Yellow, black. Yellow, black."
    "Ooh, black and yellow!"
    ,
    channel='B',
    bit_position=7,
    output_img='assets_main/bluesky_hidden_visible_B.png',
    output_mask='assets_main/bluesky_mask_visible.png'
)

msg = extract_message('assets_main/bluesky_hidden_visible_B.png', message_length=65, channel='B', bit_position=7)
print(msg)
