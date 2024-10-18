# speed_test.py
import speedtest

class SpeedTester:
    def __init__(self):
        self.speedtester = speedtest.Speedtest()

    def run_test(self):
        self.speedtester.get_best_server()
        download_speed = self.speedtester.download() / 1e6  # Mbps
        upload_speed = self.speedtester.upload() / 1e6
        return {
            'download_speed': download_speed,
            'upload_speed': upload_speed
        }
