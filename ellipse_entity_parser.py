# circle_entity_parser.py

class EllipseEntityParser:
    def __init__(self, file_path, ent_num, start_end_line = (0,10000)):
        """
        Constructor method to initialize the LogFileParser object with a file path.
        """
        self.file_path = file_path
        self.ent_num = ent_num
        self.startline = start_end_line[0]
        self.endline = start_end_line[1]
        
    def parse_ellipse(self):
        """
        Method to read and parse the log file.
        """
        vertices2D = [] #len = 2. 0 --> center point  1 --> end point at major axis
        len_variable_name = ["a", "b"] # len = 2. 0 --> len of major, 1 --> len minor
        num_lines = 0
        ratio_axis_len = 0
        
        try:
            with open(self.file_path, 'r') as file:
                for line in file:
                    if(num_lines < self.startline):
                        num_lines += 1
                        continue
                    elif(num_lines > self.endline):
                        return vertices2D, len_variable_name, ratio_axis_len

                    if line.startswith("(10 "):
                        elements = self.parse_vertex(line)
                        print(f"Line: {line.strip()}\nParsed Elements: {elements}\n")
                        vertices2D = self.add_vertex(vertices2D, elements[0], elements[1])
                    elif line.startswith("(11 "):
                        # get end point of major axis
                        elements = self.parse_major_axis_endpoint(line)
                        print(f"Line: {line.strip()}\nParsed Elements: {elements}\n")
                        vertices2D = self.add_vertex(vertices2D, elements[0], elements[1])
                    elif line.startswith("(40 "):
                        # get the ratio of the axis length 
                        elements = self.parse_minor_axis(line)
                        print(f"Line: {line.strip()}\nParsed Elements: {elements}\n")
                        ratio_axis_len = elements
                    num_lines += 1
                    
            return vertices2D, len_variable_name, ratio_axis_len
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
            elements = [ (float)(element) for element in elements[1:-1]]
            # add vertex
            return elements # return [x, y]
        except ValueError:
            print(f"Error parsing line: {line}")
            return None
    
    def parse_major_axis_endpoint(self, line):
        # new_line = line.replace(".", "")  #(11 9.5518 5.59354 0.0) 
        elements = line[1:-3].split()             
        # Convert the elements to appropriate types (e.g., float)
        elements = [ (float)(element) for element in elements[1:-1]]
        # add vertex
        return elements # return [x, y]

    def parse_minor_axis(self, line):
        # new_line = line.replace(".", "")
        elements = line[1:-3].split()
        
        # print(f"{elements}\n")
        return float(elements[2]) # return a float <= 1.0
    
    def add_vertex(self,vertices_list, x, y):
        """
        Method to add a vertex to the Polyline.
        """
        vertices_list.append((x, y))
        return vertices_list
    
# Example usage
if __name__ == "__main__":
    # Create a LogFileParser object with the file path
    parser = EllipseEntityParser(file_path="./log/ellipse.log", ent_num = 0)

    # Parse the log file
    vertices, var_name, ratio_axis_len = parser.parse_ellipse()
    print(vertices)
    print(var_name)
    print(ratio_axis_len)
    # print(f"len variables: {parser.len_varible}")
    # print(f"angle variables: {parser.ang_varible}")

