def format_size(size_bytes: int | None) -> str:
    if size_bytes is None:
        return "unknown"

    if size_bytes >= 1024**3:
        return f"{round(size_bytes / (1024**3), 2)} GB"

    if size_bytes >= 1024**2:
        return f"{round(size_bytes / (1024**2), 2)} MB"

    if size_bytes >= 1024:
        return f"{round(size_bytes / 1024, 2)} KB"

    return f"{size_bytes} bytes"