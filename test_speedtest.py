# test_speedtest.py
import speedtest

try:
    s = speedtest.Speedtest()
    s.get_best_server()
    download_speed = s.download() / 1e6  # Convert to Mbps
    upload_speed = s.upload() / 1e6
    print(f"Download speed: {download_speed:.2f} Mbps")
    print(f"Upload speed: {upload_speed:.2f} Mbps")
except Exception as e:
    print(f"An error occurred: {e}")
