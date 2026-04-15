import os
import re
import urllib.request
import json

dirs = [
    "content/studynote/1_computer_architecture",
    "content/studynote/2_operating_system",
    "content/studynote/3_network",
    "content/studynote/4_software_engineering"
]

API_KEY = os.environ.get("ANTHROPIC_AUTH_TOKEN")
API_URL = "https://api.anthropic.com/v1/messages"

def contains_korean(text):
    return bool(re.search(r'[가-힣]', text))

def is_ascii_diagram(text):
    return bool(re.search(r'[-+|<>^v]{2,}', text))

def translate_diagram(text):
    prompt = f"""
    You are an expert technical translator. You have been given an ASCII diagram containing English labels.
    Your task is to translate the English labels to Korean and append the translation ALONGSIDE the English label (e.g., `[ Cache ]` becomes `[ Cache / 캐시 ]`).
    CRITICAL INSTRUCTION: You MUST preserve the ASCII structure exactly! This means you should NOT break the vertical alignment of lines, pipes (|), arrows (↓, ^, v, <, >), and boxes.
    If adding a translation extends the string, you MUST pad or adjust the surrounding spaces, lines, and dashes so that the overall visual structure remains completely intact and vertically aligned.
    If it is impossible to add the translation without completely destroying the structure, do your best to keep alignment by extending the box and aligning the corresponding elements below or above it.
    
    Return ONLY the modified ASCII diagram text exactly as it should appear, without any markdown formatting like ```text, and without any other explanations.
    
    Diagram:
    {text}
    """
    
    data = {
        "model": "claude-3-5-sonnet-20241022",
        "max_tokens": 4096,
        "temperature": 0.0,
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }
    
    req = urllib.request.Request(API_URL, data=json.dumps(data).encode('utf-8'), headers={
        "Content-Type": "application/json",
        "x-api-key": API_KEY,
        "anthropic-version": "2023-06-01"
    })
    
    try:
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode('utf-8'))
            return result['content'][0]['text'].strip('\n` ')
    except Exception as e:
        print(f"API Error: {e}")
        return None

count = 0
for d in dirs:
    if not os.path.exists(d): continue
    for root, _, files in os.walk(d):
        for f in files:
            if f.endswith('.md'):
                filepath = os.path.join(root, f)
                try:
                    with open(filepath, 'r', encoding='utf-8', errors='ignore') as file:
                        content = file.read()
                    
                    blocks = re.findall(r'(```text\n.*?```)', content, re.DOTALL)
                    modified_content = content
                    changed = False
                    for block in blocks:
                        inner_text = block[7:-3]
                        if is_ascii_diagram(inner_text) and not contains_korean(inner_text):
                            print(f"Translating diagram in {filepath}...")
                            translated = translate_diagram(inner_text)
                            if translated:
                                new_block = f"```text\n{translated}\n```"
                                modified_content = modified_content.replace(block, new_block)
                                changed = True
                                count += 1
                                
                    if changed:
                        with open(filepath, 'w', encoding='utf-8') as file:
                            file.write(modified_content)
                except Exception as e:
                    print(f"Error processing {filepath}: {e}")

print(f"Finished translating {count} diagrams.")
