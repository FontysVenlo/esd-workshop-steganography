from PIL import Image, ImageDraw, ImageFont
import numpy as np


def image_to_bits(img):
    arr = np.array(img)
    return ''.join(f'{b:08b}' for b in arr.flatten())


def bits_to_image(bits, shape):
    arr = np.array([int(bits[i:i + 8], 2) for i in range(0, len(bits), 8)], dtype=np.uint8)
    return Image.fromarray(arr.reshape(shape))


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


def hide_image_with_mask_and_forms(carrier_path, secret_path, channels='BGR',
                                   output_img='embedded.png',
                                   output_mask='mask.png',
                                   output_forms='forms.png'):
    carrier = Image.open(carrier_path).convert('RGB')
    secret = Image.open(secret_path).convert('RGB')

    carrier_arr = np.array(carrier)
    h_c, w_c, _ = carrier_arr.shape
    max_bits = h_c * w_c * len(channels)

    secret_bits = image_to_bits(secret)
    if len(secret_bits) > max_bits:
        raise ValueError("Secret image too large for carrier with selected channels")

    flats = {ch: carrier_arr[:, :, 'RGB'.index(ch)].flatten() for ch in channels}
    mask_arr = np.zeros_like(carrier_arr)

    bit_idx = 0
    for i in range(h_c * w_c):
        for ch in channels:
            if bit_idx >= len(secret_bits):
                break
            ch_idx = 'RGB'.index(ch)
            orig_bit = flats[ch][i] & 1
            new_bit = int(secret_bits[bit_idx])
            if orig_bit != new_bit:
                flats[ch][i] = (flats[ch][i] & 0xFE) | new_bit
                mask_arr[:, :, ch_idx].flat[i] = 255
            bit_idx += 1
        if bit_idx >= len(secret_bits):
            break

    for ch in channels:
        ch_idx = 'RGB'.index(ch)
        carrier_arr[:, :, ch_idx] = flats[ch].reshape(h_c, w_c)

    Image.fromarray(carrier_arr).save(output_img)
    Image.fromarray(mask_arr).save(output_mask)

    forms_img = forms_visualization(carrier_arr, mask_arr, stride=6, glyph="0")
    forms_img.save(output_forms)

    print(f"Secret image hidden across channels {channels}")
    print(f"Modified image saved to: {output_img}")
    print(f"Mask image saved to: {output_mask}")
    print(f"Forms image saved to: {output_forms}")

    return secret.size  # width, height needed for extraction


def extract_image_from_carrier(carrier_path, secret_size, channels='BGR'):
    carrier = Image.open(carrier_path).convert('RGB')
    carrier_arr = np.array(carrier)
    bits_needed = secret_size[0] * secret_size[1] * 3 * 8

    flats = {ch: carrier_arr[:, :, 'RGB'.index(ch)].flatten() for ch in channels}
    bitstring = ''

    i = 0
    while len(bitstring) < bits_needed:
        for ch in channels:
            if len(bitstring) >= bits_needed:
                break
            bitstring += str(flats[ch][i] & 1)
        i += 1

    return bits_to_image(bitstring, (secret_size[1], secret_size[0], 3))

size = hide_image_with_mask_and_forms(
    carrier_path='assets_img/food.jpg',
    secret_path='assets_img/coffee.png',
    channels='BGR',
    output_img='assets_img/embedded.png',
    output_mask='assets_img/mask.png',
    output_forms='assets_img/forms.png'
)
recovered = extract_image_from_carrier('assets_img/embedded.png', size, channels='BGR')
recovered.save('assets_img/recovered_secret.png')