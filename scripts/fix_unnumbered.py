import os
import re

files_to_fix = [
    ("content/studynote/11_design_supervision/78.md", "78_bpr_isp_integration.md", 78),
    ("content/studynote/11_design_supervision/79.md", "79_developer_cleanroom_vdi_security.md", 79),
    ("content/studynote/11_design_supervision/80.md", "80_cobit_process_evaluation_model.md", 80),
    ("content/studynote/11_design_supervision/81.md", "81_software_architecture.md", 81),
    ("content/studynote/8_algorithm_stats/78.md", "78_probability_distribution.md", 78),
    ("content/studynote/8_algorithm_stats/79.md", "79_bayes_theorem.md", 79)
]

for old_path, new_name, weight in files_to_fix:
    if os.path.exists(old_path):
        with open(old_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Add weight if not exists
        if f'weight = {weight}' not in content:
            content = re.sub(r'(\+\+\+)', f'\\1\nweight = {weight}', content, count=1)
        
        # Write to new path
        new_path = os.path.join(os.path.dirname(old_path), new_name)
        with open(new_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        # Remove old file
        os.remove(old_path)
        print(f"Fixed and renamed {old_path} -> {new_name}")

