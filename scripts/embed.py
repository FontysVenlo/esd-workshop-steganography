from PIL import Image, ImageDraw, ImageFont
import numpy as np


def text_to_bits(text):
    return ''.join(f'{ord(c):08b}' for c in text)


def bits_to_text(bits):
    chars = [bits[i:i + 8] for i in range(0, len(bits), 8)]
    return ''.join(chr(int(b, 2)) for b in chars)


def forms_visualization(arr, mask_arr, stride=6, glyph="0"):
    h, w, _ = arr.shape
    canvas = Image.new("RGB", (w, h), (0, 0, 0))
    draw = ImageDraw.Draw(canvas)
    font = None
    try:
        font = ImageFont.load_default()
    except:
        pass
    for y in range(0, h, stride):
        for x in range(0, w, stride):
            changed = mask_arr[y, x] != 0
            if not changed.any():
                continue
            color = tuple(int(changed[i]) * 255 for i in range(3))
            draw.text((x, y), glyph, fill=color, font=font)
    return canvas


def hide_message_with_mask_and_forms(img_path, message, channels='BGR',
                                     output_img='hidden.png',
                                     output_mask='mask.png',
                                     output_forms='forms.png'):
    img = Image.open(img_path).convert('RGB')
    arr = np.array(img)
    h, w, _ = arr.shape

    bitstring = text_to_bits(message)
    n_channels = len(channels)
    max_bits = h * w * n_channels
    if len(bitstring) > max_bits:
        raise ValueError(f"Message too long. Max bits: {max_bits}, required: {len(bitstring)}")

    flats = {ch: arr[:, :, 'RGB'.index(ch)].flatten() for ch in channels}
    mask_arr = np.zeros_like(arr)

    bit_idx = 0
    for i in range(h * w):
        for ch in channels:
            if bit_idx >= len(bitstring):
                break
            ch_idx = 'RGB'.index(ch)
            orig_bit = flats[ch][i] & 1
            new_bit = int(bitstring[bit_idx])
            if orig_bit != new_bit:
                flats[ch][i] = (flats[ch][i] & 0xFE) | new_bit
                mask_arr[:, :, ch_idx].flat[i] = 255
            bit_idx += 1
        if bit_idx >= len(bitstring):
            break

    for ch in channels:
        ch_idx = 'RGB'.index(ch)
        arr[:, :, ch_idx] = flats[ch].reshape(h, w)

    Image.fromarray(arr).save(output_img)
    Image.fromarray(mask_arr).save(output_mask)

    forms_img = forms_visualization(arr, mask_arr, stride=6, glyph="0")
    forms_img.save(output_forms)

    print(f"Message hidden across channels {channels}")
    print(f"Modified image saved to: {output_img}")
    print(f"Mask showing changed pixels saved to: {output_mask}")
    print(f"Forms image showing changed pixels saved to: {output_forms}")


def extract_message_multi_channel(img_path, message_length, channels='BGR'):
    img = Image.open(img_path).convert('RGB')
    arr = np.array(img)
    bits_needed = message_length * 8
    bitstring = ''

    flats = {ch: arr[:, :, 'RGB'.index(ch)].flatten() for ch in channels}
    i = 0
    while len(bitstring) < bits_needed:
        for ch in channels:
            bitstring += str(flats[ch][i] & 1)
            if len(bitstring) >= bits_needed:
                break
        i += 1
    return bits_to_text(bitstring)


hide_message_with_mask_and_forms(
    'assets/food.jpg',
    'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA',
    channels='BGR',
    output_img='assets/food_hidden.png',
    output_mask='assets/food_mask.png',
    output_forms='assets/food_forms.png'
)
extracted = extract_message_multi_channel('assets/food_hidden.png', message_length=100, channels='BGR')
print(extracted)
