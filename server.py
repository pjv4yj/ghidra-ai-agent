from fastapi import FastAPI
from pydantic import BaseModel
import subprocess
from ghidraFunction import run_ghidra_and_get_output

app = FastAPI()

class AnalysisRequest(BaseModel):
    filename: str

def run_aiq_command(filename, analysis_text):
    prompt = f"""
Investigate the Ubuntu binary {filename}. First, use Tavily to search for how it works and any advanced or obscure functionality it may have. Then, analyze the assembly and functions from a Ghidra analysis provided here {analysis_text}. Then search for any publicly known issues or discussions around vulnerabilities in {filename}. Finally, provide a hypothesis on the most likely areas of the binary that could be vulnerable to zero-day attacks and why. Make sure your response is technical and in-depth.
    """

    process = subprocess.Popen(
        ["aiq", "run", "--config_file", "AIQToolkit/simple_workflow.yaml", "--input", prompt],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    stdout, stderr = process.communicate()

    if process.returncode != 0:
        return {"error": stderr.strip(), "stdout": stdout.strip()}
   
    #result = stdout.strip().split("Workflow Result:", 1)[1].strip()


    return {
        "stderr": stderr.strip()
    }

@app.post("/analyze")
async def run_aiq_analysis(request: AnalysisRequest):
    ghidra_output = run_ghidra_and_get_output(request.filename)
    return run_aiq_command(request.filename, ghidra_output)
