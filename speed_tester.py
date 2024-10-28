# speed_test.py
import speedtest

class SpeedTester:
    def __init__(self):
        pass  # No need to initialize the Speedtest object here

    def run_test(self):
        try:
            speedtester = speedtest.Speedtest()
            speedtester.get_best_server()
            download_speed = speedtester.download() / 1e6  # Convert to Mbps
            upload_speed = speedtester.upload() / 1e6
            print(f"Download speed: {download_speed:.2f} Mbps")
            print(f"Upload speed: {upload_speed:.2f} Mbps")
            return {
                'download_speed': download_speed,
                'upload_speed': upload_speed
            }
        except Exception as e:
            print(f"An error occurred during the speed test: {e}")
            return {
                'download_speed': None,
                'upload_speed': None
            }
