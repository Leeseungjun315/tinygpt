from __future__ import annotations

from dataclasses import dataclass
from time import perf_counter

from rich.console import Console
from rich.panel import Panel
from rich.live import Live
from rich.markdown import Markdown
from rich.text import Text
from rich.align import Align
from rich.rule import Rule

from tinygpt.settings import settings
from tinygpt.chat.prompts import SYSTEM
from tinygpt.ollama.client import stream_chat
from tinygpt.chat.memory import need_summarize, summarize_memory

console = Console()


@dataclass
class UIState:
    memory_summary: str = ""
    last_latency_s: float = 0.0


def header():
    console.print(Panel.fit(
        f"[bold cyan]TinyGPT[/bold cyan]  [dim]local • ollama[/dim]\n"
        f"[dim]Model:[/dim] [bold]{settings.model}[/bold]\n"
        f"[dim]Commands:[/dim] [green]/model[/green] [green]/memory[/green] [green]/reset[/green] [green]/exit[/green]",
        border_style="cyan",
        padding=(1, 2),
    ))
    console.print(Rule(style="grey50"))


def status_line(state: UIState) -> None:
    mem = "on" if state.memory_summary.strip() else "off"
    console.print(
        f"[dim]Latency:[/dim] [bold]{state.last_latency_s:.2f}s[/bold]   "
        f"[dim]Memory:[/dim] [bold]{mem}[/bold]",
    )
    console.print(Rule(style="grey50"))


def message_panel(role: str, content: str) -> Panel:
    if role == "user":
        return Panel(
            Align.left(Text(content)),
            title=Text("You", style="bold"),
            border_style="blue",
            padding=(1, 2),
        )
    else:
        return Panel(
            Align.left(Markdown(content or "…")),
            title=Text("Assistant", style="bold"),
            border_style="cyan",
            padding=(1, 2),
        )


def build_context_messages(messages: list[dict], memory_summary: str) -> list[dict]:
    ctx = [{"role": "system", "content": SYSTEM}]
    if memory_summary.strip():
        ctx.append({
            "role": "system",
            "content": f"다음은 이전 대화의 장기 메모리 요약이다:\n{memory_summary.strip()}"
        })
    ctx.extend(messages[1:])
    return ctx


def live_stream_answer(ctx: list[dict], state: UIState) -> str:
    """현재 답변만 Live로 부드럽게 갱신하고, 끝나면 로그로 남김"""
    stream = stream_chat(settings.model, ctx)

    assistant_text = ""
    panel = message_panel("assistant", "")

    t0 = perf_counter()
    with Live(panel, console=console, refresh_per_second=24):
        for chunk in stream:
            piece = chunk["message"]["content"]
            assistant_text += piece
            panel.renderable = Align.left(Markdown(assistant_text if assistant_text.strip() else "…"))
    state.last_latency_s = perf_counter() - t0

    return assistant_text.strip()


def run_cli():
    state = UIState()
    messages = [{"role": "system", "content": SYSTEM}]

    header()

    while True:
        try:
            user = console.input("[bold blue]You ▶[/bold blue] ").strip()
        except (KeyboardInterrupt, EOFError):
            console.print("\n[dim]종료![/dim]")
            break

        if not user:
            continue

        cmd = user.lower()
        if cmd in ("exit", "quit", "/exit"):
            console.print("[dim]종료![/dim]")
            break

        if cmd == "/model":
            console.print(Panel(f"현재 모델: [bold yellow]{settings.model}[/bold yellow]", border_style="yellow"))
            continue

        if cmd == "/memory":
            console.print(Panel(Markdown(state.memory_summary or "(메모리 없음)"), title="Memory", border_style="cyan"))
            continue

        if cmd == "/reset":
            messages = [{"role": "system", "content": SYSTEM}]
            state.memory_summary = ""
            console.print(Panel("대화를 초기화했어요.", border_style="magenta"))
            console.print(Rule(style="grey50"))
            continue

        # 유저 메시지 로그로 출력
        console.print(message_panel("user", user))
        messages.append({"role": "user", "content": user})

        # 길어지면 자동 요약 메모리
        if need_summarize(messages, settings.max_turns_before_summary):
            with console.status("[dim]대화가 길어져서 메모리를 요약 중…[/dim]"):
                state.memory_summary, messages = summarize_memory(
                    model=settings.model,
                    memory_summary=state.memory_summary,
                    messages=messages,
                    keep_last_turns=settings.keep_last_turns,
                    summary_max_chars=settings.summary_max_chars,
                )

        # 답변 생성 (Live 패널로 “현재 답변만” 갱신)
        with console.status("[dim]답변 생성 중…[/dim]"):
            ctx = build_context_messages(messages, state.memory_summary)
            assistant = live_stream_answer(ctx, state)

        messages.append({"role": "assistant", "content": assistant})

        # 상태/구분선
        status_line(state)