import numpy as np
from quantum_states import H, V, D, A, Z_basis, X_basis
from channel import channel_loss, apply_segmented_noise

def simulate_bb84(n_bits, L, alpha, qber_base, qber_proxy=0.01, n_proxies=0):
    key = []
    errors = 0
    eta = channel_loss(L, alpha)

    n_segments = n_proxies + 1
    total_noise = qber_base + qber_proxy * n_proxies

    for _ in range(n_bits):
        bit = np.random.randint(0, 2)
        basis_alice = np.random.randint(0, 2)
        state = [H, V][bit] if basis_alice == 0 else [D, A][bit]
        state = state * state.dag()

        if np.random.random() > eta:
            continue  # qubit perso

        state = apply_segmented_noise(state, total_noise, n_segments)

        basis_bob = np.random.randint(0, 2)
        if basis_alice == basis_bob:
            meas_basis = [Z_basis, X_basis][basis_bob]
            probs = [np.real(state.overlap(m)) for m in meas_basis]
            total_p = sum(probs)
            probs = [p / total_p if total_p > 0 else 0.5 for p in probs]
            outcome = np.random.choice([0, 1], p=probs)
            key.append(bit)
            if outcome != bit:
                errors += 1

    qber = errors / len(key) if key else qber_base
    key_rate = 0.5 * eta * (1 - qber)
    return qber, key_rate, len(key)

def compute_time(n_bits, segments_km, mu=1e6, latency_proxy=1e-6, burst_size=100):
    """Tempo totale per trasmissione considerando propagazione e latenza."""
    c_fiber = 2e8  # m/s
    total_time = 0
    for L in segments_km:
        total_time += 2 * (L * 1e3) / c_fiber  # RTT
        total_time += latency_proxy

    n_bursts = np.ceil(n_bits / burst_size)
    total_time += n_bursts / mu
    return total_time
