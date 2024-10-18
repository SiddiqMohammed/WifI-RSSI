# connectivity_monitor.py
import time
from datetime import datetime
import ping3

class ConnectivityMonitor:
    def __init__(self, ping_host='8.8.8.8', ping_interval=1):
        self.ping_host = ping_host
        self.ping_interval = ping_interval
        self.drop_count = 0
        self.drops = []
        self.last_status = None
        self.total_drop_time = 0
        self.drop_start_time = None
        self.total_pings = 0
        self.failed_pings = 0

    def check_connectivity(self):
        response_time = ping3.ping(self.ping_host, timeout=1)
        self.total_pings += 1
        current_time = time.time()

        if response_time is not None:
            status = 'Connected'
            if self.last_status == 'Disconnected':
                # Internet just recovered
                recovery_time = current_time
                drop_duration = recovery_time - self.drop_start_time
                self.total_drop_time += drop_duration
                self.drops.append({
                    'drop_start': self.drop_start_time,
                    'drop_end': recovery_time,
                    'duration': drop_duration
                })
            self.last_status = 'Connected'
        else:
            status = 'Disconnected'
            self.failed_pings += 1
            if self.last_status == 'Connected':
                # Internet just dropped
                self.drop_count += 1
                self.drop_start_time = current_time
            self.last_status = 'Disconnected'

        return {
            'timestamp': datetime.now(),
            'status': status,
            'response_time': response_time
        }
