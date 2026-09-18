# Admin overwrite

## Write-up

Dès que le buffer déborde, il écrase is_admin, donc is_admin n'est pas 0 et on a le flag. Il suffit de mettre plus que 32 charactères et on a le flag.

## Flag

`JDIS{adm1n0v3rwr1te}`
