# WalkingOnWaterBinsAndBits

## Write-up

Dans le description, les mots en majuscules BIN et WALK nous piste sur quoi utiliser. En effet, o voit avec binwalk qu'il y a un png de cache dans l'image originale. Il faut l'extraire avec la commande

```bash
dd if=pirate_ship.jpg of=output.png bs=1 skip=390148
```
On peut ensuite uploader output.png sur un site tel que StegOnline pour voir le flag dans le bit plane 0 du bleu.

## Flag

`JDIS{b1nw4lk_1nt0_b1tpl4n3_w4lk}`
