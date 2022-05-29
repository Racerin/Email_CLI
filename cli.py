import click

import library


# @click.command()
# @click.group()
def cli():
    pass

# @cli.command()
@click.command()
def helloworld():
    """ Send a hello world email to self. """
    email = library.Email()
    email.message = "Hello World"
    email.email_to = email.email_from
    email.send_email()


if __name__ == "__main__":
    # cli()
    helloworld()