import subprocess
import sys
from pathlib import Path


def run_cli(args):
    root = Path(__file__).resolve().parents[1]
    cmd = [sys.executable, str(root / "main.py")] + args
    completed = subprocess.run(cmd, capture_output=True, text=True, check=True)
    return completed.stdout.strip()


def test_task1_clause_satisfied():
    out = run_cli(["-question", "1", "-clause", "10 1 -2 0", "-assignment", "10"])  # 1 or not 2 with 1 0
    assert out == "1"


def test_task1_clause_unsatisfied():
    out = run_cli(["-question", "1", "-clause", "10 1 -2 0", "-assignment", "01"])  # 1 or not 2 with 0 1
    assert out == "0"


def test_task2_counts(tmp_path):
    wcnf = tmp_path / "toy.wcnf"
    wcnf.write_text("\n".join([
        "c toy instance",
        "p wcnf 2 2",
        "10 1 -2 0",
        "10 -1 2 0",
    ]))
    out = run_cli(["-question", "2", "-wdimacs", str(wcnf), "-assignment", "10"])  # satisfies first only
    assert out == "1"


