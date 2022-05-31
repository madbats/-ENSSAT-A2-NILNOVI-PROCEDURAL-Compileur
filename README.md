# INFO2 - PROJET COMPILATION: SUJET NNP - MV

*L.Connan - C.Desrayaud - K.Germain - F.Guerin - C.Nicolas - M.Rochard*

La VM utilise la structure conditionnelle match/case **Python 3.10** est donc nécesaire à son execution.

---

## Réalisées

---

## Générateur de code - NNA

Lors de l'analyse syntaxique nous parcourons l'arbre syntaxique. Pour chaque règle syntaxique correspondant à un schéma de compilation, nous rajoutons des instances des instructions de la VM correspondant, à la liste contenur dans une instance du générateur de code. Certaines instruction peuvent prendre des paramettes lors de leur instanciation. De plus on enregistre dans cette instance les symbols initialisé, les symbols sont les clef dictionnaire de Symbole dont la valeur est l'adresse dans la pile.

### Ecriture du code VM

Lorsque le générateur de code récupère le code résultant d'une instruction enregistré, il fournie à cette instance de l'instruction ça table des symboles. L'instance de l'instruction retourne alors le code généré. Si l'instruction à un paramettre (généralement un symbole), on peut récupéré l'adresse de ce symbole dans la table des symboles.

### Class d'instruction

Chaque instruction de la VM possède une classe. Cette classe peut prendre un nombre de paramettre lors de son initialisation correspondant au parramettre que prend l'instruction. Cependant, certaine class peuvent ne pas prendre de paramettre s'il le paramettre sera définit plus tard (principalement les instructions de saut). De plus certaine instruction posède le paramettre hasSymbol (default=True) qui indique si le paramettre est bien un symbol ou simplement une valeur (principalement utilisé pour empiler qui doit parfois empiler l'adresse d'un sylbole et parfois une valeur).

## Machine Virtuelle (VM) - NNA

L'ensemble des instructions de la machine possède une fonction correspondante à l'implémentation de cette instruction. Il suffit donc de parcourir chaque ligne du fichier d'entré et d'appeler la fonction correspondante avec les paramettres passé.

---

## Prévues

---

- [X] Implémenté les instructions spécifique à la machine NNP
- [ ] Implémenté les schémas de compliation spécifique à la machine NNP
- [X] Ajouté l'enregistrement des types à la table des symboles
- [X] Ajouté la vérification des types au class d'instruction VM
- [X] Gestion des environements spécifique à chaque fonction/procédure
- [ ] Gestion des mode de parametres 