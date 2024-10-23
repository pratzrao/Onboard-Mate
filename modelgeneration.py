"""generate dbt models on disk from autogen output"""

from pathlib import Path
import subprocess
import logging


def scaffold_empty_project(target_dir: Path, dbt_venv: Path):
    """scaffolds an empty dbt project"""

    if target_dir.exists():
        logging.info("target dir %s already exists", target_dir)
        return

    if not target_dir.parent.exists():
        target_dir.mkdir(parents=True, exist_ok=True)

    if not dbt_venv.exists():
        raise ValueError("dbt venv must already exist")

    cmd = [
        f"{dbt_venv}/bin/dbt",
        "init",
        "--no-version-check",
        "--profile-dir",
        "--skip-profile-setup",
        target_dir,
    ]

    logging.info("running %s", " ".join(cmd))
    result = subprocess.check_output(cmd)

    logging.info(result)

    for file in [
        "models/example/my_first_dbt_model.sql",
        "models/example/my_second_dbt_model.sql",
    ]:
        to_delete = target_dir / "models" / file
        if to_delete.exists():
            logging.info("deleting %s", str(to_delete))
            to_delete.unlink()
