import subprocess
import csv
import time
import datetime

print("Collecting real Kubernetes metrics...")

with open("k8s_metrics.csv", "a", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["timestamp", "cpu_cores", "cpu_percent", "memory_mb", "memory_percent", "label"])
    count = 0
    while count < 200:
        try:
            result = subprocess.run([r"D:\kubectl.exe", "top", "nodes", "--no-headers"], capture_output=True, text=True)
            line = result.stdout.strip().split()
            if len(line) >= 4:
                cpu = int(line[1].replace("m",""))
                cpu_pct = int(line[2].replace("%",""))
                mem = int(line[3].replace("Mi",""))
                mem_pct = int(line[4].replace("%",""))
                label = 1 if cpu_pct > 5 or mem_pct > 50 else 0
                timestamp = datetime.datetime.now().strftime("%H:%M:%S")
                writer.writerow([timestamp, cpu, cpu_pct, mem, mem_pct, label])
                f.flush()
                print(f"[{timestamp}] CPU: {cpu}m ({cpu_pct}%) | Memory: {mem}Mi ({mem_pct}%) | Label: {label}")
            count += 1
            time.sleep(2)
        except Exception as e:
            print(f"Error: {e}")
            count += 1

print("Done! k8s_metrics.csv saved!")
