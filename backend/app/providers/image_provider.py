import uuid


def generate_image(prompt: str):
    """
    Temporary image generator.

    Later this will call:
    - OpenAI Images
    - Stable Diffusion
    - Flux
    - ComfyUI
    """

    fake_url = (
        "https://animeforge.ai/generated/"
        f"{uuid.uuid4()}.png"
    )

    return fake_url