# Yummy Sharks

## Write-up

En ouvrant le pcap, on remarque seulement des tcp et des udp packets avec rien d'interessant. Dans la description, il est ecrit que nous valons 0 lors du Top Coffre Pirate (tcp). On peut deduire que UDP vaut 1. On peut donc faire un petit script pour mettre 0 au lieu de tcp et 1 au lieu de udp et avoir le flag en le decodant.

## Flag

`JDIS{1_eat_sh4rks}`
