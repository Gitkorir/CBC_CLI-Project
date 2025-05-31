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
        click.echo(f"'\u26A0\uFE0F' Sample with ID '(sample_id)' already Exists.")
        return
    
    patient_name = click.prompt("Enter patient name")

    sample = Sample(
        sample_id = sample_id,
        patient_name = patient_name,
        date_collected = datetime.utcnow()
    )
     # Predefined test list
    test_names = [
        ("WBC", "x10^9/l", 4.0, 11.0),
        ("RBC", "x10^12/l", 4.7, 6.1),
        ("Hemoglobin", "g/dl", 13.0, 17.0),
        ("Platelets", "x10^9/l", 150, 400),
        ("Hematocrit", "percent", 44, 50),
        ("MCV(mean cell volume)", "fl", 80, 100),
        ("MCH(mean cell hemoglobin)", "pg", 27, 33),
        ("MCHC(mean cell hemoglobin conc.)", "g/dl", 32, 36)
    ]
     # Collect test results interactively
    for name, unit, normal_min, normal_max in test_names:
        value = click.prompt(f"{name} ({unit})", type=float)
        if value < normal_min:
            flag = "Low"
        elif value > normal_max:
            flag = "High"
        else:
            flag = "Normal"

        result = CBCResult(
            test_name=name,
            value=value,
            Units=unit,
            normal_min=normal_min,
            normal_max=normal_max,
            flag=flag
        )
        sample.cbc_results.append(result)

     # Add a log
    log = AnalysisLog(action="Inserted CBC sample via CLI", timestamp=datetime.utcnow())
    sample.logs.append(log)

    # Save to DB
    session.add(sample)
    session.commit()

    click.echo("'\u2705'Sample added successfully.")