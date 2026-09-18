# Pirate Register 2

## Write-up

Comme on voit la requête sql qui est faite c'est plus facile de trouver comment faire l'injection.

Le but est de faire une injection de type "union". Si on fait  `%'union select null, null--`, on voit une nouvelle entrée apparaître.

Il faut trouver la table dans laquelle se trouve le flag. Par contre, on ne sait pas le DBMS, il va donc falloir essayer différentes querries pour déterminer c'est laquel. (L'équivalent de la query qui suit se trouve dans pas mal tous les DBMS, donc il faut essayer jusqu'à ce que un fonctionne) on fait donc %'. L'extension de browser `HackBar` peut vous aider un peu avec ça.

```
' union select name, null from from sqlite_master where type='table'--
```

Cela nous permet de découvrir la table `flags`.

On peut ensuite faire `%'union select flag, null from flags--` et avoir le flag

## Flag

`JDIS{un1onSql1nj3ction}`
