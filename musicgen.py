from transformers import MusicgenForConditionalGeneration

model = MusicgenForConditionalGeneration.from_pretrained("facebook/musicgen-small")

import torch

device = "cuda:0" if torch.cuda.is_available() else "cpu"
model.to(device);

new_tokens_count = 3200

from transformers import AutoProcessor

processor = AutoProcessor.from_pretrained("facebook/musicgen-small")

inputs = processor(
    text=["calm orchestral music"],
    padding=True,
    return_tensors="pt",
)

import scipy
for i in range(new_tokens_count//1536 + 1):
    audio_values = model.generate(**inputs.to(device), do_sample=True, guidance_scale=3, max_new_tokens=1536)

    sampling_rate = model.config.audio_encoder.sampling_rate
    print("sampling rate:",sampling_rate)

    audio_length_in_s = new_tokens_count / model.config.audio_encoder.frame_rate
    print("length approximation:",audio_length_in_s)


    scipy.io.wavfile.write("musicgen_out"+str(i)+".wav", rate=sampling_rate, data=audio_values[0, 0].cpu().numpy())
