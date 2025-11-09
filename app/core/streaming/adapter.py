import json

from typing import Any, Iterable


class StreamAdapter:

    def __init__(self):
        self._sent_final = False
        self._last_main_content: list[str] = []

    def encode(self, ev: dict[str, Any]) -> bytes:
        if ev.get("type") == "node_update" and ev.get("graph") == "main":
            self._last_main_content = list(ev.get("content") or [])
        if ev.get("type") == "final":
            self._sent_final = True
        return (json.dumps(ev, ensure_ascii=False) + "\n").encode("utf-8")

    def finalize_chunks(self) -> Iterable[bytes]:
        if not self._sent_final:
            yield self.encode(
                {
                    "type": "final",
                    "graph": "main",
                    "node": None,
                    "content": self._last_main_content,
                }
            )
