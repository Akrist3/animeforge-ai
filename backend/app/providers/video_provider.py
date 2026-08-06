import uuid


def generate_video(prompt: str) -> str:
    """
    Dummy AI video generator.
    Later this will call Runway, Kling, Pika, etc.
    """

    return f"https://animeforge.ai/generated/{uuid.uuid4()}.mp4"