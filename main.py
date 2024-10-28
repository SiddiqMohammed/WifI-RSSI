# main.py
import time
from datetime import datetime
from connectivity_monitor import ConnectivityMonitor
from signal_strength import SignalStrengthMonitor
from data_usage_monitor import DataUsageMonitor
from speed_tester import SpeedTester

# Initialize monitors
connectivity_monitor = ConnectivityMonitor()
signal_monitor = SignalStrengthMonitor()
data_usage_monitor = DataUsageMonitor()
speed_tester = SpeedTester()

# Initialize start time
start_time = time.time()

# Initialize last known speeds
last_download_speed = ''
last_upload_speed = ''

# Logging setup
log_file = open('internet_monitor_log.csv', 'w')
log_file.write('Timestamp,Status,ResponseTime(ms),RSSI(dBm),BytesSent,BytesReceived,DownloadSpeed(Mbps),UploadSpeed(Mbps)\n')

# Speed test interval
speedtest_interval = 600  # seconds
last_speedtest_time = time.time() - speedtest_interval  # Force initial speed test

try:
    while True:
        current_time = time.time()
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Check connectivity
        connectivity_data = connectivity_monitor.check_connectivity()

        # Get signal strength
        signal_strength = signal_monitor.get_signal_strength()

        # Get data usage
        data_usage = data_usage_monitor.get_data_usage()

        # Run speed test at intervals
        if (current_time - last_speedtest_time >= speedtest_interval) and (connectivity_data['status'] == 'Connected'):
            speed_results = speed_tester.run_test()
            if speed_results['download_speed'] is not None and speed_results['upload_speed'] is not None:
                last_download_speed = round(speed_results['download_speed'], 2)
                last_upload_speed = round(speed_results['upload_speed'], 2)
                # Print the download and upload speeds to the console
                print(f"Speed test results - Download: {last_download_speed} Mbps, Upload: {last_upload_speed} Mbps")
            else:
                print("Speed test failed or returned no data.")
            last_speedtest_time = current_time

        # Prepare log entry after speed test
        log_entry = {
            'timestamp': timestamp,
            'status': connectivity_data['status'],
            'response_time': round(connectivity_data['response_time'] * 1000, 2) if connectivity_data['response_time'] else '',
            'rssi': signal_strength,
            'bytes_sent': data_usage['bytes_sent'],
            'bytes_received': data_usage['bytes_received'],
            'download_speed': last_download_speed,
            'upload_speed': last_upload_speed
        }

        # Write to log
        log_file.write('{timestamp},{status},{response_time},{rssi},{bytes_sent},{bytes_received},{download_speed},{upload_speed}\n'.format(**log_entry))
        log_file.flush()

        # Prepare status message
        status_message = (f"[{timestamp}] Status: {log_entry['status']}, "
                          f"Response Time: {log_entry['response_time']} ms, "
                          f"RSSI: {log_entry['rssi']} dBm, "
                          f"Download Speed: {log_entry['download_speed']} Mbps, "
                          f"Upload Speed: {log_entry['upload_speed']} Mbps")

        # Print status to console
        print(status_message)

        time.sleep(connectivity_monitor.ping_interval)

except KeyboardInterrupt:
    # Move to the next line
    print()
    # Close log file
    log_file.close()

    # Calculate total monitoring time
    total_time = time.time() - start_time

    # Calculate packet loss percentage
    packet_loss_percentage = (connectivity_monitor.failed_pings / connectivity_monitor.total_pings) * 100 if connectivity_monitor.total_pings > 0 else 0

    # Print summary
    print('\n--- Internet Connection Monitoring Summary ---')
    print(f'Total monitoring time: {total_time:.2f} seconds')
    print(f'Total pings sent: {connectivity_monitor.total_pings}')
    print(f'Failed pings: {connectivity_monitor.failed_pings}')
    print(f'Packet loss: {packet_loss_percentage:.2f}%')
    print(f'Total drops: {connectivity_monitor.drop_count}')
    print(f'Total drop time: {connectivity_monitor.total_drop_time:.2f} seconds')

    # Print detailed drop events if any
    if connectivity_monitor.drops:
        print('\nDetailed drop events:')
        for idx, drop in enumerate(connectivity_monitor.drops, 1):
            drop_start = datetime.fromtimestamp(drop["drop_start"]).strftime('%Y-%m-%d %H:%M:%S')
            drop_end = datetime.fromtimestamp(drop["drop_end"]).strftime('%Y-%m-%d %H:%M:%S')
            duration = drop['duration']
            print(f'{idx}. Drop from {drop_start} to {drop_end}, duration: {duration:.2f} seconds')
    else:
        print('\nNo drops were detected during the monitoring period.')
