import uuid


def generate_voice(prompt: str) -> str:
    """
    Dummy AI voice generator.
    Later this will call ElevenLabs, OpenAI TTS, Sarvam AI, etc.
    """

    return f"https://animeforge.ai/generated/{uuid.uuid4()}.mp3"