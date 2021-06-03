from ldap3 import Server, Connection

conn = Connection('ldap1.mi.hdm-stuttgart.de', auto_bind=True)
conn.search('dc=hdm-stuttgart,dc=de', '(uid=example)')
print(conn.entries)