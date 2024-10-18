# signal_strength.py
import subprocess
import platform
import re

class SignalStrengthMonitor:
    def __init__(self):
        self.system = platform.system()

    def get_signal_strength(self):
        if self.system == 'Windows':
            return self._get_windows_signal_strength()
        elif self.system == 'Linux':
            return self._get_linux_signal_strength()
        elif self.system == 'Darwin':
            return self._get_mac_signal_strength()
        else:
            return None

    def _get_windows_signal_strength(self):
        # Windows implementation (requires additional code or libraries)
        return None

    def _get_linux_signal_strength(self):
        try:
            result = subprocess.check_output(['iwconfig'], stderr=subprocess.STDOUT).decode()
            # Use raw strings for regular expressions
            rssi = re.search(r'Signal level=(-\d+) dBm', result)
            if rssi:
                return int(rssi.group(1))
        except Exception as e:
            print(f'Error retrieving signal strength: {e}')
        return None

    def _get_mac_signal_strength(self):
        try:
            result = subprocess.check_output(
                ["/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport", "-I"]
            ).decode()
            # Use raw strings for regular expressions
            rssi = re.search(r'agrCtlRSSI: (-\d+)', result)
            if rssi:
                return int(rssi.group(1))
        except Exception as e:
            print(f'Error retrieving signal strength: {e}')
        return None
