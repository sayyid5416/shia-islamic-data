import json
from pathlib import Path
from collections import OrderedDict
from helper_ziyarah import printDone, printError, printStart


INPUT_FILE = "infallibles/template.json"
OUTPUT_FILE = "infallibles/basic_information.json"



def sync_with_template(entry: dict, template: dict) -> OrderedDict:
    synced = OrderedDict()
    for key, value in template.items():
        if key in entry:
            if isinstance(value, dict) and isinstance(entry[key], dict):
                synced[key] = sync_with_template(entry[key], value)
            else:
                synced[key] = entry[key]
        else:
            synced[key] = value
    return synced



def generate_basic_json():
    printStart(f"Generating '{OUTPUT_FILE}'")
    template_file = Path(INPUT_FILE)
    output_file = Path(OUTPUT_FILE)

    try:
        template: OrderedDict = json.loads(template_file.read_text(encoding="utf-8"), object_pairs_hook=OrderedDict)

        if output_file.exists():
            try:
                content = output_file.read_text(encoding="utf-8").strip()
                existing_data: list = json.loads(content, object_pairs_hook=OrderedDict) if content else []
            except json.JSONDecodeError:
                existing_data = []
        else:
            existing_data = []

        # Sync structure
        updated_data = [sync_with_template(entry, template) for entry in existing_data]

        # Add missing entries
        while len(updated_data) < 14:
            updated_data.append(template.copy())

        output_file.write_text(json.dumps(updated_data, indent=4, ensure_ascii=False), encoding="utf-8")
        printDone(f"Synced and ensured 14 entries. DONE!")
    except Exception as e:
        printError(str(e))



if __name__ == "__main__":
    print("\n------------------ STARTING ------------------\n")
    
    generate_basic_json()
    
    print("\n------------------ DONE ------------------\n")
