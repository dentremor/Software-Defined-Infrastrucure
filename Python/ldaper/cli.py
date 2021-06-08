import click
from ldaper.ldap import ldap_request


@click.command()
@click.argument('username', type=str, required=True)
@click.password_option('--password', required=True)
def run_ldap_request(username, password):
    click.echo('------------------ Results ------------------\n' +
               ldap_request(username, password))


if __name__ == '__main__':
    run_ldap_request()
