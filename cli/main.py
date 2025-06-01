# cli/main.py
import click
from database.db_session import session
from models.db_models import Sample


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
@click.argument("sample_id")
def view_sample(sample_id):
    """View detailed CBC results for a sample."""
    from models.db_models import Sample
    sample = session.query(Sample).filter_by(sample_id=sample_id).first()
    if not sample:
        click.echo(f"❌ Sample with ID '{sample_id}' not found.")
        return

    click.echo(f"\n🧾 Sample ID: {sample.sample_id}")
    click.echo(f"👤 Patient: {sample.patient_name}")
    click.echo(f"📅 Collected: {sample.date_collected}\n")

    click.echo("🧪 CBC Results:")
    for result in sample.cbc_results:
        click.echo(f"- {result.test_name}: {result.value} {result.units} "
                   f"(Normal: {result.normal_min}–{result.normal_max}) ➤ [{result.flag}]")



@cli.command()
@click.option('--id', 'sample_id', prompt=True, help="Sample ID to delete")
def delete_sample(sample_id):
    """Delete a sample and its associated data."""
    sample = session.query(Sample).filter_by(sample_id=sample_id).first()
    if not sample:
        click.echo(click.style(f"⚠️ Sample ID '{sample_id}' not found.", fg='red'))
        return

    confirm = click.confirm(click.style(f"Are you sure you want to delete Sample '{sample_id}'?", fg='yellow'))
    if confirm:
        session.delete(sample)
        session.commit()
        click.echo(click.style(f"✅ Sample '{sample_id}' deleted successfully.", fg='green'))
    else:
        click.echo(click.style("❌ Deletion cancelled.", fg='cyan'))




@cli.command()
def add_sample():
    """ Add a new CBC sample interactively."""
    from utils.unit_map import UNIT_MAP
    from datetime import datetime
    from models.db_models import Sample,CBCResult,AnalysisLog,CBCTest

    from database.db_session import session

    #collect basic patient info
    sample_id = click.prompt("Enter sample ID")
    existing = session.query(Sample).filter_by(sample_id = sample_id).first()
    if existing:
        click.echo(f"'\u26A0\uFE0F', Sample with ID '(sample_id)' already Exists.")
        return
    
    patient_name = click.prompt("Enter patient name")

    sample = Sample(
        sample_id = sample_id,
        patient_name = patient_name,
        date_collected = datetime.utcnow()
    )
    session.add(sample)

    click.echo("📋 Enter CBC test results:")
    while True:
        test_name = click.prompt("Test Name")
        value = float(click.prompt("Value"))

        # Fetch reference data from CBCTest
        cbctest = session.query(CBCTest).filter(CBCTest.test_name.ilike(test_name)).first()

        if not cbctest:
            click.echo(f"⚠️ No reference data found for '{test_name}'. Skipping.")
            continue

        if value < cbctest.normal_min:
          flag = "Low"
        elif value > cbctest.normal_max:
          flag = "High"
        else:
         flag = "Normal"


       

        result = CBCResult(
            test_name=test_name.upper(),
            value=value,
            units=cbctest.units,
            normal_min=cbctest.normal_min,
            normal_max=cbctest.normal_max,
            sample=sample,
            flag = flag
        )
        session.add(result)

        sample.cbc_results.append(result)

        if not click.confirm("Add another test?"):
            break

    log = AnalysisLog(action="Manual sample entry", timestamp=datetime.utcnow())
    sample.logs.append(log)

    session.add(sample)
    session.commit()
    click.echo("'\u2705', New sample added successfully.")

if __name__ == "__main__":
    cli()
