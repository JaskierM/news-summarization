from typing import Any, Iterator

SERVICE_TAGS = {"updates", "error", "final"}


def extract_content_names(payload: Any) -> list[str]:
    if isinstance(payload, dict):
        return sorted(map(str, payload.keys()))
    return []


def flatten_event(raw, depth: int = 0) -> Iterator[dict[str, Any]]:
    graph = "main" if depth == 0 else "subgraph"

    if isinstance(raw, tuple) and len(raw) == 2 and isinstance(raw[0], str):
        tag, data = raw

        if tag in SERVICE_TAGS:
            if tag == "updates":
                if isinstance(data, dict):
                    for node_name, node_payload in data.items():
                        yield {
                            "type": "node_update",
                            "graph": graph,
                            "node": str(node_name),
                            "content": extract_content_names(node_payload),
                        }
                else:
                    yield {"type": "error", "graph": graph, "node": None, "content": []}

            elif tag == "error":
                for node_name, node_payload in data.items():
                    yield {
                        "type": "error",
                        "graph": graph,
                        "node": str(node_name),
                        "content": extract_content_names(node_payload),
                        "final_answer": raw[1]["output"]["error"],
                    }

            elif tag == "final":
                for node_name, node_payload in data.items():
                    yield {
                        "type": "final",
                        "graph": graph,
                        "node": str(node_name),
                        "content": extract_content_names(node_payload),
                        "final_answer": raw[1]["output"]["last_message"],
                    }
        else:
            for ev in flatten_event(data, depth=depth + 1):
                yield ev
        return
