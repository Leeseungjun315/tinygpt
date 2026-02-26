import os
from dataclasses import dataclass

@dataclass(frozen=True)
class Settings:
    model: str = os.getenv("TINYGPT_MODEL", "qwen2.5:7b")
    max_turns_before_summary: int = int(os.getenv("TINYGPT_MAX_TURNS", "14"))
    keep_last_turns: int = int(os.getenv("TINYGPT_KEEP_LAST", "6"))
    summary_max_chars: int = int(os.getenv("TINYGPT_SUMMARY_MAX_CHARS", "1200"))

settings = Settings()