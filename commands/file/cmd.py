from langchain.tools import tool
import json5

@tool
def write_file(input_data):
    """
    Create a file with arbitrary content

    Parameters:
    - input_data: A dictionary containing the `filename` and `content`

    Returns:
    - Confirmation or error
    """
    input_data = json5.loads(input_data)  # Convert the input string to a dictionary
    print(">", input_data, type(input_data))
    
    if not input_data.get('filename') or not input_data.get('content'):
        raise ValueError("Both filename and content must be provided")

    filename = input_data['filename']
    content = input_data['content']

    with open(filename, 'w') as f:
        f.write(content)

    return "File created: " + filename  # Changed from content to filename
