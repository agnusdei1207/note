import re

stats = {
    "CA (컴퓨터구조)": (802, 802),
    "OS (운영체제)": (800, 800),
    "NW (네트워크)": (1120, 1120),
    "SE (소프트웨어공학)": (683, 800),
    "DB (데이터베이스)": (600, 600),
    "ICT (ICT융합)": (471, 552),
    "Enterprise (엔터프라이즈)": (250, 482),
    "Algorithm (알고리즘/통계)": (59, 160),
    "Security (보안)": (338, 1030),
    "AI (인공지능)": (243, 420),
    "Design (설계감리)": (145, 452),
    "IT_Mgmt (IT관리)": (150, 374),
    "Cloud (클라우드)": (157, 372),
    "DataEng (데이터엔지니어링)": (132, 258),
    "DevOps (DevOps/SRE)": (141, 372),
    "BigData (빅데이터)": (88, 236),
}

total_completed = sum(c for c, t in stats.values())
total_target = sum(t for c, t in stats.values())

with open("AGENTS.md", "r", encoding="utf-8") as f:
    content = f.read()

# Replace the table
table_start = content.find("| 과목 | 완료 | 전체(키워드) | 비율 |")
if table_start != -1:
    table_end = content.find("--- End of content ---", table_start)
    if table_end == -1:
        table_end = len(content)

    new_table = "| 과목 | 완료 | 전체(키워드) | 비율 |\n|:---:|:---:|:---:|:---:|\n"
    for name, (comp, tot) in stats.items():
        ratio = (comp / tot) * 100 if tot > 0 else 0
        new_table += f"| {name} | {comp:,} | {tot:,} | {ratio:.1f}% |\n"
    new_table += f"| **합계** | {total_completed:,} | {total_target:,} | {(total_completed/total_target)*100:.1f}% |\n"
    
    content = content[:table_start] + new_table

with open("AGENTS.md", "w", encoding="utf-8") as f:
    f.write(content)

