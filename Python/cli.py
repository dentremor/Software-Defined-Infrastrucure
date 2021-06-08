import click
from ldaper.services.ldap import ldap_request


@click.command()
@click.argument('username', type=str, required=True)
@click.password_option('--password',
                       help='Password for athentication',
                       hide_input=True,
                       required=True)
def run_ldap_request(username: str, password: str) -> None:
    click.echo(f"{username} {password}")
    ldap_request(username, password)


if __name__ == '__main__':
    run_ldap_request()
