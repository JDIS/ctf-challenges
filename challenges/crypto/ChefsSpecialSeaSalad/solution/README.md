# Chef's Special Sea Salad

## Write-up

Le titre du challenge nous fait penser a CyberChef. En suivant recipe.txt, on a un indice pour chaque etape de decryption des raw ingredients.

1. Octopus = base 8 (octal)
2. 13 rotations = ROT13
3. Twofish decrypt avec les 2 keys
4. From base85

## Flag

`JDIS{ch3f's_s4l4d}`
