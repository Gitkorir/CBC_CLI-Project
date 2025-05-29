# cli/main.py
import click
from database.db_session import session
from models.db_models import Sample  # Make sure this matches your actual model name

@click.group()
def cli():
    pass

@cli.command()
def list_samples():
    samples = session.query(Sample).all()
    if not samples:
        click.echo("No samples found.")
    else:
        for sample in samples:
            click.echo(f"Sample ID: {sample.sample_id}, Patient: {sample.patient_name}, Collected: {sample.date_collected}")

if __name__ == "__main__":
    cli()

