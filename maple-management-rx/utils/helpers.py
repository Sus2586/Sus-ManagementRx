import time

def format_uptime(start_time: float) -> str:
    """Formats bot uptime into human-readable string."""
    seconds = int(time.time() - start_time)
    days, seconds = divmod(seconds, 86400)
    hours, seconds = divmod(seconds, 3600)
    minutes, seconds = divmod(seconds, 60)
    parts = []
    if days > 0: parts.append(f"{days}d")
    if hours > 0: parts.append(f"{hours}h")
    if minutes > 0: parts.append(f"{minutes}m")
    parts.append(f"{seconds}s")
    return " ".join(parts)

def parse_duration(duration_str: str) -> int:
    """Parses duration strings like 10m, 2h, 1d into seconds."""
    duration_str = duration_str.strip().lower()
    if not duration_str:
        return 0
    unit = duration_str[-1]
    if unit in ['s', 'm', 'h', 'd']:
        try:
            val = int(duration_str[:-1])
            mult = {'s': 1, 'm': 60, 'h': 3600, 'd': 86400}[unit]
            return val * mult
        except ValueError:
            return 0
    try:
        return int(duration_str)  # default seconds
    except ValueError:
        return 0
