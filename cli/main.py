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

def add_sample():
    """ Add a new CBC sample interactively."""

    from datetime import datetime
    from models.db_models import Sample,CBCResult,AnalysisLog
    from database.db_session import session

    #collect basic patient info
    sample_id = click.prompt("Enter sample ID")
    existing = session.query(Sample).filter_by(sample_id = sample_id).first()
    if existing:
        click.echo(f"\u26A0\uFE0F Sample with ID '(sample_id)' already Exists.")
        return
    
    patient_name = click.prompt("Enter patient name")

    sample = Sample(
        sample_id = sample_id,
        patient_name = patient_name,
        date_collected = datetime.utcnow()
    )
