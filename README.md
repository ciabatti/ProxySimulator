# MyQkdSimulation

**MyQkdSimulation** è una simulazione numerica del protocollo BB84 per la distribuzione quantistica di chiavi (Quantum Key Distribution, QKD). Il progetto consente di analizzare l'impatto di perdite di canale, rumore depolarizzante e nodi intermedi (proxy) sul Quantum Bit Error Rate (QBER), sul key rate e sulla latenza complessiva della trasmissione.

## Caratteristiche principali

- Implementazione del protocollo BB84 con supporto per canali rumorosi e perdite realistiche.
- Modellazione della depolarizzazione quantistica per ogni segmento di trasmissione.
- Supporto per segmentazione della distanza tramite nodi proxy intermedi.
- Calcolo dettagliato di:
  - QBER (Quantum Bit Error Rate)
  - Key rate (bit/s)
  - Tempo totale di trasmissione, incluse latenze proxy e propagazione.
- Visualizzazione dei risultati tramite grafici.

## Struttura del progetto
MyQkdSimulation/
│ 
│ ├── channel.py # Funzioni di perdita e rumore
│ ├── protocol.py # Simulazione del BB84
│ ├── quantum_states.py # Stati e basi quantistiche
├── main.py # Script principale di esecuzione
├── requirements.txt # Dipendenze del progetto
├── README.md # Documentazione

## Requisiti

- Python 3.8 o superiore
- QuTiP
- NumPy
- Matplotlib

MEMO: installare i requisiti tramite:

```bash
pip install -r requirements.txt
