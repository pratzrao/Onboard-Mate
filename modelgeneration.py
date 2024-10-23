"""generate dbt models on disk from autogen output"""

from pathlib import Path
import subprocess
import logging
import yaml


def scaffold_empty_project(target_dir: Path, dbt_venv: Path):
    """scaffolds an empty dbt project"""

    if target_dir.exists():
        logging.info("target dir %s already exists", target_dir)
        return

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


def generate_profiles_yml(target_dir: Path, connection_info: dict):
    """generates profiles.yml"""

    # this is what should be in the dbt_project.yml
    project_name = target_dir.name

    yaml_file = {
        "config": {},
    }

    yaml_file[project_name] = {
        "outputs": {
            "prod": {
                "host": connection_info["host"],
                "port": connection_info["port"],
                "dbname": connection_info["database"],
                "user": connection_info["user"],
                "password": connection_info["password"],
                "schema": "prod",
                "threads": 4,
                "type": "postgres",
            }
        },
        "target": "prod",
    }

    (target_dir / "profiles").mkdir(exist_ok=True)

    with open(target_dir / "profiles/profiles.yml", "w", encoding="utf-8") as yamlfile:
        yaml.dump(yaml_file, yamlfile)
        logging.info("wrote %s", target_dir / "profiles/profiles.yml")


def run_dbt_project(target_dir: Path, dbt_venv: Path):
    """runs dbt project"""

    if not target_dir.exists():
        raise ValueError("target dir must exist")

    if not dbt_venv.exists():
        raise ValueError("dbt venv must already exist")

    profiles_dir = target_dir / "profiles"

    if not profiles_dir.exists():
        raise ValueError("profiles dir must exist")

    if not (profiles_dir / "profiles.yml").exists():
        raise ValueError("profiles.yml must exist")

    cmd = [
        f"{dbt_venv}/bin/dbt",
        "run",
        "--no-version-check",
        "--profiles-dir",
        str(profiles_dir),
    ]

    logging.info("running %s", " ".join(cmd))
    result = subprocess.check_output(cmd, cwd=target_dir)

    logging.info(result)

    return {"result": result}


def create_new_model(target_dir: Path, modelname: str, sqlcode: str):

    modelfile = target_dir / "models" / modelname / ".sql"
    if modelfile.exists():
        modelfile.unlink()

    modelfile.write_text(sqlcode, encoding="utf-8")
