import subprocess

def run_ghidra_and_get_output(BINARY_PATH):
    GHIDRA_PATH = "/home/pjvann/ghidra_11.3.2_PUBLIC/support/analyzeHeadless"
    PROJECT_DIR = "/tmp/ghidra_project"
    PROJECT_NAME = "BinaryAnalysis"
    SCRIPT_PATH = "/home/pjvann"  # where extract_info.py is saved

    cmd = [
        GHIDRA_PATH,
        PROJECT_DIR,
        PROJECT_NAME,
        "-import", BINARY_PATH,
        "-scriptPath", SCRIPT_PATH,
        "-postScript", "extract_info.py",
        "-deleteProject"
    ]

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=True
        )
        output = result.stdout + result.stderr
    except subprocess.CalledProcessError as e:
        output = e.stdout + e.stderr

    last_200_lines = "\n".join(output.splitlines()[-200:])
    return last_200_lines


if __name__ == "__main__":
    output = run_ghidra_and_get_output("/bin/ls")
    print(output)
