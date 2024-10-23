from pathlib import Path
import subprocess
import logging
import yaml
import os
import shutil
from dotenv import load_dotenv
load_dotenv(dotenv_path="details.env")

# Define connection info based on environment variables
connection_info = {
    "host": os.getenv('DBHOST'),
    "port": os.getenv('DBPORT'),
    "database": os.getenv('DBNAME'),
    "user": os.getenv('DBUSER'),
    "password": os.getenv('DBPASSWORD')
}

# Define target_dir and dbt_venv
target_dir = Path("/Users/pratiksharao/Desktop/Tech4Dev/Hack4Impact/Onboard-Mate/dbt_project")  # Path to the DBT project folder
dbt_venv =   Path("/Users/pratiksharao/Desktop/Tech4Dev/Hack4Impact/Onboard-Mate/.venv")# Path to the virtual environment folder
source_name = "hackathon_pratiksha"

def create_or_append_source_yml(schema_name: str, table_name: str):

    # Use the existing target_dir from the environment
    sources_dir = target_dir / "models" / "sources"
    sources_dir.mkdir(parents=True, exist_ok=True)
    source_file = sources_dir / "source.yml"

    # Check if source.yml exists and load its contents if it does
    if source_file.exists():
        with open(source_file, "r", encoding="utf-8") as yaml_file:
            source_yml = yaml.safe_load(yaml_file) or {"version": 2, "sources": []}
            logging.info(f"Loaded existing source.yml from {source_file}")
    else:
        # If the file doesn't exist, start with a new structure
        source_yml = {"version": 2, "sources": [{"name": source_name, "schema": schema_name, "tables": []}]}
        logging.info(f"Creating new source.yml at {source_file}")

    # Since the source is always "hackathon_pratiksha", we don't need to check for source names
    source = source_yml['sources'][0]

    # Check if the table already exists in the source
    if any(table['name'] == table_name for table in source['tables']):
        logging.info(f"Table {table_name} already exists in source {source_name}")
        return  # No need to append, the table already exists

    # Add the new table to the existing source
    source['tables'].append({"name": table_name})
    logging.info(f"Added table {table_name} to source {source_name}")

    # Write the updated YAML back to the file
    with open(source_file, "w", encoding="utf-8") as yaml_file:
        yaml.dump(source_yml, yaml_file, default_flow_style=False)
        logging.info(f"Updated source.yml at {source_file}")


def clear_dbt_folder():
    """Removes all contents of the 'dbt' directory but keeps the directory itself."""
    dbt_folder = Path("dbt")  # Points to the 'dbt' folder in your project root
    if dbt_folder.exists() and dbt_folder.is_dir():
        for item in dbt_folder.iterdir():
            if item.is_dir():
                shutil.rmtree(item)  # Remove subdirectory and all its contents
            else:
                item.unlink()  # Remove file
        

def scaffold_empty_project():
    """scaffolds an empty dbt project"""
    # Check if the directory exists        
    if target_dir.exists():
        shutil.rmtree(target_dir)

    if not target_dir.parent.exists():
        target_dir.parent.mkdir(parents=True, exist_ok=True)

    if not dbt_venv.exists():
        raise ValueError("dbt venv must already exist")

    cmd = [
        f"{dbt_venv}/bin/dbt",
        "init",
        "--no-version-check",
        "--skip-profile-setup",
        target_dir.name,
    ]

    logging.info("running %s", " ".join(cmd))
    result = subprocess.check_output(cmd, cwd=target_dir.parent)

    logging.info(result)

    for file in [
        "models/example/my_first_dbt_model.sql",
        "models/example/my_second_dbt_model.sql",
        "models/example/schema.yml",
        "models/example",
    ]:
        to_delete = target_dir / file
        if to_delete.exists():
            logging.info("deleting %s", str(to_delete))
            if to_delete.is_dir():
                to_delete.rmdir()
            elif to_delete.is_file():
                to_delete.unlink(missing_ok=True)


def generate_profiles_yml():
    """generates profiles.yml"""

    project_name = target_dir.name

    yaml_file = {
        "config": {},
    }

    yaml_file[project_name] = {
        "outputs": {
            "public": {
                "host": connection_info["host"],
                "port": int(connection_info["port"]),
                "dbname": connection_info["database"],
                "user": connection_info["user"],
                "password": connection_info["password"],
                "schema": "public",
                "threads": 4,
                "type": "postgres",
            }
        },
        "target": "public",
    }

    # (target_dir / "profiles").mkdir(exist_ok=True)

    with open(target_dir / "profiles.yml", "w", encoding="utf-8") as yamlfile:
        yaml.dump(yaml_file, yamlfile)
        logging.info("wrote %s", target_dir / "profiles.yml")


def run_dbt_project():
    """Runs dbt project"""
    if not target_dir.exists():
        raise ValueError("target dir must exist")

    if not dbt_venv.exists():
        raise ValueError("dbt venv must already exist")

    profiles_yml = target_dir / "profiles.yml"
    if not profiles_yml.exists():
        raise ValueError(f"Profiles.yml file must exist")
    cmd = [
        f"{dbt_venv}/bin/dbt",
        "run",
        "--no-version-check",
        "--profiles-dir",
        str(target_dir),  # Point to the root of the dbt project where profiles.yml is
    ]

    logging.info("running %s", " ".join(cmd))
    
    try:
        # Ensure we're using the absolute path to `target_dir` in `cwd`
        result = subprocess.check_output(cmd, cwd=target_dir.resolve(), stderr=subprocess.STDOUT)
        logging.info(result.decode("utf-8"))
        return {"result": result.decode("utf-8")}
    
    except subprocess.CalledProcessError as e:
        logging.error(f"Command '{e.cmd}' returned non-zero exit status {e.returncode}")
        logging.error(f"Command output:\n{e.output.decode('utf-8')}")
        raise


def create_new_model(modelname: str, sqlcode: str):
    """Creates a new dbt model file"""

    modelfile = target_dir / "models" / f"{modelname}.sql"
    if modelfile.exists():
        modelfile.unlink()

    modelfile.write_text(sqlcode, encoding="utf-8")
    logging.info("Model %s created", modelfile)



