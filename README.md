# TinyGPT

> 로컬 GPU 기반 콘솔 AI 챗봇\
> Rich 기반 세련된 CLI UI + 자동 메모리 요약 + Ollama 연동
> 가상환경 만들고 구동하는 것이 편합니다.

------------------------------------------------------------------------

## Features

-   세련된 Rich 기반 CLI UI
-   Ollama 로컬 모델 실행 (API 비용 0원)
-   대화 길어지면 자동 요약 메모리 유지
-   실시간 스트리밍 응답 (Live 업데이트)

------------------------------------------------------------------------

## Requirements

-   Python 3.10+
-   권장: 3.11 / 3.12
-   3.13: 의존성 설치 이슈(torch)
-   Ollama 설치
-   NVIDIA GPU (권장)
-   Windows / macOS / Linux

------------------------------------------------------------------------

## 가상환경 생성 (Virtual Environment Setup

Windows

```bash
python -m venv .venv
```

macOS / Linux

```bash
python3 -m venv .venv
```

## 가상환경 활성화

Windows

```bash
.venv\Scripts\Activate or .venv\Scripts\Activate.bat
```

macOS / Linux

```bash
source .venv/bin/activate
```

## 가상환경 종료
```bash
deactivate
```
------------------------------------------------------------------------

## Recommended Model

**터미널에 입력**

``` bash
ollama pull qwen2.5:7b
```

또는

``` bash
ollama pull llama3.1:8b
```

(qwen2.5:7b 권장)

------------------------------------------------------------------------

##  Installation

프로젝트 루트(pyproject.toml 있는 폴더)에서:

``` bash
pip install -e .
```

------------------------------------------------------------------------

## Run

``` bash
python -m tinygpt
```

또는

``` bash
tinygpt
```

------------------------------------------------------------------------

## Commands

  Command     Description
  ----------- --------------------------
  `/model`    현재 사용 중인 모델 표시
  `/memory`   장기 메모리 요약 보기
  `/reset`    대화 및 메모리 초기화
  `/exit`     종료

------------------------------------------------------------------------

## Memory System

대화가 길어지면:

-   오래된 메시지를 자동 요약
-   장기 메모리로 압축 저장
-   최근 대화는 그대로 유지

이를 통해 컨텍스트 길이 제한 문제를 완화합니다.

------------------------------------------------------------------------

## Configuration

환경 변수로 설정 가능:

``` bash
set TINYGPT_MODEL=qwen2.5:7b
set TINYGPT_MAX_TURNS=14
set TINYGPT_KEEP_LAST=6
```

------------------------------------------------------------------------

## License

MIT License

------------------------------------------------------------------------

## Author

Built with using: - Ollama - Qwen / Llama - Rich
