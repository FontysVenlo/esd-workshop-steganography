from PIL import Image
import numpy as np
import colorsys


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


def modify_hsv_channel(img_path, channel='S', delta=1, output_img='hsv_modified.png', output_mask='hsv_mask.png'):
    img = Image.open(img_path).convert('RGB')
    hsv = rgb_to_hsv_arr(img)

    channel_idx = {'H': 0, 'S': 1, 'V': 2}[channel]

    mask = np.zeros(hsv.shape, dtype=np.uint8)

    delta_scaled = delta / 255.0

    hsv_mod = hsv.copy()
    hsv_mod[:, :, channel_idx] = np.clip(hsv[:, :, channel_idx] + delta_scaled, 0, 1)

    mask[:, :, channel_idx] = 255 * (hsv_mod[:, :, channel_idx] != hsv[:, :, channel_idx])

    rgb_mod = hsv_to_rgb_arr(hsv_mod)
    Image.fromarray(rgb_mod).save(output_img)

    mask_rgb = np.zeros_like(rgb_mod)
    mask_rgb[:, :, channel_idx] = mask[:, :, channel_idx]
    Image.fromarray(mask_rgb).save(output_mask)

    print(f"Modified {channel} by {delta} levels, saved to {output_img} and mask {output_mask}")


modify_hsv_channel('assets_hsv/coffee.png', channel='S', delta=2, output_img='assets_hsv/coffee_S_mod.png',
                   output_mask='assets_hsv/coffee_S_mask.png')
modify_hsv_channel('assets_hsv/coffee.png', channel='V', delta=1, output_img='assets_hsv/coffee_V_mod.png',
                   output_mask='assets_hsv/coffee_V_mask.png')
