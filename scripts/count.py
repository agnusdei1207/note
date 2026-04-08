import os
import glob
import re

subjects = {
    "4_software_engineering": "SE",
    "5_database": "DB",
    "6_ict_convergence": "ICT",
    "7_enterprise_systems": "Enterprise",
    "8_algorithm_stats": "Algorithm",
    "9_security": "Security",
    "10_ai": "AI",
    "11_design_supervision": "Design",
    "12_it_management": "IT_Mgmt",
    "13_cloud_architecture": "Cloud",
    "14_data_engineering": "DataEng",
    "15_devops_sre": "DevOps",
    "16_bigdata": "BigData"
}

total = 0
for folder, name in subjects.items():
    dir_path = os.path.join("content/studynote", folder)
    count = 0
    for root, _, files in os.walk(dir_path):
        for f in files:
            if re.match(r'^0*\d+[_\.]', f):
                count += 1
    print(f"{name}: {count}")
    total += count

print(f"Total: {total + 802 + 800 + 1120}") # CA, OS, NW
