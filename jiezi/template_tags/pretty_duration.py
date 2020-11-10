def pretty_duration(duration):
    total_seconds = int(duration.total_seconds())
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60
    if hours > 0:
        return f"{hours} hours {minutes} minutes"
    elif minutes > 0:
        return f"{minutes} minutes {seconds} seconds"
    else:
        return f"{seconds} seconds"
