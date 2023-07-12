import comfy.samplers
import nodes
import math

class SDXLKSamplerAdvancedIterate:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "model_1": ("MODEL",),
                "model_2": ("MODEL",),
                "noise_seed_1": ("INT", {"default": 0, "min": 0, "max": 0xffffffffffffffff}),
                "noise_seed_2": ("INT", {"default": 0, "min": 0, "max": 0xffffffffffffffff}),
                "steps": ("INT", {"default": 20, "min": 1, "max": 10000}),
                "cfg_1": ("FLOAT", {"default": 8.0, "min": 0.0, "max": 100.0}),
                "cfg_2": ("FLOAT", {"default": 8.0, "min": 0.0, "max": 100.0}),
                "sampler_name_1": (comfy.samplers.KSampler.SAMPLERS, ),
                "sampler_name_2": (comfy.samplers.KSampler.SAMPLERS, ),
                "scheduler_1": (comfy.samplers.KSampler.SCHEDULERS, ),
                "scheduler_2": (comfy.samplers.KSampler.SCHEDULERS, ),
                "positive_1": ("CONDITIONING", ),
                "negative_1": ("CONDITIONING", ),
                "positive_2": ("CONDITIONING", ),
                "negative_2": ("CONDITIONING", ),
                "latent_image": ("LATENT", ),
                "percent_base": ("FLOAT", {"default": 1.0, "min": 0.0, "max": 1.0, "step": 0.1}),
                "denoise": ("FLOAT", {"default": 1.0, "min": 0.01, "max": 1.0, "step": 0.05}),
                "iterations": ("INT", {"default": 3, "min": 1, "max": 100, "step": 1}),
                "base_only": ("INT", {"default": 0, "min": 0, "max": 1, "step": 1}),
            },
        }

    RETURN_TYPES = ("LATENT",)
    RETURN_NAMES = ("latent",)
    FUNCTION = "sample"

    CATEGORY = "SDXL"

    def sample(self, model_1, model_2, noise_seed_1, noise_seed_2, steps, cfg_1, cfg_2, sampler_name_1, sampler_name_2, scheduler_1, scheduler_2, positive_1, negative_1, positive_2, negative_2, latent_image, percent_base, denoise, iterations, base_only):
        baseEndStep = math.floor(steps * percent_base)

        latent = nodes.common_ksampler(model_1, noise_seed_1, steps, cfg_1, sampler_name_1, scheduler_1, positive_1, negative_1, latent_image, denoise=denoise, disable_noise=False, start_step=0, last_step=baseEndStep, force_full_denoise=False)
        for i in range(iterations):
            if i != 0:
                latent = nodes.common_ksampler(model_1, noise_seed_1, steps, cfg_1, sampler_name_1, scheduler_1, positive_1, negative_1, latent[0], denoise=denoise, disable_noise=False, start_step=0, last_step=baseEndStep, force_full_denoise=False)
            
            if base_only == 0:
                latent = nodes.common_ksampler(model_2, noise_seed_2, steps, cfg_2, sampler_name_2, scheduler_2, positive_2, negative_2, latent[0], denoise=1.0, disable_noise=True, start_step=baseEndStep, last_step=steps, force_full_denoise=True)

            print(f"COMPLETED: Iteration {i+1}/{iterations}")

        return latent

NODE_CLASS_MAPPINGS = {
    "SDXLKSamplerAdvancedIterate": SDXLKSamplerAdvancedIterate
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "SDXLKSamplerAdvancedIterate": "SDXLKSamplerAdvancedIterate"
}