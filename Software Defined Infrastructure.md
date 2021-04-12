# Software Defined Infrastructure

**DNS**

1. **Queriyng DNS data**

Da keine `dig` auf dem Ubuntu-Server vorhanden war, wurde dies mit `apt install dnsutils` nachinstalliert. Nachfolgend die Abfragen für diverse Domains mit reverse lookup.

**www.hdm-stuttgart.de**

MX:
`dig +nocmd hdm-stuttgart.de mx +noall +answer`:
  `hdm-stuttgart.de.	2752	IN	MX	10 mx2.hdm-stuttgart.de.`
  `hdm-stuttgart.de.	2752	IN	MX	10 mx4.hdm-stuttgart.de.`
  `hdm-stuttgart.de.	2752	IN	MX	10 mx3.hdm-stuttgart.de.`
  `hdm-stuttgart.de.	2752	IN	MX	10 mx1.hdm-stuttgart.de.`

`dig +noall +answer 10 mx2.hdm-stuttgart.de.`:
  `mx2.hdm-stuttgart.de.	3197	IN	A	141.62.1.23`

`dig +nocmd +noall +answer -x 141.62.1.23`:
  `23.1.62.141.in-addr.arpa. 3142	IN	PTR	mx2.hdm-stuttgart.de.`

NS:
`dig +nocmd hdm-stuttgart.de ns +noall +answer`:
  `hdm-stuttgart.de.	3590	IN	NS	iz-net-4.hdm-stuttgart.de.`
  `hdm-stuttgart.de.	3590	IN	NS	iz-net-3.hdm-stuttgart.de`
  `hdm-stuttgart.de.	3590	IN	NS	dns1.belwue.de.`
  `hdm-stuttgart.de.	3590	IN	NS	iz-net-2.hdm-stuttgart.de.`
  `hdm-stuttgart.de.	3590	IN	NS	dns3.belwue.de.`

`dig +noall +answer dns1.belwue.de.`:
  `dns1.belwue.de.		86400	IN	A	129.143.2.10`

`dig +nocmd +noall +answer -x 129.143.2.10`:
  `10.2.143.129.in-addr.arpa. 86400 IN	PTR	dns1.belwue.de.`

**www.spotify.com**
  
CNAME:
`dig +noall +answer www.spotify.com`:
  `www.spotify.com.	230	IN	CNAME	edge-web-split-geo.dual-gslb.spotify.com.`
  `edge-web-split-geo.dual-gslb.spotify.com. 80 IN	A 35.186.224.25`

`dig +noall +answer -x 35.186.224.25`:
  `25.224.186.35.in-addr.arpa. 120	IN	PTR	25.224.186.35.bc.googleusercontent.com.`


2. **Installing Bind**

  Über folgenden Command wurde Bind9 inklusive den Utils installiert: `apt install bind9 bind9utils`

  In ```bash /etc/bind/``` we need to adjust the `named.conf.options`, for that we need the IP-adress of our domain `sdi3a.mi.hdm-stuttgart.de` we want to forward. For that we used the following command ```bash dig +nocmd sdi3a.mi.hdm-stuttgart.de +noall +answer```, which gives us the following answer `sdi3a.mi.hdm-stuttgart.de. 86400 IN	A	141.62.75.103`. Now we can enter the ip-adress in the already mentioned file.

  **Create zones**

  To create the foward zone we need to adjust the file `named.conf.local` which should look like following: 

  ```bash
  // Do any local configuration here
  //

  zone "forward" {

    type master;

    file "/var/cache/bind/db.forward";

    };

  zone "103.75.62.141.in-addr.arpa“ {

    type master;

    file "/var/cache/bind/db.rev-local";

    };

  // Consider adding the 1918 zones here, if they are not used in your
  // organization
  //include "/etc/bind/zones.rfc1918";
  ```

  **Create cache directory**

  ```bash mkdir -p /var/cache/bind```


  **Configure the created zones**

  In the first step we need to change our directory to ```bash cd /var/cache/bind```.
  We start to configure our forward lookup zone `bind/db.forward` with ```bash vi db.forward```

