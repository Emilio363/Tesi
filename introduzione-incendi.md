# Modellizzazione della propagazione degli incendi mediante automi cellulari
 
## 1. Introduzione
 
Gli incendi boschivi sono una componente ricorrente della dinamica di quasi tutti gli ecosistemi terrestri e, al tempo stesso, una fonte di danni ambientali ed economici di grande rilievo. La capacità di prevedere l'evoluzione di un incendio — cioè di determinare la posizione del *fronte di fiamma* nel tempo, sotto date condizioni di vento, topografia e vegetazione — è essenziale sia per la pianificazione della prevenzione sia per il supporto in tempo reale alle operazioni di spegnimento [1]. L'obiettivo tipico di un modello di propagazione è proprio la ricostruzione del fronte tempo-evolvente a partire da una configurazione iniziale nota.
 
L'approccio classico alla previsione della velocità di avanzamento del fuoco si fonda su relazioni semi-empiriche, la più influente delle quali è il modello di Rothermel per la *rate of spread* nei combustibili selvatici [2]. Tradurre però queste relazioni in una descrizione spaziale completa attraverso equazioni alle derivate parziali (PDE) risulta oneroso: la forte non-linearità del problema, la geometria irregolare del territorio e la presenza di aree con proprietà di combustione diverse rendono i sistemi di PDE difficili da trattare e computazionalmente costosi [1]. Da qui l'interesse per formulazioni discrete alternative.
 
Gli automi cellulari (CA) offrono una di queste alternative. Un CA è un sistema dinamico in cui spazio e tempo sono discreti e le interazioni sono puramente locali: il territorio è suddiviso in celle identiche, ciascuna dotata di uno stato che evolve a passi discreti secondo una regola di transizione che dipende soltanto dallo stato dei vicini. Da regole locali semplici può emergere un comportamento globale complesso, il che rende i CA particolarmente adatti a simulare fenomeni di propagazione, oltre a essere naturalmente integrabili con i sistemi informativi geografici (GIS) e computazionalmente efficienti [1]. Non sorprende quindi che i CA siano stati applicati alla propagazione degli incendi lungo due direttrici concettualmente distinte, che è utile tenere separate fin dall'inizio perché rispondono a domande scientifiche diverse.
 
### 1.1. La famiglia predittiva: la forma e la posizione del fronte
 
La prima direttrice mira a riprodurre *dove e come* si muove un fronte reale. I primi studi di simulazione su combustibili discreti mostrarono che meccanismi di propagazione differenti — accumulo di calore contro contatto di fiamma — generano forme di incendio diverse, quasi ellittiche nei combustibili continui ma assai più irregolari nei combustibili distribuiti a chiazze [3]. Il lavoro fondativo per i CA in senso proprio è quello di Karafyllidis e Thanailakis [1], nel quale lo stato di una cella non rappresenta un albero singolo bensì la *frazione di area bruciata* della cella, un numero reale che cresce dallo stato intatto (0) a quello completamente bruciato (1). La regola di transizione, definita su un vicinato di Moore, accumula i contributi delle celle vicine — con un peso ridotto per le celle diagonali, geometricamente più distanti — mentre la velocità di propagazione fissa la scala temporale e assorbe l'effetto della temperatura; vento e topografia sono incorporati modulando i contributi direzionali.
 
Su questa impostazione si innestano numerosi affinamenti. Hernández Encinas e collaboratori [4] propongono una modifica più realistica del modello di Karafyllidis, con un fattore di propagazione dalla cella diagonale più accurato e una trattazione dettagliata della velocità di propagazione, valida sia per ambienti omogenei sia disomogenei; è significativo che questo contributo provenga dallo stesso gruppo di Salamanca attivo nella modellizzazione CA delle epidemie, a testimonianza della continuità metodologica tra i due domini. Sul versante applicativo, Alexandridis e collaboratori [5] costruiscono un modello che tiene conto di tipo e densità della vegetazione, velocità e direzione del vento e del fenomeno dello *spotting* (il trasporto di materiale incandescente oltre il fronte), validandolo sul caso reale dell'incendio che devastò l'isola di Spetses nel 1990. Sviluppi più recenti rendono esplicito il carattere probabilistico della transizione, con la probabilità di ignizione espressa in funzione del numero di vicini in fiamme e dei fattori ambientali [6].
 
### 1.2. La famiglia statistico-fisica: la criticità auto-organizzata
 
La seconda direttrice ha origine e finalità completamente diverse. Bak, Chen e Tang [7] introdussero un *forest-fire model* non per prevedere incendi reali ma come modello-giocattolo per studiare lo scaling e la dissipazione frattale dell'energia in analogia con la turbolenza; in quel modello, tuttavia, i fronti assumono forme regolari a spirale e non si osserva vera criticità. Il passo decisivo è di Drossel e Schwabl [8], che aggiungono una probabilità di innesco spontaneo *f* (il "fulmine"): in presenza di una separazione delle scale temporali tra la crescita degli alberi e la combustione dei cluster, il sistema si auto-organizza verso uno stato critico, indipendente dalle condizioni iniziali e senza necessità di calibrare i parametri, caratterizzato da una distribuzione a legge di potenza delle dimensioni degli incendi. In questo quadro non compaiono vento, pendenza né vegetazione: sono deliberatamente astratti, poiché l'oggetto di studio non è un incendio specifico ma la *statistica universale* di molti incendi.
 
Questa universalità è stata oggetto di dibattito. Grassberger e Kantz [9], simulando il modello su reticoli molto più grandi, misero in dubbio la presenza di un vero fenomeno critico non banale nel limite considerato, mostrando piuttosto un'evoluzione deterministica su scale temporali dell'ordine dell'inverso del tasso di crescita. La rassegna successiva di Clar, Drossel e Schwabl [10] sistematizza le proprietà del modello, gli esponenti critici e le relazioni di scaling, e ne discute l'universalità rispetto alla simmetria del reticolo e all'introduzione dell'immunità.
 
### 1.3. Un ponte con la modellizzazione epidemica
 
Vale la pena sottolineare un legame che collega direttamente questo studio al lavoro precedente sulla diffusione delle epidemie. Il modello di incendio a stati discreti appartiene alla classe dei *mezzi eccitabili*, la stessa che descrive la propagazione delle malattie [9, 10]: la corrispondenza albero → suscettibile, albero in fiamme → infetto, cella vuota → rimosso rende la famiglia SOC degli incendi, di fatto, un modello SIR spaziale. La famiglia predittiva, per contro, adotta una descrizione dello stato di cella (frazione di area bruciata, evoluzione deterministica) che si allontana dallo schema compartimentale. I due modi di guardare al fuoco corrispondono così a due modi diversi, ma entrambi familiari, di guardare a un processo di diffusione.
 
### 1.4. Obiettivo del lavoro
 
Il presente lavoro si propone di implementare e mettere a confronto, sulla medesima griglia cellulare, un rappresentante di ciascuna delle due famiglie: un fronte deterministico di tipo Karafyllidis–Alexandridis [1, 5] e un modello stocastico auto-organizzato di tipo Drossel–Schwabl [8]. L'intento è rendere esplicita, in forma eseguibile e osservabile, la differenza tra un fronte di fiamma che avanza in modo regolare guidato da fattori fisici e un sistema che si organizza spontaneamente verso uno stato critico con statistica a legge di potenza — due comportamenti che pure condividono l'etichetta di "automa cellulare per gli incendi".
 
---
 
## Bibliografia
 
[1] Karafyllidis, I., Thanailakis, A. (1997). A model for predicting forest fire spreading using cellular automata. *Ecological Modelling*, 99(1), 87–97.
 
[2] Rothermel, R.C. (1972). *A mathematical model for predicting fire spread in wildland fuels*. Research Paper INT-115. Ogden, UT: USDA Forest Service, Intermountain Forest and Range Experiment Station.
 
[3] Green, D.G. (1983). Shapes of simulated fires in discrete fuels. *Ecological Modelling*, 20(1), 21–32.
 
[4] Hernández Encinas, A., Hernández Encinas, L., Hoya White, S., Martín del Rey, A., Rodríguez Sánchez, G. (2007). Simulation of forest fire fronts using cellular automata. *Advances in Engineering Software*, 38(6), 372–378.
 
[5] Alexandridis, A., Vakalis, D., Siettos, C.I., Bafas, G.V. (2008). A cellular automata model for forest fire spread prediction: The case of the wildfire that swept through Spetses Island in 1990. *Applied Mathematics and Computation*, 204(1), 191–201.
 
[6] Ghosh, R., Adhikary, J., Chemlal, R. (2024). *Fire Spread Modeling using Probabilistic Cellular Automata*. arXiv:2403.08817.
 
[7] Bak, P., Chen, K., Tang, C. (1990). A forest-fire model and some thoughts on turbulence. *Physics Letters A*, 147(5–6), 297–300.
 
[8] Drossel, B., Schwabl, F. (1992). Self-organized critical forest-fire model. *Physical Review Letters*, 69(11), 1629–1632.
 
[9] Grassberger, P., Kantz, H. (1991). On a forest fire model with supposed self-organized criticality. *Journal of Statistical Physics*, 63(3–4), 685–700.
 
[10] Clar, S., Drossel, B., Schwabl, F. (1996). Forest fires and other examples of self-organized criticality. arXiv:cond-mat/9610201. [Rassegna del modello di Drossel & Schwabl, 1992.]