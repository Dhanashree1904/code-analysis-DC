import json
import os
from codeload import load_code_files
from analyze import analyze_with_gemini

def run_analysis(folder):
    results = []
    files = load_code_files(folder)

    if not files:
        print("No source code files found in the folder. Please add files to analyze.")
        return

    for f in files:
        print(f"🔍 Analyzing {f['path']} ...")
        gemini_result = analyze_with_gemini(f["content"], f["path"])
        results.append({
            "file": f["path"],
            "hash": f["hash"],
            "analysis": gemini_result
        })

    with open("analysis_report.json", "w", encoding="utf-8") as out:
        json.dump(results, out, indent=2, ensure_ascii=False)

    print("Analysis complete. Results saved to analysis_report.json")

if __name__ == "__main__":
    run_analysis("source_codes")
