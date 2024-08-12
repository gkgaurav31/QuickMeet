from PyQt5.QtCore import QDateTime

def round_to_next_hour(datetime):
    """Rounds the given QDateTime to the next hour."""
    minutes = datetime.time().minute()
    seconds = datetime.time().second()
    if minutes > 0 or seconds > 0:
        # Round up to the next hour
        return datetime.addSecs((60 - minutes) * 60 - seconds)
    else:
        # Already at the top of the hour
        return datetime
