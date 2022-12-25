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
def get_events(count):
    calendar_instance = calendar.Calendar()
    calendar_instance.get_events(count)

@click.command()
def list_calendars():
    calendar_instance = calendar.Calendar()
    calendar_instance.list_calendars()

cli.add_command(login)
cli.add_command(get_events)
cli.add_command(list_calendars)

if __name__ == '__main__':
    cli()
