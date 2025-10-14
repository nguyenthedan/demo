{
  "name": "Search Keywords In Folder",
  "description": "Search for multiple keywords in all files within a given folder and its subdirectories. The result will be saved to an output file.",
  "schema": {
    "type": "object",
    "title": "Search Keywords In Folder",
    "required": [
      "folder_path",
      "keywords",
      "output_file"
    ],
    "properties": {
      "folder_path": {
        "type": "string",
        "title": "Folder Path to Search"
      },
      "keywords": {
        "type": "string",
        "title": "Keywords (one per line)"
      },
      "output_type": {
        "type": "string",
        "title": "Output Format",
        "enum": [
          "txt",
          "table"
        ],
        "default": "txt"
      },
      "output_file": {
        "type": "string",
        "title": "Output File Path",
        "default": "search_results.txt"
      }
    }
  },
  "uiSchema": {
    "keywords": {
      "ui:widget": "textarea",
      "ui:options": {
        "rows": 5
      }
    }
  },
  "bookmark": [
    "{\n  \"output_file\": \"C:\\\\Users\\\\nguye\\\\Downloads\\\\search_results.txt\",\n  \"folder_path\": \"C:\\\\Users\\\\nguye\\\\Downloads\\\\demo\",\n  \"keywords\": \"improve\\npodcast\\nbeach\"\n}",
    "{\n  \"output_type\": \"table\",\n  \"output_file\": \"C:\\\\Users\\\\nguye\\\\Downloads\\\\search_results.table\",\n  \"folder_path\": \"C:\\\\Users\\\\nguye\\\\Downloads\\\\demo\",\n  \"keywords\": \"improve\\npodcast\\nbeach\"\n}"
  ]
}