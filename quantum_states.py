from qutip import basis

# Stati di base
H = basis(2, 0)  # |0>
V = basis(2, 1)  # |1>
D = (H + V).unit()  # |+>
A = (H - V).unit()  # |->

# Basi di misura
Z_basis = [H * H.dag(), V * V.dag()]  # base rettilinea
X_basis = [D * D.dag(), A * A.dag()]  # base diagonale
