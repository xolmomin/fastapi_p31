# judge_simple.py
import os
import shutil
import subprocess
import tempfile
import textwrap
from pathlib import Path
import difflib
import sys

DOCKER_IMAGE = "crun-python-runner"  # build from Dockerfile.runner
TIMEOUT = 2.0  # seconds wall-clock
MEMORY = "128m"


def normalize_output(s: str):
    # simple normalization: strip trailing whitespace and normalize newlines
    return "\n".join(line.rstrip() for line in s.strip().splitlines())


def run_submission(source_code: str, test_input: str):
    tmp = Path(tempfile.mkdtemp(prefix="crun-judge-"))
    try:
        workspace = tmp / "workspace"
        workspace.mkdir()
        code_file = workspace / "main.py"
        code_file.write_text(source_code)

        # mount workspace read-only into container and pipe input via stdin
        docker_cmd = [
            "docker", "run", "--rm",
            "--network", "none",
            "--memory", MEMORY,
            "--cpus", "0.5",
            "--pids-limit", "64",
            "--read-only",
            "--tmpfs", "/tmp:rw,size=32m",
            "--tmpfs", "/var:rw,size=16m",
            "--tmpfs", "/root:rw,size=16m",
            "--device", "/dev/null:/dev/null",
            "--cap-drop", "ALL",
            "--security-opt", "no-new-privileges",
            "-v", f"{str(workspace)}:/home/crun_test/workspace:ro",
            "-w", "/home/crun_test/workspace",
            "-i", DOCKER_IMAGE,
        ]

        proc = subprocess.Popen(
            docker_cmd,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        try:
            stdout, stderr = proc.communicate(test_input, timeout=TIMEOUT)
        except subprocess.TimeoutExpired:
            proc.kill()
            return {"verdict": "TLE", "stdout": "", "stderr": "timeout (wall-clock)"}

        # container exit code and outputs
        exit_code = proc.returncode
        if exit_code != 0 and stderr:
            return {"verdict": "RE", "stdout": stdout, "stderr": stderr, "exit_code": exit_code}

        return {"verdict": "OK", "stdout": stdout, "stderr": stderr, "exit_code": exit_code}

    finally:
        shutil.rmtree(tmp)


def compare_output(user_out: str, expected_out: str):
    u = normalize_output(user_out)
    e = normalize_output(expected_out)
    ok = u == e
    if ok:
        return {"result": "AC"}
    else:
        diff = "\n".join(difflib.unified_diff(e.splitlines(), u.splitlines(), lineterm=""))
        return {"result": "WA", "diff": diff}


if __name__ == "__main__":
    sample = textwrap.dedent("""
l = map(int, input().split())    
print(*filter(lambda i: i % 2 == 0, l))
    """)

    base = Path(__file__).parent

    input_files = sorted(base.glob("input*.txt"))
    output_files = sorted(base.glob("output*.txt"))

    if len(input_files) != len(output_files):
        print("❌ Mismatch between number of input and output files!")
        sys.exit(1)

    total = len(input_files)
    passed = 0

    for idx, (inp_path, out_path) in enumerate(zip(input_files, output_files), start=1):
        with open(inp_path) as f:
            inp = f.read()
        with open(out_path) as f:
            expected = f.read()

        runr = run_submission(sample, inp)

        if runr["verdict"] != "OK":
            print(f"Runtime Error (Test #{idx})")
            break

        cmp = compare_output(runr["stdout"], expected)
        if cmp.get("result") == "AC":
            print(f"Accepted (Test #{idx})")
            passed += 1
        else:
            print(f"Wrong Answer (Test #{idx})")
            break

    print()
    print(f"Passed {passed}/{total} test cases.")
    if passed == total:
        print("Final Verdict: ✅ Accepted")
    else:
        print("Final Verdict: ❌ Wrong Answer")
