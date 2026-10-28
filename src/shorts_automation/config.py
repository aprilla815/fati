from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path

SLUG_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


class ConfigError(ValueError):
    """Raised when a video job is invalid."""


@dataclass(frozen=True)
class Scene:
    text: str
    duration: float


@dataclass(frozen=True)
class VideoJob:
    slug: str
    title: str
    background_color: str
    text_color: str
    scenes: tuple[Scene, ...]

    @property
    def duration(self) -> float:
        return sum(scene.duration for scene in self.scenes)


def load_job(path: str | Path) -> VideoJob:
    try:
        raw = json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ConfigError(f"Yapılandırma okunamadı: {exc}") from exc

    if not isinstance(raw, dict):
        raise ConfigError("Kök değer bir JSON nesnesi olmalıdır.")

    slug = raw.get("slug")
    title = raw.get("title")
    if not isinstance(slug, str) or not SLUG_PATTERN.fullmatch(slug):
        raise ConfigError("slug küçük harf, sayı ve tek tirelerle yazılmalıdır.")
    if not isinstance(title, str) or not title.strip():
        raise ConfigError("title boş olmayan bir metin olmalıdır.")

    raw_scenes = raw.get("scenes")
    if not isinstance(raw_scenes, list) or not raw_scenes:
        raise ConfigError("scenes en az bir sahne içermelidir.")

    scenes: list[Scene] = []
    for index, item in enumerate(raw_scenes, start=1):
        if not isinstance(item, dict):
            raise ConfigError(f"Sahne {index} bir nesne olmalıdır.")
        text = item.get("text")
        duration = item.get("duration")
        if not isinstance(text, str) or not text.strip():
            raise ConfigError(f"Sahne {index}: text boş olamaz.")
        if isinstance(duration, bool) or not isinstance(duration, (int, float)) or not 0.5 <= duration <= 15:
            raise ConfigError(f"Sahne {index}: duration 0.5 ile 15 saniye arasında olmalıdır.")
        scenes.append(Scene(text=text.strip(), duration=float(duration)))

    job = VideoJob(
        slug=slug,
        title=title.strip(),
        background_color=str(raw.get("background_color", "0x111827")),
        text_color=str(raw.get("text_color", "white")),
        scenes=tuple(scenes),
    )
    if job.duration > 60:
        raise ConfigError("Toplam video süresi 60 saniyeyi aşamaz.")
    return job
