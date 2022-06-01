# INFO2 - PROJET COMPILATION: SUJET NNP - MV

_L.Connan - C.Desrayaud - K.Germain - F.Guerin - C.Nicolas - M.Rochard_

La VM utilise la structure conditionnelle match/case **Python 3.10** est donc nécesaire à son execution.

---

## Réalisées

---

## Générateur de code - NNP

Lors de l'analyse syntaxique nous parcourons l'arbre syntaxique. Pour chaque règle syntaxique correspondant à un schéma de compilation, nous rajoutons des instances des instructions de la VM correspondant, à la liste contenur dans une instance du générateur de code. Certaines instruction peuvent prendre des paramettes lors de leur instanciation. De plus on enregistre dans cette instance les symbols initialisé, les symbols sont les clef dictionnaire de Symbole dont la valeur est l'adresse dans la pile.

### Ecriture du code VM

Lorsque le générateur de code récupère le code résultant d'une instruction enregistré, il fournie à cette instance de l'instruction ça table des symboles. L'instance de l'instruction retourne alors le code généré. Si l'instruction à un paramettre (généralement un symbole), on peut récupéré l'adresse de ce symbole dans la table des symboles.

### Class d'instruction

Chaque instruction de la VM possède une classe. Cette classe peut prendre un nombre de paramettre lors de son initialisation correspondant au parramettre que prend l'instruction. Cependant, certaine class peuvent ne pas prendre de paramettre s'il le paramettre sera définit plus tard (principalement les instructions de saut). De plus certaine instruction posède le paramettre hasSymbol (default=True) qui indique si le paramettre est bien un symbol ou simplement une valeur (principalement utilisé pour empiler qui doit parfois empiler l'adresse d'un sylbole et parfois une valeur).

## Machine Virtuelle (VM) - NNP

L'ensemble des instructions de la machine possède une fonction correspondante à l'implémentation de cette instruction. Il suffit donc de parcourir chaque ligne du fichier d'entré et d'appeler la fonction correspondante avec les paramettres passé.

## Gestion de la mémoire local - NNP

Lors de la délaration d'une opération, nous instancions une version particulère du générateur de code. Celui-ci devient le générateur de code pour la duré de la déclaration, enregistrant les parametres, les variables et les instructions propre à l'opération. Une fois la déclaration terminer l'ancien générateur de code reprend sont role et ajoute le générateur d'opération à sa liste d'opération, en prenent soit d'enregistrer le nombre d'instruction afin de mettre sont conter ordinal à jour.

---

## Prévues

---

- [x] Implémenté les instructions spécifique à la machine NNP
- [x] Implémenté les schémas de compliation spécifique à la machine NNP
- [x] Ajouté l'enregistrement des types à la table des symboles
- [x] Ajouté la vérification des types au class d'instruction VM
- [x] Gestion des environements spécifique à chaque fonction/procédure
- [x] Gestion des mode de parametres
