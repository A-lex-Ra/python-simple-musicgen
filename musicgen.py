from transformers import MusicgenForConditionalGeneration, AutoProcessor
import torch
import scipy

TOKENS_PER_STEP = 250

class PromptToMusicGenerator:
    def __init__(self, model_str="facebook/musicgen-small", new_tokens_per_step = TOKENS_PER_STEP):
        self.model = MusicgenForConditionalGeneration.from_pretrained(model_str)
        self.processor = AutoProcessor.from_pretrained(model_str)
        self.tokens_per_step = new_tokens_per_step
        self.device = "cuda:0" if torch.cuda.is_available() else "cpu"
        self.model.to(self.device);
    
    def generate(self, prompt_str, duration_seconds):
        framerate = self.model.config.audio_encoder.frame_rate
        print("framerate:",framerate)
        all_tokens_count = framerate * duration_seconds
        
        sampling_rate = self.model.config.audio_encoder.sampling_rate
        print("sampling rate:",sampling_rate)

        inputs = self.processor(
            text=[prompt_str],
            padding=True,
            return_tensors="pt",
        )
        last_step_audio_values = self.model.generate(**inputs.to(self.device), do_sample=True, guidance_scale=3,
                                              max_new_tokens=self.tokens_per_step)
        print("First step generation: array of shape",last_step_audio_values.shape)
        scipy.io.wavfile.write("musicgen_out_initial.wav", rate=sampling_rate,
                               data=last_step_audio_values[0, 0].cpu().numpy())
        # audio_values = torch.Tensor()
        for i in range(all_tokens_count//self.tokens_per_step):
            inputs = self.processor(
                audio=last_step_audio_values[0,0],
                sampling_rate=sampling_rate,
                text=[prompt_str],
                padding=True,
                return_tensors="pt",
            )
            last_step_audio_values = self.model.generate(**inputs.to(self.device), do_sample=True, guidance_scale=3, max_new_tokens=self.tokens_per_step)
            # audio_values = torch.cat(
            #     (audio_values, last_step_audio_values), dim=2
            # )

            sampling_rate = self.model.config.audio_encoder.sampling_rate
            print("Next iteration. sampling rate:",sampling_rate)

            scipy.io.wavfile.write("musicgen_out"+str(i)+".wav", rate=sampling_rate, data=last_step_audio_values[0, 0].cpu().numpy())
            
g = PromptToMusicGenerator()
g.generate("waltz mid-century piano music", 120)
