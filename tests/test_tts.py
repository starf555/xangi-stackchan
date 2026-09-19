import threading
import time

from xangi_stackchan.tts import normalize_speech_text, split_text, wait_for_complete_file


def test_split_text_keeps_japanese_sentences():
    assert split_text("こんにちは。元気ですか？はい！", max_len=8) == [
        "こんにちは。",
        "元気ですか？",
        "はい！",
    ]


def test_normalize_speech_text_reads_acronyms_dates_and_markdown():
    assert normalize_speech_text(
        "- **NT東京**は9/20開催。 [公式](https://example.com/event)"
    ) == "エヌティー東京は9月20日開催。 公式"


def test_wait_for_complete_file_waits_for_stable_size(tmp_path):
    target = tmp_path / "out.wav"

    def writer():
        target.write_bytes(b"")
        time.sleep(0.05)
        target.write_bytes(b"RIFF" + b"\0" * 60)

    thread = threading.Thread(target=writer)
    thread.start()
    data = wait_for_complete_file(target, time.time() + 2)
    thread.join()
    assert len(data) == 64
