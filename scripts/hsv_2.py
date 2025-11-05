from PIL import Image, ImageDraw, ImageFont
import numpy as np
import colorsys


def text_to_bits(text):
    return ''.join(f'{ord(c):08b}' for c in text)


def bits_to_text(bits):
    chars = [bits[i:i + 8] for i in range(0, len(bits), 8)]
    return ''.join(chr(int(b, 2)) for b in chars)


def rgb_to_hsv_arr(img):
    arr = np.array(img) / 255.0
    h, w, _ = arr.shape
    hsv = np.zeros_like(arr)
    for y in range(h):
        for x in range(w):
            r, g, b = arr[y, x]
            hsv[y, x] = colorsys.rgb_to_hsv(r, g, b)
    return hsv


def hsv_to_rgb_arr(hsv):
    h, w, _ = hsv.shape
    rgb = np.zeros_like(hsv)
    for y in range(h):
        for x in range(w):
            r, g, b = colorsys.hsv_to_rgb(*hsv[y, x])
            rgb[y, x] = [r, g, b]
    return (rgb * 255).astype(np.uint8)


def forms_visualization(arr, mask_arr, stride=6, glyph="0"):
    h, w, _ = arr.shape
    canvas = Image.new("RGB", (w, h), (0, 0, 0))
    draw = ImageDraw.Draw(canvas)
    try:
        font = ImageFont.load_default()
    except:
        font = None
    for y in range(0, h, stride):
        for x in range(0, w, stride):
            changed = mask_arr[y, x] != 0
            if not changed.any():
                continue
            color = tuple(int(changed[i]) * 255 for i in range(3))
            draw.text((x, y), glyph, fill=color, font=font)
    return canvas


def hide_message_hsv(img_path, message, channels='SV', output_img='hsv_hidden.png',
                     output_mask='hsv_mask.png', output_forms='hsv_forms.png'):
    img = Image.open(img_path).convert('RGB')
    hsv = rgb_to_hsv_arr(img)
    h, w, _ = hsv.shape
    channel_map = {'H': 0, 'S': 1, 'V': 2}

    bitstring = text_to_bits(message)
    n_channels = len(channels)
    max_bits = h * w * n_channels
    if len(bitstring) > max_bits:
        raise ValueError(f"Message too long. Max bits: {max_bits}, required: {len(bitstring)}")

    flats = {ch: (hsv[:, :, channel_map[ch]] * 255).astype(np.uint8).flatten() for ch in channels}
    mask_arr = np.zeros_like(hsv)

    bit_idx = 0
    for i in range(h * w):
        for ch in channels:
            if bit_idx >= len(bitstring):
                break
            orig = flats[ch][i]
            new = (orig & 0xFE) | int(bitstring[bit_idx])
            flats[ch][i] = new
            if orig != new:
                mask_arr[:, :, channel_map[ch]].flat[i] = 255
            bit_idx += 1
        if bit_idx >= len(bitstring):
            break

    for ch in channels:
        hsv[:, :, channel_map[ch]] = flats[ch].reshape(h, w) / 255.0

    rgb_mod = hsv_to_rgb_arr(hsv)
    Image.fromarray(rgb_mod).save(output_img)

    mask_rgb = np.zeros_like(rgb_mod)
    for ch in channels:
        mask_rgb[:, :, channel_map[ch]] = mask_arr[:, :, channel_map[ch]]
    Image.fromarray(mask_rgb).save(output_mask)

    forms_img = forms_visualization(rgb_mod, mask_arr)
    forms_img.save(output_forms)

    print(f"Message hidden in HSV channels {channels}")
    print(f"Modified image: {output_img}")
    print(f"Mask: {output_mask}")
    print(f"Forms: {output_forms}")


def extract_message_hsv(img_path, message_length, channels='SV'):
    img = Image.open(img_path).convert('RGB')
    hsv = rgb_to_hsv_arr(img)
    h, w, _ = hsv.shape
    channel_map = {'H': 0, 'S': 1, 'V': 2}
    bits_needed = message_length * 8
    bitstring = ''

    flats = {ch: (hsv[:, :, channel_map[ch]] * 255).astype(np.uint8).flatten() for ch in channels}
    i = 0
    while len(bitstring) < bits_needed:
        for ch in channels:
            if len(bitstring) >= bits_needed:
                break
            bitstring += str(flats[ch][i] & 1)
        i += 1
    return bits_to_text(bitstring)

hide_message_hsv('assets_hsv_2/coffee.png', 'Hello HSV!', channels='SV',
                 output_img='assets_hsv_2/coffee_hsv_hidden.png',
                 output_mask='assets_hsv_2/coffee_hsv_mask.png',
                 output_forms='assets_hsv_2/coffee_hsv_forms.png')
msg = extract_message_hsv('assets_hsv_2/coffee_hsv_hidden.png', message_length=10, channels='SV')
print(msg)
