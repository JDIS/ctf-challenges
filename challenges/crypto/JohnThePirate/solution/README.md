# John The Pirate

## Write-up

Le zip est locked par un mot de passe. Le titre du challenge John The Pirate fait penser a John The Ripper. On peut utiliser la commande de snap john-the-ripper
```bash
john-the-ripper.zip2john flag.zip > hash.txt
```
afin d'avoir la version hashed du zip, car john-the-ripper ne peut pas directement tester de crack le fichier. On peut ensuite brute force ce hash avec un dictionnaire de mot de passe connu comme rockyou.txt afin d'avoir le mot de passe p1r4t3k1ng

```bash
john-the-ripper --wordlist=rockyou.txt hash.txt
```

On peut ainsi ouvrir flag.txt.

## Flag

`JDIS{j0hn_z1p_cr4ck3r}`
