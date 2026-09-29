from fileProcessor import FileProcessingError, FileProcessor


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
    # with open("latin1.txt", "w", encoding="latin-1") as f:
    #     f.write("André,25,Developer\n")

    try:
      with FileProcessor(input_path,output_path) as processor:
        data = processor.process()

        return data

    except FileProcessingError as e:
      return {
        'success': False,
        'lines_processed': 0,
        'errors': None,
        'reason': e
      }
    except RuntimeError as e:
      print("Exception caught")
      return {
        'success': False,
        'lines_processed': 0,
        'errors': None,
        'reason': e
      }


input_path = "./input.txt"
output_path = "./output.txt"

print(process_file(input_path,output_path))
