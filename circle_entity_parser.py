# circle_entity_parser.py

class CircleEntityParser:
    def __init__(self, file_path, ent_num, start_end_line = (0,10000)):
        """
        Constructor method to initialize the LogFileParser object with a file path.
        """
        self.file_path = file_path
        self.ent_num = ent_num
        self.startline = start_end_line[0]
        self.endline = start_end_line[1]
        
    def parse_circle(self):
        """
        Method to read and parse the log file.
        """
        vertices2D = []
        len_variable = ["r0"]
        num_lines = 0
        diameter = 0

        try:
            with open(self.file_path, 'r') as file:
                for line in file:
                    if(num_lines < self.startline):
                        num_lines += 1
                        continue
                    elif(num_lines > self.endline):
                        return vertices2D, diameter

                    if line.startswith("(10 "):
                        elements = self.parse_vertex(line)
                        print(f"Line: {line.strip()}\nParsed Elements: {elements}\n")
                        vertices2D = self.add_vertex(vertices2D, elements[0], elements[1])
                    elif line.startswith("(40 "):
                        # get whether each segment is arc
                        diameter = self.parse_diameter(line)
                    num_lines += 1
                    
            return vertices2D, diameter
        except FileNotFoundError:
            print(f"File not found: {self.file_path}")

    def parse_vertex(self, line):
        """
        Method to extract elements from a line.
        """
        try:
            # Remove leading '(' and trailing ')', then split by space
            elements = line[1:-3].split()             
            # Convert the elements to appropriate types (e.g., float)
            elements = [ (float)(element) for element in elements[1:]]
            # add vertex
            return elements # return [x, y]
        except ValueError:
            print(f"Error parsing line: {line}")
            return None
    
    def parse_diameter(self, line):
        # new_line = line.replace(".", "")
        elements = line[1:-3].split()
        
        print(f"Line: {line.strip()}\nParsed Elements: Diameter = {float(elements[2])}\n")
        # print(f"{elements}\n")
        return float(elements[2])
    
    def add_vertex(self,vertices_list, x, y):
        """
        Method to add a vertex to the Polyline.
        """
        vertices_list.append((x, y))
        return vertices_list
    
# Example usage
if __name__ == "__main__":
    # Create a LogFileParser object with the file path
    parser = CircleEntityParser(file_path="Circle.log", ent_num = 0)

    # Parse the log file
    vertices, dia = parser.parse_circle()
    print(vertices)
    print(dia)
    # print(f"len variables: {parser.len_varible}")
    # print(f"angle variables: {parser.ang_varible}")

