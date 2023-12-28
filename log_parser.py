# log_parser.py
# Controller of the log file 
# not reading entity detail
class LogParser:
    def __init__(self, file_path):
        """
        Constructor method to initialize the LogParser object with a file path.
        """
        self.file_path = file_path
        self.entities_count = 0
        self.entity_start_end = [] #include start not include end
        self.entity_type = []
        self.entities_name = []
        self.main_ip = 0

    def parse_log_file(self):
        """
        Method to parse the log file and determine entities with start and end lines.
        """
        start, end, lines_count = 0, 0, 0
        try:
            with open(self.file_path, 'r') as file:
                for line in file:
                    if line.startswith("(-1 "):
                        # entity name
                        if(self.entities_count > 0): # not the first entity
                            end = lines_count
                            self.entity_start_end.append((start, end))
                        self.entities_count +=1
                        start = lines_count
                        self.entities_name.append(self.get_entity_name(line))
                    elif line.startswith("(0 "):
                        self.entity_type.append(self.determine_entity_type(line))
                    lines_count+=1
            # last entity
            self.entity_start_end.append((start, lines_count))
        except FileNotFoundError:
            print(f"File not found: {self.file_path}")

    def determine_entity_type(self, line):
        print("Classify Entities")
        new_line = line.replace(".", "")
        new_line = new_line.replace("\"", "")
        print(new_line)
        elements = new_line[1:-3].split()
        return elements[1]
    
    def get_entity_name(self, line):
        print("get Entities name")
        new_line = line.replace(".", "")
        new_line = new_line.replace(">", "")
        print(new_line)
        elements = new_line[1:-3].split()
        return elements[3]
             
        
# Example usage
if __name__ == "__main__":
    # Create a LogParser object with the file path
    log_parser = LogParser(file_path="multi_line.log")

    # Parse the log file
    log_parser.parse_log_file()
    print(f"count = {log_parser.entities_count}")
    print(log_parser.entities_name)
    print(log_parser.entity_start_end)
    print(f"Type = {log_parser.entity_type}")

    
