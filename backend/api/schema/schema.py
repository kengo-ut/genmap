from pydantic import BaseModel, Field


class ImageGenerationParams(BaseModel):
    prompt: str = Field(..., description="Text prompt for the image")
    width: int = Field(..., description="Width of the image")
    height: int = Field(..., description="Height of the image")
    control_image_filename_1: str | None = Field(
        None, description="Filename of the first control image"
    )
    control_image_filename_2: str | None = Field(
        None, description="Filename of the second control image"
    )
    controlnet_conditioning_scale_1: float | None = Field(
        None, description="Conditioning scale for the first control image"
    )
    controlnet_conditioning_scale_2: float | None = Field(
        None, description="Conditioning scale for the second control image"
    )
    control_guidance_end_1: float | None = Field(
        None, description="Guidance end for the first control image"
    )
    control_guidance_end_2: float | None = Field(
        None, description="Guidance end for the second control image"
    )
    num_inference_steps: int = Field(..., description="Number of inference steps")
    guidance_scale: float = Field(..., description="Guidance scale")
    seed: int = Field(..., description="Random seed for generation")


class SimpleMetadata(BaseModel):
    image_filename: str = Field(..., description="Filename of the image")
    prompt: str = Field(..., description="Text prompt for the image")


class FullMetadata(ImageGenerationParams):
    image_filename: str = Field(..., description="Filename of the generated image")


class ImageFilenames(BaseModel):
    image_filenames: list[str] = Field(
        ..., description="List of filenames of the images to be deleted"
    )


class DeleteResponse(BaseModel):
    status: str = Field(..., description="Status of the deletion")
    deleted_filenames: list[str] = Field(
        ..., description="List of filenames that were successfully deleted"
    )
    failed_filenames: list[str] = Field(
        ..., description="List of filenames that failed to delete"
    )
