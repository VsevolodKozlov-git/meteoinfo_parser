from pathlib import Path


class Config:
    project_root_path = Path(__file__).parent.parent
    sleep_time = 5
    xlsx_dir_path = project_root_path / 'xlsx'
