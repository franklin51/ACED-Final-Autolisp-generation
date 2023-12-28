# entity_log_parser.py

class PlineEntityParser:
    def __init__(self, file_path, ent_num, startline = 0, endline = 10000):
        """
        Constructor method to initialize the LogFileParser object with a file path.
        """
        self.file_path = file_path
        self.ent_num = ent_num
        self.startline = startline
        self.endline = endline
        
    def parse_pline(self):
        """
        Method to read and parse the log file.
        """
        vertices2D = []
        len_varible, ang_varible = [], []
        num_vertices, isclosed, num_lines = 0, 0, 0
        is_arc = []

        try:
            with open(self.file_path, 'r') as file:
                for line in file:
                    if(num_lines < self.startline):
                        num_lines += 1
                        continue
                    elif(num_lines > self.endline):
                        len_varible, ang_varible = self.calculate_variable_name(vertices2D)
                        return vertices2D, is_arc, len_varible, ang_varible, num_vertices, isclosed

                    if line.startswith("(10 "):
                        elements = self.parse_pline_vertex(line)
                        print(f"Line: {line.strip()}\nParsed Elements: {elements}\n")
                        vertices2D = self.add_vertex(vertices2D, elements[0], elements[1])
                    elif line.startswith("(90 "):
                        # Get number of vertices
                        num_vertices = self.parse_num_vertices(line)
                    elif line.startswith("(70 "):
                        # get whether pline is closed 
                        isclosed = self.parse_closed(line)
                    elif line.startswith("(42 "):
                        # get whether each segment is arc
                        is_arc = self.parse_arc_segment(line, is_arc)
                    num_lines += 1
                    
            len_varible, ang_varible = self.calculate_variable_name(vertices2D)
            print(f"is_arc = {is_arc}\n")
            return vertices2D, is_arc, len_varible, ang_varible, num_vertices, isclosed
        except FileNotFoundError:
            print(f"File not found: {self.file_path}")

    def parse_pline_vertex(self, line):
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
    
    def parse_arc_segment(self, line, is_arc):
        
        elements = line[1:-3].split()
        if(abs(float(elements[2])) > 0.00001):
            is_arc.append(float(elements[2]))
        else:
            is_arc.append(float(elements[2]))
        print(f"Line: {line.strip()}\nParsed Elements: is_arc = {is_arc}\n")
        # print(f"{elements}\n")
        return is_arc
    
    def parse_num_vertices(self, line):
        new_line = line.replace(".", "")
        elements = new_line[1:-3].split()
        print(f"Line: {line.strip()}\nParsed Elements: number of vertices = {elements[1]}\n")
        return int(elements[1])
    
    def parse_closed(self, line):
        new_line = line.replace(".", "")
        elements = new_line[1:-3].split()
        print(f"Line: {line.strip()}\nParsed Elements: isclosed = {elements[1]}\n")
        return int(elements[1])
    
    def add_vertex(self,vertices_list, x, y):
        """
        Method to add a vertex to the Polyline.
        """
        vertices_list.append((x, y))
        return vertices_list

    def determine_parameters(self, vertex1, vertex2, len_varible_name, ang_varible_name):
        """
        Method to determine how many parameters are needed based on the x and y coordinates of two vertices.
        """
        x1, y1 = vertex1
        x2, y2 = vertex2

        if x1 == x2 or y1 == y2:
            # If x or y is the same, only one parameter is needed (horizontal or vertical line)
            # return 1
            variable_name = f"d{len(len_varible_name)}"
            len_varible_name.append(variable_name)
        else:
            # If x and y are different, two parameters are needed
            # return 2
            variable_name = f"d{len(len_varible_name)}"
            len_varible_name.append(variable_name)
            variable_name = f"a{len(ang_varible_name)}"
            ang_varible_name.append(variable_name)
        return len_varible_name, ang_varible_name
    
    def calculate_variable_name(self, vertices2D):
        """
        Method to calculate adjacent vertices in the Polyline.
        """
        len_varible_name, ang_varible_name = [], []
        
        # If there are less than 2 vertices, no adjacent pairs
        if len(vertices2D) < 2:
            return [], []

        # Iterate through the vertices
        for i in range(len(vertices2D) - 1):
            vertex1 = vertices2D[i]
            vertex2 = vertices2D[i + 1]
            len_varible_name, ang_varible_name = self.determine_parameters(vertex1, vertex2, len_varible_name, ang_varible_name)
        return len_varible_name, ang_varible_name
    
# Example usage
if __name__ == "__main__":
    # Create a LogFileParser object with the file path
    parser = PlineEntityParser(file_path="Pline_arc.log")

    # Parse the log file
    parser.parse_pline()
    
    # print(f"len variables: {parser.len_varible}")
    # print(f"angle variables: {parser.ang_varible}")

