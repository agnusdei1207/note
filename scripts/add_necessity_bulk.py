import os
import glob
import re
import json
import urllib.request
import urllib.error
import concurrent.futures

API_KEY = os.environ.get("ANTHROPIC_API_KEY")
BASE_URL = os.environ.get("ANTHROPIC_BASE_URL", "https://api.z.ai/api/anthropic")
MODEL = "glm-4.7"

def generate_necessity(title, concept):
    url = f"{BASE_URL}/v1/messages"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }
    
    prompt = f"""당신은 IT/컴퓨터구조 기술사 문서 작성 전문가입니다.
다음 개념의 '필요성'을 작성해주세요. 

주제: {title}
개념: {concept}

작성 지침:
1. 반드시 '- **필요성**: '으로 시작할 것.
2. 이 기술/개념이 왜 필요한지, 실무와 시스템에서 해결하고자 하는 근본적인 문제와 도입 가치에 집중할 것.
3. 2~3문장으로 간결하고 명확하게 작성할 것.
4. 마크다운 형식 유지.
"""
    
    data = {
        "model": MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 512,
        "temperature": 0.7
    }
    
    req = urllib.request.Request(url, data=json.dumps(data).encode('utf-8'), headers=headers)
    try:
        with urllib.request.urlopen(req) as response:
            res_data = json.loads(response.read().decode('utf-8'))
            return res_data['content'][0]['text'].strip()
    except Exception as e:
        print(f"Error calling API for {title}: {e}")
        return None

def process_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        if "- **필요성**:" in content or "## Ⅰ. 개요 및 필요성" in content:
            return f"Skipped (already has necessity): {file_path}"

        # Extract Title
        title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
        title = title_match.group(1) if title_match else os.path.basename(file_path)
        
        # Extract 개념 (Try both 한글 and 한자)
        concept_match = re.search(r'-\s*\*\*(?:개념|概念)\*\*:\s*(.*?)(?=\n\n-\s*\*\*)', content, re.DOTALL)
        if not concept_match:
            concept_match = re.search(r'-\s*\*\*(?:개념|概念)\*\*:\s*(.*)', content)
        concept = concept_match.group(1).strip() if concept_match else ""

        # Generate 필요성
        necessity = generate_necessity(title, concept)
        if not necessity:
            return f"Failed to generate for: {file_path}"

        # Replace Header
        content = content.replace("## Ⅰ. 개요 (Context & Background)", "## Ⅰ. 개요 및 필요성 (Context & Necessity)")
        content = content.replace("## Ⅰ. 개요 및 필요성 (Context & Background)", "## Ⅰ. 개요 및 필요성 (Context & Necessity)")
        
        # Insert 필요성 before 비유
        def repl_biyu(m):
            return f"- **필요성**: {necessity}\n" + m.group(0)
            
        content = re.sub(r'(-\s*\*\*💡 비유\*\*:)', repl_biyu, content, count=1)

        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
            
        return f"Processed: {file_path}"
    except Exception as e:
        return f"Error processing {file_path}: {e}"

def main():
    target_dir = "content/studynote/1_computer_architecture"
    md_files = glob.glob(os.path.join(target_dir, "**/*.md"), recursive=True)
    
    # Exclude special files
    md_files = [f for f in md_files if not os.path.basename(f).startswith('_')]
    
    print(f"Found {len(md_files)} files. Starting processing...")
    
    import time
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        def process_with_sleep(f):
            time.sleep(1.0)
            return process_file(f)
        results = []
        for i, f in enumerate(md_files):
            r = process_with_sleep(f)
            results.append(r)
            if i % 10 == 0:
                print(f"Processed {i+1}/{len(md_files)} files...")
        
    processed_count = sum(1 for r in results if r.startswith("Processed"))
    skipped_count = sum(1 for r in results if r.startswith("Skipped"))
    error_count = len(results) - processed_count - skipped_count
    
    print(f"\nSummary: {processed_count} processed, {skipped_count} skipped, {error_count} errors.")

if __name__ == "__main__":
    main()
