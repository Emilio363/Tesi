# Automi cellulari per la propagazione spaziale e per la fisica statistica: modelli SIR, incendi boschivi e modello di Ising — un'introduzione teorica

## Introduzione generale ai CA

Il concetto di automa cellulare nasce nei primi anni '50 dal lavoro di John von Neumann, allora alla ricerca di un'organizzazione logica capace di generare strutture autoreplicanti. Uno spazio cellulare discreto, con regole locali identiche per ogni cella, permette di isolare l'essenza logica del problema e di sfruttare il parallelismo computazionale. Su una griglia von Neumann dimostrò che è possibile costruire automi capaci sia di *computazione universale* (equivalenti a una macchina di Turing) sia di *costruzione universale* (in grado, cioè, di autoreplicarsi). Negli anni '70 John Conway rende celebre il campo con il "Game of Life", un automa bidimensionale a regole minime, Turing-completo, capace di generare comportamento complesso ed emergente; negli anni '80 Stephen Wolfram propone una classificazione sistematica degli automi cellulari in quattro classi di comportamento asintotico, basata sulla complessità a lungo termine della dinamica.

Un automa cellulare (CA, *Cellular Automata*) è un sistema dinamico discreto in spazio, tempo e stati. Gli stati sono trattati come grandezze discrete, a differenza dei modelli basati su equazioni differenziali continue. È costituito da un numero finito di oggetti identici, chiamati *celle*, disposte in uno *spazio cellulare*; ogni cella è dotata di uno *stato* (elemento di un insieme finito) che evolve a passi discreti nel tempo secondo una *regola di transizione locale*, identica per ogni cella e applicata simultaneamente a tutta la griglia. Lo stato di una cella al istante $t$ dipende dagli stati delle celle del suo *vicinato* all'istante precedente $t-1$. Formalmente un automa cellulare è un sistema definito dalla quadrupla $(C, Q, V, f)$ [[3]](CA-doc/SIR/A%20Model%20Based%20on%20Cellular%20Automata%20to%20Simulate%20Epidemic%20Diseases.pdf):

1.  **$C$ Spazio cellulare :** Uno spazio discreto, solitamente una griglia $d$-dimensionale composta da celle identiche.
2.  **$Q$ Insieme degli stati:** Ogni cella può trovarsi in uno tra un numero finito di stati possibili.
3.  **$V$ Vicinato:** Per ogni cella, definisce l'insieme di celle vicine che influenzano il suo stato futuro.
4.  **$f$ Regola di transizione locale:** Una funzione che determina lo stato di una cella al passo temporale successivo in base allo stato attuale della cella stessa e dei suoi vicini.

Si indichi con $i$ una cella di un CA; lo stato della cella $i$ al tempo $t$ viene indicato con $\sigma_i(t)$. Possiamo quindi in generale definire la regola di update dello stato di una cella come:
$$\sigma_i(t+1) = f(\{\sigma_j(t) \mid j \in U(i)\})$$
dove $U(i)$ rappresenta il vicinato della cella $i$. 

Questa struttura permette di modellare una vasta gamma di fenomeni, dalla propagazione di eccitazioni nei tessuti cardiaci alla fluidodinamica (tramite i metodi *Lattice Boltzmann*), fornendo uno strumento che cattura l'essenza della complessità naturale con una minima perdita di informazioni locali.

### Automi Cellulari 2-dimensionali

Per gli scopi di questa tesi sono stati studiati gli automi cellulari a 2-dimensioni su griglia. In questo caso la definizione dell'automa diventa più rigida:

- $C = \{(\alpha,\beta) \in \mathbb{Z}^2 : 1 \le \alpha \le r, 1 \le \beta \le c\}$ è la griglia (o spazio cellulare), un reticolo finito di $r \times c$ celle
- $Q$ è l'insieme finito degli stati, a questo viene associata una funzione $\sigma: S \times N \rightarrow Q$ che ad ogni cella in un determinato istante di tempo associa un certo stato
- $V = \{(i_k, j_k) : 1 \le k \le n\} \subset \mathbb{Z} \times \mathbb{Z}$, dove $n$ è il numero di vicini di ogni cella. $V$ è un insieme di coordinate relative, dove ogni valore può essere sia positivo che negativo. In questa maniera viene definito un vicinato che ha una forma uguale e centrata sulla cella della quale si vuole conoscere il vicinato:
$$
V_{\alpha, \beta} = \{(\alpha+i_k, \beta+j_k)\; |\;\forall\; (i_k, j_k) \in V \};
$$
- $f : Q^n \to Q$ è la funzione di transizione locale, identica per ogni cella. Indichiamo con $s_{\alpha\beta}^{\,t}$ lo stato della cella $(\alpha,\beta)$ al istante $t$: 
$$
s_{\alpha\beta}^{t+1} = f\left(V_{\alpha, \beta}\right) \in Q$$

### Condizioni ai limiti della griglia

Quando si simula o si analizza un automa cellulare su un computer, ci si scontra inevitabilmente con il limite fisico della finitudine della griglia. Le celle situate lungo i bordi (o la periferia) dello spazio non possiedono lo stesso numero di vicini rispetto alle celle posizionate al centro. Per risolvere questa asimmetria e stabilire come debbano comportarsi le celle di confine, si applicano le condizioni al contorno (o condizioni al limite).
Poiché $C$ è finito, la definizione del vicinato di $(\alpha,\beta)$ non sempre è ben determinata. Infatti si potrebbe incontare dei punti che eccedono la griglia prefissata $(\alpha,\beta)+(i_k,j_k) \notin C$. Ciò richiede di fissare esplicitamente una condizione al contorno.La scelta di queste condizioni influisce profondamente sulla dinamica globale dell'automa e si divide principalmente in due approcci.

#### Condizioni al Contorno Non Periodiche

L'approccio più semplice che possiamo trovare è il troncamento del vicinato. Questo si può intendere in due maniere:
- **Troncamnento:** le coordinate che non corrispondono a una cella del reticolo, non vengono considerate dalla regola di transizione locale per la cella al centro. Questo costringe però alla non unicità della regola di transizione, dando alle celle al contorno dei comportamenti anomali.
- **Stato neutro:** per le coordinate che non appartengono alla griglia, si assume uno stato di default. Questo permette di mantenere una regola di transizione uguale per tutte le celle, ma le celle ai bordi avranno un comportamento fortemente influenzato dallo stato di default, dando quindi comunque un comportamento anomalo rispetto alle celle più interne.

|   |   |   |   |   |   |
|:-:|:-:|:-:|:-:|:-:|:-:|
|   |   |   |   |   |   |
|   |   |   |   |   |   |
|   |   |   |   |   |   |
|   |   |   |   |   |   |
|   |   |   |   | ■ | ■ |
|   |   |   |   | ■ | **C** |

#### Condizioni al Contorno Periodiche

Molti problemi che possono essere affrontati con un CA richiedono di lavorare su un ambiente infinito, ma per definizione i CA sono finiti. Per approssimare un reticolo infinito si usano dei viciniati periodici che permettono di mantenere la finitezza del modello. Questo risultato si ottiene connettendo idealmente i bordi opposti della griglia in modo che non vi sia alcuna interruzione spaziale. Rappresentando graficamente quello che avvine in una griglia 2D, si può immaginare di unire il bordo destro e sinistro (ottenendo un cilindro) e poi unendo il bordo superiore ed inferiore. In questa maniera possiamo vedere come il modello adesso sia diventato un toroide.

Così facendo si ottiene che tutti i nodi risultano equivalenti dal punto di vista della dimensione del vicinato, ed ogni cella del vicinato è mutevole nello stato. Inoltre abbiamo un essenziale passaggio di informazione tra i vari limiti del modello

|   |   |   |   |   |   |
|-|-|:-:|:-:|:-:|:-:|
| ■ |   |   |   | ■ | ■ |
|   |   |   |   |   |   |
|   |   |   |   |   |   |
|   |   |   |   |   |   |
| ■ |   |   |   | ■ | ■ |
| ■ |   |   |   | ■ | **C** |

### Tipi di vicinato

Un fattore fondamentale nello sviluppo degli automi cellulari è il vicinato. questo infatti determina quali celle influenzino la cella che si sta osservando. Un vicinato più ampio fa in modo che la cella ottenda più informazioni dal contesto e quindi osserveremo maggiormente effetti macroscopici. Riducendo il vicinato invece accentueremo l'emergenza di fenomeni locali.

Le due geometrie base per gli intorni, parametrizzate da un raggio di influenza $r \ge 1$, sono definite matematicamente in $\mathbb{Z}^d$. Quando queste definizioni generali vengono proiettate su una griglia bidimensionale classica di celle quadrate $d=2$ con raggio unitario $r = 1$, si ottengono le forme geometriche standard più utilizzate nelle simulazioni.

#### Intorno di Moore

Raccoglie tutte le celle $y$ la cui distanza dalla cella centrale $c$, misurata tramite la norma dell'infinito (o norma di Chebyshev, $\|\cdot\|_\infty$), è inferiore o uguale a $r$:

$$V_c = \{y \in \mathbb{Z}^d : \|y - c\|_\infty \le r\}$$

Questa norma definisce la distanza massima lungo una singola coordinata cartesiana. Geometricamente, l'intorno risultante forma un ipercubo $d$-dimensionale centrato in $c$ che include tutte le celle adiacenti sia per lato sia diagonalmente.

Passando alle 2 dimensioni, possiamo esprimere $c= (\alpha, \beta)$ ed $y = (i,j).$
Applicando la definizione con la norma $\|\cdot\|_\infty \le 1$, la condizione di adiacenza si traduce nel controllo simultaneo sulle due dimensioni:

$$|\alpha - i| \le 1 \quad \text{e} \quad |\beta - j| \le 1$$

Questo intorno racchiude la cella centrale, i quattro vicini cardinali e i quattro vicini diagonali, per un totale di 9 celle:

$$V_{\alpha, \beta} = \{s_{\alpha, \beta}, s_{\alpha-1, \beta}, s_{\alpha-1, \beta-1}, s_{\alpha, \beta-1}, s_{\alpha+1, \beta-1}, s_{\alpha+1, \beta}, s_{\alpha+1, \beta+1}, s_{\alpha, \beta+1}, s_{\alpha-1, \beta+1}\}$$

Geometricamente, l'intorno corrisponde a un quadrato compatto di $3 \times 3$ celle incentrato sulla cella da aggiornare.

  |   |   |   |
  |:-:|:-:|:-:|
  | ■ | ■ | ■ |
  | ■ | **C** | ■ |
  | ■ | ■ | ■ |


#### Intorno di von Neumann

Raccoglie tutte le celle $y$ la cui distanza dalla cella centrale $c$, misurata tramite la norma $L_1$ (norma di Manhattan, $\|\cdot\|_1$), è inferiore o uguale a $r$: 

$$V_c = \{y \in \mathbb{Z}^d : \|y - c\|_1 \le r\}$$

Questa norma somma le distanze assolute lungo ciascuna coordinata cartesiana. L'intorno risultante forma un iperottaedro (una sorta di rombo multidimensionale) centrato in $c$ che esclude le celle raggiungibili solo muovendosi in diagonale.

Passando alle 2 dimensioni, possiamo esprimere $c= (\alpha, \beta)$ ed $y = (i,j).$
Applicando la definizione con la norma $\|\cdot\|_1 \le 1$, la condizione di adiacenza diventa:

$$|\alpha -i | + |\beta -j| \le 1$$

Questo intorno comprende la cella centrale stessa e i suoi quattro vicini immediati situati nelle direzioni cardinali (Nord, Sud, Est, Ovest), per un totale di 5 celle:

$$V_{\alpha, \beta} = \{s_{\alpha, \beta}, s_{\alpha-1, \beta}, s_{\alpha, \beta-1}, s_{\alpha+1, \beta}, s_{\alpha, \beta+1}\}$$

Visivamente, questa configurazione disegna una croce simmetrica sulla griglia.

  |   |   |   |
  |:-:|:-:|:-:|
  |   | ■ |   |
  | ■ | **C** | ■ |
  |   | ■ |   |


## SIR

### Perché esiste il problema e breve contesto storico

Il modello SIR e le sue varianti nascono per simulare la propagazione spaziale delle malattie infettive in una popolazione. Il punto di partenza moderno è il lavoro di Kermack e McKendrick (1927), che introduce i cosiddetti modelli *compartimentali* [1], [[4]](CA-doc/SIR/Modeling%20epidemics%20using%20cellular%20automata.pdf). Nel modello **SIR** la popolazione è suddivisa in tre classi [[3]](CA-doc/SIR/A%20Model%20Based%20on%20Cellular%20Automata%20to%20Simulate%20Epidemic%20Diseases.pdf), [[4]](CA-doc/SIR/Modeling%20epidemics%20using%20cellular%20automata.pdf):

- **suscettibili** $S$ — gli individui che possono contrarre la malattia;
- **infetti** $I$ — gli individui in grado di trasmettere la malattia;
- **rimossi/guariti** $R$ — gli individui immuni, guariti in modo definitivo o deceduti.

Il modello SIR si applica alle malattie che conferiscono immunità: il ciclo di un individuo tipico attraversa in sequenza gli stati $S \to I \to R$ [[2]](CA-doc/SIR/Cellular-automata-and-epidemiological-mo_1999_Physica-A--Statistical-Mechani.pdf). La sua formulazione classica, di tipo deterministico, è un sistema di equazioni differenziali ordinarie (ODE):

$$
\frac{dS}{dt} = -\beta\, S I,
\qquad
\frac{dI}{dt} = \beta\, S I - \gamma I,
\qquad
\frac{dR}{dt} = \gamma I,
$$

dove $\beta$ è il tasso di contagio effettivo e $\gamma$ il tasso di guarigione. Poiché la popolazione totale è costante, vale in ogni istante il vincolo

$$
S(t) + I(t) + R(t) = N = \text{cost.}
$$

Una grandezza cruciale, che ricorrerà in forme diverse anche nei modelli ad automi cellulari, è il **numero di riproduzione di base** $R_0 = \beta S(0)/\gamma$, che rappresenta il numero medio di contagi secondari prodotti da un singolo infetto in una popolazione interamente suscettibile: la soglia epidemica è $R_0=1$ (se $R_0<1$ l'epidemia si estingue, se $R_0>1$ si diffonde) [1].

Varianti dello schema si ottengono modificando la partizione della popolazione: il modello **SIS** (nessuna immunità, l'individuo torna suscettibile: $S \to I \to S$) elimina la classe $R$; il modello **SEIR** introduce una classe di *esposti* $E$ per il periodo latente (infetto ma non ancora infettivo); esistono inoltre gli schemi **SIRS**, **SEIRS**, ecc. [[3]](CA-doc/SIR/A%20Model%20Based%20on%20Cellular%20Automata%20to%20Simulate%20Epidemic%20Diseases.pdf), [[4]](CA-doc/SIR/Modeling%20epidemics%20using%20cellular%20automata.pdf).

### Come si può affrontare il problema

I modelli basati su ODE, pur eleganti, presentano limiti importanti perché trascurano le caratteristiche *locali* del processo di diffusione. In particolare non riescono a simulare in modo adeguato [[4]](CA-doc/SIR/Modeling%20epidemics%20using%20cellular%20automata.pdf):

1. i processi di contatto tra i singoli individui;
2. gli effetti del comportamento individuale;
3. gli aspetti *spaziali* della diffusione epidemica;
4. gli effetti dei pattern di mescolamento (*mixing*) della popolazione.

D'altra parte, proprio perché la popolazione totale resta costante nel tempo ($S+I+R=N$), lo stato epidemiologico di ciascun individuo — o di ciascuna porzione di territorio — può essere naturalmente rappresentato come un elemento di un insieme finito di stati che evolve secondo una regola locale: è esattamente la struttura di un automa cellulare. Gli **automi cellulari** permettono così di superare i limiti dei modelli ODE mantenendo un costo computazionale nettamente inferiore rispetto all'integrazione di sistemi di equazioni differenziali, e includendo in modo diretto caratteristiche epidemiologiche come la presenza di un agente esterno o le diverse fasi del periodo infettivo [[2]](CA-doc/SIR/Cellular-automata-and-epidemiological-mo_1999_Physica-A--Statistical-Mechani.pdf), [[4]](CA-doc/SIR/Modeling%20epidemics%20using%20cellular%20automata.pdf). Di seguito le formule dei modelli CA-SIR presi in esame.

### Metodi studiati in questo lavoro

#### Fuentes–Kuperman

Fuentes e Kuperman propongono un CA che riproduce gli stessi termini presenti nelle equazioni SIS/SIR classiche, ma in un "linguaggio" differente [[2]](CA-doc/SIR/Cellular-automata-and-epidemiological-mo_1999_Physica-A--Statistical-Mechani.pdf). Ogni cella della griglia rappresenta un singolo individuo, il cui stato è determinato univocamente da **due campi** [[2]](CA-doc/SIR/Cellular-automata-and-epidemiological-mo_1999_Physica-A--Statistical-Mechani.pdf):

- $\sigma_{ij}(t)$ — legato allo **stato epidemiologico** dell'individuo (funge da *contatore* dell'avanzamento nel periodo infettivo);
- $u_{ij}(t)$ — legato allo stato del **vicinato**, ossia alla probabilità di transizione dallo stato attuale a un altro (il termine che porta l'informazione di contatto/contagio).

##### Le tre fasi del periodo infettivo: $t_i$, $t_p$, $t_l$

La caratteristica distintiva del modello è la **suddivisione del periodo infettivo in tre fasi** [[2]](CA-doc/SIR/Cellular-automata-and-epidemiological-mo_1999_Physica-A--Statistical-Mechani.pdf). Ogni volta che un individuo viene infettato, egli attraversa in successione queste tre fasi, permanendo mediamente in ciascuna per un tempo caratteristico definito [[2]](CA-doc/SIR/Cellular-automata-and-epidemiological-mo_1999_Physica-A--Statistical-Mechani.pdf):

| Fase | Tempo caratteristico | Descrizione | Infettivo? | Sintomatico? |
|------|:---:|-------------|:---:|:---:|
| **Incubazione** | $t_i$ | l'individuo è già infetto e **infettivo**, ma non presenta ancora sintomi | sì | no |
| **Infezione propria** | $t_p$ | l'individuo è **infettivo** e mostra i sintomi | sì | sì |
| **Latenza** | $t_l$ | l'individuo **non è più infettivo** ma presenta ancora i sintomi | no | sì |

Questa formulazione è generale: ponendo $t_i = 0$ o $t_l = 0$ si possono includere in modo naturale i casi in cui l'incubazione o la latenza sono trascurabili [[2]](CA-doc/SIR/Cellular-automata-and-epidemiological-mo_1999_Physica-A--Statistical-Mechani.pdf). Dal punto di vista epidemiologico, la fase di latenza agisce di fatto come una breve *immunità temporanea*, che riduce la densità media stazionaria di infetti a parità degli altri parametri [[2]](CA-doc/SIR/Cellular-automata-and-epidemiological-mo_1999_Physica-A--Statistical-Mechani.pdf).

Il contatore $\sigma_{ij}(t)$ percorre dunque l'intero periodo infettivo, di durata complessiva

$$
T = t_i + t_p + t_l .
$$

##### Le regole di evoluzione

Nel caso base (senza immunità permanente), le regole che governano l'evoluzione del campo $\sigma_{ij}$ sono [[2]](CA-doc/SIR/Cellular-automata-and-epidemiological-mo_1999_Physica-A--Statistical-Mechani.pdf):

$$
\sigma_{ij}(t+1) =
\begin{cases}
\sigma_{ij}(t) + 1, & \text{se } 0 < \sigma_{ij}(t) < t_i + t_p + t_l, $$4pt]
0, & \text{se } \sigma_{ij}(t) = t_i + t_p + t_l, $$4pt]
0, & \text{se } \sigma_{ij}(t) = 0 \ \text{ e } \ u_{ij}(t+1) < h, $$4pt]
1, & \text{se } \sigma_{ij}(t) = 0 \ \text{ e } \ u_{ij}(t+1) \ge h,
\end{cases}
$$

dove [[2]](CA-doc/SIR/Cellular-automata-and-epidemiological-mo_1999_Physica-A--Statistical-Mechani.pdf):

- la **prima riga** fa avanzare di uno il contatore per un individuo che si trova all'interno del periodo infettivo (progressione automatica attraverso le tre fasi $t_i \to t_p \to t_l$);
- la **seconda riga** riporta a $0$ (guarigione) l'individuo che ha completato l'intero periodo $T$;
- la **terza e quarta riga** governano il **contagio** di un individuo suscettibile ($\sigma_{ij} = 0$): esso diventa infetto ($\sigma_{ij} = 1$) solo se il campo di vicinato $u_{ij}$ supera una **soglia casuale** $h$, dove $h$ è un numero aleatorio nell'intervallo $[0,1]$ con distribuzione di probabilità $p(h)$ definita caso per caso.

##### Il campo di vicinato $u_{ij}$

Il campo $u_{ij}(t)$ raccoglie l'influenza infettiva proveniente dai vicini, pesata in funzione della distanza per "gusci" (shell) successivi [[2]](CA-doc/SIR/Cellular-automata-and-epidemiological-mo_1999_Physica-A--Statistical-Mechani.pdf):

$$
u_{ij}(t+1) = \frac{1}{N}\left(
\sum_{\text{1° vicini}} I_{ij}(t)\, e^{-1}
+ \sum_{\text{2° vicini}} I_{ij}(t)\, e^{-2}
+ \sum_{\text{3° vicini}} I_{ij}(t)\, e^{-3}
+ \cdots
\right),
$$

dove i termini successivi corrispondono alle somme sui vicini di primo, secondo, terzo ordine e così via, con peso esponenziale decrescente $e^{-k}$ per il $k$-esimo guscio [[2]](CA-doc/SIR/Cellular-automata-and-epidemiological-mo_1999_Physica-A--Statistical-Mechani.pdf). La costante di normalizzazione è

$$
N = \frac{1}{4}\left(e^{-1} + e^{-2} + e^{-3} + \cdots\right).
$$

Il contributo infettivo di ciascuna cella è a sua volta determinato dalla funzione $F$ [[2]](CA-doc/SIR/Cellular-automata-and-epidemiological-mo_1999_Physica-A--Statistical-Mechani.pdf):

$$
I_{ij}(t+1) =
\begin{cases}
F\!\left(\sigma_{ij}(t)\right), & \text{se } \sigma_{ij}(t) \ge 1, $$4pt]
0, & \text{se } \sigma_{ij}(t) \le 0,
\end{cases}
$$

dove $F(t): (0,\, t_i + t_p + t_l) \to \mathbb{R}^+$ è una funzione reale positiva, nulla al di fuori dell'intervallo del periodo infettivo, che rappresenta l'**infettività** in funzione della fase raggiunta [[2]](CA-doc/SIR/Cellular-automata-and-epidemiological-mo_1999_Physica-A--Statistical-Mechani.pdf). La scelta più semplice è una funzione a gradini (di tipo Heaviside) che assume un valore costante in ciascuna delle tre fasi [[2]](CA-doc/SIR/Cellular-automata-and-epidemiological-mo_1999_Physica-A--Statistical-Mechani.pdf):

$$
F\!\left(\sigma_{ij}(t)\right) =
\begin{cases}
f_i, & \text{se } 0 < \sigma_{ij}(t) \le t_i \quad \text{(incubazione)}, $$4pt]
f_p, & \text{se } t_i < \sigma_{ij}(t) \le t_i + t_p \quad \text{(infezione propria)}, $$4pt]
f_l, & \text{se } t_i + t_p < \sigma_{ij}(t) \le t_i + t_p + t_l \quad \text{(latenza)}.
\end{cases}
$$

Regolando $f_i$, $f_p$ e $f_l$ (ad esempio ponendo $f_l = 0$ per rendere la latenza non infettiva) si modula il grado di contagiosità in ciascuna fase, calibrando così il modello sulle caratteristiche della specifica malattia [[2]](CA-doc/SIR/Cellular-automata-and-epidemiological-mo_1999_Physica-A--Statistical-Mechani.pdf).

##### Varianti SIS, SIR e SIRS

Il modello incorpora in modo unificato le diverse tipologie epidemiche tramite un periodo di immunità di durata $t_r$, estendendo il contatore a valori negativi [[2]](CA-doc/SIR/Cellular-automata-and-epidemiological-mo_1999_Physica-A--Statistical-Mechani.pdf):

$$
\sigma_{ij}(t+1) =
\begin{cases}
\sigma_{ij}(t) + 1, & \text{se } 0 < \sigma_{ij}(t) < t_i + t_p + t_l, $$4pt]
-1, & \text{se } \sigma_{ij}(t) = t_i + t_p + t_l, $$4pt]
\sigma_{ij}(t) - 1, & \text{se } -t_r \le \sigma_{ij}(t) < 0, $$4pt]
0, & \text{se } \sigma_{ij}(t) < -t_r, $$4pt]
0, & \text{se } \sigma_{ij}(t) = 0 \ \text{ e } \ u_{ij}(t+1) < h, $$4pt]
1, & \text{se } \sigma_{ij}(t) = 0 \ \text{ e } \ u_{ij}(t+1) \ge h.
\end{cases}
$$

I valori negativi del contatore rappresentano il periodo di immunità. Da questo schema generale si ottengono i casi particolari [[2]](CA-doc/SIR/Cellular-automata-and-epidemiological-mo_1999_Physica-A--Statistical-Mechani.pdf):

- $t_r \to \infty$: immunità permanente $\Rightarrow$ modello **SIR**;
- $t_r = 0$: nessuna immunità $\Rightarrow$ modello **SIS**;
- $t_r \ne 0$ (finito): immunità temporanea $\Rightarrow$ modello **SIRS**.

Le simulazioni mostrano l'esistenza di un **valore di soglia critico** $f_c$ per il parametro di infettività: al di sotto di $f_c$ l'infezione non riesce a sostenersi e l'epidemia si estingue, mentre al di sopra si raggiunge una densità media stazionaria di infetti [[2]](CA-doc/SIR/Cellular-automata-and-epidemiological-mo_1999_Physica-A--Statistical-Mechani.pdf). In prossimità della soglia, la densità asintotica $I_a$ segue una legge di potenza di tipo critico [[2]](CA-doc/SIR/Cellular-automata-and-epidemiological-mo_1999_Physica-A--Statistical-Mechani.pdf):

$$
I_a = A\,\lvert f - f_c \rvert^{\nu},
$$

analoga a una transizione di fase.

Va segnalato che il modello, così come proposto da Fuentes e Kuperman, non formalizza una variante **SEIR** a sé stante tramite $t_r$: la fase di incubazione $t_i$ descrive già un individuo infetto ma non ancora sintomatico, che nello schema resta però **infettivo** — a differenza della classe "esposta" $E$ dei modelli SEIR classici, che per definizione non è infettiva. Un'eventuale variante SEIR richiederebbe quindi l'aggiunta di una quarta fase, non infettiva, precedente a $t_i$.

#### Spreadability (Slimi–El Yacoubi)

Un secondo approccio, dovuto a Slimi e El Yacoubi, affronta la diffusione epidemica come caso particolare di un fenomeno più generale di **propagazione spaziale** (*spreadability*): l'espansione nel tempo di una proprietà spaziale $\mathcal{P}$ (una copertura vegetale, un'area di inquinamento o, appunto, una zona di popolazione infetta) [[5]](CA-doc/SIR/Spreadable%20Probabilistic%20Cellular%20Automata%20Models%3A%20An%20Application%20in%20Epidemiology.pdf). Mentre il concetto era stato inizialmente studiato con equazioni alle derivate parziali (PDE), qui viene formulato tramite un automa cellulare **probabilistico**, ritenuto più realistico [[5]](CA-doc/SIR/Spreadable%20Probabilistic%20Cellular%20Automata%20Models%3A%20An%20Application%20in%20Epidemiology.pdf).

Il CA è definito dalla quadrupla $(L, S, f, N)$, dove $L$ è il reticolo, $S$ l'insieme degli stati, $f$ la funzione di transizione e $N$ il vicinato; lo stato della cella $c$ al tempo $t$ è indicato $s_t(c) \in S$ [[5]](CA-doc/SIR/Spreadable%20Probabilistic%20Cellular%20Automata%20Models%3A%20An%20Application%20in%20Epidemiology.pdf).

##### L'indicatore $\pi(s)$ e il dominio $\Omega$

Alla proprietà $\mathcal{P}$ si associa una mappa indicatrice $\pi$ [[5]](CA-doc/SIR/Spreadable%20Probabilistic%20Cellular%20Automata%20Models%3A%20An%20Application%20in%20Epidemiology.pdf):

$$
\pi: S \longrightarrow \{0,1\}, \qquad
\pi(x) =
\begin{cases}
1, & \text{se } x \text{ soddisfa } \mathcal{P}, \\
0, & \text{altrimenti,}
\end{cases}
$$

il cui supporto è $K = \{x \in S \mid \pi(x) = 1\}$. Data una proprietà spaziale $\mathcal{P}$, si definisce quindi la successione di **domini** in cui $\mathcal{P}$ è soddisfatta al tempo $t$ [[5]](CA-doc/SIR/Spreadable%20Probabilistic%20Cellular%20Automata%20Models%3A%20An%20Application%20in%20Epidemiology.pdf):

$$
\Omega_t = \{c \in L \mid \mathcal{P}\, s_t(c)\} = \{c \in L \mid s_t(c) \in K\}.
$$

Il CA si dice **$\mathcal{P}$-spreadable** a partire da un dominio iniziale $\Omega_0$ se la successione dei domini è *crescente* [[5]](CA-doc/SIR/Spreadable%20Probabilistic%20Cellular%20Automata%20Models%3A%20An%20Application%20in%20Epidemiology.pdf):

$$
\Omega_t \subseteq \Omega_{t+1}.
$$

##### Vicinato $N(c)$ e densità locale $p(c)$

L'impatto dell'ambiente locale è misurato dalla **densità locale** della proprietà nel vicinato di $c$ [[5]](CA-doc/SIR/Spreadable%20Probabilistic%20Cellular%20Automata%20Models%3A%20An%20Application%20in%20Epidemiology.pdf):

$$
y_t(c) = \sum_{c' \in \dot{N}(c)} \pi\!\left(s_t(c')\right),
\qquad
p_t(c) = \frac{y_t(c)}{n},
$$

dove $n = |N(c)|$ è la dimensione del vicinato, $\dot{N}(c) = N(c) \setminus \{c\}$ il vicinato privato della cella centrale, e $y_t(c)$ conta quanti vicini di $c$ soddisfano $\mathcal{P}$ al tempo $t$.

##### Nascita $\nu(p)$ e sopravvivenza $\sigma$

La dinamica è governata da due funzioni probabilistiche, entrambe espresse in funzione della densità locale $p_t(c)$ [[5]](CA-doc/SIR/Spreadable%20Probabilistic%20Cellular%20Automata%20Models%3A%20An%20Application%20in%20Epidemiology.pdf):

**Funzione di nascita** $\nu$ — regola la comparsa della proprietà in una cella che ancora non la possiede, in base a ciò che accade attorno:

$$
\nu(p) =
\begin{cases}
1, & \text{se } p \ge \theta_1 \ \text{ con probabilità } p_1, \\
0, & \text{altrimenti,}
\end{cases}
$$

dove $0 \le \theta_1 \le 1$ è la **soglia di nascita** e $p_1$ la probabilità associata.

**Funzione di sopravvivenza** $\sigma: K \to K$ — regola il mantenimento della proprietà in una cella che già la possiede. Nella versione probabilistica è definita anch'essa tramite una soglia sulla densità locale [[5]](CA-doc/SIR/Spreadable%20Probabilistic%20Cellular%20Automata%20Models%3A%20An%20Application%20in%20Epidemiology.pdf):

$$
\sigma\!\left(s_t(c)\right) \in
\begin{cases}
K, & \text{se } p_t(c) - \frac{1}{n} \ge \theta_2 \ \text{ con probabilità } p_2, \\
K^{c}, & \text{altrimenti.}
\end{cases}
$$

##### La regola generica $\delta_1$, $\delta_2$

Combinando nascita e sopravvivenza, la regola di transizione locale assume la forma unificata [[5]](CA-doc/SIR/Spreadable%20Probabilistic%20Cellular%20Automata%20Models%3A%20An%20Application%20in%20Epidemiology.pdf):

$$
s_{t+1}(c) = \Big(\delta_1(x)\, \nu(p) + \delta_2(x)\, \big(1 - \nu(p)\big)\Big)\big(1 - \pi(x)\big) + \sigma(x)\, \pi(x),
$$

dove $x = s_t(c)$, $p = p_t(c)$, e $\delta_1: S \to K$, $\delta_2: S \to K^{c}$ sono due mappe arbitrarie. Il primo addendo agisce sulle celle che *non* soddisfano ancora $\mathcal{P}$ (fattore $1 - \pi(x)$), governandone la possibile *nascita*; il secondo addendo agisce sulle celle che *già* soddisfano $\mathcal{P}$ (fattore $\pi(x)$), governandone la *sopravvivenza*. Se al tempo $t_0$ la configurazione soddisfa $\mathcal{P}$, la successione dei domini diventa, per costruzione, crescente [[5]](CA-doc/SIR/Spreadable%20Probabilistic%20Cellular%20Automata%20Models%3A%20An%20Application%20in%20Epidemiology.pdf):

$$
\Omega_{t+1} = \Omega_t \cup \{c \in \Omega_t^{c} \mid \nu(p_t(c)) = 1\}.
$$

##### Applicazione epidemiologica: un modello SIR probabilistico

Il formalismo si specializza a un modello **SIR** in cui ogni sito del reticolo $L \times L$ è occupato da un individuo il cui stato assume tre valori [[5]](CA-doc/SIR/Spreadable%20Probabilistic%20Cellular%20Automata%20Models%3A%20An%20Application%20in%20Epidemiology.pdf):

$$
s_t(c) \in \{0,\ 1,\ 2\} = \{\text{suscettibile},\ \text{infetto},\ \text{guarito}\}.
$$

Le transizioni avvengono con date probabilità, secondo le tre regole di interazione [[5]](CA-doc/SIR/Spreadable%20Probabilistic%20Cellular%20Automata%20Models%3A%20An%20Application%20in%20Epidemiology.pdf):

1. **Contagio** — un individuo *suscettibile* (stato 0) diventa *infetto* (stato 1) con probabilità $p_i$ se la densità locale di infetti supera la soglia $\theta_1$;
2. **Persistenza dell'infezione / guarigione** — un individuo *infetto* (stato 1) rimane infetto con probabilità $p_s$ se la densità locale di infetti supera la soglia $\theta_2$; in caso contrario guarisce (passa allo stato 2);
3. **Persistenza dell'immunità / perdita di immunità** — un individuo *guarito* (stato 2) rimane guarito con probabilità $p_r$, oppure ridiventa suscettibile.

La terza regola, ammettendo il ritorno alla suscettibilità, conferisce di fatto al modello un carattere di tipo **SIRS**. Le simulazioni sono condotte su un reticolo $200 \times 200$ con vicinato di **Moore di raggio** $r = 2$ e parametri $\theta_1 = 0.16$, $\theta_2 = 0.40$, $p_i = 0.7$, $p_s = 0.8$, $p_r = 0.9$; la proprietà propagata $\mathcal{P}$ corrisponde all'infezione (stato $1$) [[5]](CA-doc/SIR/Spreadable%20Probabilistic%20Cellular%20Automata%20Models%3A%20An%20Application%20in%20Epidemiology.pdf). Si osserva la crescita delle zone infette e una marcata dipendenza dalla configurazione iniziale: partendo da un seme quadrato compatto l'intero dominio si riempie in circa 150 iterazioni, mentre da un seme casuale di pari densità bastano circa 50 iterazioni [[5]](CA-doc/SIR/Spreadable%20Probabilistic%20Cellular%20Automata%20Models%3A%20An%20Application%20in%20Epidemiology.pdf).

La differenza sostanziale rispetto all'approccio di Fuentes–Kuperman è che qui la transizione di contagio non dipende da un tasso continuo, ma dal **superamento di una soglia di densità locale di infetti** combinato con un **esito probabilistico**: il contagio avviene solo se una quota sufficiente del vicinato è infetta *e* solo con una data probabilità.

---

## Automi cellulari per la propagazione degli incendi boschivi

### Perché esiste il problema e contesto storico

Gli incendi boschivi sono una componente ricorrente della dinamica di quasi tutti gli ecosistemi terrestri e, al tempo stesso, una fonte di danni ambientali ed economici di grande rilievo. La capacità di prevedere l'evoluzione di un incendio — cioè di determinare la posizione del *fronte di fiamma* nel tempo, sotto date condizioni di vento, topografia e vegetazione — è essenziale sia per la pianificazione della prevenzione sia per il supporto in tempo reale alle operazioni di spegnimento [[11]](CA-doc/Fire/karafyllidis_1997.pdf). Il secondo grande dominio di applicazione degli automi cellulari a fenomeni di propagazione spaziale è appunto la simulazione degli incendi boschivi: rispetto ai modelli SIR descritti in precedenza, qui la "malattia" che si propaga da cella a cella è il fuoco stesso, e il ruolo dei suscettibili/infetti/rimossi è preso da combustibile/fiamma/cenere.

L'approccio classico alla previsione della velocità di avanzamento del fuoco si fonda su relazioni semi-empiriche, la più influente delle quali è il modello di Rothermel per la *rate of spread* nei combustibili selvatici [20]. Tradurre però queste relazioni in una descrizione spaziale completa attraverso equazioni alle derivate parziali (PDE) risulta oneroso: la forte non-linearità del problema, la geometria irregolare del territorio e la presenza di aree con proprietà di combustione diverse rendono i sistemi di PDE difficili da trattare e computazionalmente costosi [[11]](CA-doc/Fire/karafyllidis_1997.pdf). Da qui l'interesse per formulazioni discrete alternative.

Storicamente il filone nasce come un modello giocattolo di meccanica statistica per lo studio dell'**autorganizzazione critica** (Bak–Chen–Tang, Drossel–Schwabl), evolve poi verso una lettura geometrica legata alla percolazione e alla forma del fronte (Green), e infine converge — attraverso una sequenza di modelli sempre più raffinati con vicinato di Moore — in strumenti quantitativi calibrati su incendi reali con vento, pendenza e vegetazione (Karafyllidis–Thanailakis, Hernández Encinas et al., Alexandridis et al., e gli sviluppi più recenti).

### Come si può affrontare il problema

Gli automi cellulari offrono un'alternativa discreta alle PDE: il territorio è suddiviso in celle identiche, ciascuna dotata di uno stato che evolve a passi discreti secondo una regola di transizione che dipende soltanto dallo stato dei vicini; da regole locali semplici può emergere un comportamento globale complesso, il che rende i CA particolarmente adatti a simulare fenomeni di propagazione, oltre a essere naturalmente integrabili con i sistemi informativi geografici (GIS) e computazionalmente efficienti [[11]](CA-doc/Fire/karafyllidis_1997.pdf). I CA sono stati applicati alla propagazione degli incendi lungo due direttrici concettualmente distinte, che è utile tenere separate perché rispondono a domande scientifiche diverse.

La prima direttrice, **predittiva**, mira a riprodurre *dove e come* si muove un fronte reale: i primi studi di simulazione su combustibili discreti mostrarono che meccanismi di propagazione differenti — accumulo di calore contro contatto di fiamma — generano forme di incendio diverse, quasi ellittiche nei combustibili continui ma assai più irregolari nei combustibili a chiazze [[10]](CA-doc/Fire/green1983.pdf); da qui si sviluppa la sequenza di modelli a vicinato di Moore, sempre più raffinati e infine calibrati su incendi reali, presentata di seguito. La seconda direttrice, **statistico-fisica**, ha origine e finalità diverse: nasce come modello-giocattolo per studiare lo scaling e la dissipazione frattale dell'energia in analogia con la turbolenza, senza l'obiettivo di prevedere un incendio specifico ma di caratterizzare la *statistica universale* di molti incendi — in questo quadro vento, pendenza e vegetazione sono deliberatamente astratti.

Vale la pena sottolineare un legame che collega questa seconda direttrice al lavoro precedente sulla diffusione delle epidemie: il modello di incendio a stati discreti appartiene alla classe dei *mezzi eccitabili*, la stessa che descrive la propagazione delle malattie [[9]](CA-doc/Fire/clar_drossel_schwabl_review.pdf); la corrispondenza albero → suscettibile, albero in fiamme → infetto, cella vuota → rimosso rende la famiglia SOC degli incendi, di fatto, un modello SIR spaziale. La famiglia predittiva, per contro, adotta una descrizione dello stato di cella (frazione di area bruciata, evoluzione deterministica o probabilistica calibrata) che si allontana dallo schema compartimentale. I due modi di guardare al fuoco corrispondono così a due modi diversi, ma entrambi familiari, di guardare a un processo di diffusione.

### Metodi studiati in questo lavoro

Data l'ampiezza di entrambe le direttrici, il presente lavoro le tiene esplicitamente distinte, ripercorrendo la famiglia statistico-fisica (SOC) e la famiglia predittiva (Green, Karafyllidis–Thanailakis, Hernández Encinas et al., Alexandridis et al. e gli sviluppi recenti) come due modi diversi, ma entrambi legittimi, di etichettare un "automa cellulare per gli incendi": un fronte che si organizza spontaneamente verso uno stato critico con statistica a legge di potenza, e un fronte deterministico o probabilistico guidato da fattori fisici osservabili.

#### Il modello di autorganizzazione critica (SOC): Bak–Chen–Tang (1990) e Drossel–Schwabl (1992)

Il capostipite dei modelli CA per gli incendi boschivi non nasce in ambito forestale ma in fisica statistica, come esempio di **criticità autoorganizzata** (*self-organized criticality*, SOC) [[7]](CA-doc/Fire/Forestfire.pdf). Bak, Chen e Tang definiscono un automa cellulare su reticolo ipercubico $d$-dimensionale di $L^d$ siti, con vicinato dei **primi vicini** (von Neumann) e tre stati per cella: **vuoto**, **albero**, **albero in fiamme**. Le regole, aggiornate in parallelo, sono [[7]](CA-doc/Fire/Forestfire.pdf):

1. un albero in fiamme diventa un sito vuoto;
2. un albero il cui vicinato contiene almeno un albero in fiamme prende fuoco (propagazione deterministica e istantanea);
3. su un sito vuoto cresce un nuovo albero con probabilità $p$.

L'unico parametro del modello è dunque il tasso di crescita $p$; non essendovi innesco spontaneo, il fuoco deve essere introdotto "a mano" nella configurazione iniziale (o re-innescato quando si estingue per effetti di taglia finita) [[7]](CA-doc/Fire/Forestfire.pdf). Drossel e Schwabl generalizzano il modello aggiungendo una **quarta regola** che rende il sistema autosufficiente [[8]](CA-doc/Fire/PhysRevLett.69.1629.pdf):

4. un albero senza vicini in fiamme prende fuoco spontaneamente (fulmine) con probabilità $f$.

Non esiste uno stato distinto di "cenere": l'albero bruciato torna vuoto nello stesso passo (regola 1) e da lì potrà ricrescere (regola 3). Nello stato stazionario vale il bilancio tra densità di sito vuoto $\rho_e$, albero $\rho_t$ e fuoco $\rho_f$ [[9]](CA-doc/Fire/clar_drossel_schwabl_review.pdf):

$$
\rho_e+\rho_t+\rho_f=1, \qquad \rho_f = p\,\rho_e .
$$

**Autorganizzazione critica.** Il numero medio di alberi distrutti da un fulmine è legato al rapporto tra il tasso di crescita e quello di fulmine [[8]](CA-doc/Fire/PhysRevLett.69.1629.pdf), [[9]](CA-doc/Fire/clar_drossel_schwabl_review.pdf):

$$
\bar s \simeq \frac{p}{f}\cdot\frac{1-\rho_t}{\rho_t} \;\propto\; (f/p)^{-1},
$$

che diverge come una legge di potenza nel limite $f/p \to 0$: **il punto critico del sistema è $f/p\to 0$**, raggiunto senza alcuna calibrazione fine di parametri (da cui il nome "autoorganizzata"). Perché il regime critico sia effettivamente osservabile occorre inoltre che il tempo di combustione di un intero cluster sia molto più breve del tempo di ricrescita di un albero ai suoi bordi, il che produce una **doppia separazione di scale temporali** [[8]](CA-doc/Fire/PhysRevLett.69.1629.pdf), [[9]](CA-doc/Fire/clar_drossel_schwabl_review.pdf):

$$
(f/p)^{-\nu} \;\ll\; p^{-1} \;\ll\; f^{-1},
$$

cioè: tempo di combustione di un cluster $\ll$ tempo di crescita di un albero $\ll$ tempo medio tra due fulmini sullo stesso sito. In questo regime la distribuzione dei cluster di alberi bruciati $n(s)$ (numero medio di cluster di dimensione $s$ per sito) segue una **legge di potenza con cutoff**:

$$
n(s)\propto s^{-\tau}\,\mathcal{C}(s/s_{max}), \qquad s_{max}\propto (f/p)^{-\lambda},
$$

con relazione di scala $d=\mu(\tau-1)$ tra la dimensione frattale del cluster $\mu$ e l'esponente $\tau$ [[9]](CA-doc/Fire/clar_drossel_schwabl_review.pdf). In due dimensioni le simulazioni danno $\tau\approx 2.14$, $\rho_t^c\approx 0.41$, $\mu\approx1.96$, $\nu\approx0.58$; in una dimensione il risultato è **esatto**, $\tau=2$ [[8]](CA-doc/Fire/PhysRevLett.69.1629.pdf), [[9]](CA-doc/Fire/clar_drossel_schwabl_review.pdf). Il paper di Drossel e Schwabl introduce anche un parametro di **immunità** $g$ (probabilità che un albero adiacente al fuoco non si accenda), che collega il modello alla teoria della **percolazione di legame**: per $g\to g_c=1/2$ (soglia di percolazione in 2D) la densità critica di foresta tende a $1$ e gli esponenti coincidono con quelli della percolazione ordinaria [[9]](CA-doc/Fire/clar_drossel_schwabl_review.pdf).

Va segnalato che questo filone (SOC) **non modella vento, pendenza o eterogeneità del combustibile**: il suo interesse, ai fini della tesi, è puramente concettuale — mostra che una regola locale elementare (crescita + innesco + propagazione ai primi vicini) genera da sola comportamento critico e fronti di fuoco autosimili, ed è il punto di partenza storico da cui i modelli seguenti si allontanano progressivamente per includere realismo fisico.

L'universalità di questo comportamento critico è stata oggetto di dibattito. Grassberger e Kantz [21], simulando il modello su reticoli molto più grandi, misero in dubbio la presenza di un vero fenomeno critico non banale nel limite considerato, mostrando piuttosto un'evoluzione deterministica su scale temporali dell'ordine dell'inverso del tasso di crescita — un richiamo importante a non sopravvalutare la genericità della SOC senza verifiche di taglia finita.

#### Percolazione geometrica e forma del fronte: il modello di Green (1983)

Un secondo filone, indipendente dal precedente, nasce in ecologia con l'obiettivo di riprodurre la **forma geometrica** dei fronti di incendio reali in funzione della continuità del combustibile [[10]](CA-doc/Fire/green1983.pdf). Green rappresenta il combustibile come un reticolo 2D di celle piene/vuote (con frazione di celle piene, o *fuel cover*, che modula la spaziatura media del combustibile) e introduce il concetto di **template di accensione**: un array che descrive l'effetto di un punto in combustione sui punti circostanti, tipicamente di forma **ellittica** con eccentricità $e$ crescente con la velocità del vento (o quadrata, per confronto) [[10]](CA-doc/Fire/green1983.pdf).

Sono confrontati due meccanismi di propagazione punto-punto. Nel modello a **contatto**, il tempo necessario perché il punto $X$ acceso inneschi il punto $Y$ è:

$$
t(X,Y) = \frac{C\,M\,(1-e^2)}{d(X,Y)\,(1-e\cos\theta)},
$$

dove $M$ è la dimensione del template, $\theta$ l'angolo di $Y$ rispetto a $X$ misurato da sottovento, $d(X,Y)$ la distanza e $C$ una costante; il tempo di accensione di ogni punto si aggiorna scandendo ripetutamente il template, $T'(Y)=\min\big(T(Y),\,T(X)+t(X,Y)\big)$, e l'area bruciata a un istante $T_{max}$ è l'insieme $\{X : T(X)\le T_{max}\}$ [[10]](CA-doc/Fire/green1983.pdf). Nel modello ad **accumulo di calore**, si accumula invece un flusso termico $H'(Y)=H(Y)+h(X,Y)$ fino al raggiungimento di una soglia critica di accensione [[10]](CA-doc/Fire/green1983.pdf).

Il risultato principale è che la **continuità del combustibile** determina la forma del fronte: in combustibile continuo entrambi i meccanismi producono fronti **ellittici** (in accordo con i classici modelli di crescita ellittica del fuoco); in combustibile molto discontinuo (*patchy*) emergono forme **non ellittiche** — ovoidali, "a goccia", semi-ellittiche, fino a degenerare in una linea retta per venti molto forti — con back-burning ridotto o assente [[10]](CA-doc/Fire/green1983.pdf). Va segnalato con onestà che il paper **non formalizza esplicitamente una soglia critica di percolazione**: si limita a osservare, qualitativamente, che in combustibile molto discontinuo alcuni elementi di combustibile interni all'area "raggiunta" dal fronte non si accendono effettivamente — un'osservazione concettualmente affine alla percolazione, ma non sviluppata come tale [[10]](CA-doc/Fire/green1983.pdf). Il valore di questo modello per la tesi è soprattutto **metodologico**: introduce l'idea di un template di propagazione anisotropo, dipendente dalla direzione del vento, distribuito sul vicinato di una cella — l'idea che, discretizzata su un vicinato di Moore, sta alla base dei modelli delle sezioni successive.

#### Automi a stato continuo con vicinato di Moore: Karafyllidis–Thanailakis (1997)

Karafyllidis e Thanailakis propongono il primo modello CA di incendio con vicinato di **Moore** (le $3\times3$ celle centrate sulla cella in esame) e uno stato **continuo** anziché discreto [[11]](CA-doc/Fire/karafyllidis_1997.pdf):

$$
S_{ij}^{\,t} = \frac{A_b}{A_t} \in [0,1],
$$

pari alla frazione di area bruciata della cella (0 = intatta, 1 = completamente bruciata); le aree incombustibili sono semplicemente celle con tasso di propagazione $R=0$ [[11]](CA-doc/Fire/karafyllidis_1997.pdf). A ciascuna cella è associato un tasso di propagazione $R_{ij}$ (m/s), fornito da un modello esterno (es. Rothermel/McRae). Ponendo il passo temporale pari al tempo di combustione lungo un lato, $t_a = a/R_{ij}$, un vicino ortogonale completamente bruciato brucia interamente la cella in un passo, mentre un vicino diagonale, per ragioni geometriche, ne brucia solo una frazione:

$$
2(\sqrt2-1) \cong 0.83 .
$$

La regola base (foresta omogenea, senza vento) è quindi:

$$
S_{i,j}^{t+1}=S_{i,j}^{t}+\Big(S_{i-1,j}^{t}+S_{i,j-1}^{t}+S_{i,j+1}^{t}+S_{i+1,j}^{t}\Big)+0.83\Big(S_{i-1,j-1}^{t}+S_{i-1,j+1}^{t}+S_{i+1,j-1}^{t}+S_{i+1,j+1}^{t}\Big),
$$

troncata a $1$ se supera tale valore [[11]](CA-doc/Fire/karafyllidis_1997.pdf). Il **vento** è incorporato assegnando un peso moltiplicativo a ciascuna delle otto direzioni del vicinato di Moore ($n,s,e,w,ne,nw,se,sw$):

$$
S_{i,j}^{t+1}=S_{i,j}^{t}+\big(n S_{i-1,j}^{t}+w S_{i,j-1}^{t}+e S_{i,j+1}^{t}+s S_{i+1,j}^{t}\big)+0.83\big(nw S_{i-1,j-1}^{t}+ne S_{i-1,j+1}^{t}+sw S_{i+1,j-1}^{t}+se S_{i+1,j+1}^{t}\big),
$$

con pesi $>1$ nella direzione sopravento e $<1$ in quella sottovento (tutti $=1$ in assenza di vento) [[11]](CA-doc/Fire/karafyllidis_1997.pdf). Un meccanismo analogo, con pesi $H_{k,l}$ funzione (in prima approssimazione lineare) del dislivello tra celle, incorpora la **pendenza del terreno** [[11]](CA-doc/Fire/karafyllidis_1997.pdf). Il modello è interamente **deterministico** — nessuna componente probabilistica, $R_{ij}$ è un dato esterno — e non è validato quantitativamente contro incendi reali, solo su foreste ipotetiche (fronti circolari senza vento, allungati nella direzione del vento, deformati da rilievi) [[11]](CA-doc/Fire/karafyllidis_1997.pdf). Questo è, concettualmente, l'antenato diretto di uno schema "vicinato di Moore + matrice di propagazione anisotropa per direzione, modulata dal vento", ripreso e reso probabilistico dai modelli successivi.

#### Fronte circolare e caso disomogeneo: Hernández Encinas et al. (2007)

Una revisione del modello precedente nota che il coefficiente diagonale $0.83$ di Karafyllidis–Thanailakis produce fronti leggermente ottagonali anziché circolari, e lo sostituisce con un coefficiente calibrato geometricamente sull'area di un settore circolare [[12]](CA-doc/Fire/10.1016@j.advengsoft.2006.09.002.pdf):

$$
\lambda = \pi/4 \cong 0.785 .
$$

Il modello viene formalizzato come automa cellulare in senso stretto, quadrupla $\mathscr{A}=(C,S,V,f)$ con vicinato di Moore $V_M$ diviso in celle adiacenti $V_M^{adj}$ e diagonali $V_M^{diag}$, e stato $a_{ij}^{(t)}\in[0,1]$ pari alla frazione di area bruciata [[12]](CA-doc/Fire/10.1016@j.advengsoft.2006.09.002.pdf). La regola generale, per foresta disomogenea (tasso di propagazione $R_{ij}$ diverso per cella) con vento e pendenza variabili nel tempo, è:

$$
a_{ij}^{(t+1)}=\frac{R_{ij}}{R}\,a_{ij}^{(t)}
+\!\!\sum_{(\alpha,\beta)\in V_M^{adj}}\!\! w_{i+\alpha,j+\beta}^{(t)}\,h_{i+\alpha,j+\beta}\,\frac{R_{i+\alpha,j+\beta}}{R}\,a_{i+\alpha,j+\beta}^{(t)}
+\!\!\sum_{(\alpha,\beta)\in V_M^{diag}}\!\! w_{i+\alpha,j+\beta}^{(t)}\,h_{i+\alpha,j+\beta}\,\frac{\pi R_{i+\alpha,j+\beta}^{2}}{4R^{2}}\,a_{i+\alpha,j+\beta}^{(t)},
$$

dove $R=\max\{R_{ij}\}$ fissa il passo temporale comune $\tilde t = L/R$, $w$ è la matrice di vento e $h$ la matrice di pendenza [[12]](CA-doc/Fire/10.1016@j.advengsoft.2006.09.002.pdf). Anche questo modello resta **deterministico** e testato solo su foreste ipotetiche $1024\times1024$, senza confronto con incendi reali [[12]](CA-doc/Fire/10.1016@j.advengsoft.2006.09.002.pdf). Significativamente, gli autori indicano tra gli sviluppi futuri proprio il passaggio a **regole di aggiornamento probabilistiche** (ad esempio per modellare l'accensione spontanea) [[12]](CA-doc/Fire/10.1016@j.advengsoft.2006.09.002.pdf) — la direzione presa dai modelli descritti di seguito.

#### Modelli probabilistici calibrati su incendi reali: Alexandridis et al. (2008)

Alexandridis, Vakalis, Siettos e Bafas riformulano il problema in termini interamente **probabilistici**, tornando a stati discreti su un reticolo di celle quadrate con vicinato di Moore [[13]](CA-doc/Fire/alexandridis2008.pdf):

- **stato 1** — cella priva di combustibile forestale (aree urbane/rurali);
- **stato 2** — cella con combustibile non ancora incendiato;
- **stato 3** — cella in fiamme;
- **stato 4** — cella completamente bruciata.

Le regole di transizione sono [[13]](CA-doc/Fire/alexandridis2008.pdf): una cella in fiamme diventa bruciata al passo successivo (un solo timestep di combustione, Rule 2); le celle senza combustibile o già bruciate restano tali (Rule 1, 3); una cella con combustibile adiacente a una cella in fiamme prende fuoco con probabilità $p_{burn}$ (Rule 4); inoltre un meccanismo di **spotting** (lancio di braci/pigne ardenti) può incendiare celle non adiacenti a distanza $d_p$ con probabilità $p_c$ (Rule 5). La probabilità di propagazione è il prodotto di un valore di base e di quattro fattori correttivi:

$$
p_{burn} = p_h\,(1+p_{den})\,(1+p_{veg})\,p_w\,p_s ,
$$

dove $p_h$ è la probabilità costante di base (combustibile di riferimento, vento nullo, terreno piatto), $p_{den}$ e $p_{veg}$ dipendono da categorie discrete di densità e tipo di vegetazione [[13]](CA-doc/Fire/alexandridis2008.pdf). Il fattore vento, ispirato alla relazione empirica $R_w=R_{0w}e^{\beta\theta_f}$ della letteratura sul *rate of spread*, è reso continuo nell'angolo:

$$
p_w = \exp(c_1 V)\,f_t, \qquad f_t=\exp\!\big(Vc_2(\cos\theta-1)\big),
$$

con $V$ velocità del vento e $\theta$ angolo tra la direzione di propagazione e quella del vento [[13]](CA-doc/Fire/alexandridis2008.pdf). Il fattore di pendenza è

$$
p_s = \exp(a\,\theta_s), \qquad \theta_s = \tan^{-1}\!\left(\frac{E_1-E_2}{l}\right)\ \text{(celle adiacenti)}, \quad \theta_s = \tan^{-1}\!\left(\frac{E_1-E_2}{l\sqrt2}\right)\ \text{(celle diagonali)},
$$

con $E_1,E_2$ quote delle due celle e $l$ lato della cella [[13]](CA-doc/Fire/alexandridis2008.pdf). Lo spotting lancia un numero di braci $N_p\sim\mathrm{Poisson}(\lambda)$ a distanza $d_p = r_n\exp\big(Vc_2(\cos\theta_p-1)\big)$, con probabilità di attecchimento $p_c=p_{c0}(1+p_{cd})$ [[13]](CA-doc/Fire/alexandridis2008.pdf). Il modello è stato **calibrato quantitativamente** (ottimizzazione di Nelder–Mead) sull'incendio reale dell'isola di Spetses (Grecia, agosto 1990, area bruciata reale $5.9\,\mathrm{km}^2$ in circa 11 ore), ottenendo parametri $p_h=0.58$, $a=0.078$, $c_1=0.045$, $c_2=0.131$ e un'area simulata di $5.4\,\mathrm{km}^2$ in $11.3$ ore — un accordo definito dagli autori "molto vicino" al dato osservato [[13]](CA-doc/Fire/alexandridis2008.pdf). È il primo modello della rassegna validato numericamente contro un incendio reale misurato, e la sua struttura moltiplicativa $p_{burn}=p_h(1+p_{veg})(1+p_{den})p_w p_s$ è diventata uno schema di riferimento ripreso dalla letteratura successiva.

#### Sviluppi recenti: regola di ignizione a sigmoide e integrazione GIS

Un lavoro più recente riprende lo schema di Alexandridis aggiungendo una **soglia morbida** sul numero di vicini in fiamme, tramite una funzione sigmoide, e un'integrazione diretta con dati GIS [[14]](CA-doc/Fire/probabilistic_ca_2024.pdf). Gli stati di cella sono TREE, BURNING, BURNING DURATION, EMPTY, WATER, CITY, su vicinato di Moore (8 direzioni). La probabilità di ignizione è modulata dal numero di vicini in fiamme:

$$
P_{ignition}(burning_{neighbours}) = \frac{1}{1+\exp\!\big(-k\,(burning_{neighbours}-threshold)\big)},
$$

con $k$ parametro di ripidità della sigmoide e $threshold$ soglia di ignizione [[14]](CA-doc/Fire/probabilistic_ca_2024.pdf). La probabilità di propagazione riprende la forma moltiplicativa di Alexandridis,

$$
p_b = p_o\,(1+p_{veg})(1+p_{den})\,p_w ,
$$

mentre l'effetto del vento sulla frazione $F$ di vicini in fiamme è descritto da un'equazione differenziale fenomenologica:

$$
\frac{dF}{dt} = k\cdot Wind_{Speed}\cdot Wind_{Direction} - m\,F ,
$$

con $m$ tasso di estinzione [[14]](CA-doc/Fire/probabilistic_ca_2024.pdf). Il modello è validato qualitativamente (confronto con mappe satellitari) su due incendi reali greci: Spetses 1990 e l'incendio di Evia del 2021 [[14]](CA-doc/Fire/probabilistic_ca_2024.pdf). Si segnala, per completezza bibliografica, che la sede di pubblicazione di questo lavoro non è determinabile con certezza dal solo PDF (nota a piè di pagina: elaborato nell'ambito della *Summer School on Cellular Automata Technology*, 2023) [[14]](CA-doc/Fire/probabilistic_ca_2024.pdf).

#### Sintesi comparativa dei modelli Fire

| Aspetto | Bak–Chen–Tang / Drossel–Schwabl [[7]](CA-doc/Fire/Forestfire.pdf), [[8]](CA-doc/Fire/PhysRevLett.69.1629.pdf), [[9]](CA-doc/Fire/clar_drossel_schwabl_review.pdf) | Green (1983) [[10]](CA-doc/Fire/green1983.pdf) | Karafyllidis–Thanailakis (1997) [[11]](CA-doc/Fire/karafyllidis_1997.pdf) | Hernández Encinas et al. (2007) [[12]](CA-doc/Fire/10.1016@j.advengsoft.2006.09.002.pdf) | Alexandridis et al. (2008) [[13]](CA-doc/Fire/alexandridis2008.pdf) |
|---------|---|---|---|---|---|
| Vicinato | von Neumann (primi vicini) | template anisotropo (ellittico/quadrato) | Moore ($3\times3$) | Moore ($3\times3$) | Moore ($3\times3$) |
| Stato della cella | vuoto / albero / fuoco | tempo di accensione $T(X)$ o calore accumulato $H(X)$ | frazione bruciata $S_{ij}\in[0,1]$ | frazione bruciata $a_{ij}\in[0,1]$ | discreto $\{1,2,3,4\}$ |
| Natura del modello | stocastica (crescita $p$, fulmine $f$) | deterministica (template geometrico) | deterministica ($R_{ij}$ esterno) | deterministica ($R_{ij}$ esterno) | probabilistica ($p_{burn}$) |
| Ruolo del vento | assente | eccentricità $e$ del template | pesi direzionali $n,s,e,w,\dots$ | matrice vento $w$ | fattore $p_w=\exp(c_1V)f_t$ |
| Fenomeno chiave | criticità autoorganizzata, legge di potenza $n(s)\propto s^{-\tau}$ | forma del fronte (ellisse/ovoide) vs. continuità combustibile | fronte con artefatti ottagonali | fronte circolare corretto ($\pi/4$) | area bruciata calibrata su dato reale |
| Validazione | statistica (esponenti critici) | qualitativa (forma) | qualitativa (foreste ipotetiche) | qualitativa (foreste ipotetiche) | quantitativa (incendio di Spetses, 1990) |

Il filo conduttore è una progressiva **concretizzazione fisica** della stessa idea di fondo — un fronte che avanza per contatto locale, cella dopo cella — a partire da un modello astratto di meccanica statistica (Bak–Chen–Tang/Drossel–Schwabl), passando per una lettura puramente geometrica (Green), fino a uno schema di vicinato di Moore via via arricchito di vento, pendenza e vegetazione, prima in forma deterministica (Karafyllidis–Thanailakis, Hernández Encinas et al.) e infine probabilistica e calibrata su dati reali (Alexandridis et al. e gli sviluppi recenti).

---

## Sintesi generale: due famiglie di automi cellulari per fenomeni di propagazione spaziale

I modelli SIR e i modelli di incendio, pur descrivendo fenomeni fisicamente diversi, condividono la stessa struttura logica di fondo: una **grandezza binaria o continua che si propaga per contatto locale** su un reticolo discreto, con una soglia (deterministica o probabilistica) che decide se la propagazione avviene o si arresta. In entrambe le famiglie di modelli si ritrova:

- una nozione di **soglia critica di propagazione**, che nei modelli SIR prende la forma del numero di riproduzione di base ($R_0=\beta S(0)/\gamma$ nell'ODE, $X=vS_O^0/\varepsilon$ nel CA di White, del Rey e Sánchez [[3]](CA-doc/SIR/A%20Model%20Based%20on%20Cellular%20Automata%20to%20Simulate%20Epidemic%20Diseases.pdf), [[4]](CA-doc/SIR/Modeling%20epidemics%20using%20cellular%20automata.pdf)) e nei modelli di incendio quella del rapporto critico $f/p\to0$ dell'autorganizzazione critica, oppure della soglia di percolazione del combustibile;
- una **funzione di contagio/ignizione locale**, sempre scomponibile in un fattore di suscettibilità della cella ricevente (frazione di suscettibili $S_{ij}$, o presenza di combustibile) moltiplicato per un termine legato ai vicini "infetti"/"in fiamme", a sua volta modulato da fattori ambientali locali (densità di popolazione e connessioni di trasporto per il SIR; vento, pendenza e vegetazione per il fuoco);
- una tensione tra **modelli meccanicistici astratti**, nati per studiare un fenomeno critico in sé (i contatori di fase $t_i,t_p,t_l$ di Fuentes–Kuperman, la criticità autoorganizzata di Bak–Chen–Tang/Drossel–Schwabl) e **modelli ingegneristici via via più realistici**, calibrati o calibrabili su dati osservati (le frazioni $(S,I,R)$ di White, del Rey e Sánchez [[3]](CA-doc/SIR/A%20Model%20Based%20on%20Cellular%20Automata%20to%20Simulate%20Epidemic%20Diseases.pdf), [[4]](CA-doc/SIR/Modeling%20epidemics%20using%20cellular%20automata.pdf) con il fattore di connessione $c$, la propagazione moltiplicativa $p_{burn}$ di Alexandridis validata sull'incendio di Spetses).

Per l'implementazione in codice, questa lettura comparativa suggerisce un parallelismo diretto: il modello SIR "a contatore" di Fuentes–Kuperman [[2]](CA-doc/SIR/Cellular-automata-and-epidemiological-mo_1999_Physica-A--Statistical-Mechani.pdf), con vicinato di von Neumann e propagazione probabilistica per singolo vicino (e la sua variante stocastica dovuta a Landguth [[6]](CA-doc/SIR/A%20Cellular%20Automata%20SIR%20Model%20for%20Landscape%20Epidemiology.pdf)), e il modello di incendio a vicinato di Moore con matrice di propagazione anisotropa modulata dal vento (Karafyllidis–Thanailakis, Hernández Encinas et al., Alexandridis et al.) rappresentano, per le rispettive famiglie, il punto di equilibrio più naturale tra semplicità della regola locale e fedeltà fisica — ed è su questi due schemi che si baserà la fase successiva di implementazione.

---

## Automi cellulari per il modello di Ising

### Perché esiste il problema e contesto storico

Le sezioni precedenti trattano automi cellulari usati per riprodurre un **fronte di propagazione spaziale** (epidemia o incendio) che avanza nel tempo. Il modello di Ising rappresenta un'applicazione di natura diversa: qui l'obiettivo non è seguire l'avanzare di un fronte, ma usare l'automa cellulare come strumento per campionare le proprietà di **equilibrio** di un sistema di meccanica statistica — un reticolo di spin che interagiscono con i primi vicini — alternativo ai metodi Monte Carlo classici. La domanda, posta per prima in modo sistematico da Vichniac nel 1984, è se un automa cellulare a duplice stato per cella possa riprodurre esattamente le proprietà di equilibrio di questo sistema.

### Come si può affrontare il problema

Il filo conduttore di questa sezione è la tensione tra due esigenze in conflitto: da un lato la **parallelizzazione totale** propria degli automi cellulari (aggiornare tutte le celle simultaneamente), dall'altro la necessità di riprodurre correttamente la distribuzione di Boltzmann all'equilibrio, che — come si vedrà — impone vincoli non banali sulla regola locale. Le strategie proposte in letteratura per conciliare le due esigenze si dividono in due filoni: un filone **deterministico**, che rinuncia in parte al parallelismo totale (aggiornamento a scacchiera) e introduce meccanismi ausiliari — parità, variabili "demone", sistemi di spin accessori — per garantire la conservazione dell'energia a livello locale (Vichniac, Creutz, Ottavi–Parodi, Xiao); e il termine di paragone classico, non basato su automi cellulari, del campionamento **Monte Carlo** di una catena di Markov ergodica.

### Metodi studiati in questo lavoro

#### Il limite della parallelizzazione totale e la regola Q2R: Vichniac (1984)

Vichniac affronta per primo, in modo sistematico, la domanda se un automa cellulare a duplice stato per cella possa riprodurre le proprietà di equilibrio del modello di Ising, definito dall'Hamiltoniana [[15]](CA-doc/Ising/vichniac1984.pdf)

$$
H = -J \sum_{\langle i,j \rangle} \sigma_i \sigma_j ,
$$

con spin $\sigma_i \in \{+1,-1\}$ sui siti di un reticolo e somma sui soli primi vicini. All'equilibrio con un bagno termico a temperatura $T$, il valore medio di un osservabile $A$ nell'insieme canonico è dato dalla consueta media pesata con il fattore di Boltzmann e normalizzata dalla funzione di partizione $Z(T)$ [[15]](CA-doc/Ising/vichniac1984.pdf).

Un risultato centrale del lavoro è un **argomento contro la parallelizzazione totale**: nessuna regola di automa cellulare che aggiorni *simultaneamente* tutti gli spin può riprodurre esattamente la distribuzione canonica (4.2). La ragione è che l'energia di Ising è un operatore a due corpi: il calcolo dell'incremento di energia globale associato al ribaltamento di un singolo spin, $\Delta\epsilon_i$, resta valido solo se gli spin aggiornati non sono mutuamente adiacenti; se due celle contigue vengono ribaltate nello stesso passo, la relazione tra variazione locale e variazione globale dell'energia si rompe, e la regola di transizione non ha più accesso all'informazione necessaria per riprodurre il peso di Boltzmann corretto [[15]](CA-doc/Ising/vichniac1984.pdf). Da qui l'esigenza, comune a tutti i modelli successivi, di un aggiornamento **a scacchiera** (metà delle celle per passo) anziché completamente parallelo.

Su questa base Vichniac introduce la regola reversibile **Q2R**, definita sul vicinato di von Neumann tramite l'espressione booleana [[15]](CA-doc/Ising/vichniac1984.pdf)

$$
Y = \big((Q=2)\ \text{XOR}\ \text{CPAST}\big),
$$

dove $Q$ è il numero di vicini con spin "su" e CPAST è lo stato della cella al passo precedente: uno spin è candidato al ribaltamento quando ha esattamente due vicini "su" e due "giù" (condizione di neutralità energetica, l'unico caso in cui il flip non altera l'energia), e l'operazione XOR con lo stato precedente rende la regola **esattamente reversibile**, evitando che la cella ritorni immediatamente sullo stato di partenza. Questa è, nella sostanza, la stessa regola che la letteratura successiva chiama modello **VPH** (Vichniac–Pomeau–Herrmann): il ribaltamento avviene se e solo se non altera l'energia magnetica, con aggiornamento a scacchiera in due sotto-passi [[17]](CA-doc/Ising/ottavi1989.pdf).

Q2R conserva **esattamente** l'energia totale ed è **deterministica e reversibile**, ma non è **ergodica**: la dinamica è simmetrica rispetto a traslazioni del reticolo e all'inversione globale degli spin, e a basse temperature si blocca in cicli-limite periodici ("mostri oscillanti") anziché esplorare l'intero spazio delle configurazioni a parità di energia — un fenomeno che Vichniac collega concettualmente alla fisica dei sistemi frustrati e dei vetri di spin (disordine e frustrazione producono buche di potenziale profonde e strette nella superficie di energia, analoghe a quelle di uno spin-glass) [[15]](CA-doc/Ising/vichniac1984.pdf). Vichniac nota anche che, proprio per questa tendenza a "congelarsi" in configurazioni di energia localmente minima, Q2R può essere sfruttata in senso costruttivo come algoritmo di ottimizzazione a $T=0$ per la ricerca di stati fondamentali.

#### Il modello a demoni deterministico: Creutz (1986)

Creutz propone un'alternativa che rinuncia alla reversibilità in senso stretto in cambio di un controllo diretto sulla temperatura. Ogni sito porta, oltre allo spin, una variabile "demone" locale (2 bit) che funge da riserva di energia cinetica coniugata allo spin, più un bit di parità per l'aggiornamento a scacchiera; un flip di spin è accettato se e solo se la variazione di energia magnetica può essere esattamente compensata dalla variabile demone del sito, mantenendo così invariata l'energia totale. Il dettaglio completo delle equazioni, dell'algoritmo e degli esperimenti numerici (correlazione tra primi vicini, flusso di calore, conducibilità termica, correlazioni temporali e mixing) è riportato nel file [pub088-creutz1986-summary.md](Ising/pub088-creutz1986-summary.md) [[16]](CA-doc/Ising/pub088-1-10.pdf).

#### I limiti a bassa temperatura e le correzioni di Ottavi–Parodi (1989)

Testando il modello C2 di Creutz su un calcolatore parallelo SIMD (schede GAPP), Ottavi e Parodi mostrano che il meccanismo si blocca a bassa temperatura ($T \lesssim 0.91\,T_c$) esattamente come il modello VPH/Q2R: al di sotto di questa soglia i pochi siti con energia di riserva sufficiente per ribaltare lo spin sono troppo isolati perché l'informazione si propaghi attraverso il campione, in un processo che gli autori assimilano a una **soglia di percolazione** — la lunghezza di coerenza magnetica diventa più corta della distanza media tra questi siti "fortunati" [[17]](CA-doc/Ising/ottavi1989.pdf).

Per risolvere il problema propongono due varianti che aggiungono un secondo meccanismo di trasferimento energetico indipendente dallo spin di Ising:

- il **modello del lancio (toss model)**: ogni coppia di siti primi vicini "lancia una moneta" a ogni passo, trasferendo un'unità di energia $J$ dal perdente al vincitore (a meno che il perdente sia già a energia nulla o il vincitore al massimo consentito);
- il **modello a doppio spin (double-spin model)**: si affianca al sistema di Ising originale un secondo sistema di spin, accoppiato con costante di scambio dimezzata $J' = J/2$ (e quindi temperatura critica dimezzata $T_c' = T_c/2$), che agisce da bagno termico ausiliario sempre disordinato nell'intervallo di temperature di interesse.

Entrambe le varianti restano compatibili con l'implementazione a operazioni bit a bit su architetture parallele e funzionano correttamente anche a bassa temperatura; il modello a doppio spin, in particolare, risulta più veloce del modello del lancio (non richiede un generatore di bit casuali) e viene confrontato favorevolmente, in termini di accuratezza ed efficienza per ciclo di aggiornamento, con l'algoritmo Metropolis classico — pur restando, sul hardware SIMD dell'epoca, circa dieci volte più rapido in tempo di calcolo reale [[17]](CA-doc/Ising/ottavi1989.pdf). Gli autori stimano inoltre l'esponente critico $\beta \approx 1/8.25$, in buon accordo con il valore esatto $1/8$ del modello di Ising 2D, tenuto conto delle dimensioni finite del campione simulato.

#### Verifiche moderne e generalizzazione al modello di Potts: Xiao (2023)

Un lavoro più recente riprende l'algoritmo deterministico di Creutz per verificarne la validità con gli strumenti computazionali attuali, confrontando correlazione tra primi vicini, energia interna e magnetizzazione con i risultati esatti noti per il modello di Ising 2D, e stimando l'esponente critico $\beta = 0.1069(25)$ — non compatibile, entro l'incertezza dichiarata, con il valore esatto $1/8$, una discrepanza attribuita a effetti di dimensione finita vicino a $T_c$ [[18]](CA-doc/Ising/XiaoBrian.pdf). Lo stesso schema viene poi generalizzato al **modello di Potts a $q$ stati** ($q=3,4,5$), verificando la coerenza della magnetizzazione con la temperatura critica esatta e stimando l'esponente $\beta$ anche in questo caso ($\beta \approx 0.0658(64)$ per $q=3$ e $\beta \approx 0.0650(21)$ per $q=4$), anch'esso non pienamente in accordo con i valori esatti per le stesse ragioni di taglia finita [[18]](CA-doc/Ising/XiaoBrian.pdf).

#### Il termine di confronto classico: campionamento Monte Carlo

Tutti i modelli precedenti vengono, direttamente o indirettamente, confrontati con il metodo di riferimento non basato su automi cellulari: il campionamento **Monte Carlo** di una catena di Markov che converge alla distribuzione di Boltzmann. Nella versione più semplice (algoritmo "a bagno di calore"), si sceglie uno spin a caso e lo si assegna al valore $\pm1$ con probabilità proporzionale al corrispondente fattore di Boltzmann calcolato nel campo locale dei vicini; nella versione **Metropolis**, si calcola invece la variazione di energia $\Delta E$ associata al ribaltamento di uno spin scelto a caso, accettando sempre il ribaltamento se $\Delta E<0$ e accettandolo con probabilità $e^{-\Delta E/kT}$ altrimenti [[19]](CA-doc/Ising/a4.pdf). Entrambi gli schemi sono catene di Markov **ergodiche** che soddisfano la condizione di **bilancio dettagliato**, e quindi convergono, per costruzione, a un'unica distribuzione di equilibrio — proprietà che, come mostrato da Vichniac [[15]](CA-doc/Ising/vichniac1984.pdf), nessun automa cellulare a parallelismo totale può garantire in modo altrettanto diretto. È proprio rispetto a questo standard che i modelli di Vichniac, Creutz, Ottavi–Parodi e Xiao misurano la propria validità ed efficienza computazionale.

#### Sintesi comparativa dei modelli di Ising

| Aspetto | Q2R / VPH [[15]](CA-doc/Ising/vichniac1984.pdf), [[17]](CA-doc/Ising/ottavi1989.pdf) | Creutz C2 (1986) [[16]](CA-doc/Ising/pub088-1-10.pdf) | Ottavi–Parodi (1989) [[17]](CA-doc/Ising/ottavi1989.pdf) | Xiao / Potts (2023) [[18]](CA-doc/Ising/XiaoBrian.pdf) | Monte Carlo (Metropolis/heat-bath) [[19]](CA-doc/Ising/a4.pdf) |
|---|---|---|---|---|---|
| Natura | deterministica, reversibile | deterministica, non reversibile | deterministica (2 varianti) | deterministica (algoritmo di Creutz) | stocastica (catena di Markov) |
| Variabili per sito | spin + bit di parità | spin + demone (2 bit) + parità | spin + demone(i) + parità | spin + demone (+ generalizzazione a $q$ stati) | solo spin |
| Meccanismo di trasferimento energia | scambio diretto tra vicini (flip a energia costante) | riserva locale (demone) fissa per sito | demone + lancio casuale, o secondo sistema di spin ausiliario | demone (schema di Creutz) | bagno termico esterno implicito nella regola di accettazione |
| Comportamento a bassa $T$ | si blocca in cicli-limite ($T\lesssim0.91T_c$) | si blocca in cicli-limite ($T\lesssim0.91T_c$) | corretto anche a bassa $T$ | corretto (con scarti da taglia finita vicino a $T_c$) | corretto (per definizione, ergodica) |
| Ruolo dell'ergodicità | non ergodica (simmetrie conservate) | non dimostrata ergodica | ripristinata dal meccanismo ausiliario | eredita il meccanismo di Creutz | ergodica per costruzione (bilancio dettagliato) |
| Uso principale nella tesi | riferimento storico/concettuale, limite della parallelizzazione | riferimento per l'algoritmo "a demone" | correzioni pratiche per l'implementazione | verifica/estensione a Potts, benchmark critico | termine di paragone quantitativo |

Il filo conduttore di questa sezione è complementare a quello dei modelli SIR e Fire descritti in precedenza: mentre in quei modelli l'automa cellulare serve a *generare* un fenomeno di propagazione a partire da regole locali, nel caso di Ising l'automa cellulare deve *riprodurre* una distribuzione di equilibrio nota a priori — un compito più vincolato, in cui il parallelismo totale proprio degli automi cellulari si scontra con la struttura a due corpi dell'energia, imponendo l'introduzione di meccanismi ausiliari (parità, demoni, sistemi di spin accessori) assenti nei modelli di propagazione spaziale.

---

## Scelte di implementazione

### Perché servono scelte implementative concrete

La definizione formale di automa cellulare — la quadrupla $(C,Q,V,f)$ vista nell'introduzione — lascia aperti diversi gradi di libertà che i modelli teorici presentati nei capitoli precedenti non sempre fissano in modo univoco: la dimensione e la finitezza della griglia, il trattamento dei bordi, il raggio e la forma esatta del vicinato, la natura sincrona o asincrona dell'aggiornamento. Per passare dalla teoria al codice queste scelte vanno rese esplicite, in modo coerente per tutti e tre i modelli, cosicché il confronto fra di essi sia significativo.

### Come si è proceduto

In questa tesi i tre modelli (SIR, incendio boschivo, Ising) sono implementati su una griglia quadrata bidimensionale $G=\mathbb{Z}^2$, con vicinato di raggio 1 di tipo **von Neumann** (4 vicini, distanza di Manhattan) o **Moore** (8 vicini, distanza di Chebyshev) a seconda del modello. Per ciascun modello la griglia può essere trattata come **finita** — le celle di bordo e d'angolo hanno un vicinato incompleto, limitato alle sole celle interne alla griglia — oppure come **toroidale**, un'approssimazione pratica dell'infinitezza in cui il vicinato "avvolge" la griglia sui lati opposti, cosicché ogni cella (bordi e angoli inclusi) abbia sempre un vicinato completo.

La logica di evoluzione dei tre modelli è scritta in C (compilata in librerie condivise) e pilotata da Python tramite `ctypes`, con visualizzazione in `pygame`. L'aggiornamento della griglia avviene per la maggior parte dei modelli con un doppio buffer: la regola legge dalla griglia al passo corrente e scrive su una griglia di appoggio, scambiate a fine passo, così da garantire un aggiornamento **sincrono** in cui il nuovo stato di ogni cella dipende solo dalla configurazione al passo precedente. Il generatore di numeri pseudocasuali usato per le componenti probabilistiche delle regole è un `xorshift32`.

### Metodi scelti in questo lavoro

**Modello SIR.** Lo stato di cella è un contatore intero: `0` indica un individuo suscettibile, i valori successivi la progressione attraverso l'infezione e poi la resistenza, fino a una soglia finale oltre la quale la cella torna suscettibile (variante SIRS) o resta immune per sempre (SIR puro). Il vicinato è di **von Neumann** su griglia **toroidale**; una cella suscettibile diventa infetta con una prova di contagio indipendente per ciascun vicino infetto, ciascuna con probabilità fissa. È, nella sostanza, una versione semplificata dell'idea di contatore di fase di Fuentes–Kuperman, qui applicata a un vicinato più ristretto e con propagazione probabilistica per singolo vicino anziché tramite un campo di vicinato aggregato.

**Modello di incendio boschivo.** Lo stato di cella è discreto su quattro valori (vuoto, albero, albero in fiamme, albero bruciato), su vicinato di **Moore** e griglia **toroidale**. Un albero prende fuoco con una probabilità che dipende, per ciascun vicino in fiamme, dall'allineamento tra la sua direzione relativa e la direzione del vento (probabilità massima sottovento, pressoché nulla controvento); un albero in fiamme diventa bruciato al passo successivo, senza ricrescita. Lo schema riprende così, in forma discreta e probabilistica, l'idea di matrice di propagazione anisotropa modulata dal vento introdotta da Karafyllidis–Thanailakis e ripresa da Alexandridis et al., senza includere pendenza, tipo di vegetazione o spotting.

**Modello di Ising.** Lo stato di cella è uno spin $\pm1$ su vicinato di **von Neumann**, con boundary selezionabile (periodico o aperto). A differenza degli altri due modelli, l'aggiornamento è **asincrono**: a ogni passo viene tentato il flip di una singola cella scelta a caso, accettato secondo il criterio di **Metropolis** (sempre se l'energia diminuisce, altrimenti con probabilità $e^{-\Delta E/T}$) — la stessa dinamica presa come termine di paragone classico nel capitolo precedente, piuttosto che una delle regole deterministiche a scacchiera (Q2R, demoni di Creutz) discusse in teoria. È una scelta implementativa consapevole: Metropolis è l'algoritmo di riferimento più semplice da realizzare correttamente ed è quello rispetto a cui gli altri schemi vengono giudicati.

Accanto a queste tre implementazioni in C, sono stati realizzati anche due prototipi preliminari in solo Python/NumPy: una prima variante del modello SIR con vicinato di Moore e probabilità di contagio fissa, e un automa eccitabile deterministico in stile Greenberg–Hastings che genera fronti d'onda propagantisi sulla griglia — utili come banco di prova concettuale prima del passaggio all'implementazione in C.

---

## Bibliografia

[1] W. O. Kermack, A. G. McKendrick, *Contributions to the mathematical theory of epidemics, part I*, Proc. Roy. Soc. Edin. A **115** (1927) 700–721.

[[2]](CA-doc/SIR/Cellular-automata-and-epidemiological-mo_1999_Physica-A--Statistical-Mechani.pdf) M. A. Fuentes, M. N. Kuperman, *Cellular automata and epidemiological models with spatial dependence*, Physica A **267** (1999) 471–486.

[[3]](CA-doc/SIR/A%20Model%20Based%20on%20Cellular%20Automata%20to%20Simulate%20Epidemic%20Diseases.pdf) S. H. White, A. Martín del Rey, G. Rodríguez Sánchez, *A model based on cellular automata to simulate epidemic diseases*, in: S. El Yacoubi, B. Chopard, S. Bandini (Eds.), ACRI 2006, LNCS **4173**, pp. 304–310, Springer, Heidelberg.

[[4]](CA-doc/SIR/Modeling%20epidemics%20using%20cellular%20automata.pdf) S. H. White, A. Martín del Rey, G. Rodríguez Sánchez, *Modeling epidemics using cellular automata*, Applied Mathematics and Computation **186** (2007) 193–202.

[[5]](CA-doc/SIR/Spreadable%20Probabilistic%20Cellular%20Automata%20Models%3A%20An%20Application%20in%20Epidemiology.pdf) R. Slimi, S. El Yacoubi, *Spreadable probabilistic cellular automata models: an application in epidemiology*, in: S. El Yacoubi, B. Chopard, S. Bandini (Eds.), ACRI 2006, LNCS **4173**, pp. 330–336, Springer, Heidelberg.

[[6]](CA-doc/SIR/A%20Cellular%20Automata%20SIR%20Model%20for%20Landscape%20Epidemiology.pdf) E. L. Landguth, *A cellular automata SIR model for landscape epidemiology* (2007).

[[7]](CA-doc/Fire/Forestfire.pdf) P. Bak, K. Chen, C. Tang, *A forest-fire model and some thoughts on turbulence*, Physics Letters A **147** (1990) 297–300.

[[8]](CA-doc/Fire/PhysRevLett.69.1629.pdf) B. Drossel, F. Schwabl, *Self-organized criticality in a forest-fire model*, Physical Review Letters **69** (1992) 1629–1632.

[[9]](CA-doc/Fire/clar_drossel_schwabl_review.pdf) S. Clar, B. Drossel, F. Schwabl, *Forest fires and other examples of self-organized criticality*, Journal of Physics: Condensed Matter **8** (1996) 6803–6824 (arXiv:cond-mat/9610201).

[[10]](CA-doc/Fire/green1983.pdf) D. G. Green, *Shapes of simulated fires in discrete fuels*, Ecological Modelling **20** (1983) 21–32.

[[11]](CA-doc/Fire/karafyllidis_1997.pdf) I. Karafyllidis, A. Thanailakis, *A model for predicting forest fire spreading using cellular automata*, Ecological Modelling **99** (1997) 87–97.

[[12]](CA-doc/Fire/10.1016@j.advengsoft.2006.09.002.pdf) A. Hernández Encinas, L. Hernández Encinas, S. Hoya White, A. Martín del Rey, G. Rodríguez Sánchez, *Simulation of forest fire fronts using cellular automata*, Advances in Engineering Software **38** (2007) 372–378.

[[13]](CA-doc/Fire/alexandridis2008.pdf) A. Alexandridis, D. Vakalis, C. I. Siettos, G. V. Bafas, *A cellular automata model for forest fire spread prediction: the case of the wildfire that swept through Spetses Island in 1990*, Applied Mathematics and Computation **204** (2008) 191–201.

[[14]](CA-doc/Fire/probabilistic_ca_2024.pdf) R. Ghosh, J. Adhikary, R. Chemlal, *Fire Spread Modeling using Probabilistic Cellular Automata*, Summer School on Cellular Automata Technology (2023) — sede di pubblicazione definitiva non accertata, si veda la nota bibliografica.

[[15]](CA-doc/Ising/vichniac1984.pdf) G. Y. Vichniac, *Simulating physics with cellular automata*, Physica D **10** (1984) 96–116.

[[16]](CA-doc/Ising/pub088-1-10.pdf) M. Creutz, *Deterministic Ising dynamics*, Annals of Physics **167** (1986) 62–72.

[[17]](CA-doc/Ising/ottavi1989.pdf) H. Ottavi, O. Parodi, *Simulation of the Ising model by cellular automata*, Europhysics Letters **8** (8) (1989) 741–746.

[[18]](CA-doc/Ising/XiaoBrian.pdf) B. Xiao, *Cellular Automata Algorithms for Lattice Models*, MIT 8.334 course paper (2023).

[[19]](CA-doc/Ising/a4.pdf) Note del corso *Statistical Mechanics*, University of Sydney (S. Flammia) — *Ising model and Metropolis Monte Carlo*.

[20] R. C. Rothermel, *A mathematical model for predicting fire spread in wildland fuels*, Research Paper INT-115, USDA Forest Service, Intermountain Forest and Range Experiment Station, Ogden, UT (1972).

[21] P. Grassberger, H. Kantz, *On a forest fire model with supposed self-organized criticality*, Journal of Statistical Physics **63** (1991) 685–700.

---

> **Nota bibliografica (modelli SIR).** La struttura generale dei modelli SIR/SIS/SEIR e i limiti dell'approccio a ODE sono tratti da [1], [[3]](CA-doc/SIR/A%20Model%20Based%20on%20Cellular%20Automata%20to%20Simulate%20Epidemic%20Diseases.pdf) e [[4]](CA-doc/SIR/Modeling%20epidemics%20using%20cellular%20automata.pdf); l'impianto formale dell'automa cellulare — quadrupla $(C,Q,V,f)$, vicinati di von Neumann e Moore — da [[3]](CA-doc/SIR/A%20Model%20Based%20on%20Cellular%20Automata%20to%20Simulate%20Epidemic%20Diseases.pdf). Il modello di Fuentes–Kuperman (campi $\sigma_{ij}$ e $u_{ij}$, i tre stati $t_i, t_p, t_l$, le regole di evoluzione, la funzione $F$ e le varianti SIS/SIR/SIRS) è basato su [[2]](CA-doc/SIR/Cellular-automata-and-epidemiological-mo_1999_Physica-A--Statistical-Mechani.pdf); la sua variante stocastica, dovuta a Landguth [[6]](CA-doc/SIR/A%20Cellular%20Automata%20SIR%20Model%20for%20Landscape%20Epidemiology.pdf), non è più trattata in una sottosezione dedicata in questa versione del documento. Il modello *spreadability* (concetto di spreadability, indicatore $\pi$, densità locale, funzioni di nascita $\nu$ e sopravvivenza $\sigma$, regola generica probabilistica e modello SIR a tre stati con probabilità $p_i, p_s, p_r$) è basato su [[5]](CA-doc/SIR/Spreadable%20Probabilistic%20Cellular%20Automata%20Models%3A%20An%20Application%20in%20Epidemiology.pdf). Il modello CA-SIR di White, del Rey e Sánchez (stato a tripla $(S,I,R)$, funzione di transizione, calcolo dell'influenza del vicinato con $\mu = c \cdot m \cdot v$, condizione di soglia e numero riproduttivo $X$) è basato su [[3]](CA-doc/SIR/A%20Model%20Based%20on%20Cellular%20Automata%20to%20Simulate%20Epidemic%20Diseases.pdf), [[4]](CA-doc/SIR/Modeling%20epidemics%20using%20cellular%20automata.pdf); non ha più una sottosezione propria in questa versione del documento e viene richiamato solo nella sintesi generale finale. Si segnala che l'espressione del numero riproduttivo $X$ andrebbe verificata sull'originale [[4]](CA-doc/SIR/Modeling%20epidemics%20using%20cellular%20automata.pdf), Eq. 16, poiché la sua estrazione dal testo era parzialmente illeggibile.

> **Nota bibliografica (modelli Fire).** L'apertura del capitolo (rilevanza degli incendi boschivi, modello di Rothermel e limiti dell'approccio a PDE, le due direttrici predittiva/statistico-fisica, il ponte con la modellizzazione epidemica) è tratta da `introduzione-incendi.md`, un documento distinto poi fuso in questa sede, basato su [[11]](CA-doc/Fire/karafyllidis_1997.pdf) e [20]; la critica di Grassberger e Kantz all'universalità della criticità autoorganizzata è basata su [21]. Il modello di autorganizzazione critica è basato su [[7]](CA-doc/Fire/Forestfire.pdf) (versione originale senza fulmine, di Bak, Chen e Tang) e su [[8]](CA-doc/Fire/PhysRevLett.69.1629.pdf) (introduzione del parametro di fulmine $f$ e degli esponenti critici fondamentali); gli esponenti critici dettagliati, le relazioni di scala e la variante con immunità $g$ sono tratti dalla review [[9]](CA-doc/Fire/clar_drossel_schwabl_review.pdf). Il modello di Green (template di accensione, modelli a contatto e ad accumulo di calore, forma del fronte in funzione della continuità del combustibile) è basato su [[10]](CA-doc/Fire/green1983.pdf); si segnala che [[10]](CA-doc/Fire/green1983.pdf) non formalizza esplicitamente una soglia di percolazione, a differenza di quanto il titolo/contesto potrebbe suggerire — il collegamento con la percolazione resta qualitativo. Il modello di Karafyllidis–Thanailakis (stato continuo, vicinato di Moore, coefficiente diagonale $0.83$, pesi direzionali per vento e pendenza) è basato su [[11]](CA-doc/Fire/karafyllidis_1997.pdf). Il modello di Hernández Encinas et al. (formalizzazione a quadrupla, coefficiente diagonale corretto $\pi/4$, caso disomogeneo) è basato su [[12]](CA-doc/Fire/10.1016@j.advengsoft.2006.09.002.pdf); si segnala che il file sorgente di questo paper era originariamente etichettato come "Alexandridis 2006 / incendio di Spetses" ma il suo contenuto reale corrisponde a Hernández Encinas et al. (2007) — l'attribuzione bibliografica [[12]](CA-doc/Fire/10.1016@j.advengsoft.2006.09.002.pdf) riflette il contenuto effettivamente letto, non l'etichetta del file. Il modello di Alexandridis et al. (stati discreti, regola moltiplicativa $p_{burn}$, fattori vento/pendenza/spotting, calibrazione quantitativa sull'incendio di Spetses 1990) è basato su [[13]](CA-doc/Fire/alexandridis2008.pdf), che è il vero paper Alexandridis–Vakalis–Siettos–Bafas (2008). Gli sviluppi recenti (regola di ignizione a sigmoide, stati TREE/BURNING/BURNING DURATION/EMPTY/WATER/CITY, integrazione GIS, validazione su Spetses 1990 ed Evia 2021) sono basati su [[14]](CA-doc/Fire/probabilistic_ca_2024.pdf), la cui sede di pubblicazione non è accertabile con certezza dal solo testo del PDF (si dichiara solo un collegamento alla Summer School on Cellular Automata Technology, 2023) e andrebbe verificata prima di un uso in bibliografia definitiva.

> **Nota bibliografica (modello di Ising).** La sezione su Vichniac (Hamiltoniana di Ising, argomento contro la parallelizzazione totale, regola Q2R e sua identificazione con il modello VPH, collegamento a frustrazione e vetri di spin) è basata su [[15]](CA-doc/Ising/vichniac1984.pdf), letto direttamente dal PDF (pp. 104-109 dell'edizione originale). La sezione su Creutz è un rimando al riassunto dedicato [pub088-creutz1986-summary.md](Ising/pub088-creutz1986-summary.md), basato su [[16]](CA-doc/Ising/pub088-1-10.pdf); per lo stesso motivo di tutela del copyright non è stata prodotta una trascrizione integrale di [[16]](CA-doc/Ising/pub088-1-10.pdf), ma solo un riassunto strutturato con le equazioni e i risultati numerici principali. La sezione su Ottavi–Parodi (fallimento a bassa temperatura, analogia con la percolazione, modello del lancio e modello a doppio spin, confronto con Metropolis, stima di $\beta\approx1/8.25$) è basata su [[17]](CA-doc/Ising/ottavi1989.pdf), di cui nella cartella `Ising/` è disponibile una trascrizione completa in [ottavi1989.md](Ising/ottavi1989.md). La sezione su Xiao (verifica dell'algoritmo di Creutz, stima di $\beta=0.1069(25)$, estensione al modello di Potts per $q=3,4,5$) è basata su [[18]](CA-doc/Ising/XiaoBrian.pdf). La sezione sul confronto Monte Carlo (algoritmo a bagno di calore, algoritmo Metropolis, bilancio dettagliato ed ergodicità delle catene di Markov) è basata su [[19]](CA-doc/Ising/a4.pdf), note didattiche che non riportano un anno di pubblicazione verificabile nel PDF sorgente.

> **Nota bibliografica (introduzione generale e scelte di implementazione).** Alcuni dettagli storici dell'introduzione generale ai CA (costruzione universale di von Neumann, Turing-completezza del Game of Life) e l'intero capitolo "Scelte di implementazione" sono tratti da un documento distinto, `descrizione_modelli.md`, poi fuso in questa sede; quest'ultimo descrive nel dettaglio, con tabelle di parametri e frammenti di codice qui volutamente omessi per brevità, l'implementazione in C/Python dei tre modelli nella cartella `CellularAutomata-SIR` — si rimanda a quel documento per il dettaglio implementativo completo (parametri di default, convenzioni di segno, note sul generatore di numeri casuali).
