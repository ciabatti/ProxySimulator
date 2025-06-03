import numpy as np
from qutip import qeye

def channel_loss(L_km, alpha_db_per_km):
    """Trasmittanza (perdita esponenziale) in funzione della distanza."""
    return 10 ** (-alpha_db_per_km * L_km / 10)

def depolarizing_noise(rho, p):
    """Rumore depolarizzante: stato misto con identità."""
    I = qeye(2)
    return (1 - p) * rho + p / 2 * I

def apply_segmented_noise(rho, total_p, n_steps):
    """Applica rumore depolarizzante in più step più realistici."""
    p_step = 1 - (1 - total_p) ** (1 / n_steps)
    for _ in range(n_steps):
        rho = depolarizing_noise(rho, p_step)
    return rho
