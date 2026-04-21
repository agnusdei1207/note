import os
import subprocess
import re

PE_GUIDELINE_PATH = "/mnt/c/workspace/brainscience/PE_GUIDELINE.md"
PE_EXAMPLE_PATH = "/mnt/c/workspace/brainscience/PE_EXAMPLE.md"

with open(PE_GUIDELINE_PATH, "r", encoding="utf-8") as f:
    pe_guideline = f.read()

with open(PE_EXAMPLE_PATH, "r", encoding="utf-8") as f:
    pe_example = f.read()

files_to_process = [
    "621_scale_up_system_bus.md",
    "622_scale_out_cluster.md",
    "623_datacenter_pue.md",
    "624_bmt_procedure.md",
    "625_sla_hardware_availability.md",
    "626_drs_storage_mirroring.md",
    "627_rpo.md",
    "628_rto.md",
    "629_bare_metal_cloud.md",
    "630_hci.md",
    "631_sddc.md",
    "632_sds.md",
    "633_sdn_whitebox.md",
    "635_on_device_ai.md",
    "636_federated_learning.md",
    "637_tinyml_hardware.md",
    "639_rack_scale_architecture.md",
    "640_open_compute_project.md",
    "641_data_lake_storage.md",
    "642_observability_telemetry.md"
]

base_dir = "/mnt/c/workspace/brainscience/content/studynote/01_computer_architecture/15_advanced_topics/"

def process_file(file_name):
    file_path = os.path.join(base_dir, file_name)
    with open(file_path, "r", encoding="utf-8") as f:
        original_content = f.read()
    
    # Extract title from original content
    title_match = re.search(r'title\s*=\s*"(.*?)"', original_content)
    title = title_match.group(1) if title_match else file_name
    
    prompt = f"""
You are an expert technical writer and computer architect.
Rewrite the following file: {file_name}
Topic: {title}

Follow the High-Quality PE Standard:
- 3-line core insights.
- Sections I to V with summary analogies for EACH section.
- Detailed ASCII diagrams (at least 2-3 per file, well-aligned).
- Proper front matter (date 2026-04-20).
- 15KB+ depth (extremely detailed technical content). This is CRITICAL.
- Abbreviations expanded (e.g., SMP (Symmetric Multi-Processing)).
- Language: Korean.

Guidelines:
{pe_guideline}

Example:
{pe_example}

Original Draft:
{original_content}

Instructions:
1. Be extremely verbose and detailed. Provide deep technical explanations, historical context, architectural trade-offs, and real-world implementation details (e.g., specific protocols like UPI, MOESI, MESIF, or specific vendor implementations like Intel, AMD, AWS, etc.).
2. Ensure the output is at least 3000-4000 words in Korean to reach the 15KB+ target.
3. Use multiple sub-sections (1.1, 1.2, 2.1, etc.) within each main section (I, II, III, IV, V).
4. Include detailed tables for comparisons.
5. Ensure ASCII diagrams are complex and informative.
6. The date in front matter must be "2026-04-20".
7. Keep the weight as it was in the original file.

Return ONLY the markdown content.
"""
    
    print(f"Generating content for {file_name}...")
    try:
        # Use npx claude -p with the prompt
        # We need to escape the prompt for shell
        result = subprocess.run(
            ["npx", "claude", "-p", prompt],
            capture_output=True,
            text=True,
            encoding="utf-8"
        )
        
        if result.returncode != 0:
            print(f"Error generating {file_name}: {result.stderr}")
            return
        
        generated_content = result.stdout.strip()
        
        # Sometimes Claude adds markdown code blocks around the response
        if generated_content.startswith("```md"):
            generated_content = generated_content[5:]
        if generated_content.startswith("```markdown"):
            generated_content = generated_content[11:]
        if generated_content.endswith("```"):
            generated_content = generated_content[:-3]
        
        generated_content = generated_content.strip()

        # Aligner for ASCII box (similar to the original script)
        # (Omitted for brevity in this generator, but we'll try to keep it clean)
        
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(generated_content)
        
        print(f"Successfully updated {file_name} (Size: {len(generated_content.encode('utf-8'))} bytes)")
        
    except Exception as e:
        print(f"Exception while processing {file_name}: {e}")

# Process in small batches to avoid overloading the system or timeout
# I'll do 4 files at a time to be safe.
import sys
start_idx = int(sys.argv[1]) if len(sys.argv) > 1 else 0
end_idx = int(sys.argv[2]) if len(sys.argv) > 2 else len(files_to_process)

for i in range(start_idx, end_idx):
    process_file(files_to_process[i])
