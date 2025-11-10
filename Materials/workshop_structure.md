## Workshop structure

**0–15 min: Icebreaker**

Start with a hidden message challenge:
- Show them two identical-looking images
“One of these contains a secret. Can you tell which?”
- Let them guess or inspect (maybe even try opening it in a text editor or hex viewer or give it to an ai and trick it into finding the message).
- Reveal the hidden message using your code (or a quick prebuilt script).

**15–40 min: Mini-lecture**
- Briefly explain:
    - What steganography is
    - The difference from cryptography
    - Real-world uses (digital watermarking, covert comms, DRM)
- Show 2–3 visual examples (image, text, audio stego)
- Ask: “Where else could we hide data?”; Let the room brainstorm.

**40–50 min: Demo**
- Pick one of the coded algorithms, the one embedding into the RGB - B (blue) channel
- Explain the code 
- Choose a photo and a message, then embed the message in the image with the code
- Take the de-embedder and reveal the secret message it found
- Show the mask, where it is shown which part of the data is being modified
- Show the images side by side 


**50–80 min: Hands-On Activity / Challenge**
- Split into groups 
- Give them the script and make them embed a message
- Send it to another team and make them de-embed it 
- Try image in image as well and make the other person find the images

**80–90 min: Wrap-Up**

Ask:
- Where could this be useful or dangerous?
- When is hiding something _smarter_ than encrypting it? 
- Do you think this is ethical?
- 
“Steganography isn’t just about hiding; it’s about control over visibility.”
