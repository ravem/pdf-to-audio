# PDF-to-Audio

**PDF-to-Audio** è uno script Python che legge un file PDF (`.pdf`) e lo converte in audio MP3 con voce italiana naturale.  
Lo script include **pause dinamiche tra paragrafi** e **micro-pause dopo la punteggiatura principale** (`.`, `,`, `;`, `:`), rendendo la lettura più fluida e simile a quella umana.

## Caratteristiche

- Estrazione automatica del testo dai file `.pdf`.  
- Conversione del testo in voce italiana tramite `edge-TTS`.  
- Lettura naturale con pause dinamiche e micro-pause integrate.  
- Velocità di lettura regolabile (parametro `rate`).
- Lo script è pensato per determinare la lingua prevalente del testo basandosi sui primi 1000 caratteri, e in base a quanto rilevato sarà scelta la lingua per la lettura e trasformazione in audio

## Requisiti

- **Python 3.7** o superiore.  
- Moduli Python necessari:
  - `pymupdf` (per leggere file PDF)
  - `edge-tts` (per la conversione in audio MP3)

### Installazione dei moduli

```bash
pip install pymupdf edge-tts
```

### Utilizzo
Posizionare il file .pdf nella stessa cartella dello script.

Aggiornare il nome o il percorso dei file di input e output nello script, se necessario.

Per eseguire lo script:
```bash
python pdf-to-audio.py
```

### Opzioni

Velocità di lettura: modificabile tramite il parametro rate (es. +10% o -10%).

Pause tra paragrafi: dinamiche in base alla lunghezza del testo.

Micro-pause: aggiunte automaticamente dopo la punteggiatura principale per una lettura più naturale.
