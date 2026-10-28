from __future__ import annotations

import shutil
import subprocess
import tempfile
from pathlib import Path

from .config import VideoJob


def _escape_drawtext(text: str) -> str:
    return text.replace("\\", r"\\").replace("'", r"\'").replace(":", r"\:").replace("%", r"\%")


def render(job: VideoJob, output: Path) -> Path:
    if shutil.which("ffmpeg") is None:
        raise RuntimeError("FFmpeg bulunamadı. FFmpeg 6 veya daha yeni bir sürüm kurun.")

    output = output.resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="shorts-") as temp_dir:
        temp = Path(temp_dir)
        clips: list[Path] = []
        for index, scene in enumerate(job.scenes):
            clip = temp / f"scene-{index:03d}.mp4"
            text = _escape_drawtext(scene.text)
            vf = (
                "drawtext="
                f"text='{text}':fontcolor={job.text_color}:fontsize=72:"
                "x=(w-text_w)/2:y=(h-text_h)/2:"
                "box=1:boxcolor=black@0.45:boxborderw=36"
            )
            command = [
                "ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
                "-f", "lavfi", "-i", f"color=c={job.background_color}:s=1080x1920:r=30",
                "-f", "lavfi", "-i", "anullsrc=r=48000:cl=stereo",
                "-t", str(scene.duration), "-vf", vf,
                "-c:v", "libx264", "-pix_fmt", "yuv420p", "-c:a", "aac",
                "-shortest", str(clip),
            ]
            subprocess.run(command, check=True)
            clips.append(clip)

        concat_file = temp / "clips.txt"
        concat_file.write_text("".join(f"file '{clip.as_posix()}'\n" for clip in clips), encoding="utf-8")
        subprocess.run(
            [
                "ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
                "-f", "concat", "-safe", "0", "-i", str(concat_file),
                "-c", "copy", "-movflags", "+faststart", str(output),
            ],
            check=True,
        )
    return output
