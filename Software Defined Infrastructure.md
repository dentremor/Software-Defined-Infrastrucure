# Software Defined Infrastructure
## 1. DNS 

### 1.1 Queriyng DNS data

Due to the absence of `dig`, this was installed with the following command 
```bash
$ apt install dnsutils
```

#### 1.1.1 Queriyng www.hdm-stuttgart.de

MX:

```bash
$ dig +nocmd hdm-stuttgart.de mx +noall +answer:
  hdm-stuttgart.de.	2752	IN	MX	10 mx2.hdm-stuttgart.de.
  hdm-stuttgart.de.	2752	IN	MX	10 mx4.hdm-stuttgart.de.
  hdm-stuttgart.de.	2752	IN	MX	10 mx3.hdm-stuttgart.de.
  hdm-stuttgart.de.	2752	IN	MX	10 mx1.hdm-stuttgart.de.
```

```bash
$ dig +noall +answer 10 mx2.hdm-stuttgart.de.:
  mx2.hdm-stuttgart.de.	3197	IN	A	141.62.1.23
```

```bash
$ dig +nocmd +noall +answer -x 141.62.1.23:
  23.1.62.141.in-addr.arpa. 3142	IN	PTR	mx2.hdm-stuttgart.de.
```

NS:
```bash
$ dig +nocmd hdm-stuttgart.de ns +noall +answer:
  hdm-stuttgart.de.	3590	IN	NS	iz-net-4.hdm-stuttgart.de.
  hdm-stuttgart.de.	3590	IN	NS	iz-net-3.hdm-stuttgart.de
  hdm-stuttgart.de.	3590	IN	NS	dns1.belwue.de.
  hdm-stuttgart.de.	3590	IN	NS	iz-net-2.hdm-stuttgart.de.
  hdm-stuttgart.de.	3590	IN	NS	dns3.belwue.de.
```

```bash
$ dig +noall +answer dns1.belwue.de.:
  dns1.belwue.de.		86400	IN	A	129.143.2.10
```

```bash
$ dig +nocmd +noall +answer -x 129.143.2.10:
  10.2.143.129.in-addr.arpa. 86400 IN	PTR	dns1.belwue.de.
```

### 1.1.2 Queriyng www.spotify.com
  
CNAME:
```bash
$ dig +noall +answer www.spotify.com:
  www.spotify.com.	230	IN	CNAME	edge-web-split-geo.dual-gslb.spotify.com.
  edge-web-split-geo.dual-gslb.spotify.com. 80 IN	A 35.186.224.25
```

```bash
$ dig +noall +answer -x 35.186.224.25:
  25.224.186.35.in-addr.arpa. 120	IN	PTR	25.224.186.35.bc.googleusercontent.com.
```


### 1.2 Installing Bind

  Über folgenden Command wurde Bind9 inklusive den Utils installiert: 
  ```bash
  apt install bind9 bind9utils
  ```

  In `/etc/bind/` we need to adjust the `named.conf.options`, for that we need the IP-adress of our domain `sdi3a.mi.hdm-stuttgart.de` we want to forward. For that we used the following command 
  ```bash
  $ dig +nocmd sdi3a.mi.hdm-stuttgart.de +noall +answer:
    sdi3a.mi.hdm-stuttgart.de. 86400 IN	A	141.62.75.103
   ```
   Now we can enter the ip-adress in the already mentioned file.

#### 1.2.1 Create zones

  To create the foward zone we need to adjust the file `named.conf.local` which should look like following: 

  ```bash
  // Do any local configuration here
  //

  zone "forward" {

    type master;

    file "/etc/bind/zones/db.forward";

    };

  zone "103.75.62.141.in-addr.arpa" {

    type master;

    file "/etc/bind/zones/db.rev-local";

    };

  // Consider adding the 1918 zones here, if they are not used in your
  // organization
  //include "/etc/bind/zones.rfc1918";
  ```

#### 1.2.2 Create cache directory

  ```bash 
  $ mkdir -p /var/cache/bind
  ```


#### 1.2.3 Configure the created zones

  In the first step we need to change our directory to
  ```bash 
  $ cd /etc/bind
  $ mkdir zones
  ```
##### 1.2.3.1 Configure forward zone
  We start to configure our forward lookup zone `zones/db.forward` with 
```bash 
$ vim db.forward
```

To get the host record we need to `dig` sdi4a.mi.hdm-stuttgart.de.

```bash
$ dig +noall +answer sdi4a.mi.hdm-stuttgart.de.:
  sdi4a.mi.hdm-stuttgart.de. 86400 IN	A	141.62.75.104
```
With this information we can adjust our file `zones/db.forward` which looks like the following
```
;; db.forward
;; Forward lookup zone

$TTL 604800 
$ORIGIN mi.hdm-stuttgart.de.
@                    IN            SOA            ns4.mi.hdm-stuttgart.de. mail.mi.hdm-stuttgart.de. (

                                                         01

                                                         9H

                                                         3H

                                                         4W

                                                         3H) 

@                                IN            NS                  ns4.mi.hdm-stuttgart.de.

ns4                              IN            A                   141.62.75.104

www4-1                           IN            CNAME               ns4

www4-2                           IN            CNAME               ns4
```

##### 1.2.3.2 Configure reverse zone

With the information we became above from the dig command, we can configure our reverse zone:
```
;; db.rev-local
;; reverse lookup zone

$TTL 604800

@                    IN            SOA            ns4.mi.hdm-stuttgart.de. mail.mi.hdm-stuttgart.de. (

                                                         01     ;<serial-number> 

                                                         9H     ;<time-to-refresh>

                                                         3H     ;<time-to-retry>

                                                         4W     ;<serial-to-expire>

                                                         3H )   ;<minimum-TTL>

@                              IN            NS            ns4.mi.hdm-stuttgart.de.

ns4.mi.hdm-stuttgart.de.       IN            A             141.62.75.104

```

##### 1.2.4 Forwarders

To add forward entry for `www.w3.org` we need the IP-adress which this domain is refering to:
```bash
$ dig +nocmd www.w3.org +noall +answer
  www.w3.org.		247	IN	A	128.30.52.100
```

Now we can add the forwarder in the file `/etc/bind/named.conf.options`:
```
forwarders {
	141.62.75.103;
  128.30.52.100;
};
```

##### 1.2.5 Set mail exchange record

For this we need to set another record in our forward zone `etc/bind/zones/db.forward`:
```
mi.hdm-stuttgart.de.             IN            MX          10      ns4.mi.hdm-stuttgart.de.
```

Test the record via `dig`:
```bash
$ dig +noall +answer mx1.hdm-stuttgart.de.:
  mx1.hdm-stuttgart.de.	2714	IN	A	141.62.1.22
```

## Bibliography


## 2. LDAP 

### 2.1 Recommended Preparations

#### What is the LDAP Protocol? What is the difference between the two protocols ldap and ldaps?
```
"The Lightweight Directory Access Protocol can be used for queriyng and modifying information from distributed directory services." 

The difference between these two protocols are the encrytpion, LDAPS is encrypted via SSL and running on the default port 636, LDAP is encrypted via STARTTLS or decrypted and running on default port 389.
("Editorial - LDAP", 2021)
```

#### What does the acronym dc in dc=somedomain, dc=org stand for?
```
It stands for domain component and represents the namespaces of an object (Willeke, 2019).
```

#### What is the role of LDAP objectclass definitions? How do they relate to LDAP schema definitions?
```
The ObjectClass is a LDAP Schema element AttributeType (Willeke, 2019).
```

#### Describe the relationship between LDAP entries and objectClass values.
```
Each LDAP Entry in the Directory Information Tree has an ObjectClass attribute. The Values of this attribute can be modified but not removed (Willeke, 2019).
```

#### Is it possible to dynamically change an entries structure?
```
No, the structure must conforms the constraint defined by the LDAP Schema (Willeke, 2019).
```

#### What does the term “bind to an LDAP” server mean? What is an “anonymous” bind?
```
Bind is used to authenticate clients to the directory server.

There are three elements inlude in the request:
1. LDAP protocol version
2. Distinguished Name (DN)
3. Credentials for user authentication

At an anonymous bind the above points 2. and 3. are submitted as an empty string.

(Wilson, -)
```

#### Do LDAP servers in general support database features like transactions, ACID semantic etc.?
```
"Lightweight Directory Access Protocol (LDAP) Transactions is define din RFC 5805 and is defined as "Experimental".

As with distinct update operations, each transaction has atomic, consistency, isolation, and durability properties ACID."
(Willeke, 2017)
```

#### Explain the term “replication” in an LDAP server context.
```
For distribution reasons the LDAP-database can be distributed to several servers. There exists one master, on which write-operations are allowed, at the others can only pull the changes from the master (Anonym, 2019).
```

#### Why do organizations sometimes prefer LDAP data repositories rather than using relational database systems?
```
LDAP is very suitable in cases of high read rates and low write rates (write-once-read-many-times). 
Furthermore relational databases like SQL requieres a detailed knowledge about the data structure, which isnt the case when it comes to LDAP.
(ZyTrax, 2019)
```


#### How is the LDIF format being organized? Explain the practical use of LDIF data when running a LDAP service.
```
The format is organized with abjects and attributes. The LDIF datas describes the directory structure which is needed for exchange 
("Editorial - LDIF", 2021)
```

#### LDAP filters

##### How do LDAP filters work?
```
There are several filters in LDAP, with these filters its possible to add criterias to an object search.
(Föckeler, -)
```

##### What is the meaning of the term scope?
```
The LDAP search scope indicates the set of entries at or below the BaseDN that may be considered potential matches for a SearchRequest (Willeke, 2019).
```

##### How do predicate based filters connected by logical and/or/not look like?
```
And:  (& (...K1...) (...K2...) (...K3...) (...K4...))
Or:   (| (...K1...) (...K2...) (...K3...) (...K4...)) 
Not:  (! (...K1...) (...K2...) (...K3...) (...K4...))
```

#### OpenLDAP server software specific questions

##### What does the term “database backend” refer to with respect to OpenLDAP server implementation?
```
Backends do the actual work of storing or retrieving data in response to LDAP requests. Backends may be compiled statically into slapd, or when module support is enabled, they may be dynamically loaded (Open LDAP Foundation, 2021). 
```

##### Why is LDAP replication important?
```
The risk of a failure will be minimized and the traffic load will be reduced.
```
##### How do you restrict access to LDAP directories?
<!-- TODO finish questions. -->


## Bibliography
Willeke, J. (various dates). LDAP Wiki 3. May 2021, from https://ldapwiki.com/wiki

Editorial - LDAP. (2021, April 19). In Wikipedia. https://de.wikipedia.org/wiki/Lightweight_Directory_Access_Protocol

Editorial - LDIF. (2021, April 19). In Wikipedia. https://de.wikipedia.org/wiki/LDAP_Data_Interchange_Format

Bosswell, W. (2003, October 10). ObjectClasses queried 3. May 2021, from https://www.informit.com/articles/article.aspx?p=101405&seqNum=7#:~:text=Domain%20Component%20(DC).,%3DCompany%2Cdc%3Dcom.

Wilson, N. (No datum availabel). The LDAP Bind Operation queried 3. May 2021, from https://ldap.com/the-ldap-bind-operation/

Anonym (2019, September 3). LDAP Wiki 3. May 2021, from https://ldapwiki.com/wiki

ZyTrax Inc. (2019, February 19). LDAP Concepts & Overview 7. May 2021, from http://www.zytrax.com/books/ldap/ch2/

Föckeler, P. (No datum availabel). Das LDAP Scripting Tutorial queried 10. May 2021, from http://www.selfadsi.de/ldap-filter.htm

Open LDAP Foundation. (2021, February 26). OpenLDAP queried 10. May 2021, from https://www.openldap.org/doc/admin25/


### 2.2 Exercises

#### 2.2.1 Browse an existing LDAP Server

##### 2.2.1.1 No Authentication vs. Authentication?
When you are authenticated on the LDPA-server, you can see all datas which belongs to your user. When you are not authenticated you can also see all datas with the exception of the ```matrikelNr```.


#### 2.2.2 Set up an OpenLdap server
First we need to install several packages on our server:
```bash
$ apt install slapd ldap-utils dialog
```
To reconfigure ```slapd``` we need to type ```$ dpkg-reconfigure slapd```.

#### 2.2.3 Populating your DIT
After add all entrys in our tree, it look like the following:
```
version: 1

dn: dc=betrayer,dc=com
objectClass: dcObject
objectClass: organization
objectClass: top
dc: betrayer
o: betrayer.com

dn: cn=admin,dc=betrayer,dc=com
objectClass: organizationalRole
objectClass: simpleSecurityObject
cn: admin
userPassword:: e1NTSEF9UUpzZm96RVFxVTFadEhGN3VrWE96dDNZRi9hc09LaXY=
description: LDAP administrator

dn: ou=departments,dc=betrayer,dc=com
objectClass: organizationalUnit
objectClass: top
ou: departments

dn: ou=software,ou=departments,dc=betrayer,dc=com
objectClass: organizationalUnit
objectClass: top
ou: software

dn: ou=financial,ou=departments,dc=betrayer,dc=com
objectClass: organizationalUnit
objectClass: top
ou: financial

dn: ou=devel,ou=software,ou=departments,dc=betrayer,dc=com
objectClass: organizationalUnit
objectClass: top
ou: devel

dn: ou=testing,ou=software,ou=departments,dc=betrayer,dc=com
objectClass: organizationalUnit
objectClass: top
ou: testing

dn: uid=diana,ou=devel,ou=software,ou=departments,dc=betrayer,dc=com
objectClass: inetOrgPerson
objectClass: organizationalPerson
objectClass: person
objectClass: top
cn: Diana Smith
sn: Smith
uid: diana

dn: uid=daniel,ou=devel,ou=software,ou=departments,dc=betrayer,dc=com
objectClass: inetOrgPerson
objectClass: organizationalPerson
objectClass: person
objectClass: top
cn: Daniel Bean
sn: Bean
uid: daniel
userPassword:: e1NNRDV9QlRqWVBrL2tuSjkrUGNIRk1SeUhBWXdCOHFLeGVMQ2I=

dn: uid=tina,ou=testing,ou=software,ou=departments,dc=betrayer,dc=com
objectClass: inetOrgPerson
objectClass: organizationalPerson
objectClass: person
objectClass: top
cn: Tina Bean
sn: Bean
uid: tina

dn: uid=thomas,ou=testing,ou=software,ou=departments,dc=betrayer,dc=com
objectClass: inetOrgPerson
objectClass: organizationalPerson
objectClass: person
objectClass: top
cn: Thomas Smith
sn: Smith
uid: thomas

dn: uid=frida,ou=financial,ou=departments,dc=betrayer,dc=com
objectClass: inetOrgPerson
objectClass: organizationalPerson
objectClass: person
objectClass: top
cn: Frida Smith
sn: Smith
uid: frida

dn: uid=frederick,ou=financial,ou=departments,dc=betrayer,dc=com
objectClass: inetOrgPerson
objectClass: organizationalPerson
objectClass: person
objectClass: top
cn: Frederick Bean
sn: Bean
uid: frederick
```

#### 2.2.4 Testing a bind operation as non - admin user
![alt text](images/bind_login.png "Screenshot")

#### 2.2.5 Filter based search

All users with a ```uid``` attribute value starting with the letter “b”:
```
(uid=b*)
```

All entries with either a defined ```uid``` attribute or a ```ou``` attribute starting with letter “d”:
```
(|(uid=d*)(ou=d*))
```

All users entries within the whole DIT having a gidNumber value of 100:
![alt text](images/gidNumber_equal_100.png "Screenshot")

All users entries within the whole DIT having a gidNumber value greater then 1023:
![alt text](images/gidNumber_greater_than_1023.png "Screenshot")

All users entries within the whole DIT having the substring "ei" in their cn attribute:
![alt text](images/cn_contains_ei.png "Screenshot")

All users entries within the whole DIT having starting with the character "t" in their uid attribute or the gidNumber is equal to 100:
![alt text](images/last.png "Screenshot")


#### 2.2.6 Extending an existing entry
The entry uid=bean,ou=devel,ou=software,ou=departments,dc=betrayer;dc=com may be extended by the objectclass posixAccount. Construct a LDIF file to add the attributes uidNumber, gidNumber and homeDirectory by a modify/add operation.

```
uid=bean, ou=devel, ou=software, ou=departments, dc=betrayer, dc=com
changetype: add
objectClass: posixAccount
uidNumber: 42
gidNumber: 1337
homeDirectory: /
```

#### 2.2.7 Accessing LDAP data by a mail client
![alt text](images/LDAP-Thunderbird.png "Screenshot")

#### 2.2.8 LDAP configuration
![alt text](images/LDAP-Bind-Authentication.png "Screenshot")

#### 2.2.9 LDAP based user login
##### 2.2.9.1 Test connection to active directory
```
$ root@sdi3b:~# telnet sdi3a.mi.hdm-stuttgart.de 389
```
```
Trying 141.62.75.103...
Connected to sdi3a.mi.hdm-stuttgart.de.
Escape character is '^]'.
```

##### 2.2.9.2 Install and configure libpam-ldapd
```
$ apt-get install libpam-ldapd
```
After the installation a window will open, where we can configure the package.

In the following window we need to enter the hostname to our arctive directories.
![alt text](images/pam1.png "Screenshot")

After that we need to enter the distinguished name.
![alt text](images/pam2.png "Screenshot")

TEXT
![alt text](images/pam3.png "Screenshot")

After the configuration the installation of the package will be finished and we need to reboot the VM.

After that we can run request
```
$ id daniel
uid=42(daniel) gid=1337 Gruppen=1337
```

In the last step we need to create a user and a group accordingly, which we need to assign to the user:
```bash
$ groupadd -g 1337 betrayer_software_devel
$ useradd -u 42 daniel
$ usermod -g betrayer_software_devel daniel
$ mkhomedir_helper daniel
```


#### 2.2.10 Backup and recovery / restore

Create a backup of the OpenLDAP database configuration to an LDIF file. 
```bash
$ slapcat -b cn=config -l ldap-config.ldif
```

Create a backup of the OpenLDAP data. 
```bash 
$ slapcat -l ldap-data.ldif
```

Copy the data and configuration backup from the OpenLDAP provider server to the OpenLDAP consumer server. 
```bash 
$ scp {ldap-data.ldif,ldap-config.ldif} root@sdi3b.mi.hdm-stuttgart.de:
```

Now we need to access our consumer server via ssh.
```bash
$ ssh root@sdi3b.mi.hdm-stuttgart.de
```

Restore the OpenLDAP provider Data and configs on the consumer server.
Stop the LDAP service.
```bash 
$ systemctl stop slapd
```

Ensure that the LDAP configuration and data directories are empty.
```bash 
$ rm -rf /etc/ldap/slapd.d/* 
$ rm -rf /var/lib/ldap/*
```

Restore the configuration backup. 
```bash
$ slapadd -b cn=config -l /root/ldap-config.ldif -F /etc/ldap/slapd.d/
```

Restore the LDAP data directories. 
```bash
$ slapadd -n 1 -l /root/ldap-data.ldif -F /etc/ldap/slapd.d/
```

#### 2.2.11 Accessing LDAP by a Pyhton application.
<!-- Is it possible to use Pyhton pretty please -->
https://www.python-ldap.org/en/python-ldap-3.3.0/
https://github.com/python-ldap/python-ldap