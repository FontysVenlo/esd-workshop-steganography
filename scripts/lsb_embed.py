import numpy as np
from PIL import Image
import os


class IntensityGuidedLSB:
    def __init__(self, dark_threshold=64, bright_threshold=192):
        self.dark_threshold = dark_threshold
        self.bright_threshold = bright_threshold

    def _get_bits_per_pixel(self, intensity):
        base_intensity = intensity & 0xFC  # Clear 2 LSBs
        if base_intensity < self.dark_threshold or base_intensity >= self.bright_threshold:
            return 1
        else:
            return 2

    def _text_to_bits(self, text):
        bits = ''.join(format(ord(char), '08b') for char in text)
        return bits

    def _bits_to_text(self, bits):
        chars = []
        for i in range(0, len(bits), 8):
            byte = bits[i:i + 8]
            if len(byte) == 8:
                chars.append(chr(int(byte, 2)))
        return ''.join(chars)

    def encode(self, image_path, message, output_path='encoded_image.png'):
        if not output_path.lower().endswith('.png'):
            print("⚠️  WARNING: Changing output to PNG (JPG destroys LSB data!)")
            output_path = os.path.splitext(output_path)[0] + '.png'

        # Load image
        img = Image.open(image_path)
        img_array = np.array(img)

        original_shape = img_array.shape
        flat_img = img_array.flatten().copy()

        capacity = 0
        for pixel_val in flat_img:
            capacity += self._get_bits_per_pixel(pixel_val)

        # Prepare message with length header
        message_bits = self._text_to_bits(message)
        message_length = len(message_bits)
        length_header = format(message_length, '032b')  # 32-bit length header
        full_message = length_header + message_bits

        # Check if message fits
        if len(full_message) > capacity:
            raise ValueError(f"Message too large! Need {len(full_message)} bits, "
                             f"but capacity is only {capacity} bits")

        bit_index = 0
        bits_embedded = {'1bit': 0, '2bit': 0}

        # Embed message
        for i in range(len(flat_img)):
            if bit_index >= len(full_message):
                break

            pixel_val = flat_img[i]
            bits_to_embed = self._get_bits_per_pixel(pixel_val)

            if bits_to_embed == 1:
                # Embed 1 bit in LSB
                if bit_index < len(full_message):
                    flat_img[i] = (pixel_val & 0xFE) | int(full_message[bit_index])
                    bit_index += 1
                    bits_embedded['1bit'] += 1
            else:  # bits_to_embed == 2
                # Embed 2 bits in 2 LSBs
                bits_available = min(2, len(full_message) - bit_index)
                if bits_available == 2:
                    new_bits = full_message[bit_index:bit_index + 2]
                    # Clear 2 LSBs and set new bits (MSB first, then LSB)
                    flat_img[i] = (pixel_val & 0xFC) | int(new_bits, 2)
                    bit_index += 2
                    bits_embedded['2bit'] += 2
                elif bits_available == 1:
                    # Only 1 bit left, embed in bit 1 (second LSB)
                    flat_img[i] = (pixel_val & 0xFD) | (int(full_message[bit_index]) << 1)
                    bit_index += 1
                    bits_embedded['2bit'] += 1

        # save as PNG
        stego_img = flat_img.reshape(original_shape)
        Image.fromarray(stego_img.astype(np.uint8)).save(output_path, 'PNG')

        return {
            'message_length': message_length,
            'total_capacity': capacity,
            'utilization': f"{(len(full_message) / capacity) * 100:.2f}%",
            '1bit_pixels': bits_embedded['1bit'],
            '2bit_pixels': bits_embedded['2bit'] // 2,
            'output_path': output_path
        }

    def decode(self, image_path):
        # Load image
        img = Image.open(image_path)
        img_array = np.array(img)
        flat_img = img_array.flatten()

        # Extract length header (first 32 bits)
        extracted_bits = []
        pixel_index = 0

        while len(extracted_bits) < 32 and pixel_index < len(flat_img):
            pixel_val = flat_img[pixel_index]
            bits_per_pixel = self._get_bits_per_pixel(pixel_val)

            if bits_per_pixel == 1:
                extracted_bits.append(str(pixel_val & 1))
            else:  # 2 bits
                # Extract bit 1 (second LSB) first, then bit 0 (LSB)
                extracted_bits.append(str((pixel_val >> 1) & 1))
                if len(extracted_bits) < 32:
                    extracted_bits.append(str(pixel_val & 1))

            pixel_index += 1

        # decode message length
        if len(extracted_bits) < 32:
            return ""

        message_length = int(''.join(extracted_bits[:32]), 2)

        if message_length == 0 or message_length > 1000000:  # Sanity check
            return ""

        # Extract message bits
        extracted_bits = []
        while len(extracted_bits) < message_length and pixel_index < len(flat_img):
            pixel_val = flat_img[pixel_index]
            bits_per_pixel = self._get_bits_per_pixel(pixel_val)

            if bits_per_pixel == 1:
                extracted_bits.append(str(pixel_val & 1))
            else:  # 2 bits
                # Extract bit 1 first, then bit 0
                extracted_bits.append(str((pixel_val >> 1) & 1))
                if len(extracted_bits) < message_length:
                    extracted_bits.append(str(pixel_val & 1))

            pixel_index += 1

        # Convert bits to text
        message_bits = ''.join(extracted_bits[:message_length])
        return self._bits_to_text(message_bits)



if __name__ == "__main__":
    ig_lsb = IntensityGuidedLSB(dark_threshold=64, bright_threshold=192)


    with open('secret_message.txt', 'r', encoding='utf-8') as f:
        secret_message = f.read().strip()

    print("Encoding message...")
    stats = ig_lsb.encode('test_cover.png', secret_message, 'stego_image.png')

    print(f"  Message length: {stats['message_length']} bits")
    print(f"  Total capacity: {stats['total_capacity']} bits")
    print(f"  Pixels using 1-bit: {stats['1bit_pixels']}")
    print(f"  Pixels using 2-bit: {stats['2bit_pixels']}")

    decoded_message = ig_lsb.decode('stego_image.png')
    print(f"\nDecoded message: '{decoded_message}'")

    if decoded_message == secret_message:
        print("\n Message decoded correctly!")
    else:
        print("\ERROR: Decoded message doesn't match!")
        print(f"Expected: '{secret_message}'")
        print(f"Got: '{decoded_message}'")