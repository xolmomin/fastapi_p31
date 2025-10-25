import difflib
import shutil
import subprocess
import tempfile
import textwrap
from pathlib import Path

DOCKER_IMAGE = "crun-python-runner"  # build from Dockerfile.runner
TIMEOUT = 2.0  # seconds wall-clock
MEMORY = "128m"

from database import Problem


def normalize_output(s: str):
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


async def check_code(problem_id: int, code: str):
    print("Checking ...")
    code = textwrap.dedent(code)
    problem = await Problem.get(Problem.id == problem_id, relationship=Problem.examples)

    for testcase in problem.examples:
        print(f"""TestCase {testcase.order_number}
    Input: {testcase.input}
    Output: {testcase.output}
    """)

        progress_submission = run_submission(code, testcase.input)

        if progress_submission["verdict"] != "OK":
            print(f"Runtime Error (Test #{testcase.order_number})")
            break

        cmp = compare_output(progress_submission["stdout"], testcase.output)
        if cmp.get("result") == "AC":
            print(f"Accepted (Test #{testcase.order_number})")
        else:
            print(f"Wrong Answer (Test #{testcase.order_number})")
            break
