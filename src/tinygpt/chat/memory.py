from __future__ import annotations

from tinygpt.ollama.client import one_shot
from tinygpt.chat.prompts import SUMMARIZER_SYSTEM


def need_summarize(messages: list[dict], max_turns: int) -> bool:
    """user 메시지 개수가 max_turns 이상이면 요약 트리거"""
    turns = sum(1 for m in messages if m.get("role") == "user")
    return turns >= max_turns


def summarize_memory(
    model: str,
    memory_summary: str,
    messages: list[dict],
    keep_last_turns: int,
    summary_max_chars: int,
) -> tuple[str, list[dict]]:
    """
    오래된 대화를 요약해 memory_summary에 누적하고,
    messages는 최근 keep_last_turns 쌍만 유지한다.
    """
    # user 메시지 인덱스 기준으로 자르기
    user_indices = [i for i, m in enumerate(messages) if m.get("role") == "user"]
    if len(user_indices) <= keep_last_turns:
        return memory_summary, messages

    cut_user_i = user_indices[-keep_last_turns]
    old_part = messages[1:cut_user_i]           # system 제외하고 오래된 부분
    new_part = messages[:1] + messages[cut_user_i:]  # system + 최근 부분

    # 요약할 대화 transcript 만들기
    transcript_lines: list[str] = []
    for m in old_part:
        role = m.get("role")
        content = (m.get("content") or "").strip()
        if not content:
            continue
        if role == "user":
            transcript_lines.append(f"사용자: {content}")
        elif role == "assistant":
            transcript_lines.append(f"봇: {content}")

    transcript_text = "\n".join(transcript_lines).strip()
    if not transcript_text:
        return memory_summary, new_part

    prompt = f"""
[기존 장기 메모리(있다면)]:
{memory_summary.strip() or "(없음)"}

[새로 요약할 대화]:
{transcript_text}

요청:
- 기존 장기 메모리를 갱신/통합해서 최종 장기 메모리를 작성해줘.
- {summary_max_chars}자 내외로 압축해줘.
- 불릿 목록으로 작성해줘.
""".strip()

    updated = one_shot(model, [
        {"role": "system", "content": SUMMARIZER_SYSTEM},
        {"role": "user", "content": prompt},
    ]).strip()

    return updated, new_part