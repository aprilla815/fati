import json

import pytest

from shorts_automation.config import ConfigError, load_job


def write_job(tmp_path, payload):
    path = tmp_path / "job.json"
    path.write_text(json.dumps(payload), encoding="utf-8")
    return path


def test_loads_valid_job(tmp_path):
    job = load_job(write_job(tmp_path, {
        "slug": "test-short",
        "title": "Test",
        "scenes": [{"text": "Merhaba", "duration": 1.5}],
    }))
    assert job.slug == "test-short"
    assert job.duration == 1.5


def test_rejects_more_than_sixty_seconds(tmp_path):
    path = write_job(tmp_path, {
        "slug": "too-long",
        "title": "Uzun",
        "scenes": [{"text": str(i), "duration": 15} for i in range(5)],
    })
    with pytest.raises(ConfigError, match="60"):
        load_job(path)


def test_rejects_invalid_slug(tmp_path):
    path = write_job(tmp_path, {
        "slug": "Yanlış Slug",
        "title": "Test",
        "scenes": [{"text": "Merhaba", "duration": 1}],
    })
    with pytest.raises(ConfigError, match="slug"):
        load_job(path)
