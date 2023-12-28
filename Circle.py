# Circle.py
from circle_entity_parser import CircleEntityParser
from get_user_input import UserInput
from LSPFileHandle import LSPFileHandler
import math

class Ent_Circle:
    def __init__(self, ent_num, ent_name, log_start_end_line = (0, 10000), ip = (0.0, 0.0), points=[]):
        """
        Constructor method to initialize the Polyline object with a list of points.
        """
        self.ent_num = ent_num
        self.ent_name = ent_name
        self.vertices2D = points
        self.len_varible_name = ["r0"]
        self.diameter = 0
        self.ip = ip # insertion point
        self.num_vertices = 1
        self.log_start_end_line = log_start_end_line
        self.Input_Variables = 0
        
    def add_point(self, x, y):
        """
        Method to add a point to the Polyline.
        """
        self.vertices2D.append((x, y))

    def read_entity_circle_from_path(self, file_path, Input_Variables):
        parser = CircleEntityParser(file_path, self.ent_num, self.log_start_end_line)
        self.vertices2D, self.diameter = parser.parse_circle()
        self.Input_Variables = Input_Variables
        # get every vertices and # of variables needed in pline
        #transform information from parser to pline object
    
    def set_insertion_point(self, offset): # offset = [x, y]
        self.ip = offset

    # ========================================================
    # =========== Under are for output .lsp file =============
    # ========================================================
    
    def lisp_get_variables(self):
        # get insertion point lisp code
        lines = []
        if (self.ip == (0.0, 0.0)):
            lines.append("(setq ip (getpoint \"Input the insertion point : \") )" )
        else:
            if(self.Input_Variables == 0):
                lines.append(f"(setq ip_x {self.ip[0]})" )
                lines.append(f"(setq ip_y {self.ip[1]})" )
            else:
                lines.append(f"(setq ip_x (getreal \"Input x offset from the insertion point <{self.ip[0]}>: \") )" )
                lines.append(f"(setq ip_y (getreal \"Input y offset from the insertion point <{self.ip[1]}>: \") )" )
            lines.append(f"(setq ip_o (rpoint ip ip_x ip_y))")
        
        for i in range(len(self.len_varible_name)):
            # lines.append(f"(setq {self.len_varible_name[i]} (getreal \"Input radius <{self.diameter}>: \") )" )

            lines.append(f"( setq {self.len_varible_name[i]} {self.diameter})")
        return lines
    
    def lisp_set_points(self):
        lines = []
        # p0 = insetion point
        if (self.ip == (0.0, 0.0)):
            lines.append("(setq p0 ip)")
        else:
            lines.append("(setq p0 ip_o)")
        # p0 ~ pi-1
        return lines

    def lisp_command_pline(self):
        points = ""
        
        for i in range(self.num_vertices):
            points+= f" p{i}"
            # consider arc
        
        line = [f"(command \"circle\" {points} r0)"]
        return line
    
# Example usage
if __name__ == "__main__":
    # Create a Polyline object
    polyline = Ent_Circle(0, "test circle")

    # Add points to the Polyline
    polyline.add_point(0, 0)
    polyline.add_point(1, 1)
    polyline.add_point(2, 0)

