# Circle.py
from ellipse_entity_parser import EllipseEntityParser
from get_user_input import UserInput
from LSPFileHandle import LSPFileHandler
import math


class Ent_Ellipse:
    def __init__(self, ent_num, ent_name, log_start_end_line = (0, 10000), ip = (0.0, 0.0), points=[]):
        """
        Constructor method to initialize the Polyline object with a list of points.
        """
        self.ent_num = ent_num
        self.ent_name = ent_name
        self.vertices2D = points
        self.len_varible_name = []
        self.ratio_axis_len = 0
        self.ip = ip # insertion point
        self.num_vertices = 1
        self.log_start_end_line = log_start_end_line
        self.axis_len = [0, 0] # major, minor len
        self.Input_Variables = 0

    def read_entity_ellipse_from_path(self, file_path, Input_Variables):
        parser = EllipseEntityParser(file_path, self.ent_num, self.log_start_end_line)
        self.vertices2D, self.len_varible_name, self.ratio_axis_len = parser.parse_ellipse()
        self.get_axis_len()
        self.Input_Variables = Input_Variables
        # get every vertices and # of variables needed in pline
        #transform information from parser to pline object
    def get_axis_len(self):
        # x1, y1 = self.vertices2D[0]
        x, y = self.vertices2D[1]

        self.axis_len[0] = math.sqrt(x**2 + y**2)
        self.axis_len[1] = self.axis_len[0] * self.ratio_axis_len
        print(f"axis length = {self.axis_len}")
    def set_insertion_point(self, offset): # offset = [x, y]
        self.ip = offset
    def determine_angle(self):
        """
        Method to determine how many parameters are needed based on the x and y coordinates of two vertices.
        """
        vertex  =  self.vertices2D[1]
        
        x2, y2 = vertex
        # Calculate the angle using arctangent
        angle_rad = math.atan2(y2 , x2)
        return angle_rad
    # ========================================================
    # =========== Under are for output .lsp file =============
    # ========================================================
    
    def lisp_get_variables(self):
        # get insertion point lisp code
        lines = []
        lines.append("(print \"Drawing a Ellipse!\\n\" )" )

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
            lines.append(f"( setq {self.len_varible_name[i]} {self.axis_len[i]})")
        return lines
    
    def lisp_set_points(self):
        lines = []
        # p0 = insetion point
        if (self.ip == (0.0, 0.0)):
            lines.append("(setq p0 ip)")
        else:
            lines.append("(setq p0 ip_o)")
        # p1 the end point of the major axis
        angle_btw_in_rad = self.determine_angle()
        lines.append( f"( setq p1 (polar p0 {angle_btw_in_rad} a) )" )
        
        return lines

    def lisp_command_pline(self):
        points = ""
        
        for i in range(self.num_vertices):
            points+= f" p{i}"
            # consider arc
        
        line = [f"(command \"ellipse\" \"c\" p0 p1 b)"]
        return line
    
# Example usage
if __name__ == "__main__":
    # Create a Polyline object
    polyline = Ent_Ellipse(0, "test circle")

    # Add points to the Polyline
    

