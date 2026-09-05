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

Il modello SIR e le sue varianti nascono per simulare la propagazione spaziale delle malattie infettive in una popolazione. Il punto di partenza moderno è il lavoro di Kermack e McKendrick (1927), che introduce i cosiddetti modelli *compartimentali* [1], [[4]](CA-doc/SIR/Modeling%20epidemics%20using%20cellular%20automata.pdf). Nel modello SIR la popolazione è suddivisa in tre classi [[3]](CA-doc/SIR/A%20Model%20Based%20on%20Cellular%20Automata%20to%20Simulate%20Epidemic%20Diseases.pdf), [[4]](CA-doc/SIR/Modeling%20epidemics%20using%20cellular%20automata.pdf):

- **suscettibili** $S$ — gli individui che possono contrarre la malattia;
- **infetti** $I$ — gli individui in grado di trasmettere la malattia;
- **rimossi/guariti** $R$ — gli individui immuni, guariti in modo definitivo o deceduti.

Il modello SIR si applica alle malattie che conferiscono immunità: il ciclo di un individuo tipico attraversa in sequenza gli stati $S \to I \to R$ [[2]](CA-doc/SIR/Cellular-automata-and-epidemiological-mo_1999_Physica-A--Statistical-Mechani.pdf). La sua formulazione classica, di tipo deterministico, è un sistema di equazioni differenziali ordinarie (ODE):

$$
\frac{dS}{dt} = -\beta\, S I
\qquad
\frac{dI}{dt} = \beta\, S I - \gamma I
\qquad
\frac{dR}{dt} = \gamma I
$$

dove $\beta$ è il tasso di contagio effettivo e $\gamma$ il tasso di guarigione. Poiché la popolazione totale è costante, vale in ogni istante il vincolo

$$
S(t) + I(t) + R(t) = N
$$

Una grandezza cruciale, che ricorrerà in forme diverse anche nei modelli ad automi cellulari, è l'indice di contagio $R_0 = \beta S(0)/\gamma$, che rappresenta il numero medio di contagi secondari prodotti da un singolo infetto in una popolazione interamente suscettibile: la soglia epidemica è $R_0=1$ (se $R_0<1$ l'epidemia si estingue, se $R_0>1$ si diffonde) [1].

Varianti dello schema si ottengono modificando il comportamento della popolazione: il modello SIS (nessuna immunità, l'individuo torna suscettibile: $S \to I \to S$) elimina la classe $R$; il modello SEIR introduce una classe di *esposti* $E$ per il periodo latente (infetto ma non ancora infettivo); esistono inoltre gli schemi SIRS, SEIRS, ecc. [[3]](CA-doc/SIR/A%20Model%20Based%20on%20Cellular%20Automata%20to%20Simulate%20Epidemic%20Diseases.pdf), [[4]](CA-doc/SIR/Modeling%20epidemics%20using%20cellular%20automata.pdf).

I modelli basati su ODE, pur eleganti, presentano limiti importanti perché trascurano le caratteristiche *locali* del processo di diffusione. In particolare non riescono a simulare in modo adeguato [[4]](CA-doc/SIR/Modeling%20epidemics%20using%20cellular%20automata.pdf):

1. i processi di contatto tra i singoli individui;
2. gli effetti del comportamento individuale;
3. gli aspetti *spaziali* della diffusione epidemica;
4. gli effetti dei pattern di mescolamento (*mixing*) della popolazione.

D'altra parte, proprio perché la popolazione totale resta costante nel tempo, lo stato epidemiologico di ciascun individuo — o di ciascuna porzione di territorio — può essere naturalmente rappresentato come un elemento di un insieme finito di stati che evolve secondo una regola locale: è esattamente la struttura di un automa cellulare. I CA permettono così di superare i limiti dei modelli ODE mantenendo un costo computazionale nettamente inferiore rispetto all'integrazione di sistemi di equazioni differenziali, e includendo in modo diretto caratteristiche epidemiologiche come la presenza di un agente esterno o le diverse fasi del periodo infettivo [[2]](CA-doc/SIR/Cellular-automata-and-epidemiological-mo_1999_Physica-A--Statistical-Mechani.pdf), [[4]](CA-doc/SIR/Modeling%20epidemics%20using%20cellular%20automata.pdf). 

sono state identificate diverse metodologie per studiare questo problema, delle quali analizzeremo il lavoro di Fuentes-Kuperman e di Slimi - El Yacoubi

### Fuentes – Kuperman

Fuentes e Kuperman propongono un CA che riproduce gli stessi termini presenti nelle equazioni SIS/SIR classiche, ma in un "linguaggio" differente [[2]](CA-doc/SIR/Cellular-automata-and-epidemiological-mo_1999_Physica-A--Statistical-Mechani.pdf). Ogni cella della griglia rappresenta un singolo individuo, il cui stato è determinato univocamente da due campi [[2]](CA-doc/SIR/Cellular-automata-and-epidemiological-mo_1999_Physica-A--Statistical-Mechani.pdf):

- $\sigma_{ij}(t)$ — legato allo *stato epidemiologico* dell'individuo (funge da *contatore* dell'avanzamento nel periodo infettivo);
- $u_{ij}(t)$ — legato allo stato del vicinato, ossia alla probabilità di transizione dallo stato attuale a un altro (il termine che porta l'informazione di contatto/contagio).

#### Le tre fasi del periodo infettivo: $t_i$, $t_p$, $t_l$

La caratteristica distintiva del modello è la suddivisione del periodo infettivo in tre fasi [[2]](CA-doc/SIR/Cellular-automata-and-epidemiological-mo_1999_Physica-A--Statistical-Mechani.pdf). Ogni volta che un individuo viene infettato, egli attraversa in successione queste tre fasi, permanendo mediamente in ciascuna per un tempo caratteristico definito [[2]](CA-doc/SIR/Cellular-automata-and-epidemiological-mo_1999_Physica-A--Statistical-Mechani.pdf):

| Fase | Tempo caratteristico | Descrizione | Infettivo? | Sintomatico? |
|------|:---:|-------------|:---:|:---:|
| **Incubazione** | $t_i$ | l'individuo è già infetto e infettivo, ma non presenta ancora sintomi | sì | no |
| **Infezione propria** | $t_p$ | l'individuo è infettivo e mostra i sintomi | sì | sì |
| **Latenza** | $t_l$ | l'individuo non è più infettivo ma presenta ancora i sintomi | no | sì |

Questa formulazione è generale: ponendo $t_i = 0$ o $t_l = 0$ si possono includere in modo naturale i casi in cui l'incubazione o la latenza sono trascurabili [[2]](CA-doc/SIR/Cellular-automata-and-epidemiological-mo_1999_Physica-A--Statistical-Mechani.pdf). Dal punto di vista epidemiologico, la fase di latenza agisce di fatto come una breve *immunità temporanea*, che riduce la densità media stazionaria di infetti a parità degli altri parametri [[2]](CA-doc/SIR/Cellular-automata-and-epidemiological-mo_1999_Physica-A--Statistical-Mechani.pdf).

Il contatore $\sigma_{ij}(t)$ percorre dunque l'intero periodo infettivo, di durata complessiva

$$
T = t_i + t_p + t_l
$$

#### Le regole di evoluzione

Nel caso base (senza immunità permanente), le regole che governano l'evoluzione del campo $\sigma_{ij}$ sono [[2]](CA-doc/SIR/Cellular-automata-and-epidemiological-mo_1999_Physica-A--Statistical-Mechani.pdf):

$$
\sigma_{ij}(t+1) =
\begin{cases}
\sigma_{ij}(t) + 1 & \text{se } 0 < \sigma_{ij}(t) < t_i + t_p + t_l \\
0 & \text{se } \sigma_{ij}(t) = t_i + t_p + t_l \\
0 & \text{se } \sigma_{ij}(t) = 0 \ \text{ e } \ u_{ij}(t+1) < h \\
1 & \text{se } \sigma_{ij}(t) = 0 \ \text{ e } \ u_{ij}(t+1) \ge h
\end{cases}
$$

dove [[2]](CA-doc/SIR/Cellular-automata-and-epidemiological-mo_1999_Physica-A--Statistical-Mechani.pdf):

- la prima riga fa avanzare di uno il contatore per un individuo che si trova all'interno del periodo infettivo (progressione automatica attraverso le tre fasi $t_i \to t_p \to t_l$);
- la seconda riga riporta a $0$ (guarigione) l'individuo che ha completato l'intero periodo $T$;
- la terza e quarta riga governano il *contagio* di un individuo suscettibile ($\sigma_{ij} = 0$): esso diventa infetto ($\sigma_{ij} = 1$) solo se il campo di vicinato $u_{ij}$ supera una *soglia casuale* $h$, dove $h$ è un numero aleatorio nell'intervallo $[0,1]$ con distribuzione di probabilità $p(h)$ definita caso per caso.

#### Il campo di vicinato $u_{ij}$

Il campo $u_{ij}(t)$ raccoglie l'influenza infettiva proveniente dai vicini, pesata in funzione della distanza per "gusci" (shell) successivi [[2]](CA-doc/SIR/Cellular-automata-and-epidemiological-mo_1999_Physica-A--Statistical-Mechani.pdf):

$$
u_{ij}(t+1) = \frac{1}{N}\left(
\sum_{\text{1° vicini}} I_{ij}(t)\, e^{-1}
+ \sum_{\text{2° vicini}} I_{ij}(t)\, e^{-2}
+ \sum_{\text{3° vicini}} I_{ij}(t)\, e^{-3}
+ \cdots
\right)
$$

dove i termini successivi corrispondono alle somme sui vicini di primo, secondo, terzo ordine e così via, con peso esponenziale decrescente $e^{-k}$ per il $k$-esimo guscio [[2]](CA-doc/SIR/Cellular-automata-and-epidemiological-mo_1999_Physica-A--Statistical-Mechani.pdf). La costante di normalizzazione è

$$
N = \frac{1}{4}\left(e^{-1} + e^{-2} + e^{-3} + \cdots\right).
$$

Il contributo infettivo di ciascuna cella è a sua volta determinato dalla funzione $F$ [[2]](CA-doc/SIR/Cellular-automata-and-epidemiological-mo_1999_Physica-A--Statistical-Mechani.pdf):

$$
I_{ij}(t+1) =
\begin{cases}
F\left(
\sigma_{ij}(t)\right), & \text{se } \sigma_{ij}(t) \ge 1 \\
0 & \text{se } \sigma_{ij}(t) \le 0
\end{cases}
$$

dove $F(t): (0,\, t_i + t_p + t_l) \to \mathbb{R}^+$ è una funzione reale positiva, nulla al di fuori dell'intervallo del periodo infettivo, che rappresenta l'*infettività* in funzione della fase raggiunta [[2]](CA-doc/SIR/Cellular-automata-and-epidemiological-mo_1999_Physica-A--Statistical-Mechani.pdf). La scelta più semplice è una funzione a gradini (di tipo Heaviside) che assume un valore costante in ciascuna delle tre fasi [[2]](CA-doc/SIR/Cellular-automata-and-epidemiological-mo_1999_Physica-A--Statistical-Mechani.pdf):

$$
F\!\left(\sigma_{ij}(t)\right) =
\begin{cases}
f_i & \text{se } 0 < \sigma_{ij}(t) \le t_i \quad \text{(incubazione)} \\
f_p & \text{se } t_i < \sigma_{ij}(t) \le t_i + t_p \quad \text{(infezione propria)} \\
f_l & \text{se } t_i + t_p < \sigma_{ij}(t) \le t_i + t_p + t_l \quad \text{(latenza)}
\end{cases}
$$

Regolando $f_i$, $f_p$ e $f_l$ (ad esempio ponendo $f_l = 0$ per rendere la latenza non infettiva) si modula il grado di contagiosità in ciascuna fase, calibrando così il modello sulle caratteristiche della specifica malattia [[2]](CA-doc/SIR/Cellular-automata-and-epidemiological-mo_1999_Physica-A--Statistical-Mechani.pdf).

#### Varianti SIS, SIR e SIRS

Il modello incorpora in modo unificato le diverse tipologie epidemiche tramite un periodo di immunità di durata $t_r$, estendendo il contatore a valori negativi [[2]](CA-doc/SIR/Cellular-automata-and-epidemiological-mo_1999_Physica-A--Statistical-Mechani.pdf):

$$
\sigma_{ij}(t+1) =
\begin{cases}
\sigma_{ij}(t) + 1 & \text{se } 0 < \sigma_{ij}(t) < t_i + t_p + t_l \\
-1 & \text{se } \sigma_{ij}(t) = t_i + t_p + t_l  \\
\sigma_{ij}(t) - 1 & \text{se } -t_r \le \sigma_{ij}(t) < 0 \\
0 & \text{se } \sigma_{ij}(t) < -t_r \\
0 & \text{se } \sigma_{ij}(t) = 0 \ \text{ e } \ u_{ij}(t+1) < h \\
1 & \text{se } \sigma_{ij}(t) = 0 \ \text{ e } \ u_{ij}(t+1) \ge h
\end{cases}
$$

I valori negativi del contatore rappresentano il periodo di immunità. Da questo schema generale si ottengono i casi particolari [[2]](CA-doc/SIR/Cellular-automata-and-epidemiological-mo_1999_Physica-A--Statistical-Mechani.pdf):

- $t_r \to \infty$: immunità permanente $\Rightarrow$ modello *SIR*;
- $t_r = 0$: nessuna immunità $\Rightarrow$ modello *SIS*;
- $t_r \ne 0$ (finito): immunità temporanea $\Rightarrow$ modello *SIRS*.

Le simulazioni mostrano l'esistenza di un *valore di soglia critico* $f_c$ per il parametro di infettività: al di sotto di $f_c$ l'infezione non riesce a sostenersi e l'epidemia si estingue, mentre al di sopra si raggiunge una densità media stazionaria di infetti [[2]](CA-doc/SIR/Cellular-automata-and-epidemiological-mo_1999_Physica-A--Statistical-Mechani.pdf). In prossimità della soglia, la densità asintotica $I_a$ segue una legge di potenza di tipo critico [[2]](CA-doc/SIR/Cellular-automata-and-epidemiological-mo_1999_Physica-A--Statistical-Mechani.pdf):

$$
I_a = A\,\lvert f - f_c \rvert^{\nu},
$$

analoga a una transizione di fase.

Va segnalato che il modello, così come proposto da Fuentes e Kuperman, non formalizza una variante SEIR a sé stante tramite $t_r$: la fase di incubazione $t_i$ descrive già un individuo infetto ma non ancora sintomatico, che nello schema resta però infettivo — a differenza della classe "esposta" $E$ dei modelli SEIR classici, che per definizione non è infettiva. Un'eventuale variante SEIR richiederebbe quindi l'aggiunta di una quarta fase, non infettiva, precedente a $t_i$.

### Spreadability (Slimi–El - Yacoubi)

Un secondo approccio, dovuto a Slimi e El Yacoubi, non nasce come modello epidemiologico in senso stretto, ma come teoria generale della *spreadability*, cioè della propagazione spaziale di una qualunque proprietà [[5]](CA-doc/SIR/Spreadable%20Probabilistic%20Cellular%20Automata%20Models%3A%20An%20Application%20in%20Epidemiology.pdf). Il concetto nasce nell'ambito dei sistemi a parametri distribuiti descritti da equazioni alle derivate parziali, dove si studia come un dominio iniziale limitato, in cui una certa proprietà spaziale $\mathcal{P}$ è verificata, si espanda o si riassorba nel tempo. Esempi tipici di $\mathcal{P}$ sono una copertura vegetale, un'area di inquinamento, oppure una zona di popolazione infetta [[5]](CA-doc/SIR/Spreadable%20Probabilistic%20Cellular%20Automata%20Models%3A%20An%20Application%20in%20Epidemiology.pdf). Inizialmente questo approccio vienete trattato tramite equazioni differeniali, ma per migliorare il tempo computazionale, viene formulato il processo come metodo per gli automi cellulari.

$(C, Q, V, f)$

Introduciamo una mappa indicatrice $\pi$ che indica per ognis stato dell'automa se questo soddisfa o meno la proprietà:[[5]](CA-doc/SIR/Spreadable%20Probabilistic%20Cellular%20Automata%20Models%3A%20An%20Application%20in%20Epidemiology.pdf):

$$
\pi: Q \longrightarrow \{0,1\}, \qquad
\pi(x) =
\begin{cases}
1, & \text{se } x \text{ soddisfa } \mathcal{P}, \\
0, & \text{altrimenti,}
\end{cases}
$$

<!-- il cui supporto è $K = \{x \in Q \mid \pi(x) = 1\}$: l'insieme degli stati che, per definizione, "contano come" $\mathcal{P}$. -->

A partire da $\pi$ si definisce come *dominio* $\Omega$, l'insieme delle celle che soddisfano $\mathcal{P}$ in un determinato istante di tempo $t$ 
$$\Omega_t = \{c \in L \mid \pi(s_t(c)) = 1\}$$

intuiitivamente si definisce la successione dei domini per ogni istante di tempo [[5]](CA-doc/SIR/Spreadable%20Probabilistic%20Cellular%20Automata%20Models%3A%20An%20Application%20in%20Epidemiology.pdf):

$$
\{\Omega_t\}_{t} = \Omega_0,\, \Omega_1,\, \Omega_2,\, \dots
$$

Il CA si dice $\mathcal{P}$-spreadable a partire da un dominio iniziale $\Omega_0$ se la successione dei domini è crescente [[5]](CA-doc/SIR/Spreadable%20Probabilistic%20Cellular%20Automata%20Models%3A%20An%20Application%20in%20Epidemiology.pdf):

$$
\Omega_t \subseteq \Omega_{t+1}.
$$

Questa crescita monotona è la condizione che *definisce* la spreadability, ma  non è imposta a priori sulla regola locale: è una conseguenza che si verifica a seconda della regola di transizione locale.

Lo studio della dinamica globale è utile quindi ad analizzare come la proprietà si diffonda nel modello, ma lo stesso approcio può essere utilizzato anche per lo studio della dinamica e quindi la regola locale. La probabilità che una cella acquisisca un certo stato, dipende anche dalla densità di $\mathcal{P}$ nel suo vicinato $V_c$, cioè da quanti vicini la possiedono già. La densità locale si espireme come [[5]](CA-doc/SIR/Spreadable%20Probabilistic%20Cellular%20Automata%20Models%3A%20An%20Application%20in%20Epidemiology.pdf):

$$
y_t(c) = \sum_{c' \in \dot{N}(c)} \pi\!\left(s_t(c')\right),
\qquad
p_t(c) = \frac{y_t(c)}{n},
$$

dove $n = |V_c|$ è la dimensione del vicinato e $\dot{V}_c = N_c \setminus \{c\}$ il vicinato privato della cella centrale; $y_t(c)$ conta quindi quanti vicini di $c$ soddisfano $\mathcal{P}$ al istante $t$, e $p_t(c)$ ne è la frazione.

Su questa densità locale sono costruite due regole probabilistiche, che governano rispettivamente la nascita e la sopravvivenza della proprietà $\mathcal{P}$ in una cella. Costruiamo una semplice mappa $\nu: [0,1[\rightarrow \{0,1\}$ che viene accettata con una certa probabiltà se la densità intorno a una certa cella supera la soglia di contagio [[5]](CA-doc/SIR/Spreadable%20Probabilistic%20Cellular%20Automata%20Models%3A%20An%20Application%20in%20Epidemiology.pdf):



$$
\nu(c) =
\begin{cases}
1, & \text{se } p_t(c) \ge \theta_1 \ \text{ con probabilità } p_1, \\
0, & \text{altrimenti,}
\end{cases}
$$

dove $0 \le \theta_1 \le 1$ è la soglia di nascita e $p_1$ la probabilità con cui la nascita si realizza una volta superata la soglia. La funzione di sopravvivenza $\sigma: K \to K$ regola invece il mantenimento della proprietà in una cella che già la possiede; nella versione probabilistica è definita, in modo simmetrico, da una soglia sulla stessa densità locale [[5]](CA-doc/SIR/Spreadable%20Probabilistic%20Cellular%20Automata%20Models%3A%20An%20Application%20in%20Epidemiology.pdf):

$$
\sigma\!\left(s_{t+1}(c)\right) \in
\begin{cases}
K, & \text{se } p_t(c) - \frac{1}{n} \ge \theta_2 \ \text{ con probabilità } p_2, \\
K^{c}, & \text{altrimenti.}
\end{cases}
$$

Nascita e sopravvivenza si combinano in un'unica regola di transizione locale [[5]](CA-doc/SIR/Spreadable%20Probabilistic%20Cellular%20Automata%20Models%3A%20An%20Application%20in%20Epidemiology.pdf):

$$
s_{t+1}(c) = \Big(\delta_1(x)\, \nu(p) + \delta_2(x)\, \big(1 - \nu(p)\big)\Big)\big(1 - \pi(x)\big) + \sigma(x)\, \pi(x),
$$

dove $x = s_t(c)$, $p = p_t(c)$, e $\delta_1: S \to K$, $\delta_2: S \to K^{c}$ sono due mappe arbitrarie. Il senso della formula si legge nei suoi due addendi: il primo si attiva solo sulle celle che non soddisfano ancora $\mathcal{P}$ (fattore $1-\pi(x)$) e ne decide l'eventuale nascita tramite $\nu$; il secondo si attiva solo sulle celle che la soddisfano già (fattore $\pi(x)$) e ne decide, tramite $\sigma$, la sopravvivenza. Poiché i due fattori $1-\pi(x)$ e $\pi(x)$ sono per costruzione mutuamente esclusivi, a ogni cella si applica sempre uno solo dei due meccanismi [[5]](CA-doc/SIR/Spreadable%20Probabilistic%20Cellular%20Automata%20Models%3A%20An%20Application%20in%20Epidemiology.pdf)

#### SIR con diffusione

Possiamo ora applicare questo formalismo al modello SIR in cui ogni sito del reticolo $L \times L$ è occupato da un individuo il cui stato assume tre valori [[5]](CA-doc/SIR/Spreadable%20Probabilistic%20Cellular%20Automata%20Models%3A%20An%20Application%20in%20Epidemiology.pdf):

$$
s_t(c) \in \{0,\ 1,\ 2\} = \{\text{suscettibile},\ \text{infetto},\ \text{guarito}\}.
$$

La proprietà $\mathcal{P}$ propagata è qui, semplicemente, l'infezione: $K = \{1\}$, e $\Omega_t$ è l'insie,e delle celle con valore 1. Le tre regole locali del paragrafo precedente si traducono, in questo caso specifico, in tre regole epidemiologiche [[5]](CA-doc/SIR/Spreadable%20Probabilistic%20Cellular%20Automata%20Models%3A%20An%20Application%20in%20Epidemiology.pdf):

1. contagio — un individuo suscettibile (stato 0) diventa infetto (stato 1) con probabilità $p_i$ se la densità locale di infetti supera la soglia $\theta_1$: è la funzione di nascita $\nu$ applicata allo stato infetto;
2. persistenza dell'infezione o guarigione — un individuo infetto (stato 1) rimane infetto con probabilità $p_s$ se la densità locale di infetti supera la soglia $\theta_2$, altrimenti guarisce e passa allo stato 2: è la funzione di sopravvivenza $\sigma$;
3. persistenza dell'immunità o perdita di immunità — un individuo guarito (stato 2) rimane guarito con probabilità $p_r$, oppure ridiventa suscettibile.

La terza regola, ammettendo il ritorno alla suscettibilità, conferisce di fatto al modello un carattere di tipo SIRS più che di SIR puro.

I valori usati nelle simulazioni sono i seguenti: reticolo $200 \times 200$, vicinato di Moore di raggio $r = 2$, soglie $\theta_1 = 0.16$ e $\theta_2 = 0.40$, probabilità $p_i = 0.7$, $p_s = 0.8$, $p_r = 0.9$ [[5]](CA-doc/SIR/Spreadable%20Probabilistic%20Cellular%20Automata%20Models%3A%20An%20Application%20in%20Epidemiology.pdf). Con questi parametri si osserva la crescita delle zone infette e una marcata dipendenza dalla configurazione iniziale: partendo da un seme quadrato compatto l'intero dominio si riempie in circa 150 iterazioni, mentre da un seme casuale di pari densità bastano circa 50 iterazioni [[5]](CA-doc/SIR/Spreadable%20Probabilistic%20Cellular%20Automata%20Models%3A%20An%20Application%20in%20Epidemiology.pdf).

La differenza sostanziale rispetto all'approccio di Fuentes–Kuperman è che qui la transizione di contagio non dipende da un tasso continuo, ma dal superamento di una soglia di densità locale di infetti combinato con un esito probabilistico: il contagio avviene solo se una quota sufficiente del vicinato è infetta, e solo con una data probabilità.

## Automi cellulari per la propagazione degli incendi boschivi

Gli incendi boschivi sono una componente ricorrente della dinamica di quasi tutti gli ecosistemi terrestri e, al tempo stesso, una fonte di danni ambientali ed economici di grande rilievo. La capacità di prevedere l'evoluzione di un incendio  è essenziale sia per la pianificazione della prevenzione sia per il supporto in tempo reale alle operazioni di spegnimento [[11]](CA-doc/Fire/karafyllidis_1997.pdf). Il secondo grande dominio di applicazione degli automi cellulari a fenomeni di propagazione spaziale è appunto la simulazione degli incendi boschivi: rispetto ai modelli SIR descritti in precedenza, qui studiamo la propagazione da cella a cella del fuoco stesso, considerando le caratteristiche del terreno e della vegetazione.

L'approccio classico alla previsione della velocità di avanzamento del fuoco si fonda su relazioni semi-empiriche, la più influente delle quali è il modello di Rothermel per la *rate of spread* nei combustibili selvatici [20]. Tradurre però queste relazioni in una descrizione spaziale completa attraverso equazioni alle derivate parziali (PDE) risulta oneroso: la forte non-linearità del problema, la geometria irregolare del territorio e la presenza di aree con proprietà di combustione diverse rendono i sistemi di PDE difficili da trattare e computazionalmente costosi [[11]](CA-doc/Fire/karafyllidis_1997.pdf). Da qui l'interesse per formulazioni discrete alternative.

Storicamente il filone nasce come un modello giocattolo di meccanica statistica per lo studio dell'autorganizzazione critica (Bak–Chen–Tang [[7]](CA-doc/Fire/Forestfire.pdf), Drossel–Schwabl [[8]](CA-doc/Fire/PhysRevLett.69.1629.pdf)), evolve poi verso una lettura geometrica legata alla percolazione e alla forma del fronte (Green [[10]](CA-doc/Fire/green1983.pdf)), e infine converge — attraverso una sequenza di modelli sempre più raffinati con vicinato di Moore — in strumenti quantitativi calibrati su incendi reali con vento, pendenza e vegetazione (Karafyllidis–Thanailakis [[11]](CA-doc/Fire/karafyllidis_1997.pdf), Hernández Encinas et al. [[12]](CA-doc/Fire/10.1016@j.advengsoft.2006.09.002.pdf), Alexandridis et al. [[13]](CA-doc/Fire/alexandridis2008.pdf), e gli sviluppi più recenti [[14]](CA-doc/Fire/probabilistic_ca_2024.pdf)).

Gli automi cellulari offrono un'alternativa discreta alle PDE: il territorio è suddiviso in celle identiche, ciascuna dotata di uno stato che evolve a passi discreti secondo una regola di transizione che dipende soltanto dallo stato dei vicini; da regole locali semplici può emergere un comportamento globale complesso, il che rende i CA particolarmente adatti a simulare fenomeni di propagazione, oltre a essere naturalmente integrabili con i sistemi informativi geografici (GIS) e computazionalmente efficienti [[11]](CA-doc/Fire/karafyllidis_1997.pdf). I CA sono stati applicati alla propagazione degli incendi lungo due filoni concettualmente distinti, che è utile tenere separati perché cercano di rispondere a due domande diffenreti:

- Conoscendo le caratteristiche di vento, terreno e vegetazione, possiamo prevedere quale sarà il movimento del fronte di fiamma nel tempo?
- Come risponde il bosco se sottoposto a diversi incendi ripetuti?

### Termini chiave

Prima di descrivere i mdoelli CA per gli incendi, conviene introdurre l'apparato concettuale su cui poggeranno. Il fenomeno di fondo è la *percolazione*, cioè lo studio della connettività di un insieme di elementi disposti a caso su un reticolo. Non è un caso che questo linguaggio ricorra nei lavori sugli incendi boschivi: la propagazione del fuoco è, geometricamente, un problema di connettività fra celle combustibili [[9]](CA-doc/Fire/clar_drossel_schwabl_review.pdf), [21].

**Il problema della connettività.** Si consideri una griglia in cui ogni cella è *occupata* (per esempio da un albero) con probabilità $\rho$ e *vuota* con probabilità $1-\rho$, in modo indipendente. Due celle occupate si dicono connesse se appartengono al vicinato l'una dell'altra; un cluster è un insieme massimale di celle occupate connesse fra loro. La domanda centrale della *percolazione di siti* (*site percolation*) è: esiste un cammino di celle occupate che attraversa l'intero sistema, da un bordo a quello opposto? È la stessa domanda che ci si pone sulla continuità del combustibile — se le chiazze di vegetazione siano abbastanza fitte da permettere al fuoco di attraversare il paesaggio.

**La soglia di percolazione.** La risposta dipende da $\rho$, ma non in modo graduale. Esiste un valore *soglia* $\rho_c$ (la *soglia di percolazione*) che separa nettamente due regimi [22]:

- per $\rho < \rho_c$ esistono solo cluster finiti e isolati: nessuno attraversa il sistema. Un incendio innescato in un cluster lo consuma e si estingue, perché non trova un ponte di celle occupate verso il resto della griglia;
- per $\rho > \rho_c$ compare un *cluster percolante* (*spanning cluster*), un unico cluster che connette lati opposti del reticolo. Il fuoco può in principio attraversare l'intero sistema.

Il valore di $\rho_c$ dipende dal reticolo e dal vicinato: per la percolazione di siti su reticolo quadrato con vicinato di von Neumann si ha $\rho_c \approx 0.593$, mentre con vicinato di Moore la soglia scende a $\rho_c \approx 0.407$, perché ogni cella dispone di più connessioni possibili e quindi la connettività globale si raggiunge già a densità inferiori [22].

**Una transizione di fase geometrica.** Il passaggio attraverso $\rho_c$ non è una gradazione dolce ma una vera *transizione di fase*: la probabilità $P_\infty(\rho)$ che una cella occupata appartenga al cluster percolante — il *parametro d'ordine* del sistema — vale zero per $\rho \le \rho_c$ e cresce con continuità al di sopra della soglia. Al punto critico la *lunghezza di correlazione* $\xi$, cioè la scala tipica di estensione dei cluster, diverge: il sistema perde ogni dimensione di riferimento interna [22].

**Assenza di scala caratteristica e leggi di potenza.** Questa divergenza è la chiave che collega la percolazione alla criticità. Lontano dalla soglia i cluster hanno una *scala caratteristica*, cioè una dimensione tipica attorno a cui si concentrano — così come l'altezza degli individui di una popolazione ha un valore tipico e non esistono persone alte dieci metri. Esattamente a $\rho_c$ questa scala tipica scompare: la distribuzione delle dimensioni dei cluster diventa una *legge di potenza*,

$$
n(s) \propto s^{-\tau},
$$

dove $n(s)$ è il numero di cluster di dimensione $s$ e $\tau$ un esponente critico. Una legge di potenza non ha scala caratteristica: si osservano cluster di *ogni* dimensione, i piccoli frequentissimi e i grandi via via più rari, fino a quello che attraversa l'intero sistema, senza una taglia privilegiata. È l'opposto di una distribuzione a campana, dominata dal suo valore medio. Graficamente, in scala doppio-logaritmica, la legge di potenza è una retta. Il cluster percolante al punto critico è inoltre un oggetto *frattale*, statisticamente autosimile a ogni scala di osservazione [22]. Questa assenza di scala caratteristica — leggi di potenza, autosimilarità — è la *firma osservabile* della criticità, ed è esattamente ciò che si ritrova nel modello di autorganizzazione critica descritto più avanti.

**Percolazione di siti e di legami.** Nella formulazione appena data è la *occupazione delle celle* a essere aleatoria (siti aperti o chiusi). Una variante, la *percolazione di legami* (*bond percolation*), tiene invece tutte le celle occupate ma rende aleatori i *collegamenti* fra celle adiacenti: ogni legame è "aperto" con probabilità $p$ e "chiuso" con probabilità $1-p$, e si chiede se esista un cammino di legami aperti che attraversi il sistema. La distinzione è importante per i modelli di incendio probabilistici, perché i due meccanismi vi coesistono: la *densità iniziale di alberi* $\rho$ è un parametro di percolazione di siti (quali celle possono bruciare), mentre la *probabilità di propagazione* $p$ fra una cella in fiamme e una vicina combustibile è un parametro di percolazione di legami (quali contatti trasmettono davvero il fuoco). Esiste allora una soglia effettiva combinata nello spazio $(\rho, p)$, al di sotto della quale l'incendio si estingue quasi sempre e al di sopra della quale dilaga.

**Percolazione dinamica e diretta.** La propagazione di un incendio è, di fatto, il cluster percolante *percorso nel tempo*: il fuoco parte da un innesco e attraversa progressivamente il cluster connesso a cui appartiene. Quando la dinamica introduce una *direzione privilegiata* — il tempo, che scorre in un solo verso, e l'eventuale immunità temporanea delle celle già bruciate — il problema ricade nella classe della *percolazione diretta* (*directed percolation*), una classe di universalità distinta dalla percolazione isotropa. La rassegna di Clar, Drossel e Schwabl mostra esplicitamente che, introducendo l'immunità, la propagazione del fuoco nel modello di incendio cade proprio in questa classe [[9]](CA-doc/Fire/clar_drossel_schwabl_review.pdf).

**Criticità classica e criticità autoorganizzata.** Resta un punto essenziale, che prepara la sezione seguente. Nella percolazione appena descritta la criticità è un fenomeno *classico*: il punto critico è un singolo valore isolato $\rho_c$, e per osservare le leggi di potenza occorre regolare finemente il parametro $\rho$ (o $p$) fino a centrarlo. È una condizione fragile — scegliendo il parametro a caso, in pratica non si colpisce mai la soglia — e come tale non ci si aspetterebbe di trovarla spontaneamente in natura. L'*autorganizzazione critica* (SOC), oggetto della prossima sezione, è precisamente il meccanismo per cui certi sistemi dinamici raggiungono da soli il punto critico, senza che alcun parametro venga calibrato dall'esterno: lo stato critico diventa un attrattore della dinamica anziché un valore da centrare. Il modello di incendio di Drossel–Schwabl ne è l'esempio paradigmatico, e si può leggere come una percolazione che si auto-sintonizza sulla propria soglia.

**Ricaduta sui modelli di questa tesi.** Questo apparato non è solo di sfondo. Il modello di autorganizzazione critica descritto di seguito vive esattamente a un punto critico di tipo percolativo, raggiunto per auto-sintonizzazione. Il modello di incendio semplificato implementato più avanti (senza vento, senza ricrescita, con propagazione probabilistica su vicinato di Moore) è, alla lettera, un problema di percolazione: la densità iniziale di alberi ne è il parametro di sito e la probabilità di propagazione il parametro di legame, e la comparsa della soglia — il passaggio brusco da "il fuoco si spegne subito" a "il fuoco attraversa tutto" al variare di quei parametri — costituisce il primo banco di prova della correttezza dell'implementazione. Lo stesso concetto di soglia critica di propagazione ritorna, in forma epidemiologica, nel numero di riproduzione di base $R_0 = 1$ dei modelli SIR: la percolazione è così il linguaggio comune che unifica la soglia epidemica e la soglia di propagazione del fuoco.

### Il modello di autorganizzazione critica (SOC)

Il capostipite dei modelli CA per gli incendi boschivi non nasce in ambito forestale ma in fisica statistica, come esempio di criticità autoorganizzata (*self-organized criticality*, SOC) [[7]](CA-doc/Fire/Forestfire.pdf). Bak, Chen e Tang definiscono un automa cellulare su reticolo ipercubico $d$-dimensionale di $L^d$ siti, con vicinato di von Neumann e tre stati per cella: vuoto, albero, albero in fiamme. Le regole, aggiornate in parallelo, sono [[7]](CA-doc/Fire/Forestfire.pdf):

1. un albero in fiamme diventa un sito vuoto;
2. un albero il cui vicinato contiene almeno un albero in fiamme prende fuoco (propagazione deterministica e istantanea);
3. su un sito vuoto cresce un nuovo albero con probabilità $p$.

L'unico parametro del modello è dunque il tasso di crescita $p$; non essendovi innesco spontaneo, il fuoco deve essere già presente nella configurazione iniziale (o re-innescato quando si estingue) [[7]](CA-doc/Fire/Forestfire.pdf). Grazie alla possibile nascita di nuove piante, possiamo definire come *cluster* un gruppo di celle di stato albero connesse tra loro.

Simulando il modello di Bak–Chen–Tang si osservano due comportamenti distinti a seconda del tasso di crescita $p$. Se $p$ è basso, il fuoco consuma rapidamente il cluster in cui è nato e poi si estingue, perché attorno la vegetazione non ha ancora avuto il tempo di ricrescere: l'incendio resta un evento isolato e di dimensione limitata. Se invece $p$ è sufficientemente alto, mentre il fuoco brucia un'estremità del cluster nuovi alberi ricrescono all'estremità opposta; il fronte trova così sempre nuovo combustibile davanti a sé e si automantiene, dando luogo a un fronte di fiamma perpetuo.

Proprio quest'ultimo regime rivela il limite del modello: poiché un albero prende fuoco solo se ha un vicino già in fiamme, un piccolo gruppo isolato di alberi non può accendersi «dall'interno», ma deve prima crescere fino a saldarsi con il cluster che sta già bruciando. L'unica scala spaziale del sistema è allora fissata dalla sola crescita: i fronti di fuoco hanno dimensione dell'ordine di $1/p$ e, al diminuire di $p$, si organizzano in spirali regolari sempre più deterministiche. Mancano cioè gli incendi di dimensioni differenti che caratterizzano un vero stato critico. Il modello di Bak–Chen–Tang, da solo, non è realmente critico [[8]](CA-doc/Fire/PhysRevLett.69.1629.pdf).


Per recuperare la criticità serve un meccanismo che permetta di incendiare anche i cluster piccoli, indipendentemente da ciò che accade ai loro bordi. Drossel e Schwabl [[8]](CA-doc/Fire/PhysRevLett.69.1629.pdf) lo introducono aggiungendo alle tre regole precedenti una quarta regola, cioè una piccola probabilità di innesco spontaneo (un «fulmine»):

4. un albero senza vicini in fiamme prende fuoco spontaneamente (fulmine) con probabilità $f$.

Nello stato stazionario vale un bilancio tra le densità medie di sito vuoto $\rho_e$, di albero $\rho_t$ e di fuoco $\rho_f$ [[9]](CA-doc/Fire/clar_drossel_schwabl_review.pdf):

$$
\rho_e+\rho_t+\rho_f=1, \qquad \rho_f = p\,\rho_e .
$$

La seconda uguaglianza esprime che, a regime, il numero di alberi che crescono eguaglia quello degli alberi che bruciano. Il punto critico del sistema è per $f/p\to 0$, quindi quando la frequenza dei fulmini è molto inferiore alla crescita di nuove piante. Il punto critico viene raggiunto senza alcuna calibrazione fine dei parametri (autorganizzazione). Perché il regime critico sia effettivamente osservabile occorre inoltre che il tempo di combustione di un intero cluster sia molto più breve del tempo di ricrescita di un albero ai suoi bordi, il che produce una doppia separazione di scale temporali [[8]](CA-doc/Fire/PhysRevLett.69.1629.pdf), [[9]](CA-doc/Fire/clar_drossel_schwabl_review.pdf):

$$
(f/p)^{-\nu} \;\ll\; p^{-1} \;\ll\; f^{-1},
$$

cioè: il tempo di combustione di un cluster deve essere molto breve rispoetto al tempo di crescita di un albero che a sua volta è notevolmente inferiore al tempo medio tra due fulmini sullo stesso sito.

Va segnalato che questo filone (SOC) non modella vento, pendenza o eterogeneità del combustibile: il suo interesse, ai fini della tesi, è puramente concettuale. 
mostra che una regola locale elementare può generare da sola comportamento critico e fronti di fuoco autosimili, ed è il punto di partenza storico da cui i modelli seguenti si allontanano progressivamente per includere realismo fisico.

### Percolazione geometrica e forma del fronte: il modello di Green (1983)

<!-- Un secondo filone, indipendente dal precedente, nasce in ecologia con l'obiettivo di riprodurre la forma geometrica dei fronti di incendio reali in funzione della continuità del combustibile [[10]](CA-doc/Fire/green1983.pdf). Green rappresenta il combustibile come un reticolo 2D di celle piene/vuote e introduce il concetto di *template di accensione*: un array che descrive l'effetto di un punto in combustione sui punti circostanti, tipicamente di forma ellittica con eccentricità $e$ crescente con la velocità del vento (o quadrata, per confronto) [[10]](CA-doc/Fire/green1983.pdf).

Sono confrontati due meccanismi di propagazione punto-punto. Nel modello a *contatto*, il tempo necessario perché il punto $X$ acceso inneschi il punto $Y$ è:

$$
t(X,Y) = \frac{C\,M\,(1-e^2)}{d(X,Y)\,(1-e\cos\theta)},
$$

dove $M$ è la dimensione del template, $\theta$ l'angolo di $Y$ rispetto a $X$ misurato da sottovento, $d(X,Y)$ la distanza e $C$ una costante; il tempo di accensione di ogni punto si aggiorna scandendo ripetutamente il template, $T'(Y)=\min\big(T(Y),\,T(X)+t(X,Y)\big)$, e l'area bruciata a un istante $T_{max}$ è l'insieme $\{X : T(X)\le T_{max}\}$ [[10]](CA-doc/Fire/green1983.pdf). Nel modello ad *accumulo di calore*, si accumula invece un flusso termico $H'(Y)=H(Y)+h(X,Y)$ fino al raggiungimento di una soglia critica di accensione [[10]](CA-doc/Fire/green1983.pdf).

Il risultato principale è che la *continuità del combustibile* determina la forma del fronte: in combustibile continuo entrambi i meccanismi producono fronti ellittici (in accordo con i classici modelli di crescita ellittica del fuoco); in combustibile molto discontinuo (*patchy*) emergono forme non ellittiche — ovoidali, "a goccia", semi-ellittiche, fino a degenerare in una linea retta per venti molto forti — con back-burning ridotto o assente [[10]](CA-doc/Fire/green1983.pdf). Va segnalato con onestà che il paper non formalizza esplicitamente una soglia critica di percolazione: si limita a osservare, qualitativamente, che in combustibile molto discontinuo alcuni elementi di combustibile interni all'area "raggiunta" dal fronte non si accendono effettivamente — un'osservazione concettualmente affine alla percolazione, ma non sviluppata come tale [[10]](CA-doc/Fire/green1983.pdf). Il valore di questo modello per la tesi è soprattutto metodologico: introduce l'idea di un template di propagazione anisotropo, dipendente dalla direzione del vento, distribuito sul vicinato di una cella — l'idea che, discretizzata su un vicinato di Moore, sta alla base dei modelli delle sezioni successive. -->

#### Automi a stato continuo con vicinato di Moore: Karafyllidis–Thanailakis (1997)

Karafyllidis e Thanailakis propongono il primo modello CA di incendio con vicinato di Moore (le $3\times3$ celle centrate sulla cella in esame) e uno stato *continuo* anziché discreto [[11]](CA-doc/Fire/karafyllidis_1997.pdf):

$$
S_{ij}^{\,t} = \frac{A_b}{A_t} \in [0,1],
$$

pari alla frazione di area bruciata della cella (0 = intatta, 1 = completamente bruciata); le aree incombustibili sono semplicemente celle con tasso di propagazione $R=0$ [[11]](CA-doc/Fire/karafyllidis_1997.pdf). A ciascuna cella è associato un tasso di propagazione $R_{ij}$ (m/s), fornito da un modello esterno. In questo sistema, un vicino ortogonale completamente bruciato brucia interamente la cella adiacente al passo successivo, mentre un vicino diagonale ne brucia solo una frazione $2(\sqrt2-1) \cong 0.83 .$

La regola base è quindi:
<!-- tutta questa notazione è da rivedere in maniera che sia più leggera e intuitiva. HELL OF NOTATION -->
$$
\begin{aligned}
S_{i,j}^{t+1} = &S_{i,j}^{t}
+ \Big(S_{i-1,j}^{t}+S_{i,j-1}^{t}+S_{i,j+1}^{t}+S_{i+1,j}^{t}\Big) \\
&+ 0.83\Big(S_{i-1,j-1}^{t}+S_{i-1,j+1}^{t}+S_{i+1,j-1}^{t}+S_{i+1,j+1}^{t}\Big)
\end{aligned}
$$

troncata a $1$ se supera tale valore [[11]](CA-doc/Fire/karafyllidis_1997.pdf). Il vento è incorporato assegnando un peso moltiplicativo a ciascuna delle otto direzioni del vicinato di Moore ($n,s,e,w,ne,nw,se,sw$):

$$
\begin{aligned}
S_{i,j}^{t+1}= & S_{i,j}^{t}+\big(n S_{i-1,j}^{t}+w S_{i,j-1}^{t}+e S_{i,j+1}^{t}+s S_{i+1,j}^{t}\big) \\
 & +0.83\big(nw S_{i-1,j-1}^{t}+ne S_{i-1,j+1}^{t}+sw S_{i+1,j-1}^{t}+se S_{i+1,j+1}^{t}\big)
\end{aligned}
$$

con pesi $>1$ nella direzione sopravento e $<1$ in quella sottovento (tutti $=1$ in assenza di vento) [[11]](CA-doc/Fire/karafyllidis_1997.pdf). La *pendenza del terreno* è incorporata con un meccanismo del tutto analogo, sostituendo ai pesi del vento dei pesi $H_{k,l}$ che dipendono dal dislivello tra le celle — il fuoco procede più rapidamente in salita e più lentamente in discesa. La regola locale con la sola topografia è [[11]](CA-doc/Fire/karafyllidis_1997.pdf):

$$
\begin{aligned}
S_{i,j}^{t+1}= S_{i,j}^{t}+\big( & H_{i-1,j}S_{i-1,j}^{t}+H_{i,j-1}S_{i,j-1}^{t}+H_{i,j+1}S_{i,j+1}^{t}+H_{i+1,j}S_{i+1,j}^{t}\big) \\
+0.83\big( & H_{i-1,j-1}S_{i-1,j-1}^{t}+H_{i-1,j+1}S_{i-1,j+1}^{t} \\ 
+ & H_{i+1,j-1}S_{i+1,j-1}^{t}+H_{i+1,j+1}S_{i+1,j+1}^{t}\big)
\end{aligned}
$$

dove il peso $H_{k,l}$ è funzione della differenza di quota tra il centro della cella $(k,l)$ e quello della cella $(i,j)$:

$$
H_{k,l} = F\big(h_{i,j} - h_{k,l}\big),
$$

con $h_{i,j}$ e $h_{k,l}$ le rispettive altezze; in prima approssimazione tale dipendenza si assume lineare. Vento e pendenza si combinano infine in un'unica regola locale generale, in cui ogni contributo è pesato dal prodotto del fattore di vento per quello di quota [[11]](CA-doc/Fire/karafyllidis_1997.pdf):

$$
\begin{aligned}
S_{i,j}^{t+1}= S_{i,j}^{t}+\big( & n H_{i-1,j}S_{i-1,j}^{t}+w H_{i,j-1}S_{i,j-1}^{t}+e H_{i,j+1}S_{i,j+1}^{t}+s H_{i+1,j}S_{i+1,j}^{t}\big) \\
+0.83\big( & nw\,H_{i-1,j-1}S_{i-1,j-1}^{t}+ne\,H_{i-1,j+1}S_{i-1,j+1}^{t}\\
 +& sw\,H_{i+1,j-1}S_{i+1,j-1}^{t}+se\,H_{i+1,j+1}S_{i+1,j+1}^{t}\big)
\end{aligned}
$$

Il modello è interamente *deterministico* — nessuna componente probabilistica, $R_{ij}$ è un dato esterno — e non è validato quantitativamente contro incendi reali, solo su foreste ipotetiche (fronti circolari senza vento, allungati nella direzione del vento, deformati da rilievi) [[11]](CA-doc/Fire/karafyllidis_1997.pdf). Questo è, concettualmente, l'antenato diretto di uno schema "vicinato di Moore + matrice di propagazione anisotropa per direzione, modulata dal vento", ripreso e reso probabilistico dai modelli successivi.

#### Fronte circolare e caso disomogeneo: Hernández Encinas et al. (2007)

Dalla revisione del modello precedente si nota che il coefficiente diagonale $0.83$ di Karafyllidis–Thanailakis produce fronti leggermente ottagonali anziché circolari. Sostituendolo con un coefficiente calibrato geometricamente sull'area di un settore circolare [[12]](CA-doc/Fire/10.1016@j.advengsoft.2006.09.002.pdf)$\lambda = \pi/4 \cong 0.785$ Il modello viene formalizzato con vicinato di Moore $V_M$ diviso in celle adiacenti $V_M^{adj}$ e diagonali $V_M^{diag}$, e stato $a_{ij}^{t}\in[0,1]$ pari alla frazione di area bruciata [[12]](CA-doc/Fire/10.1016@j.advengsoft.2006.09.002.pdf). La regola generale, per foresta disomogenea con tasso di propagazione $R_{ij}$ diverso per cella, con vento e pendenza variabili nel tempo, è:

$$
\begin{aligned}
a_{ij}^{(t+1)}=\frac{R_{ij}}{R}\,a_{ij}^{(t)}
+& \sum_{(\alpha,\beta)\in V_M^{adj}}\!\! w_{i+\alpha,j+\beta}^{(t)}\,h_{i+\alpha,j+\beta}\,\frac{R_{i+\alpha,j+\beta}}{R}\,a_{i+\alpha,j+\beta}^{(t)} \\
+&\sum_{(\alpha,\beta)\in V_M^{diag}}\!\! w_{i+\alpha,j+\beta}^{(t)}\,h_{i+\alpha,j+\beta}\,\frac{\pi R_{i+\alpha,j+\beta}^{2}}{4R^{2}}\,a_{i+\alpha,j+\beta}^{(t)}
\end{aligned}
$$

dove $R=\max\{R_{ij}\}$, $w$ è la matrice di vento e $h$ la matrice di pendenza [[12]](CA-doc/Fire/10.1016@j.advengsoft.2006.09.002.pdf).

#### Modelli probabilistici calibrati su incendi reali: Alexandridis et al. (2008)

Alexandridis, Vakalis, Siettos e Bafas riformulano il problema in termini interamente *probabilistici*, in maniera da porter tornare a stati discreti su un reticolo di celle quadrate con vicinato di Moore [[13]](CA-doc/Fire/alexandridis2008.pdf):

- **stato 1** — cella priva di combustibile forestale (aree urbane/rurali);
- **stato 2** — cella con combustibile non ancora incendiato;
- **stato 3** — cella in fiamme;
- **stato 4** — cella completamente bruciata.

Le regole di transizione sono [[13]](CA-doc/Fire/alexandridis2008.pdf): 

- una cella in fiamme diventa bruciata al passo successivo
- le celle senza combustibile o già bruciate restano tali
- una cella con combustibile adiacente a una cella in fiamme prende fuoco con probabilità $p_{burn}$
 
La probabilità di propagazione è il prodotto di un valore di base e di quattro fattori correttivi:

$$
p_{burn} = p_h\,(1+p_{den})\,(1+p_{veg})\,p_w\,p_s ,
$$

dove $p_h$ è la probabilità costante di base (combustibile di riferimento, vento nullo, terreno piatto), $p_{den}$ e $p_{veg}$ dipendono da categorie discrete di densità e tipo di vegetazione [[13]](CA-doc/Fire/alexandridis2008.pdf). Il fattore vento, è reso continuo nell'angolo:

$$
p_w = \exp(c_1 V)\,f_t, \qquad f_t=\exp\!\big(Vc_2(\cos\theta-1)\big),
$$

con $V$ velocità del vento e $\theta$ angolo tra la direzione di propagazione e quella del vento [[13]](CA-doc/Fire/alexandridis2008.pdf). Il fattore di pendenza è

$$
p_s = \exp(a\,\theta_s) \\
\theta_s = \tan^{-1}\!\left(\frac{E_1-E_2}{l}\right)\ \text{(celle adiacenti)} \\
\theta_s = \tan^{-1}\!\left(\frac{E_1-E_2}{l\sqrt2}\right)\ \text{(celle diagonali)}
$$

con $E_1,E_2$ quote delle due celle e $l$ lato della cella [[13]](CA-doc/Fire/alexandridis2008.pdf)


## Automi cellulari per il modello di Ising

### Perché esiste il problema e contesto storico

Le sezioni precedenti trattano automi cellulari usati per riprodurre un *fronte di propagazione spaziale* (epidemia o incendio) che avanza nel tempo. Il modello di Ising rappresenta un'applicazione di natura diversa: qui l'obiettivo non è seguire l'avanzare di un fronte, ma usare l'automa cellulare come strumento per campionare le proprietà di equilibrio di un sistema di meccanica statistica — un reticolo di spin che interagiscono con i primi vicini — alternativo ai metodi Monte Carlo classici. La domanda, posta per prima in modo sistematico da Vichniac nel 1984, è se un automa cellulare a duplice stato per cella possa riprodurre esattamente le proprietà di equilibrio di questo sistema.

### Come si può affrontare il problema

Il filo conduttore di questa sezione è la tensione tra due esigenze in conflitto: da un lato la *parallelizzazione totale* propria degli automi cellulari (aggiornare tutte le celle simultaneamente), dall'altro la necessità di riprodurre correttamente la distribuzione di Boltzmann all'equilibrio, che — come si vedrà — impone vincoli non banali sulla regola locale. Le strategie proposte in letteratura per conciliare le due esigenze si dividono in due filoni: un filone *deterministico*, che rinuncia in parte al parallelismo totale (aggiornamento a scacchiera) e introduce meccanismi ausiliari — parità, variabili "demone", sistemi di spin accessori — per garantire la conservazione dell'energia a livello locale (Vichniac, Creutz, Ottavi–Parodi, Xiao); e il termine di paragone classico, non basato su automi cellulari, del campionamento *Monte Carlo* di una catena di Markov ergodica.

### Metodi studiati in questo lavoro

#### Il limite della parallelizzazione totale e la regola Q2R: Vichniac (1984)

Vichniac affronta per primo, in modo sistematico, la domanda se un automa cellulare a duplice stato per cella possa riprodurre le proprietà di equilibrio del modello di Ising, definito dall'Hamiltoniana [[15]](CA-doc/Ising/vichniac1984.pdf)

$$
H = -J \sum_{\langle i,j \rangle} \sigma_i \sigma_j ,
$$

con spin $\sigma_i \in \{+1,-1\}$ sui siti di un reticolo e somma sui soli primi vicini. All'equilibrio con un bagno termico a temperatura $T$, il valore medio di un osservabile $A$ nell'insieme canonico è dato dalla consueta media pesata con il fattore di Boltzmann e normalizzata dalla funzione di partizione $Z(T)$ [[15]](CA-doc/Ising/vichniac1984.pdf).

Un risultato centrale del lavoro è un argomento contro la parallelizzazione totale: nessuna regola di automa cellulare che aggiorni *simultaneamente* tutti gli spin può riprodurre esattamente la distribuzione canonica (4.2). La ragione è che l'energia di Ising è un operatore a due corpi: il calcolo dell'incremento di energia globale associato al ribaltamento di un singolo spin, $\Delta\epsilon_i$, resta valido solo se gli spin aggiornati non sono mutuamente adiacenti; se due celle contigue vengono ribaltate nello stesso passo, la relazione tra variazione locale e variazione globale dell'energia si rompe, e la regola di transizione non ha più accesso all'informazione necessaria per riprodurre il peso di Boltzmann corretto [[15]](CA-doc/Ising/vichniac1984.pdf). Da qui l'esigenza, comune a tutti i modelli successivi, di un aggiornamento *a scacchiera* (metà delle celle per passo) anziché completamente parallelo.

Su questa base Vichniac introduce la regola reversibile *Q2R*, definita sul vicinato di von Neumann tramite l'espressione booleana [[15]](CA-doc/Ising/vichniac1984.pdf)

$$
Y = \big((Q=2)\ \text{XOR}\ \text{CPAST}\big),
$$

dove $Q$ è il numero di vicini con spin "su" e CPAST è lo stato della cella al passo precedente: uno spin è candidato al ribaltamento quando ha esattamente due vicini "su" e due "giù" (condizione di neutralità energetica, l'unico caso in cui il flip non altera l'energia), e l'operazione XOR con lo stato precedente rende la regola esattamente reversibile, evitando che la cella ritorni immediatamente sullo stato di partenza. Questa è, nella sostanza, la stessa regola che la letteratura successiva chiama modello *VPH* (Vichniac–Pomeau–Herrmann): il ribaltamento avviene se e solo se non altera l'energia magnetica, con aggiornamento a scacchiera in due sotto-passi [[17]](CA-doc/Ising/ottavi1989.pdf).

Q2R conserva esattamente l'energia totale ed è deterministica e reversibile, ma non è *ergodica*: la dinamica è simmetrica rispetto a traslazioni del reticolo e all'inversione globale degli spin, e a basse temperature si blocca in cicli-limite periodici ("mostri oscillanti") anziché esplorare l'intero spazio delle configurazioni a parità di energia — un fenomeno che Vichniac collega concettualmente alla fisica dei sistemi frustrati e dei vetri di spin (disordine e frustrazione producono buche di potenziale profonde e strette nella superficie di energia, analoghe a quelle di uno spin-glass) [[15]](CA-doc/Ising/vichniac1984.pdf). Vichniac nota anche che, proprio per questa tendenza a "congelarsi" in configurazioni di energia localmente minima, Q2R può essere sfruttata in senso costruttivo come algoritmo di ottimizzazione a $T=0$ per la ricerca di stati fondamentali.

#### Il modello a demoni deterministico: Creutz (1986)

Creutz propone un'alternativa che rinuncia alla reversibilità in senso stretto in cambio di un controllo diretto sulla temperatura. Ogni sito porta, oltre allo spin, una variabile "demone" locale (2 bit) che funge da riserva di energia cinetica coniugata allo spin, più un bit di parità per l'aggiornamento a scacchiera; un flip di spin è accettato se e solo se la variazione di energia magnetica può essere esattamente compensata dalla variabile demone del sito, mantenendo così invariata l'energia totale. Il dettaglio completo delle equazioni, dell'algoritmo e degli esperimenti numerici (correlazione tra primi vicini, flusso di calore, conducibilità termica, correlazioni temporali e mixing) è riportato nel file [pub088-creutz1986-summary.md](Ising/pub088-creutz1986-summary.md) [[16]](CA-doc/Ising/pub088-1-10.pdf).

#### I limiti a bassa temperatura e le correzioni di Ottavi–Parodi (1989)

Testando il modello C2 di Creutz su un calcolatore parallelo SIMD (schede GAPP), Ottavi e Parodi mostrano che il meccanismo si blocca a bassa temperatura ($T \lesssim 0.91\,T_c$) esattamente come il modello VPH/Q2R: al di sotto di questa soglia i pochi siti con energia di riserva sufficiente per ribaltare lo spin sono troppo isolati perché l'informazione si propaghi attraverso il campione, in un processo che gli autori assimilano a una *soglia di percolazione* — la lunghezza di coerenza magnetica diventa più corta della distanza media tra questi siti "fortunati" [[17]](CA-doc/Ising/ottavi1989.pdf).

Per risolvere il problema propongono due varianti che aggiungono un secondo meccanismo di trasferimento energetico indipendente dallo spin di Ising:

- il *modello del lancio (toss model)*: ogni coppia di siti primi vicini "lancia una moneta" a ogni passo, trasferendo un'unità di energia $J$ dal perdente al vincitore (a meno che il perdente sia già a energia nulla o il vincitore al massimo consentito);
- il *modello a doppio spin (double-spin model)*: si affianca al sistema di Ising originale un secondo sistema di spin, accoppiato con costante di scambio dimezzata $J' = J/2$ (e quindi temperatura critica dimezzata $T_c' = T_c/2$), che agisce da bagno termico ausiliario sempre disordinato nell'intervallo di temperature di interesse.

Entrambe le varianti restano compatibili con l'implementazione a operazioni bit a bit su architetture parallele e funzionano correttamente anche a bassa temperatura; il modello a doppio spin, in particolare, risulta più veloce del modello del lancio (non richiede un generatore di bit casuali) e viene confrontato favorevolmente, in termini di accuratezza ed efficienza per ciclo di aggiornamento, con l'algoritmo Metropolis classico — pur restando, sul hardware SIMD dell'epoca, circa dieci volte più rapido in tempo di calcolo reale [[17]](CA-doc/Ising/ottavi1989.pdf). Gli autori stimano inoltre l'esponente critico $\beta \approx 1/8.25$, in buon accordo con il valore esatto $1/8$ del modello di Ising 2D, tenuto conto delle dimensioni finite del campione simulato.

#### Verifiche moderne e generalizzazione al modello di Potts: Xiao (2023)

Un lavoro più recente riprende l'algoritmo deterministico di Creutz per verificarne la validità con gli strumenti computazionali attuali, confrontando correlazione tra primi vicini, energia interna e magnetizzazione con i risultati esatti noti per il modello di Ising 2D, e stimando l'esponente critico $\beta = 0.1069(25)$ — non compatibile, entro l'incertezza dichiarata, con il valore esatto $1/8$, una discrepanza attribuita a effetti di dimensione finita vicino a $T_c$ [[18]](CA-doc/Ising/XiaoBrian.pdf). Lo stesso schema viene poi generalizzato al *modello di Potts a $q$ stati* ($q=3,4,5$), verificando la coerenza della magnetizzazione con la temperatura critica esatta e stimando l'esponente $\beta$ anche in questo caso ($\beta \approx 0.0658(64)$ per $q=3$ e $\beta \approx 0.0650(21)$ per $q=4$), anch'esso non pienamente in accordo con i valori esatti per le stesse ragioni di taglia finita [[18]](CA-doc/Ising/XiaoBrian.pdf).

#### Il termine di confronto classico: campionamento Monte Carlo

Tutti i modelli precedenti vengono, direttamente o indirettamente, confrontati con il metodo di riferimento non basato su automi cellulari: il campionamento Monte Carlo di una catena di Markov che converge alla distribuzione di Boltzmann. Nella versione più semplice (algoritmo "a bagno di calore"), si sceglie uno spin a caso e lo si assegna al valore $\pm1$ con probabilità proporzionale al corrispondente fattore di Boltzmann calcolato nel campo locale dei vicini; nella versione *Metropolis*, si calcola invece la variazione di energia $\Delta E$ associata al ribaltamento di uno spin scelto a caso, accettando sempre il ribaltamento se $\Delta E<0$ e accettandolo con probabilità $e^{-\Delta E/kT}$ altrimenti [[19]](CA-doc/Ising/a4.pdf). Entrambi gli schemi sono catene di Markov ergodiche che soddisfano la condizione di *bilancio dettagliato*, e quindi convergono, per costruzione, a un'unica distribuzione di equilibrio — proprietà che, come mostrato da Vichniac [[15]](CA-doc/Ising/vichniac1984.pdf), nessun automa cellulare a parallelismo totale può garantire in modo altrettanto diretto. È proprio rispetto a questo standard che i modelli di Vichniac, Creutz, Ottavi–Parodi e Xiao misurano la propria validità ed efficienza computazionale.

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

[22] D. Stauffer, A. Aharony, *Introduction to Percolation Theory*, 2nd ed., Taylor & Francis, London (1994). — riferimento standard sulla teoria della percolazione; non presente tra i file del progetto, da verificare/caricare.
