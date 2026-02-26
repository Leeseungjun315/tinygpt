from tinygpt.chat.memory import need_summarize

def test_need_summarize_false():
    messages = [
        {"role": "system", "content": "x"},
        {"role": "user", "content": "a"},
        {"role": "assistant", "content": "b"},
    ]
    assert need_summarize(messages, max_turns=5) is False


def test_need_summarize_true():
    messages = [{"role": "system", "content": "x"}]

    # user 턴 6개 만들기
    for i in range(6):
        messages.append({"role": "user", "content": f"u{i}"})
        messages.append({"role": "assistant", "content": f"a{i}"})

    assert need_summarize(messages, max_turns=5) is True