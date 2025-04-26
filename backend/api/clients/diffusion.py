import torch
from diffusers import (
    ControlNetModel,
    StableDiffusionControlNetPipeline,
    UniPCMultistepScheduler,
)
from PIL import Image

from api.config import Settings


class DiffusionClient:
    def __init__(self, settings: Settings):
        self.pipe = self._load_pipeline(settings)

    def _load_pipeline(self, settings):
        """Stable Diffusionのパイプラインをロード"""
        controlnet = ControlNetModel.from_pretrained(
            settings.CONTROLNET_MODEL, torch_dtype=torch.bfloat16
        ).to(settings.DEVICE)

        pipe = StableDiffusionControlNetPipeline.from_pretrained(
            settings.SD_BASE_MODEL,
            controlnet=controlnet,
            safety_checker=None,
            torch_dtype=torch.bfloat16,
        ).to(settings.DEVICE)

        pipe.scheduler = UniPCMultistepScheduler.from_config(pipe.scheduler.config)
        return pipe

    def generate_image(
        self,
        prompt: str,
        control_images: list[Image.Image] | Image.Image,
        width: int,
        height: int,
        controlnet_conditioning_scale: list[float] | float,
        control_guidance_end: list[float] | float,
        num_inference_steps: int,
        guidance_scale: float,
        seed: int,
    ) -> Image.Image:
        """パラメータに基づいて画像を1枚生成"""
        # Generate images
        image: Image.Image = self.pipe(
            prompt=prompt,
            image=control_images,
            width=width,
            height=height,
            controlnet_conditioning_scale=controlnet_conditioning_scale,
            control_guidance_end=control_guidance_end,
            num_inference_steps=num_inference_steps,
            guidance_scale=guidance_scale,
            generator=torch.Generator(device=self.pipe.device).manual_seed(seed),
        ).images[0]  # type: ignore

        return image
