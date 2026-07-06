
CA: Cellular Automata
CML: Coupled Map Lattice

Graph Attention Network
CBAM: Convolutional Block Attention Module
Coupled Map Lattice

un primo passaggio viene fatto applicando un filtro al vettore delle informazioni, che evidenzia alcuni aspetti rilevanti del vettore. qui abbiamo un passaggio che non modifica le dimensioni delle informazioni della cella e neanche della matrice.
A questo punto andiamo a valutare una funzione su ogni cella e il suo vicinato. In genere la funzione più semplice potrebbe essere concatenare i due vettori di informazioni della cella e di uno dei suo vicini e moltoplicare per un vettore beta di dimensione adeguata in maniera da ottenere uno scalare. questa operazione viene ripetuta con tutti i vicini della cella e anche con se stessa. ottenuti questi pesi, posso valutare il softmax dei valori e moltiplicarli per il relativo vettore. Su questa seconda parte del vettore può essere valutata un altra funzione oppure una NN.
Commenti:
invece di avere un solo 


altra idea. e se associata alle varie celle potessimo mettere un vettore non interpretabile che deriva dalle informazioni precedenti? tipo una Recursive. In pratica metto associata a una cella un vettore inizialmente nullo che poi viene a


paper:
loro allenano una rete per predirre il funzionamento di un automa cellulare
https://distill.pub/2020/growing-ca/

# Modelli
## SIR
nel modello SIR i resistenti di base non tornano ad essere suscettibili.
si può provare a introdurre una temperatura nel sistema in maniera che la forza di infezione vari in base al tempo.
tentare di introdurre la generazione di numeri pseudorandom.
## Fire Propagation
in genere andiamo a lavorare con un modello dove le celle rappresentano una macchia di vegetazione. la vegetazione viene incendiata a random o dai vicini. una volta che prende fuoco passa un po' di tempo e brucia diventando prima contagiosa e poi immune essendo bruciata.
In certi casi la cella può tornare ad essere susciettibile al fuoco dopo un certo tempo.
