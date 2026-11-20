import os
import re

DOCS_DIR = os.path.dirname(os.path.abspath(__file__))
MD_PATH = os.path.join(DOCS_DIR, "FINAL_PROJECT_REPORT_BIS786.md")

with open(MD_PATH, "r", encoding="utf-8") as f:
    text = f.read()

# Fix Figure 3.1
pattern_3_1 = r'```mermaid\s*\n!\[Figure 3\.1:.*?\]\(figures/fig_3_1_workflow_pipeline\.png\)\n<div.*?</div>\s*\n```\s*\n<div.*?</div>'
repl_3_1 = '![Figure 3.1: End-to-End System Processing and Signal Generation Pipeline](figures/fig_3_1_workflow_pipeline.png)\n<div align="center"><b>Figure 3.1:</b> End-to-End System Processing and Signal Generation Pipeline</div>'
text = re.sub(pattern_3_1, repl_3_1, text, flags=re.DOTALL)

# Fix Figure 4.2
pattern_4_2 = r'```mermaid\s*\n!\[Figure 4\.2:.*?\]\(figures/fig_4_2_xai_attribution\.png\)\n<div.*?</div>\s*\n```\s*\n<div.*?</div>'
repl_4_2 = '![Figure 4.2: Explainable AI (XAI) Feature Attribution and Reason Mapping Flow](figures/fig_4_2_xai_attribution.png)\n<div align="center"><b>Figure 4.2:</b> Explainable AI (XAI) Feature Attribution and Reason Mapping Flow</div>'
text = re.sub(pattern_4_2, repl_4_2, text, flags=re.DOTALL)

# Fix Figure 5.1
pattern_5_1 = r'```mermaid\s*\n!\[Figure 5\.1:.*?\]\(figures/fig_5_1_system_architecture\.png\)\n<div.*?</div>\s*\n```\s*\n<div.*?</div>'
repl_5_1 = '![Figure 5.1: Layered Multi-Tier System Architecture (Data, App, AI, UI)](figures/fig_5_1_system_architecture.png)\n<div align="center"><b>Figure 5.1:</b> Layered Multi-Tier System Architecture (Data, App, AI, UI)</div>'
text = re.sub(pattern_5_1, repl_5_1, text, flags=re.DOTALL)

# Clean any remaining rogue ```mermaid around images
text = re.sub(r'```mermaid\s*\n(!\[Figure.*?\))\n```', r'\1', text)

with open(MD_PATH, "w", encoding="utf-8") as f:
    f.write(text)

print("Cleaned mermaid wrappers around Figures 3.1, 4.2, and 5.1!")
