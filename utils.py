from PyQt5.QtCore import QDateTime

def round_to_next_hour(dt):
    """Round the given datetime to the next hour if minutes or seconds are not zero."""
    time = dt.time()
    if time.minute() == 0 and time.second() == 0:
        return dt
    # Round up to the next hour
    return dt.addSecs(3600 - (time.minute() * 60 + time.second()))
