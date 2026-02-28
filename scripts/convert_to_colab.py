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
  3. Replaces PROJECT_ROOT / NOTEBOOK_DIR with the Google Drive mountpoint path
  4. Embeds local images (misc/assets/img/) as base64 data URIs in markdown cells
  5. Removes .mkdir() calls from path setup cells (directories exist in shared Drive)
  6. Clears all cell outputs (clean slate for students)

Google Drive layout expected on the student side:
    MyDrive/
    └── Distant_viewing/          ← PROJECT_FOLDER (shared with students)
        ├── notebooks/
        │   ├── 01_europeana_api_and_data.ipynb
        │   └── ...
        ├── data/
        │   ├── images/
        │   └── embeddings/
        ├── models/
        └── misc/
            └── api-key-europeana.txt   ← students put their key here
"""

import argparse
import base64
import json
import mimetypes
import re
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
# Path patterns to detect and replace
# ---------------------------------------------------------------------------

# NB01 — imports cell:
#   NOTEBOOK_DIR = Path(".").resolve()
#   PROJECT_ROOT = NOTEBOOK_DIR.parent
NB01_OLD = 'NOTEBOOK_DIR = Path(".").resolve()\nPROJECT_ROOT = NOTEBOOK_DIR.parent'

# NB02 / 03 / 04 — paths cell (regex handles the double-space alignment):
#   CURRENT_DIR  = Path.cwd()
#   PROJECT_ROOT = CURRENT_DIR.parent
NB_CURRENT_DIR_RE = re.compile(
    r'CURRENT_DIR\s*=\s*Path\.cwd\(\)\s*\nPROJECT_ROOT\s*=\s*CURRENT_DIR\.parent'
)

# NB00 — environment-detection block marker:
#   # Detect environment and set up paths
#   try:
#       import google.colab
NB00_DETECT = "# Detect environment and set up paths\ntry:\n    import google.colab"

# Regex to match the full NB00 setup block (replaced as a whole)
NB00_BLOCK_RE = re.compile(
    r"# Detect environment and set up paths\ntry:.*?print\(f'Models dir.*?'\)",
    re.DOTALL,
)

# Standalone NOTEBOOK_DIR in non-setup cells (e.g. the API key cell):
#   NOTEBOOK_DIR = Path(".").resolve()
# → replaced with NOTEBOOK_DIR = PROJECT_ROOT so the variable stays defined
STANDALONE_NOTEBOOK_DIR_OLD = 'NOTEBOOK_DIR = Path(".").resolve()'
STANDALONE_NOTEBOOK_DIR_NEW = 'NOTEBOOK_DIR = PROJECT_ROOT'


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
# Conversion helpers
# ---------------------------------------------------------------------------

def remove_mkdir_lines(source: str) -> str:
    """Remove .mkdir() call lines from source and collapse extra blank lines."""
    lines = source.split('\n')
    filtered = [line for line in lines if '.mkdir(' not in line]
    result = '\n'.join(filtered)
    # Collapse three or more consecutive newlines into two
    result = re.sub(r'\n{3,}', '\n\n', result)
    return result


def replace_project_root(source: str, project_root_value: str) -> str:
    """
    Replace any known local PROJECT_ROOT assignment with the Colab Drive path.
    Also removes .mkdir() calls from the detected setup cell.
    """
    new_line = f'PROJECT_ROOT = Path("{project_root_value}")'
    was_setup_cell = False

    # NB00: replace the entire environment-detection block with a clean assignment
    if NB00_DETECT in source:
        nb00_replacement = (
            f'PROJECT_ROOT = Path("{project_root_value}")\n'
            'NOTEBOOK_DIR = PROJECT_ROOT\n'
            '\n'
            "DATA_DIR   = PROJECT_ROOT / 'data'\n"
            "IMAGES_DIR = DATA_DIR / 'images'\n"
            "MODELS_DIR = PROJECT_ROOT / 'models' / 'CLIP'\n"
            '\n'
            "print(f'Project root : {PROJECT_ROOT}')\n"
            "print(f'Data dir     : {DATA_DIR}')\n"
            "print(f'Models dir   : {MODELS_DIR}')"
        )
        source, n = NB00_BLOCK_RE.subn(nb00_replacement, source)
        if n:
            was_setup_cell = True

    # NB01: NOTEBOOK_DIR / PROJECT_ROOT block
    if NB01_OLD in source:
        source = source.replace(NB01_OLD, new_line)
        was_setup_cell = True

    # NB02 / 03 / 04: CURRENT_DIR / PROJECT_ROOT block (regex for whitespace variants)
    if NB_CURRENT_DIR_RE.search(source):
        source = NB_CURRENT_DIR_RE.sub(new_line, source)
        was_setup_cell = True

    # Strip .mkdir() calls from setup cells — directories exist in the shared Drive
    if was_setup_cell:
        source = remove_mkdir_lines(source)

    # Standalone NOTEBOOK_DIR in non-setup cells (e.g. API key cell) — keep it defined
    if STANDALONE_NOTEBOOK_DIR_OLD in source:
        source = source.replace(STANDALONE_NOTEBOOK_DIR_OLD, STANDALONE_NOTEBOOK_DIR_NEW)

    return source


def image_to_data_uri(img_path: Path) -> str:
    """Read an image file and return a base64 data URI."""
    mime, _ = mimetypes.guess_type(str(img_path))
    if mime is None:
        ext = img_path.suffix.lower()
        mime = {'svg': 'image/svg+xml', 'webp': 'image/webp'}.get(ext.lstrip('.'), 'application/octet-stream')
    b64 = base64.b64encode(img_path.read_bytes()).decode('ascii')
    return f'data:{mime};base64,{b64}'


def embed_images(source: str, assets_dir: Path) -> str:
    """Replace ../misc/assets/img/<file> references with inline base64 data URIs."""
    def replacer(m):
        alt, rel = m.group(1), m.group(2)
        if '../misc/assets/img/' in rel:
            filename = rel.split('../misc/assets/img/')[-1]
            img_path = assets_dir / filename
            if img_path.exists():
                return f'![{alt}]({image_to_data_uri(img_path)})'
        return m.group(0)

    return re.sub(r'!\[([^\]]*)\]\(([^)]+)\)', replacer, source)


# ---------------------------------------------------------------------------
# Conversion logic
# ---------------------------------------------------------------------------

def convert_notebook(input_path: Path, output_path: Path, project_folder: str,
                     assets_dir: Path) -> None:
    project_root_value = f"{DRIVE_BASE}/{project_folder}"

    with open(input_path, encoding="utf-8") as f:
        nb = json.load(f)

    cells = nb.get("cells", [])

    # 1. Fix paths and embed images
    for cell in cells:
        if cell.get("cell_type") == "code":
            src = source_as_str(cell)
            new_src = replace_project_root(src, project_root_value)
            if new_src != src:
                cell["source"] = str_to_source(new_src)
        elif cell.get("cell_type") == "markdown":
            src = source_as_str(cell)
            new_src = embed_images(src, assets_dir)
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
    script_dir    = Path(__file__).resolve().parent
    repo_root     = script_dir.parent
    notebooks_dir = Path(args.notebooks_dir) if args.notebooks_dir else repo_root / "notebooks"
    output_dir    = notebooks_dir / "colab"
    assets_dir    = repo_root / "misc" / "assets" / "img"

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
            convert_notebook(nb_path, out_path, project_folder, assets_dir)
        except Exception as e:
            print(f"  ✗  {nb_path.name}: {e}")

    print()
    print("Done!")
    print()
    print("Next steps:")
    print(f"  1. Share the following folder with students via Google Drive:")
    print(f"       MyDrive/{project_folder}/")
    print(f"     It should contain: data/  models/  misc/  and the colab notebooks")
    print(f"  2. Put the Europeana API key in misc/api-key-europeana.txt")
    print(f"  3. Students open a notebook in Colab, run the mount cell, then the install cell")


if __name__ == "__main__":
    main()
