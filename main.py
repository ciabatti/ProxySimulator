import numpy as np
import matplotlib.pyplot as plt
from protocol import simulate_bb84, compute_time

# Parametri
alpha = 0.2
mu = 1e6
qber_base = 0.02
qber_proxy = 0.01
n_bits = 1000
burst_size = 100
L_values = np.arange(10, 200, 10)

results = {
    "direct": {"qber": [], "rate": [], "time": []},
    "proxy_1": {"qber": [], "rate": [], "time": []},
    "proxy_2": {"qber": [], "rate": [], "time": []},
}

for L in L_values:
    print(f"\n📏 Distanza totale: {L} km")

    # Diretto
    qber_d, rate_d, _ = simulate_bb84(n_bits, L, alpha, qber_base, qber_proxy, 0)
    time_d = compute_time(n_bits, [L], mu, 0, burst_size)
    results["direct"]["qber"].append(qber_d)
    results["direct"]["rate"].append(rate_d * mu)
    results["direct"]["time"].append(time_d)

    print(f"  🔹 Diretto: QBER={qber_d:.3f}, Rate={rate_d*mu:.1f} bps, Tempo={time_d*1e3:.2f} ms")

    # 1 Proxy
    Ls = [L/2, L/2]
    rates, qbers = [], []
    for seg in Ls:
        qber, rate, _ = simulate_bb84(n_bits, seg, alpha, qber_base, qber_proxy, 1)
        qbers.append(qber)
        rates.append(rate)
    qber_1 = 1 - np.prod([1 - q for q in qbers]) * (1 - qber_proxy)
    rate_1 = min(rates) * mu
    time_1 = compute_time(n_bits, Ls, mu, 1e-6, burst_size)
    results["proxy_1"]["qber"].append(qber_1)
    results["proxy_1"]["rate"].append(rate_1)
    results["proxy_1"]["time"].append(time_1)
    print(f"  🔸 1 Proxy: QBER={qber_1:.3f}, Rate={rate_1:.1f} bps, Tempo={time_1*1e3:.2f} ms")

    # 2 Proxy
    Ls = [L/3] * 3
    rates, qbers = [], []
    for seg in Ls:
        qber, rate, _ = simulate_bb84(n_bits, seg, alpha, qber_base, qber_proxy, 2)
        qbers.append(qber)
        rates.append(rate)
    qber_2 = 1 - np.prod([1 - q for q in qbers]) * (1 - qber_proxy)**2
    rate_2 = min(rates) * mu
    time_2 = compute_time(n_bits, Ls, mu, 1e-6, burst_size)
    results["proxy_2"]["qber"].append(qber_2)
    results["proxy_2"]["rate"].append(rate_2)
    results["proxy_2"]["time"].append(time_2)
    print(f"  🔻 2 Proxy: QBER={qber_2:.3f}, Rate={rate_2:.1f} bps, Tempo={time_2*1e3:.2f} ms")

# Plot
plt.figure(figsize=(15, 5))

plt.subplot(1, 3, 1)
plt.plot(L_values, results["direct"]["qber"], label="Diretto")
plt.plot(L_values, results["proxy_1"]["qber"], label="1 Proxy")
plt.plot(L_values, results["proxy_2"]["qber"], label="2 Proxy")
plt.xlabel("Distanza (km)")
plt.ylabel("QBER")
plt.legend()
plt.title("QBER vs Distanza")

plt.subplot(1, 3, 2)
plt.plot(L_values, results["direct"]["rate"], label="Diretto")
plt.plot(L_values, results["proxy_1"]["rate"], label="1 Proxy")
plt.plot(L_values, results["proxy_2"]["rate"], label="2 Proxy")
plt.xlabel("Distanza (km)")
plt.ylabel("Key rate (bit/s)")
plt.yscale('log')
plt.legend()
plt.title("Key rate vs Distanza")

plt.subplot(1, 3, 3)
plt.plot(L_values, np.array(results["direct"]["time"]) * 1e3, label="Diretto")
plt.plot(L_values, np.array(results["proxy_1"]["time"]) * 1e3, label="1 Proxy")
plt.plot(L_values, np.array(results["proxy_2"]["time"]) * 1e3, label="2 Proxy")
plt.xlabel("Distanza (km)")
plt.ylabel("Tempo totale (ms)")
plt.legend()
plt.title("Tempo vs Distanza")

plt.tight_layout()
plt.show()
