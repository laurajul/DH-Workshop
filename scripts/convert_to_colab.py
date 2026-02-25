#!/usr/bin/env python3
"""
Convert local development notebooks to Google Colab format.

Usage:
    python3 scripts/convert_to_colab.py
    python3 scripts/convert_to_colab.py --project-folder MyFolder

Output:
    notebooks/colab/<same_filename>.ipynb

What the script does for each notebook:
  1. Inserts a Google Drive mount cell at the very top
  2. Inserts a pip install cell for CLIP and other dependencies
  3. Replaces PROJECT_ROOT with the Google Drive mountpoint path
  4. Clears all cell outputs (clean slate for students)

Google Drive layout expected on the student side:
    MyDrive/
    └── Distant_viewing/          ← PROJECT_FOLDER (shared with students)
        ├── notebooks/
        │   ├── 01_europeana_api_and_data.ipynb
        │   └── ...
        ├── data/
        ├── images/
        └── misc/
            └── api-key-europeana.txt   ← students put their key here
"""

import argparse
import json
import copy
from pathlib import Path


# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

DRIVE_MOUNT = "/content/drive"
DRIVE_BASE  = f"{DRIVE_MOUNT}/MyDrive"

# ---------------------------------------------------------------------------
# Colab cells to inject
# ---------------------------------------------------------------------------

MOUNT_CELL_SOURCE = """\
# Mount Google Drive
# If already mounted this will show "Drive is already mounted" — that's fine.
from google.colab import drive
drive.mount('/content/drive')\
"""

INSTALL_CELL_SOURCE = """\
# Install packages that are not pre-installed in Colab
# (torch, torchvision, numpy, Pillow, requests are already available)
!pip install -q git+https://github.com/openai/CLIP.git ftfy\
"""

# ---------------------------------------------------------------------------
# Path patterns to replace
# ---------------------------------------------------------------------------

# Notebook 01 — setup-code cell:
#   PROJECT_ROOT = Path("../").resolve()
NB01_OLD = 'PROJECT_ROOT = Path("../").resolve()'

# Notebooks 02 / 03 / 04 — paths cell:
#   CURRENT_DIR = Path.cwd()
#   PROJECT_ROOT = CURRENT_DIR.parent
NB_OLD_BLOCK = "CURRENT_DIR = Path.cwd()\nPROJECT_ROOT = CURRENT_DIR.parent"

# Notebook 04 has a slightly shorter paths cell (no extra path vars):
#   CURRENT_DIR = Path.cwd()
#   PROJECT_ROOT = CURRENT_DIR.parent


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def source_as_str(cell: dict) -> str:
    """Return cell source as a plain string regardless of list vs str."""
    src = cell.get("source", "")
    return "".join(src) if isinstance(src, list) else src


def str_to_source(text: str) -> list:
    """Store source as a list of lines (notebook convention)."""
    if not text:
        return []
    lines = text.split("\n")
    return [line + "\n" for line in lines[:-1]] + [lines[-1]]


def make_code_cell(cell_id: str, source: str) -> dict:
    return {
        "cell_type": "code",
        "id": cell_id,
        "metadata": {},
        "source": str_to_source(source),
        "outputs": [],
        "execution_count": None,
    }


def make_markdown_cell(cell_id: str, source: str) -> dict:
    return {
        "cell_type": "markdown",
        "id": cell_id,
        "metadata": {},
        "source": str_to_source(source),
    }


# ---------------------------------------------------------------------------
# Conversion logic
# ---------------------------------------------------------------------------

def replace_project_root(source: str, project_root_value: str) -> str:
    """
    Replace any known local PROJECT_ROOT assignment with the Colab path.
    Returns the (possibly modified) source string.
    """
    new_line = f'PROJECT_ROOT = Path("{project_root_value}")'

    # Pattern used in notebook 01
    if NB01_OLD in source:
        source = source.replace(NB01_OLD, new_line)

    # Pattern used in notebooks 02 / 03 / 04
    if NB_OLD_BLOCK in source:
        source = source.replace(NB_OLD_BLOCK, new_line)

    return source


def convert_notebook(input_path: Path, output_path: Path, project_folder: str) -> None:
    project_root_value = f"{DRIVE_BASE}/{project_folder}"

    with open(input_path, encoding="utf-8") as f:
        nb = json.load(f)

    cells = nb.get("cells", [])

    # 1. Replace PROJECT_ROOT in all code cells
    for cell in cells:
        if cell.get("cell_type") != "code":
            continue
        src = source_as_str(cell)
        new_src = replace_project_root(src, project_root_value)
        if new_src != src:
            cell["source"] = str_to_source(new_src)

    # 2. Clear all outputs for a clean student experience
    for cell in cells:
        if cell.get("cell_type") == "code":
            cell["outputs"] = []
            cell["execution_count"] = None

    # 3. Prepend mount + install cells (mount first, then install)
    install_cell = make_code_cell("colab-install-deps", INSTALL_CELL_SOURCE)
    mount_cell   = make_code_cell("colab-mount-drive",  MOUNT_CELL_SOURCE)

    nb["cells"] = [mount_cell, install_cell] + cells

    # 4. Write output
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(nb, f, indent=1, ensure_ascii=False)
        f.write("\n")  # trailing newline

    print(f"  ✓  {input_path.name}")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument(
        "--project-folder",
        default="Distant_viewing",
        metavar="NAME",
        help="Name of the shared Google Drive folder (default: Distant_viewing)",
    )
    parser.add_argument(
        "--notebooks-dir",
        default=None,
        metavar="PATH",
        help="Path to the notebooks directory (default: <repo_root>/notebooks)",
    )
    args = parser.parse_args()

    # Resolve paths relative to this script's location
    script_dir   = Path(__file__).resolve().parent
    repo_root    = script_dir.parent
    notebooks_dir = Path(args.notebooks_dir) if args.notebooks_dir else repo_root / "notebooks"
    output_dir   = notebooks_dir / "colab"

    notebooks = sorted(notebooks_dir.glob("*.ipynb"))
    if not notebooks:
        print(f"No notebooks found in {notebooks_dir}")
        return

    project_folder = args.project_folder
    drive_path = f"{DRIVE_BASE}/{project_folder}"

    print(f"Converting {len(notebooks)} notebook(s) → {output_dir}/")
    print(f"  Google Drive path : {drive_path}")
    print(f"  Project folder    : {project_folder}")
    print()

    for nb_path in notebooks:
        out_path = output_dir / nb_path.name
        try:
            convert_notebook(nb_path, out_path, project_folder)
        except Exception as e:
            print(f"  ✗  {nb_path.name}: {e}")

    print()
    print("Done!")
    print()
    print("Next steps:")
    print(f"  1. Copy the following folders to MyDrive/{project_folder}/:")
    print(f"       data/  images/  misc/  notebooks/colab/  (rename colab/ → notebooks/)")
    print(f"  2. Put the Europeana API key in misc/api-key-europeana.txt")
    print(f"  3. Open a notebook in Colab and run the mount + install cells first")


if __name__ == "__main__":
    main()
