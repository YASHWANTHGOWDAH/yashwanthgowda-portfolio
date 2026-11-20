import os

DOCS_DIR = os.path.dirname(os.path.abspath(__file__))
MD_PATH = os.path.join(DOCS_DIR, "FINAL_PROJECT_REPORT_BIS786.md")

with open(MD_PATH, "r", encoding="utf-8") as f:
    text = f.read()

idx1 = text.find("flowchart TD")
if idx1 != -1:
    # find preceding ```
    m_start = text.rfind("```", 0, idx1)
    # find following ```
    m_end = text.find("```", idx1)
    if m_end != -1:
        m_end += 3
        fig_tag = '\n\n![Figure 4.1: Random Forest 100-Tree Ensemble Voting & Gini Impurity Structure](figures/fig_4_1_random_forest.png)\n<div align="center"><b>Figure 4.1:</b> Random Forest 100-Tree Ensemble Voting & Gini Impurity Structure</div>\n\n'
        text = text[:m_start] + fig_tag + text[m_end:]
        print("Successfully replaced flowchart with Figure 4.1!")

with open(MD_PATH, "w", encoding="utf-8") as f:
    f.write(text)

print("Remaining flowchart count:", text.count("flowchart"))
