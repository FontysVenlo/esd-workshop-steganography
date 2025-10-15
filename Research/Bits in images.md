We can change several different bits in an image, while it still looks the same after. 
Some of the things we could change are:
1. The RGB domain:
- modifying the least-significant bit of the R, G, B (choose a color channel)
- changing the lowest bit of each pixel changes the color in a way that is undetectable to the human eye
- we can change 1 or 2 bits to still remain safe per channel and in order of noticeability, it would go from blue, to green and, least recommended, to red 
- the human eye is least sensitive to blue 
2. HSV domain
- Hue, Saturation or Value (brightness) components 
- changing Saturation or Value by 1–2 levels out of 255 is often imperceptible, however Hue is riskier, small changes can shift color tone
3. YCbCr domain (luminance/chrominance) 
- used in JPEG and video encoding 
- should avoid modifying the Y (luminescence) much, because it controls the brightness
- Cb and Cr control color differences, safer for minor changes 
4. Frequency domain (transform-based)
- operate on frequency coefficients instead of raw pixels.
- DCT (Discrete Cosine Transform) used in JPEG steganography. Hide bits in mid-frequency DCT coefficients.
- DWT (Discrete Wavelet Transform) works similarly for wavelet-compressed images.