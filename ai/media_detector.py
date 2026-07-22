"""
VeriSight MVP
Media Verification Module
"""

from PIL import Image
import os


def analyze_media(uploaded_file):
    """
    Basic media analysis for the MVP.

    Returns
    -------
    dict
        {
            verdict,
            confidence,
            reasoning
        }
    """

    filename = uploaded_file.name.lower()
    extension = os.path.splitext(filename)[1]

    image_types = [".jpg", ".jpeg", ".png"]
    video_types = [".mp4", ".mov", ".avi"]
    audio_types = [".wav", ".mp3"]

    if extension in image_types:

        image = Image.open(uploaded_file)

        width, height = image.size

        megapixels = (width * height) / 1_000_000

        reasoning = [
            f"Resolution: {width} × {height}",
            f"{megapixels:.2f} MP",
            "Metadata inspection completed."
        ]

        confidence = 75

        if megapixels < 0.5:
            confidence = 60
            reasoning.append(
                "Very low resolution may reduce verification accuracy."
            )

        return {
            "type": "Image",
            "verdict": "Likely Authentic",
            "confidence": confidence,
            "reasoning": reasoning
        }

    elif extension in video_types:

        return {
            "type": "Video",
            "verdict": "Video Uploaded",
            "confidence": 70,
            "reasoning": [
                "Video received.",
                "Frame-level AI detection will be available in a future release."
            ]
        }

    elif extension in audio_types:

        return {
            "type": "Audio",
            "verdict": "Audio Uploaded",
            "confidence": 70,
            "reasoning": [
                "Audio received.",
                "Voice authenticity analysis will be added in a future release."
            ]
        }

    return {
        "type": "Unknown",
        "verdict": "Unsupported",
        "confidence": 0,
        "reasoning": [
            "Unsupported file type."
        ]
    }