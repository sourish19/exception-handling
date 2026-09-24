import tempfile
from io import TextIOWrapper, _WrappedBuffer
from tempfile import _TemporaryFileWrapper


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
  input_file:None |  TextIOWrapper[_WrappedBuffer]
  output_file: None | TextIOWrapper[_WrappedBuffer]
  temporaryFile: None | _TemporaryFileWrapper[str]
  errors: list[str]

  def __init__(self,input_file:str,output_file:str):
    self.input_file_name = input_file
    self.output_file_name = output_file
    self.input_file = None
    self.output_file = None
    self.temporaryFile = None
    self.errors = []

  def __enter__(self):
    """Set up resources"""
    try:
      self.input_file = open(self.input_file_name,"r",encoding="UTF-8")
      self.output_file = open(self.output_file_name,"w",encoding="UTF-8")
      self.temporaryFile = tempfile.NamedTemporaryFile(mode="w",delete=True)
      return self
    except FileNotFoundError:
      raise FileProcessingError(f"Input file not found: {self.input_file_name}")

  def process(self):
    print("process")

  def __exit__(self):
    """Clean up - runs even if exception"""
    self.output_file.close() if self.output_file is not None
    self.input_file.close() if self.input_file is not None
    self.temporaryFile.close() if self.temporaryFile is not None
