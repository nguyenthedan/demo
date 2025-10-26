import sys
import os
import json
import uuid

def log_to_file(log_path, message):
    """Appends a message to the specified log file."""
    try:
        with open(log_path, 'a', encoding='utf-8') as f:
            f.write(message + '\n')
    except Exception as e:
        print(f"Critical Error: Failed to write to log file {log_path}: {e}", file=sys.stderr)

def write_txt_output(output_file, found_matches, keyword_list):
    """Writes the search results in the original text format."""
    if not found_matches:
        result_summary = "No matches found."
        content = result_summary + '\n'
    else:
        result_summary = f"Found {len(found_matches)} match(es)."
        content = f"{result_summary} for keywords: {', '.join(keyword_list)}\n"
        content += "="*50 + "\n"
        for match in found_matches:
            content += f"File: {match['file']}\n"
            content += f"Line {match['line_num']}: {match['line_content']}\n"
            content += "-" * 20 + "\n"
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(content)
    return result_summary

def write_table_output(output_file, found_matches):
    """Writes the search results in the JSON table format."""
    if not found_matches:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump({"column": [], "rowData": []}, f, indent=2)
        return "No matches found."

    # Aggregate keywords by file
    found_files = {}
    for match in found_matches:
        file_path = match['file']
        keyword = match['keyword']
        if file_path not in found_files:
            found_files[file_path] = set()
        found_files[file_path].add(keyword)

    # Define table structure
    columns = [
        {"id": "id", "name": "ID"},
        {"id": "file_path", "name": "File Path"},
        {"id": "file_name", "name": "File Name"},
        {"id": "keywords", "name": "Keywords"}
    ]

    # Create row data
    row_data = []
    for file_path, keywords in found_files.items():
        row_data.append({
            "id": str(uuid.uuid4()),
            "file_path": file_path,
            "file_name": os.path.basename(file_path),
            "keywords": ", ".join(sorted(list(keywords)))
        })

    table_json = {
        "column": columns,
        "rowData": row_data
    }

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(table_json, f, indent=2)
        
    return f"Found matches in {len(row_data)} file(s)."


def search_keywords_in_folder(folder_path, keywords, output_file, log_path, output_type):
    """
    Searches for keywords, then calls the appropriate writer function based on output_type.
    """
    log_to_file(log_path, f"Starting search in folder: {folder_path}")
    log_to_file(log_path, f"Output format: {output_type}")

    keyword_list = [k.strip() for k in keywords.splitlines() if k.strip()]
    
    if not keyword_list:
        log_to_file(log_path, "Error: No valid keywords provided. Process stopped.")
        return

    log_to_file(log_path, f"Searching for keywords: {', '.join(keyword_list)}")
    
    found_matches = []
    
    for root, _, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    for line_num, line in enumerate(f, 1):
                        for keyword in keyword_list:
                            if keyword in line:
                                match = {
                                    "file": file_path,
                                    "line_num": line_num,
                                    "line_content": line.strip(),
                                    "keyword": keyword
                                }
                                found_matches.append(match)
                                # Don't break, a line might have multiple keywords
            except Exception as e:
                log_to_file(log_path, f"Warning: Could not read file {file_path}: {e}")

    try:
        result_summary = ""
        if output_type == 'table':
            result_summary = write_table_output(output_file, found_matches)
        else: # Default to txt
            result_summary = write_txt_output(output_file, found_matches, keyword_list)
        
        log_to_file(log_path, f"Process finished. {result_summary}")
        log_to_file(log_path, f"Search results have been successfully saved to {output_file}")

    except Exception as e:
        error_message = f"Error writing to results file {output_file}: {e}"
        log_to_file(log_path, error_message)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Error: Script expected a single JSON string argument.", file=sys.stderr)
        sys.exit(1)

    log_file_path = None
    try:
        inputs = json.loads(sys.argv[1])

        folder_to_search = inputs['folder_path']
        search_keywords = inputs['keywords']
        output_file_path = inputs['output_file']
        log_file_path = inputs['fileOutPath']
        output_format = inputs.get('output_type', 'txt') # Safely get output_type

        with open(log_file_path, 'w', encoding='utf-8') as f:
            f.write("Log for Search Keywords In Folder\n" + "="*30 + "\n")

        search_keywords_in_folder(folder_to_search, search_keywords, output_file_path, log_file_path, output_format)

    except Exception as e:
        error_message = f"A critical error occurred: {e}"
        if log_file_path:
            log_to_file(log_file_path, error_message)
        else:
            print(error_message, file=sys.stderr)
        sys.exit(1)
