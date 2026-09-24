class FileProcessingError(Exception):
    pass

class ValidationError(FileProcessingError):
    pass

class EncodingError(FileProcessingError):
    pass

class IOError_Custom(FileProcessingError):
    pass


class FileProcessor:
  def __init__(self,input_file:str,output_file:str,mode:str) -> None:
    self.input_file = input_file
    self.output_file = output_file
    self.mode = mode

  def __enter__(self) -> None:


  def __exit__(self) -> None:
    pass
