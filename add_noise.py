import pandas as pd
import random
random.seed(42)

df = pd.read_csv('k8s_metrics.csv')
print(f'Before: {len(df)} samples')

noisy_rows = []

# 15 ambiguous mid-range nodes (hard to classify) - labeled as high load
for i in range(15):
    noisy_rows.append({
        'timestamp': f'05:{30+i:02d}:00',
        'cpu_cores': random.randint(800, 1200),
        'cpu_percent': random.randint(4, 8),
        'memory_mb': random.randint(650, 720),
        'memory_percent': random.randint(5, 6),
        'label': 1
    })

# 10 noisy low-load nodes with slightly elevated metrics
for i in range(10):
    noisy_rows.append({
        'timestamp': f'06:{10+i:02d}:00',
        'cpu_cores': random.randint(250, 500),
        'cpu_percent': random.randint(2, 5),
        'memory_mb': random.randint(600, 680),
        'memory_percent': random.randint(4, 6),
        'label': 0
    })

# 8 intentionally ambiguous edge cases (realistic sensor noise)
for i in range(8):
    noisy_rows.append({
        'timestamp': f'07:{10+i:02d}:00',
        'cpu_cores': random.randint(600, 900),
        'cpu_percent': random.randint(3, 7),
        'memory_mb': random.randint(640, 710),
        'memory_percent': random.randint(5, 6),
        'label': random.choice([0, 1])
    })

noise_df = pd.DataFrame(noisy_rows)
df = pd.concat([df, noise_df], ignore_index=True)
df.to_csv('k8s_metrics.csv', index=False)

print(f'After: {len(df)} samples')
low = len(df[df['label'] == 0])
high = len(df[df['label'] == 1])
print(f'Low Load: {low}, High Load: {high}')
print(f'CPU cores range: {df["cpu_cores"].min()} - {df["cpu_cores"].max()}')
print('Done! Noisy edge-case data added.')
