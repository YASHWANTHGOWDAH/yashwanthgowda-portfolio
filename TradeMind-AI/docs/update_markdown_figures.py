import os
import re

DOCS_DIR = os.path.dirname(os.path.abspath(__file__))
MD_PATH = os.path.join(DOCS_DIR, "FINAL_PROJECT_REPORT_BIS786.md")

with open(MD_PATH, "r", encoding="utf-8") as f:
    text = f.read()

# Replace any leftover flowchart
start_str = 'flowchart TD\n    A["13 Scaled Technical Features'
if start_str in text:
    idx1 = text.find(start_str)
    # find end of block (either ``` or \n\n)
    idx2 = text.find('P(DOWN) = 1 - P(UP)"]', idx1)
    if idx2 != -1:
        end_idx = idx2 + len('P(DOWN) = 1 - P(UP)"]')
        # check if followed by ```
        if text[end_idx:end_idx+3] == '```':
            end_idx += 3
        # check if preceded by ```mermaid
        mermaid_start = text.rfind('```', 0, idx1)
        if mermaid_start != -1 and idx1 - mermaid_start < 20:
            start_idx = mermaid_start
        else:
            start_idx = idx1
        
        replacement = '![Figure 4.1: Random Forest 100-Tree Ensemble Voting & Gini Impurity Structure](figures/fig_4_1_random_forest.png)\n<div align="center"><b>Figure 4.1:</b> Random Forest 100-Tree Ensemble Voting & Gini Impurity Structure</div>'
        text = text[:start_idx] + replacement + text[end_idx:]
        print("Replaced Figure 4.1 cleanly!")

with open(MD_PATH, "w", encoding="utf-8") as f:
    f.write(text)

print("Saved updated markdown.")
