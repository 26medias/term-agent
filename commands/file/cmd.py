
def cmd(params={}):
    filename = params.get("filename", "")
    content = params.get("content", "")

    # Ensure filename and content are provided
    if not filename or not content:
        raise ValueError("Both filename and content must be provided")

    with open(filename, 'w') as f:
        f.write(content)
    
    return "File created: "+content+""