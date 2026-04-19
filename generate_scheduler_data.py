import pandas as pd
import random
import datetime

def generate_realistic_data(num_samples=2500):
    print(f"Synthesizing {num_samples} realistic K8s scheduling samples...")
    data = []
    
    # Assume our hypothetical node capacity is 4000m CPU and 8000MB Memory.
    MAX_CPU = 4000
    MAX_MEM = 8000
    
    # Safety thresholds: We shouldn't schedule if node load exceeds 85% capacity.
    SAFE_CPU_LIMIT = int(MAX_CPU * 0.85)
    SAFE_MEM_LIMIT = int(MAX_MEM * 0.85)

    base_time = datetime.datetime.now()

    for idx in range(num_samples):
        # 1. Generate current node state
        # Varying from almost idle to heavily loaded
        node_cpu_cores = random.randint(100, 3900)
        node_cpu_percent = round((node_cpu_cores / MAX_CPU) * 100, 1)
        
        node_memory_mb = random.randint(500, 7800)
        node_memory_percent = round((node_memory_mb / MAX_MEM) * 100, 1)

        # 2. Generate incoming Pod requirements
        # Different sized pods (microservices vs heavy workers)
        pod_req_cpu = random.randint(50, 2500)
        pod_req_mem = random.randint(64, 4000)

        # 3. Intelligent labeling logic
        # Is the node capable of taking this pod safely?
        cpu_fit = (node_cpu_cores + pod_req_cpu) <= SAFE_CPU_LIMIT
        mem_fit = (node_memory_mb + pod_req_mem) <= SAFE_MEM_LIMIT
        
        # Add a tiny bit of random noise (sensor jitter or edge-case network overhead)
        # In 2% of cases, we incorrectly label to make the ML model robust
        label = 1 if (cpu_fit and mem_fit) else 0
        if random.random() < 0.02:
            label = 1 - label # Flip it

        # Timestamp purely for formatting
        timestamp = (base_time + datetime.timedelta(minutes=idx)).strftime("%H:%M:%S")

        data.append({
            "timestamp": timestamp,
            "node_cpu_cores": node_cpu_cores,
            "node_cpu_percent": node_cpu_percent,
            "node_memory_mb": node_memory_mb,
            "node_memory_percent": node_memory_percent,
            "pod_req_cpu": pod_req_cpu,
            "pod_req_mem": pod_req_mem,
            "label": label
        })

    df = pd.DataFrame(data)
    df.to_csv("k8s_metrics_v2.csv", index=False)
    
    print("Done! Saved to k8s_metrics_v2.csv")
    print("\nDataset Profile:")
    print(df['label'].value_counts(normalize=True))

if __name__ == "__main__":
    random.seed(42)
    generate_realistic_data(10000)
