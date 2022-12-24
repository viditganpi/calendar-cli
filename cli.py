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
@click.option("--count", default=10, help="Count of future events you want to see")
def get_calendar(count):
    calendar_instance = calendar.Calendar()
    calendar_instance.get_calendar(count)

cli.add_command(login)
cli.add_command(get_calendar)

if __name__ == '__main__':
    cli()
