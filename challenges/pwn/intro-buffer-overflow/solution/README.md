# pwnme

## Write-up

Commencez par ouvrir l'exécutable dans ghidra pour voir dequoi il a l'air.

On voit qu'il y a une fonction secret qui print le flag. Il faut donc réussir à l'appeler.

Première étape est de trouve l'offset pour overwrite le stack et y écrire l'addresse de la fonction "secret" afin qu'elle soit appelée au lieu de ret.

Pour se faire on envoie plein de 'A'. Ça va nous permettre de déterminer combien de charactères il faut envoyer avant que ces charactères ne se rendent au rip (le registre qui contient l'addresse de la prochaine instruction à exécuter). Voir l'étape 1 de [la solution](./solve.py).

Avec l'offset trouvé, il suffit juste d'envoyer le bon nombre de A, puis l'adresse de la fonction qu'on veut appeler pour avoir le flag. Voir l'étape 2 de [la solution](./solve.py).

## Flag

`JDIS{buff3r0verf1ow}`
