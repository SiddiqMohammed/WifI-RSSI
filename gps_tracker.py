# gps_tracker.py
import threading
import gps

class GPSTracker:
    def __init__(self):
        self.gpsd = gps.gps(mode=gps.WATCH_ENABLE | gps.WATCH_NEWSTYLE)
        self.current_value = None
        self.running = True
        self.thread = threading.Thread(target=self._run)
        self.thread.start()

    def _run(self):
        while self.running:
            try:
                self.current_value = self.gpsd.next()
            except StopIteration:
                pass

    def get_current_fix(self):
        if self.current_value and hasattr(self.current_value, 'lat'):
            return {
                'latitude': self.current_value.lat,
                'longitude': self.current_value.lon,
                'speed': self.current_value.speed
            }
        else:
            return None

    def stop(self):
        self.running = False
        self.thread.join()
