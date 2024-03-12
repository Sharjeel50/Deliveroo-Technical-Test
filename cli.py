import click

from cron_parser import CronParser


@click.command()
@click.option("--expression", prompt="Cron Expression")
def cli(expression):
    cron_parser_instance = CronParser()
    cron_parser_instance.parse(expression)
    click.echo(cron_parser_instance.logg_results())


if __name__ == "__main__":
    cli()

# */15 1 1-15 1-12 1,5 /usr/bin/find
