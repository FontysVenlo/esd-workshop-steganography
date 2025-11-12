import os
import sys
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


def text_to_bits(text):
    return ''.join(f"{ord(c):08b}" for c in text)


def bits_to_text(bits):
    chars = []
    for i in range(0, len(bits), 8):
        byte = bits[i:i + 8]
        if byte == '00000000':
            break
        chars.append(chr(int(byte, 2)))
    return ''.join(chars)


def embed_rgb(img_path, message, channel, bit, output_img, output_mask):
    img = Image.open(img_path).convert('RGB')
    arr = np.array(img)
    ch_idx = 'RGB'.index(channel.upper())
    flat = arr[:, :, ch_idx].flatten()

    max_chars = len(flat) // 8
    if len(message) > max_chars:
        raise ValueError(f"Message too long! Max characters for this image: {max_chars}")

    bits = text_to_bits(message) + '00000000'

    mask_arr = np.zeros_like(flat, dtype=np.uint8)
    bit_mask = 1 << bit
    inv_mask = (~bit_mask) & 0xFF

    for i, b in enumerate(bits):
        new = (flat[i] & inv_mask) | ((int(b) << bit) & 0xFF)
        if new != flat[i]:
            mask_arr[i] = 255
        flat[i] = new

    h, w, _ = arr.shape
    arr[:, :, ch_idx] = flat.reshape(h, w)
    Image.fromarray(arr).save(output_img)

    mask_img = np.zeros_like(arr)
    mask_img[:, :, ch_idx] = mask_arr.reshape(h, w)
    Image.fromarray(mask_img).save(output_mask)
    print(f"RGB embedding done. Max chars: {max_chars}. Saved {output_img} and {output_mask}")


def extract_rgb(img_path, channel, bit):
    img = Image.open(img_path).convert('RGB')
    arr = np.array(img)
    ch_idx = 'RGB'.index(channel.upper())
    flat = arr[:, :, ch_idx].flatten()

    bits = ''.join(str((flat[i] >> bit) & 1) for i in range(len(flat)))
    return bits_to_text(bits)


def embed_hsv(img_path, message, channel, bit, output_img, output_mask):
    img = Image.open(img_path).convert('RGB')
    hsv = rgb_to_hsv_arr(img)
    channel_idx = {'H': 0, 'S': 1, 'V': 2}[channel.upper()]
    data = (hsv[:, :, channel_idx] * 255).astype(np.uint8)
    h, w = data.shape
    flat = data.flatten()

    max_chars = len(flat) // 8
    if len(message) > max_chars:
        raise ValueError(f"Message too long! Max characters for this image: {max_chars}")

    bits = text_to_bits(message) + '00000000'
    bit_mask = 1 << bit
    inv_mask = (~bit_mask) & 0xFF
    for i, b in enumerate(bits):
        flat[i] = (flat[i] & inv_mask) | ((int(b) << bit) & 0xFF)
    data_mod = flat.reshape(h, w)
    mask = ((data ^ data_mod) != 0).astype(np.uint8) * 255
    hsv_mod = hsv.copy()
    hsv_mod[:, :, channel_idx] = data_mod / 255.0
    rgb_mod = hsv_to_rgb_arr(hsv_mod)
    Image.fromarray(rgb_mod).save(output_img)
    mask_rgb = np.zeros_like(rgb_mod)
    mask_rgb[:, :, channel_idx] = mask
    Image.fromarray(mask_rgb).save(output_mask)
    print(f"HSV embedding done. Saved {output_img} and {output_mask}")


def extract_hsv(img_path, channel, bit, max_chars=200):
    img = Image.open(img_path).convert('RGB')
    hsv = rgb_to_hsv_arr(img)
    channel_idx = {'H': 0, 'S': 1, 'V': 2}[channel.upper()]
    data = (hsv[:, :, channel_idx] * 255).astype(np.uint8)
    flat = data.flatten()
    bits = ''.join(str((flat[i] >> bit) & 1) for i in range(min(len(flat), max_chars * 8)))
    return bits_to_text(bits)


def input_strict(prompt, valid_options):
    val = input(prompt).strip().lower()
    if val not in [v.lower() for v in valid_options]:
        print("Invalid input. Exiting.")
        sys.exit()
    return val


def input_int_strict(prompt, min_val, max_val):
    try:
        val = int(input(prompt).strip())
    except:
        print("Invalid input. Exiting.")
        sys.exit()
    if val < min_val or val > max_val:
        print("Invalid input. Exiting.")
        sys.exit()
    return val


def main():
    os.makedirs("images", exist_ok=True)
    os.makedirs("output", exist_ok=True)

    print("\n=== Steganography Tool (RGB & HSV) ===\n")
    while True:
        print("\nWrite 'exit' to terminate. All progress will be lost.")

        mode = input_strict("Select mode (embed/extract/exit): ", ['embed', 'extract', 'exit'])
        if mode == 'exit':
            print("Exiting.")
            break

        domain = input_strict("Select domain (RGB/HSV): ", ['RGB', 'HSV'])

        folder = "images" if mode == "embed" else "output"
        images = [f for f in os.listdir(folder) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
        if not images:
            print(f"No images found in ./{folder}/")
            continue

        print(f"\nImages available in {folder}/:")
        for i, f in enumerate(images, 1):
            print(f"{i}. {f}")

        idx = input_int_strict("Select image number: ", 1, len(images)) - 1
        img_name = images[idx]
        img_path = os.path.join(folder, img_name)

        if domain.lower() == 'rgb':
            channel = input_strict("Select channel (R/G/B): ", ['R', 'G', 'B'])
        else:
            channel = input_strict("Select channel (H/S/V): ", ['H', 'S', 'V'])
        bit = input_int_strict("Select bit (0-7): ", 0, 7)

        base, ext = os.path.splitext(img_name)
        out_img = os.path.join("output", f"{base}_HIDDEN{ext}")
        out_mask = os.path.join("output", f"{base}_MASK{ext}")

        if mode == 'embed':
            message = input("Enter secret message: ").strip()
            if domain.lower() == 'rgb':
                embed_rgb(img_path, message, channel, bit, out_img, out_mask)
            else:
                embed_hsv(img_path, message, channel, bit, out_img, out_mask)
        else:
            print("\nExtracting...")
            if domain.lower() == 'rgb':
                msg = extract_rgb(img_path, channel, bit)
            else:
                msg = extract_hsv(img_path, channel, bit)
            print("\n=== Extracted Message ===")
            print(msg if msg else "[No message found]")
            print("=========================\n")


if __name__ == "__main__":
    main()
