import radish.extensions.time_recorder
import datetime
import mock

def current_utc_time():
    return datetime.datetime.now(datetime.timezone.utc)

def apply_utctime_patch():
    # Patch datetime specifically within radish.extensions.time_recorder
    radish.extensions.time_recorder.datetime = mock.Mock()
    radish.extensions.time_recorder.datetime.utcnow = current_utc_time