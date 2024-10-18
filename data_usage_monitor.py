# data_usage_monitor.py
import psutil

class DataUsageMonitor:
    def __init__(self):
        self.initial_counters = psutil.net_io_counters()

    def get_data_usage(self):
        counters = psutil.net_io_counters()
        sent = counters.bytes_sent - self.initial_counters.bytes_sent
        recv = counters.bytes_recv - self.initial_counters.bytes_recv
        return {
            'bytes_sent': sent,
            'bytes_received': recv
        }
