import click


@click.group()
def cli():
    """Login"""
    pass

@cli.command()
def username(): 
    @click.option('--username',
                    help='Username for athentication',
                    required=True)
    
@cli.command()
def password(): 
    @click.option('--password',
                    help='Password for athentication',
                    hide_input=True,
                    required=True)



# def run_ldap_request(username: str, password: str) -> None:
#     ldap_request(username, password)

# if __name__ == '__main__':
#     run_ldap_request()