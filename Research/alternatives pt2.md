## What is Steganography?

[Steganography](http://en.wikipedia.org/wiki/Steganography) is the science of hiding secret message inside another larger and harmless looking message. This is one notch above regular cryptography; which just obscures the original message. Steganography tries to conceal the fact that there is a message in the first place. Steganographic message often appears to be something else than the original (secret) message, like a picture, sound, larger text, etc.

Some terms related to Steganography:

- **plaintext:** The original secret message that needs to be communicated.
- **ciphertext:** Secret message is often first encrypted using traditional methods. Encrypted message is known as ciphertext.
- **covertext:** A larger and harmless looking data which is used as container for the plaintext/ciphertext. This can be a picture, sound, text, etc.
- **stegotext:** The data generated after embedding the plaintext/ciphertext into the covertext.

The normal procedure is to first encrypt the plaintext to generate the ciphertext, and then modify the covertext in some way to contain the ciphertext. The generated stegotext is sent over to the intended recepient. If a third party snoops the stegotext in between, then they will just see some harmless looking picture (or sound, etc). Once the recepient receives the stegotext, the ciphertext is extracted from it by reversing the logic that was used to embed it in the first place. The ciphertext is decrypted using the traditional cryptography to get back the original plaintext.

## What is Digital Watermarking?

[Digital Watermarking](http://en.wikipedia.org/wiki/Digital_watermarking) is the process of embedding a covert marker in a noise-tolerant signal such as image data. It is typically used to identify ownership of the copyright of such signal. The hidden information should but does not necessarily need to contain a relation to the carrier signal. Digital watermarks may be used to verify the authenticity or integrity of the carrier signal or to show the identity of its owners. It is prominently used for tracing copyright infringements and for banknote authentication. Like traditional watermarks, digital watermarks are only perceptible under certain conditions, i.e. after using some algorithm, and imperceptible anytime else. If a digital watermark distorts the carrier signal in a way that it becomes perceivable, it is of no use.

OpenStego provides robust digital watermarking capabilities such that the watermark strength is not easily reduced when the watermarked image is resized, cropped or some other minor modifications are done.