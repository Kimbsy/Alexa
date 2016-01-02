# # Play the sound file
# aplay rec.wav

# Temporarily send the file to Minty to play it
scp rec.wav kimbsy@minty:/tmp/rec.wav
ssh minty 'aplay /tmp/rec.wav'