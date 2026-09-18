# Pirate Register 1

## Write-up

C'est une injection sql basique. La requête est `SELECT * FROM users WHERE username = '{username}' AND password = '{password}'`, donc on peut simplement mettre `admin' --` dans le username.

## Flag

`JDIS{s1mpl3_sql1_byp4ss_succ3ss}`
