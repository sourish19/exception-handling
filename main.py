from fileProcessor import FileProcessor


def process_file(input_path: str, output_path: str):
    """
    Returns {
        'success': bool,
        'lines_processed': int,
        'errors': [
            {'line_num': 5, 'error': 'Invalid format'},
            ...
        ],
        'reason': str if not success else None
    }

    Handle:
    - File not found
    - File encoding issues (try UTF-8, then latin-1, then skip)
    - Invalid line format (log, skip, continue)
    - Write permission denied
    - Disk full (simulate with max lines)
    - Keyboard interrupt (cleanup gracefully)
    """
    file = FileProcessor(input_path,output_path)
    file.process()
    

input_path = "./input.txt"
output_path = "./output.txt"

process_file(input_path,output_path)
