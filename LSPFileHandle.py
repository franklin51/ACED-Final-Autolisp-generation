class LSPFileHandler:
    def __init__(self, file_path):
        """
        Constructor method to initialize the LSPFileWriter object with a file path.
        """
        self.file_path = file_path
        self.lines = []

    def output_lines_to_lsp(self):
        """
        Method to write lines to the .lsp file.
        """
        try:
            with open(self.file_path, 'w') as file:
                for line in self.lines:
                    file.write(f"{line}\n")
            print(f"File '{self.file_path}' successfully created.")
        except Exception as e:
            print(f"Error writing to file: {e}")

    def initiate_file(self, function_name):
        self.lines.append(f"(defun c:{function_name}( / )")
        self.lines.append("(command \"erase\" \"all\" \"\")")
        self.lines.append("(graphscr) (command \"osnap\" \"none\")" )
        
    def end_file(self, function_name):
        self.lines.append(f"(princ)")
        self.lines.append(f");end-c:{function_name}()")
    
    def write_lines(self, lines):
        for line in lines:
            self.lines.append(line)

# Example usage
if __name__ == "__main__":
    # Create an instance of the LSPFileWriter class with a file path
    lsp_writer = LSPFileHandler(file_path="./output/output.lsp")

    # Example list of lines to write to the .lsp file
    lsp_writer.lines = [
        "(commandA 10.0 20.0)",
        "(commandB 30.0 40.0)",
        "(commandC 50.0 60.0)",
    ]

    # Use the write_lines method to write the lines to the .lsp file
    lsp_writer.output_lines_to_lsp()
