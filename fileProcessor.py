from io import TextIOWrapper


class FileProcessingError(Exception):
  pass

class ValidationError(FileProcessingError):
  pass

class EncodingError(FileProcessingError):
  pass

class IOError_Custom(FileProcessingError):
  pass


class FileProcessor:
  input_file_name:str
  output_file_name: str
  errors: list[dict[str,str|int]]
  _valid_lines:  list[str]
  _input_file:None |  TextIOWrapper
  _output_file: None | TextIOWrapper
  _lines: list[str]
  _input_encoding: str
  _output_encoding: str
  _lines_processed: int

  def __init__(self,_input_file_name:str,_output_file_name:str):
    self.input_file_name = _input_file_name
    self.output_file_name = _output_file_name
    self._input_file = None
    self._output_file = None
    self._lines = []
    self._input_encoding = "utf-8"
    self._output_encoding = "utf-8"
    self.errors = []
    self._lines_processed = 0
    self._valid_lines = []

  def __enter__(self):
    """Set up resources"""
    try:
      self._input_file = open(self.input_file_name,"r",encoding=self._input_encoding)
      self._output_file = open(self.output_file_name,"w",encoding=self._output_encoding)
      return self
    except FileNotFoundError:
      raise FileProcessingError(f"Input file not found: {self.input_file_name}")
    except PermissionError:
      if self._input_file is None:
        raise FileProcessingError(f"Permission denied for {self.input_file_name}")
      else:
        self._input_file.close()
        raise FileProcessingError(f"Permission denied for {self.output_file_name}")

  def process(self):
    try:
      if self._input_file:
        self._lines = self._input_file.read().splitlines()

      if self._lines:
        _ = self.validate(self._lines)

      if self._output_file:
        _ = self._output_file.write("\n".join(self._valid_lines))

      # raise RuntimeError("testing clenup")

      return {
        'success': True,
        'lines_processed': self._lines_processed,
        'errors': self.errors,
        'reason': ""
      }

    except UnicodeDecodeError:
      if self._input_encoding == "latin-1":
        self.errors.append({
            "file": self.input_file_name,
            "error": "Unable to decode file with supported encodings"
        })
        raise EncodingError("Unable to decode file with supported encodings")
      else:
        self._input_encoding = "latin-1"
        self._input_file.close() if self._input_file else None
        self._input_file = open(self.input_file_name,"r",encoding=self._input_encoding)
        _ = self.process()

    except UnicodeEncodeError:
      if self._output_encoding == "latin-1":
        self.errors.append({
            "file": self.output_file_name,
            "error": "Unable to encode file with supported encodings"
        })
        raise EncodingError("Unable to decode file with supported encodings")
      else:
        self._output_encoding = "latin-1"
        self._output_file.close() if self._output_file else None
        self._output_file = open(self.output_file_name,"w",encoding=self._output_encoding)
        _ = self.process()

  def validate(self,_lines:list[str]):
    """Validate each _lines"""
    for idx,line in enumerate(_lines):
      self._lines_processed += 1

      data = line.split(",",3)

      if len(data) < 3:
        self.errors.append({'line_num': idx + 1, 'error': 'Invalid format'})
        continue

      name, age, job = data

      # Here better to check with regex
      is_valid_name = name.replace('.','',1).isdigit()
      is_valid_age = age.replace('.','',1).isdigit()
      is_valid_job = job.replace('.','',1).isdigit()

      if is_valid_name:
        self.errors.append({"line_num": idx + 1, "error": "Invalid name"})
        continue

      if is_valid_age is False:
        self.errors.append({"line_num": idx + 1, "error": "Invalid age"})
        continue

      if is_valid_job:
        self.errors.append({"line_num": idx + 1, "error": "Invalid job"})
        continue

      self._valid_lines.append(f"{name},{age},{job}")

  def __exit__(self,exc_type, exc_val, exc_tb):
    """Clean up - runs even if exception"""
    self._output_file.close() if self._output_file else None
    self._input_file.close() if self._input_file  else None
    # print("Error")
    return False
