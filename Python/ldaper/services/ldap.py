from ldap3 import SYNC, Server, Connection, SASL, SUBTREE


def ldap_request(username: str, password: str) -> None:
    server = Server('ldap1.mi.hdm-stuttgart.de', port=636, use_ssl=True)
    connection = Connection(server,
                            auto_bind=False,
                            version=3,
                            client_strategy=SYNC,
                            authentication=SASL,
                            sasl_mechanism='DIGEST-MD5',
                            sasl_credentials=(None, 'username', 'password',
                                              None, 'sign'))
    connection.start_tls()
    result = connection.search('dc=hdm-stuttgart,dc=de',
                               '(uid=dh102)',
                               SUBTREE,
                               attributes=[
                                   'mail', 'gidNumber', 'cn', 'objectClass',
                                   'hdmCategory', 'uid', 'uidNumber',
                                   'shadowLastChange', 'homeDirectory',
                                   'sambaNTPassword', 'sn', 'matrikelNr'
                               ])
    ldif_output = connection.response_to_ldif()
    print(ldif_output)