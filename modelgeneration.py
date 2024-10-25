import os
import shutil
from pathlib import Path
import subprocess
import logging
import yaml
from dotenv import load_dotenv

load_dotenv(dotenv_path="details.env")

source_name = os.getenv("DBT_SOURCE_NAME")


def create_or_append_source_yml(target_dir: Path, schema_name: str, table_name: str):

    # Use the existing target_dir from the environment
    sources_dir = target_dir / "models" / "sources"
    sources_dir.mkdir(parents=True, exist_ok=True)
    source_file = sources_dir / "sources.yml"

    # Check if sources.yml exists and load its contents if it does
    if source_file.exists():
        with open(source_file, "r", encoding="utf-8") as yaml_file:
            source_yml = yaml.safe_load(yaml_file) or {"version": 2, "sources": []}
            logging.info("Loaded existing sources.yml from %s", source_file)
    else:
        # If the file doesn't exist, start with a new structure
        source_yml = {
            "version": 2,
            "sources": [{"name": source_name, "schema": schema_name, "tables": []}],
        }
        logging.info("Creating new sources.yml at %s", source_file)

    # Since the source is always "hackathon_pratiksha", we don't need to check for source names
    source = source_yml["sources"][0]

    # Check if the table already exists in the source
    if any(table["name"] == table_name for table in source["tables"]):
        logging.info("Table %s already exists in source %s", table_name, source_name)
        return  # No need to append, the table already exists

    # Add the new table to the existing source
    source["tables"].append({"name": table_name})
    logging.info("Added table %s to source %s", table_name, source_name)

    # Write the updated YAML back to the file
    with open(source_file, "w", encoding="utf-8") as yaml_file:
        yaml.dump(source_yml, yaml_file, default_flow_style=False)
        logging.info("Updated sources.yml at %s", source_file)


def clear_dbt_folder(dbt_folder: Path):
    """Removes all contents of the 'dbt' directory but keeps the directory itself."""
    if dbt_folder.exists() and dbt_folder.is_dir():
        for item in dbt_folder.iterdir():
            if item.is_dir():
                shutil.rmtree(item)  # Remove subdirectory and all its contents
            else:
                item.unlink()  # Remove file


def scaffold_empty_project(target_dir: Path, dbt_venv: Path):
    """scaffolds an empty dbt project"""
    # Check if the directory exists
    if target_dir.exists():
        shutil.rmtree(target_dir)

    if not target_dir.parent.exists():
        target_dir.parent.mkdir(parents=True, exist_ok=True)

    if not dbt_venv.exists():
        raise ValueError("dbt venv must already exist")

    cmd = [
        str(dbt_venv / "bin/dbt"),
        "init",
        "--no-version-check",
        "--skip-profile-setup",
        "--project-dir",
        str(target_dir.parent),
        target_dir.name,
    ]

    logging.info("running %s", " ".join(cmd) + " from within " + str(target_dir.parent))
    result = subprocess.check_output(cmd, cwd=str(target_dir.parent))

    logging.info(result)

    (target_dir / "profiles").mkdir()

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


def generate_profiles_yml(target_dir: Path, connection_info: dict):
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

    profiles_yml = target_dir / "profiles/profiles.yml"

    with open(profiles_yml, "w", encoding="utf-8") as yamlfile:
        yaml.dump(yaml_file, yamlfile)
        logging.info("wrote %s", profiles_yml)


def run_dbt_project(target_dir: Path, dbt_venv: Path):
    """Runs dbt project"""
    if not target_dir.exists():
        raise ValueError("target dir must exist")

    if not dbt_venv.exists():
        raise ValueError("dbt venv must already exist")

    profiles_yml = target_dir / "profiles/profiles.yml"
    if not profiles_yml.exists():
        raise ValueError(str(profiles_yml) + " file must exist")

    cmd = [
        str(dbt_venv / "bin/dbt"),
        "run",
        "--no-version-check",
        "--profiles-dir",
        str(profiles_yml.parent),
    ]

    logging.info("running %s", " ".join(cmd))

    try:
        # Ensure we're using the absolute path to `target_dir` in `cwd`
        result = subprocess.check_output(
            cmd, cwd=target_dir.resolve(), stderr=subprocess.STDOUT
        )
        logging.info(result.decode("utf-8"))
        return {"result": result.decode("utf-8")}

    except subprocess.CalledProcessError as e:
        logging.error(f"Command '{e.cmd}' returned non-zero exit status {e.returncode}")
        logging.error(f"Command output:\n{e.output.decode('utf-8')}")
        raise


def create_new_model(target_dir: Path, modelname: str, sqlcode: str):
    """Creates a new dbt model file"""

    modelfile = target_dir / "models" / f"{modelname}.sql"
    if modelfile.exists():
        modelfile.unlink()

    modelfile.write_text(sqlcode, encoding="utf-8")
    logging.info("Model %s created", modelfile)
