from cli import calendar
import click

@click.group()
def cli():
    pass

@click.command()
def login():
    calendar_instance = calendar.Calendar()
    calendar_instance.login()

@click.command()
def get_calendar():
    calendar_instance = calendar.Calendar()
    calendar_instance.get_calendar()

cli.add_command(login)
cli.add_command(get_calendar)

if __name__ == '__main__':
    cli()
