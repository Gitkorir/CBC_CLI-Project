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


@cli.command()
def add_sample():
    """ Add a new CBC sample interactively."""

    from datetime import datetime
    from models.db_models import Sample,CBCResult,AnalysisLog
    from database.db_session import session

    #collect basic patient info
    sample_id = click.prompt("Enter sample ID")
    existing = session.query(Sample).filter_by(sample_id = sample_id).first()
    if existing:
        click.echo(f"'\u26A0\uFE0F' Sample with ID '(sample_id)' already Exists.")
        return
    
    patient_name = click.prompt("Enter patient name")

    sample = Sample(
        sample_id = sample_id,
        patient_name = patient_name,
        date_collected = datetime.utcnow()
    )
    click.echo("📋 Enter CBC test results:")
    while True:
        test_name = click.prompt("Test Name")
        value = float(click.prompt("Value"))
        units = click.prompt("Units")
        normal_min = float(click.prompt("Normal Range Min"))
        normal_max = float(click.prompt("Normal Range Max"))

        if value < normal_min:
            flag = "Low"
        elif value > normal_max:
            flag = "High"
        else:
            flag = "Normal"

        result = CBCResult(
            test_name=test_name,
            value=value,
            normal_min=normal_min,
            normal_max=normal_max,
            flag=flag
        )

        sample.cbc_results.append(result)

        if not click.confirm("Add another test?"):
            break

    log = AnalysisLog(action="Manual sample entry", timestamp=datetime.utcnow())
    sample.logs.append(log)

    session.add(sample)
    session.commit()
    click.echo("'/u2705' New sample added successfully.")

if __name__ == "__main__":
    cli()
