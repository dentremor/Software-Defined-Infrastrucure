# Software Defined Infrastructure

**DNS**

1. **Queriyng DNS data**

Da keine `dig` auf dem Ubuntu-Server vorhanden war, wurde dies mit `apt install dnsutils` nachinstalliert. Nachfolgend die Abfragen für diverse Domains mit reverse lookup.

- **www.hdm-stuttgart.de**
`dig +noall +answer www.hdm-stuttgart.de`:
  `www.hdm-stuttgart.de.	2420	IN	A	141.62.1.53`
  `www.hdm-stuttgart.de.	2420	IN	A	141.62.1.59`

`dig +noall +answer -x 141.62.1.53`:
  `53.1.62.141.in-addr.arpa. 3590	IN	PTR	iz-www-2.hdm-stuttgart.de.`

`dig +noall +answer -x 141.62.1.59`:
  `59.1.62.141.in-addr.arpa. 3600	IN	PTR	iz-www-1.hdm-stuttgart.de.`


- **www.spotify.com**
`dig +noall +answer www.spotify.com`:
  `www.spotify.com.	230	IN	CNAME	edge-web-split-geo.dual-gslb.spotify.com.`
  `edge-web-split-geo.dual-gslb.spotify.com. 80 IN	A 35.186.224.25`

`dig +noall +answer -x 35.186.224.25`:
  `25.224.186.35.in-addr.arpa. 120	IN	PTR	25.224.186.35.bc.googleusercontent.com.`



