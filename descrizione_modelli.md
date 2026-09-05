# Implementazione

Questo documento descrive i modelli di automa cellulare implementati nella cartella
`CellularAutomata-SIR`. I tre modelli principali (SIR, incendio boschivo, Ising) hanno la
logica di evoluzione scritta in C (cartella `C_file/`, compilata in librerie condivise) e
vengono pilotati da Python tramite `ctypes`; la visualizzazione è fatta con `pygame`.

## Sintesi generale: due famiglie di automi cellulari per fenomeni di propagazione spaziale

I modelli SIR e i modelli di incendio, pur descrivendo fenomeni fisicamente diversi, condividono la stessa struttura logica di fondo: una grandezza binaria o continua che si propaga per contatto locale su un reticolo discreto, con una soglia (deterministica o probabilistica) che decide se la propagazione avviene o si arresta. In entrambe le famiglie di modelli si ritrova:

- una nozione di *soglia critica di propagazione*, che nei modelli SIR prende la forma del numero di riproduzione di base ($R_0=\beta S(0)/\gamma$ nell'ODE, $X=vS_O^0/\varepsilon$ nel CA di White, del Rey e Sánchez [[3]](CA-doc/SIR/A%20Model%20Based%20on%20Cellular%20Automata%20to%20Simulate%20Epidemic%20Diseases.pdf), [[4]](CA-doc/SIR/Modeling%20epidemics%20using%20cellular%20automata.pdf)) e nei modelli di incendio quella del rapporto critico $f/p\to0$ dell'autorganizzazione critica, oppure della soglia di percolazione del combustibile;
- una *funzione di contagio/ignizione locale*, sempre scomponibile in un fattore di suscettibilità della cella ricevente (frazione di suscettibili $S_{ij}$, o presenza di combustibile) moltiplicato per un termine legato ai vicini "infetti"/"in fiamme", a sua volta modulato da fattori ambientali locali (densità di popolazione e connessioni di trasporto per il SIR; vento, pendenza e vegetazione per il fuoco);
- una tensione tra *modelli meccanicistici astratti*, nati per studiare un fenomeno critico in sé (i contatori di fase $t_i,t_p,t_l$ di Fuentes–Kuperman, la criticità autoorganizzata di Bak–Chen–Tang/Drossel–Schwabl) e *modelli ingegneristici via via più realistici*, calibrati o calibrabili su dati osservati (le frazioni $(S,I,R)$ di White, del Rey e Sánchez [[3]](CA-doc/SIR/A%20Model%20Based%20on%20Cellular%20Automata%20to%20Simulate%20Epidemic%20Diseases.pdf), [[4]](CA-doc/SIR/Modeling%20epidemics%20using%20cellular%20automata.pdf) con il fattore di connessione $c$, la propagazione moltiplicativa $p_{burn}$ di Alexandridis validata sull'incendio di Spetses).

Per l'implementazione in codice, questa lettura comparativa suggerisce un parallelismo diretto: il modello SIR "a contatore" di Fuentes–Kuperman [[2]](CA-doc/SIR/Cellular-automata-and-epidemiological-mo_1999_Physica-A--Statistical-Mechani.pdf), con vicinato di von Neumann e propagazione probabilistica per singolo vicino (e la sua variante stocastica dovuta a Landguth [[6]](CA-doc/SIR/A%20Cellular%20Automata%20SIR%20Model%20for%20Landscape%20Epidemiology.pdf)), e il modello di incendio a vicinato di Moore con matrice di propagazione anisotropa modulata dal vento (Karafyllidis–Thanailakis, Hernández Encinas et al., Alexandridis et al.) rappresentano, per le rispettive famiglie, il punto di equilibrio più naturale tra semplicità della regola locale e fedeltà fisica — ed è su questi due schemi che si baserà la fase successiva di implementazione.

---

## Architettura comune

- **Griglia**: quadrata `dim × dim` di interi (`int **` in C).
- **Doppia griglia (double buffering)**: l'update legge dalla griglia attiva (`initial`) e
  scrive su una griglia di appoggio (`target`); a fine passo le due griglie vengono
  scambiate lato Python (`update_generation`). Per SIR e Fire questo rende l'update
  **sincrono**: il nuovo stato di ogni cella dipende solo dalla configurazione al passo
  precedente. Il modello di Ising fa eccezione (vedi sotto).
- **Generatore pseudocasuale**: `xorshift32` (in `formulas.c`), inizializzato con `rand()`
  a ogni chiamata di update; i numeri casuali in $[0,1)$ si ottengono dividendo per 2³².
- **Connessione Python ↔ C**: `c_connector.py` carica `formulas.so`, `game.so`,
  `parameters.so` da `C_file/`; `c_type_manager.py` replica le struct dei parametri come
  `ctypes.Structure` e dichiara le firme delle funzioni usate.
- **Parametri ereditati**: tutte le struct contengono anche `max_iteration`,
  `image_proportion`, `image_step`, ereditati dal progetto originale (prisoned-in-c) per
  la generazione di immagini PPM; nel ciclo di visualizzazione Python non hanno effetto.

---

## Modello SIR (`Model_SIR_connected.py`)

Modello epidemico Susceptible–Infected–Recovered su reticolo.

### Stati
Lo stato di una cella è un **contatore intero**:

| Valore | Significato |
|---|---|
| `0` | suscettibile |
| `1 … infected_time` | infetta |
| `infected_time+1 … resistent_time` | resistente (immune) |

### Boundary e vicinato
- **Boundary periodico** (toroidale): gli indici dei vicini sono calcolati modulo `dim`.
- **Vicinato di von Neumann** (4 vicini: nord, sud, est, ovest).

### Regola di update (sincrona)
Per ogni cella:
1. **Suscettibile (0)**: per ciascuno dei 4 vicini che risulta infetto
   (`1 ≤ valore ≤ infected_time`) viene estratto un numero casuale indipendente; se
   `rand ≤ propagation_ratio` la cella diventa infetta (`target = 1`). Ogni vicino infetto
   costituisce quindi un tentativo di contagio indipendente.
2. **Contatore a fine corsa (`valore == resistent_time`)**: se `reinfected ≠ 0` la cella
   torna suscettibile (`0`), chiudendo il ciclo SIRS; altrimenti resta resistente per
   sempre (SIR puro).
3. **Altrimenti**: il contatore avanza di 1 (la cella percorre infezione e poi resistenza
   a passi deterministici).

### Inizializzazione
Griglia azzerata (`intMatrixCreator`), poi ogni cella viene posta a `1` (infetta) con
probabilità `initial_infected_ratio` (`intMatrixPopulator`).

### Parametri (default di `easySirParameters`)

| Parametro | Default | Significato |
|---|---|---|
| `dim` | 20 | lato della griglia |
| `infected_time` | 8 | durata (in passi) dell'infezione |
| `resistent_time` | 8 | soglia finale del contatore; **cumulativo**: il wrapper Python somma la durata della resistenza a `sic_time`, quindi `resistent_time = infected_time + durata resistenza` |
| `propagation_ratio` | 0.9 | probabilità di contagio per singolo vicino infetto per passo |
| `initial_infected_ratio` | 0.0002 | frazione iniziale di celle infette |
| `reinfected` | 0 | se ≠ 0 la cella a fine resistenza torna suscettibile (modello SIRS) |

---

## Modello di incendio boschivo (`Fire_connected.py`, `cellFireUpdate`)

Modello di propagazione di un incendio in una foresta, con effetto del vento.

### Stati

| Valore | Significato |
|---|---|
| `0` | terreno vuoto |
| `1` | albero |
| `2` | albero in fiamme |
| `3` | albero bruciato |

### Boundary e vicinato
- **Boundary periodico** (toroidale, indici modulo `dim`).
- **Vicinato di Moore** (8 vicini; il ciclo 3×3 include anche l'offset nullo, che però è
  ininfluente: la cella centrale, essendo un albero, non può risultare in fiamme, e la
  corrispondente entrata della matrice di propagazione è `NaN`).

### Regola di update (sincrona)
1. **Albero (1)**: per ogni vicino in fiamme (`2`) in direzione relativa *v* viene
   estratto un numero casuale; la cella prende fuoco se
   `rand ≤ propagation_matrix[v]`. La probabilità è quindi **anisotropa** e dipende
   dall'allineamento tra la direzione del vicino e il vento.
2. **In fiamme (2)**: al passo successivo diventa bruciata (`3`).
3. **Vuota (0) o bruciata (3)**: resta invariata (nessuna ricrescita).

### Effetto del vento
La matrice 3×3 `propagation_matrix` è costruita da `firePropMatrix`: per ogni direzione
*v* del vicinato si calcola il coseno dell'angolo con il vettore `wind_direction` e la
probabilità

```
P(v) = (cos θ(v, wind) · 1.22 + 1.2) · propagation_ratio
```

Il fattore varia quindi da ~−0.02 (controvento: propagazione di fatto impossibile) a 2.42
(sottovento: con `propagation_ratio` abbastanza alto la probabilità satura a 1, cioè
propagazione certa); in direzione perpendicolare al vento vale `1.2 · propagation_ratio`.

### Inizializzazione
`FireMatrixCreator` estrae **un solo** numero casuale per cella: la cella diventa albero
se `rand < initial_tree_ratio` e in fiamme se `rand < initial_burn_ratio` (le celle in
fiamme sono quindi un sottoinsieme di quelle che sarebbero state alberi; serve
`initial_burn_ratio < initial_tree_ratio`).

### Parametri (default di `easyFireParameters`)

| Parametro | Default | Significato |
|---|---|---|
| `dim` | 20 | lato della griglia |
| `propagation_ratio` | 0.5 | fattore di scala della probabilità di propagazione |
| `wind_direction` | (0, 1) | vettore 2D della direzione del vento |
| `propagation_matrix` | derivata | matrice 3×3 di probabilità direzionali (calcolata da vento e `propagation_ratio`) |
| `spontaneus_burning` | 0 | probabilità di autocombustione — **presente nella struct ma non ancora usata nella regola di update** |
| `initial_burn_ratio` | 0.005 | frazione iniziale di celle in fiamme |
| `initial_tree_ratio` | 0.7 | densità iniziale di alberi |

---

## Modello di Ising (`Ising_connected.py`, `cellIsingUpdate`)

Modello di Ising 2D con dinamica di Metropolis a singolo spin-flip.

### Stati
Spin `s = ±1`.

### Boundary e vicinato
- **Boundary selezionabile** tramite `periodic_boundary`: `1` = periodico (toroidale),
  `0` = aperto/statico (i vicini oltre il bordo semplicemente non contribuiscono alla
  somma). È l'unico dei tre modelli con boundary configurabile.
- **Vicinato di von Neumann** (4 vicini).

### Regola di update (asincrona, Metropolis)
A differenza di SIR e Fire, l'update è **asincrono**: `matrixIsingUpdate` esegue
`step_iteration` tentativi di flip per chiamata (per frame di visualizzazione), e il flip
accettato modifica subito anche la griglia `initial`, quindi i tentativi successivi vedono
la configurazione già aggiornata.

Per ogni tentativo su una cella con spin `s`:

```
ΔE = −2 · s · (coupling · Σ_vicini + magnetic_field)
```

- se `ΔE ≤ 0` il flip è accettato;
- altrimenti è accettato con probabilità `exp(−ΔE / temperature)` (test di Metropolis).

Se accettato, lo spin viene invertito su entrambe le griglie e `hamiltonian` viene
aggiornata di `ΔE`.

> **Nota sulla convenzione dei segni.** Con la definizione implementata di ΔE la dinamica
> risulta invertita rispetto alla convenzione usuale `H = −J Σ sᵢsⱼ − h Σ sᵢ` (per la
> quale ΔE = +2s(JΣ+h)): in pratica `coupling` **negativo** produce comportamento
> ferromagnetico e positivo antiferromagnetico (infatti nel `__main__` di
> `Ising_connected.py` si usa `coupling = −10`). L'energia iniziale calcolata da
> `isingMatrix` usa invece la convenzione standard, quindi il valore assoluto di
> `hamiltonian` va interpretato con cautela.

> **Nota implementativa.** In `matrixIsingUpdate` il numero casuale `intrand` viene
> generato una sola volta prima del ciclo e non rigenerato a ogni iterazione: all'interno
> di una stessa chiamata i `step_iteration` tentativi cadono quindi tutti sulla stessa
> cella `(row, col)` e usano lo stesso numero per il test di Metropolis. Cella e numero
> cambiano solo da un frame all'altro (nuovo seed da `rand()`).

### Inizializzazione
`isingMatrix` assegna spin `+1` con probabilità `initial_ratio` e `−1` altrimenti, poi
calcola l'energia iniziale `H = −J Σ sᵢsⱼ − h Σ sᵢ` (somma sulle coppie destra/basso,
con o senza avvolgimento periodico a seconda del boundary) e la salva in `hamiltonian`.

### Parametri (default di `isingParam`)

| Parametro | Default | Significato |
|---|---|---|
| `dim` | 20 | lato della griglia |
| `temperature` | 2 | temperatura T del bagno termico |
| `coupling` | 1 | costante di accoppiamento J (vedi nota sui segni) |
| `magnetic_field` | 0 | campo magnetico esterno h |
| `step_iteration` | 100 | tentativi di flip per frame |
| `initial_ratio` | 0.5 | frazione iniziale di spin +1 |
| `periodic_boundary` | 0 | 0 = boundary aperto, 1 = periodico |
| `hamiltonian` | — | variabile di stato: energia corrente del sistema |

---

## Prototipi in puro Python

Due versioni precedenti, interamente in Python/NumPy, senza backend C:

### `Model_SIR.py`
Variante SIR con **vicinato di Moore** (8 vicini) e probabilità di contagio fissa a 0.2
(`np.random.rand() > 0.8`), senza reinfezione. Il boundary è **non uniforme**: gli indici
fuori griglia positivi sollevano `IndexError` e vengono ignorati (bordo aperto in basso/a
destra), ma gli indici negativi sfruttano l'indicizzazione negativa di NumPy (bordo di
fatto periodico in alto/a sinistra).

### `wave.py`
Automa **eccitabile deterministico** in stile Greenberg–Hastings, derivato dal codice SIR:
una cella a riposo si eccita se un vicino (Moore) è sul fronte d'onda, poi decade a passi
di 1 fino a tornare a riposo; il valore massimo rilancia il ciclo. Genera fronti d'onda
che si propagano sulla griglia. Stesso boundary non uniforme di `Model_SIR.py`.

## Scelte di implementazione

### Perché servono scelte implementative concrete

La definizione formale di automa cellulare — la quadrupla $(C,Q,V,f)$ vista nell'introduzione — lascia aperti diversi gradi di libertà che i modelli teorici presentati nei capitoli precedenti non sempre fissano in modo univoco: la dimensione e la finitezza della griglia, il trattamento dei bordi, il raggio e la forma esatta del vicinato, la natura sincrona o asincrona dell'aggiornamento. Per passare dalla teoria al codice queste scelte vanno rese esplicite, in modo coerente per tutti e tre i modelli, cosicché il confronto fra di essi sia significativo.

### Come si è proceduto

In questa tesi i tre modelli (SIR, incendio boschivo, Ising) sono implementati su una griglia quadrata bidimensionale $G=\mathbb{Z}^2$, con vicinato di raggio 1 di tipo von Neumann (4 vicini, distanza di Manhattan) o Moore (8 vicini, distanza di Chebyshev) a seconda del modello. Per ciascun modello la griglia può essere trattata come *finita* — le celle di bordo e d'angolo hanno un vicinato incompleto, limitato alle sole celle interne alla griglia — oppure come *toroidale*, un'approssimazione pratica dell'infinitezza in cui il vicinato "avvolge" la griglia sui lati opposti, cosicché ogni cella (bordi e angoli inclusi) abbia sempre un vicinato completo.

La logica di evoluzione dei tre modelli è scritta in C (compilata in librerie condivise) e pilotata da Python tramite `ctypes`, con visualizzazione in `pygame`. L'aggiornamento della griglia avviene per la maggior parte dei modelli con un doppio buffer: la regola legge dalla griglia al passo corrente e scrive su una griglia di appoggio, scambiate a fine passo, così da garantire un aggiornamento *sincrono* in cui il nuovo stato di ogni cella dipende solo dalla configurazione al passo precedente. Il generatore di numeri pseudocasuali usato per le componenti probabilistiche delle regole è un `xorshift32`.

### Metodi scelti in questo lavoro

**Modello SIR.** Lo stato di cella è un contatore intero: `0` indica un individuo suscettibile, i valori successivi la progressione attraverso l'infezione e poi la resistenza, fino a una soglia finale oltre la quale la cella torna suscettibile (variante SIRS) o resta immune per sempre (SIR puro). Il vicinato è di von Neumann su griglia toroidale; una cella suscettibile diventa infetta con una prova di contagio indipendente per ciascun vicino infetto, ciascuna con probabilità fissa. È, nella sostanza, una versione semplificata dell'idea di contatore di fase di Fuentes–Kuperman, qui applicata a un vicinato più ristretto e con propagazione probabilistica per singolo vicino anziché tramite un campo di vicinato aggregato.

**Modello di incendio boschivo.** Lo stato di cella è discreto su quattro valori (vuoto, albero, albero in fiamme, albero bruciato), su vicinato di Moore e griglia toroidale. Un albero prende fuoco con una probabilità che dipende, per ciascun vicino in fiamme, dall'allineamento tra la sua direzione relativa e la direzione del vento (probabilità massima sottovento, pressoché nulla controvento); un albero in fiamme diventa bruciato al passo successivo, senza ricrescita. Lo schema riprende così, in forma discreta e probabilistica, l'idea di matrice di propagazione anisotropa modulata dal vento introdotta da Karafyllidis–Thanailakis e ripresa da Alexandridis et al., senza includere pendenza, tipo di vegetazione o spotting.

**Modello di Ising.** Lo stato di cella è uno spin $\pm1$ su vicinato di von Neumann, con boundary selezionabile (periodico o aperto). A differenza degli altri due modelli, l'aggiornamento è *asincrono*: a ogni passo viene tentato il flip di una singola cella scelta a caso, accettato secondo il criterio di Metropolis (sempre se l'energia diminuisce, altrimenti con probabilità $e^{-\Delta E/T}$) — la stessa dinamica presa come termine di paragone classico nel capitolo precedente, piuttosto che una delle regole deterministiche a scacchiera (Q2R, demoni di Creutz) discusse in teoria. È una scelta implementativa consapevole: Metropolis è l'algoritmo di riferimento più semplice da realizzare correttamente ed è quello rispetto a cui gli altri schemi vengono giudicati.

Accanto a queste tre implementazioni in C, sono stati realizzati anche due prototipi preliminari in solo Python/NumPy: una prima variante del modello SIR con vicinato di Moore e probabilità di contagio fissa, e un automa eccitabile deterministico in stile Greenberg–Hastings che genera fronti d'onda propagantisi sulla griglia — utili come banco di prova concettuale prima del passaggio all'implementazione in C.

---
