# Industry Lab - Progetto

Riccardo Cervero\
Marco Savino\
Luca Lazzati
--------------------------------------------------------------------------------
## Istruzioni per utilizzo del sistema di monitoraggio
1. Inizializzazione di due producer di Kafka, rispettivamente per simulare:
  - sensore di misurazione del coefficiente di perdita
  - sensore di misurazione della media di portata a 140rpm
2. Esecuzione del `writer.py` per l'analisi realtime degli outlier e la scrittura dei dati in un database locale 
3. Esecuzione del file `MonitoringSystem.py`
4. Collegamento alla porta http://127.0.0.1:8050
