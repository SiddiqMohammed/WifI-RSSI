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
        try:
            result = subprocess.check_output(['netsh', 'wlan', 'show', 'interfaces'], stderr=subprocess.STDOUT).decode()
            # Use regular expressions to find the signal quality
            match = re.search(r'Signal\s*:\s*(\d+)%', result)
            if match:
                signal_quality = int(match.group(1))
                # Convert signal quality (percentage) to RSSI (dBm)
                rssi = self._quality_to_rssi(signal_quality)
                return rssi
        except Exception as e:
            print(f'Error retrieving signal strength: {e}')
        return None

    def _quality_to_rssi(self, quality):
        # Approximate conversion from signal quality (%) to RSSI (dBm)
        if quality <= 0:
            return -100
        elif quality >= 100:
            return -50
        else:
            return -100 + (quality / 2)

    def _get_linux_signal_strength(self):
        try:
            result = subprocess.check_output(['iwconfig'], stderr=subprocess.STDOUT).decode()
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
            rssi = re.search(r'agrCtlRSSI:\s*(-\d+)', result)
            if rssi:
                return int(rssi.group(1))
        except Exception as e:
            print(f'Error retrieving signal strength: {e}')
        return None
