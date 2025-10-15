Slipping past anti-virus, data loss protection, intrusion protection systems and other security controls every day - how??

encryption - scrambles data
steganography - even someone who knows what they are doing, knows its there; basically invisible

During safe hacking, it is used in penetration testing to simulate how attackers might exfiltrate information or how to bypass security controlls or to slip by firewalls to install malware or command and control tools; can also be used in phishing campaigns to deliver payloads

- steghide - works for linux, mac and windows
- steghide does not use LSB - LSB is easily detectable

Test image
![[original.jpeg]]

steghide embed -cf original.jpeg  -ef nnadmin.txt
![[stego.jpeg]]

compare original.jpeg stego.jpeg diff.png
![[diff.jpeg]]
shows exact pixel differences between the two images (dark = identical, bright = changed)

convert original.jpeg stego.jpeg -compose difference -composite -evaluate multiply 10 diff2.png

![[diff2.jpeg]]
exaggerates those tiny hidden changes ×10 so they become visible (bright noise = where data was embedded)

--- 
extract command - steghide extract -sf img1.jpg 
stegcracker img1.jpg bt4_passwords.txt (stegcracker used to bypass steghide password)