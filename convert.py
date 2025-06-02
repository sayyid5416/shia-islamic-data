"""Reads lines from raw.txt and writes them with total_lines to result.json."""
import json


def printStart(msg: str):
    print(f"> {msg}")
    
def printDone(msg: str):
    print(f"⩥ {msg}\n")
    
def printError(msg: str):
    print(f"[x] {msg}\n")



def convert_text_to_json(input_file: str = "raw.txt", output_file: str = "result.json") -> None:
    try:
        printStart(f"Reading from {input_file}...")
        with open(input_file, "r", encoding="utf-8") as f:
            lines = [line.strip() for line in f if line.strip()]
        printDone(f"Total non-empty lines read: {len(lines)}")

        result = {
            "total_lines": len(lines),
            "text": lines
        }

        printStart(f"Writing result to {output_file}...")
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=4)
        printDone("Done.")
        
    except FileNotFoundError:
        printError(f"Error: File '{input_file}' not found.")
        
    except IOError as e:
        printError(f"I/O error({e.errno}): {e.strerror}")
        
    except Exception as e:
        printError(f"Unexpected error: {e}")


if __name__ == "__main__":
    convert_text_to_json()
