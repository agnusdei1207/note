#!/usr/bin/env python3
"""
Zola 빌드 에러: 프론트매터 없는 모든 .md 파일에 프론트매터 추가
"""
import os
import re
from pathlib import Path
from datetime import datetime

def add_frontmatter(file_path):
    """파일에 프론트매터 추가"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"  ❌ 읽기 실패: {file_path} - {e}")
        return False
    
    # 이미 프론트매터가 있으면 스킵
    if content.startswith('+++') or content.startswith('---'):
        return False
    
    # 파일명에서 제목 추출
    filename = Path(file_path).stem
    title = filename.replace('_', ' ').replace('-', ' ').title()
    
    # 경로에서 카테고리 추출
    rel_path = str(file_path).split('content/')[-1]
    parts = rel_path.split('/')
    category = '-'.join(parts[:-1]) if len(parts) > 1 else 'misc'
    
    # 프론트매터 생성
    frontmatter = f'''+++
title = "{title}"
date = "{datetime.now().strftime('%Y-%m-%d')}"
weight = 999
[extra]
categories = "{category}"
+++

{content}'''
    
    # 파일 저장
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(frontmatter)
        return True
    except Exception as e:
        print(f"  ❌ 쓰기 실패: {file_path} - {e}")
        return False

def main():
    """메인 실행"""
    os.chdir('/mnt/c/workspace/brainscience')
    
    # 프론트매터 없는 모든 .md 파일 찾기
    md_files = []
    for root, dirs, files in os.walk('content'):
        # studynote는 제외 (이미 처리됨)
        if 'studynote' in root:
            continue
        
        for file in files:
            if not file.endswith('.md'):
                continue
            
            file_path = os.path.join(root, file)
            
            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    first_line = f.readline().strip()
                
                # 프론트매터 확인
                if not (first_line.startswith('+++') or first_line.startswith('---')):
                    md_files.append(file_path)
            except:
                pass
    
    print(f"📝 프론트매터 없는 파일: {len(md_files)}개")
    
    fixed = 0
    skipped = 0
    
    for file_path in sorted(md_files):
        if add_frontmatter(file_path):
            fixed += 1
            if fixed % 50 == 0:
                print(f"  ✅ {fixed}개 수정 완료...")
        else:
            skipped += 1
    
    print(f"\n✅ 완료: {fixed}개 수정, {skipped}개 스킵")
    print(f"총 {len(md_files)}개 파일 처리")

if __name__ == '__main__':
    main()
