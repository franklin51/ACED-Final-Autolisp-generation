# polyline.py
from pline_entity_parser import PlineEntityParser
from get_user_input import UserInput
from LSPFileHandle import LSPFileHandler
import math

class Ent_Polyline:
    def __init__(self, ent_num, ent_name, log_start_end_line = (0, 10000), ip = (0, 0), points=[]):
        """
        Constructor method to initialize the Polyline object with a list of points.
        """
        self.ent_num = ent_num
        self.ent_name = ent_name
        self.vertices2D = points
        self.len_varible_name, self.ang_varible_name = [], []
        self.len_varible, self.ang_varible = [], []
        self.is_arc = []
        self.ip = ip # insertion point
        self.num_vertices, self.closed = 0, 0
        self.log_start_line = log_start_end_line[0]
        self.log_end_line = log_start_end_line[1]
        self.Input_Variables = 0
        
    def add_point(self, x, y):
        """
        Method to add a point to the Polyline.
        """
        self.vertices2D.append((x, y))
    
    def determine_angle(self, vertex_num_1, vertex_num_2):
        """
        Method to determine how many parameters are needed based on the x and y coordinates of two vertices.
        """
        vertex1, vertex2 = self.vertices2D[vertex_num_1], self.vertices2D[vertex_num_2]
        x1, y1 = vertex1
        x2, y2 = vertex2
        # Calculate the angle using arctangent
        angle_rad = math.atan2(y2 - y1, x2 - x1)
        return angle_rad
    def get_vertices_distance(self, vertex_num_1, vertex_num_2):
        vertex1, vertex2 = self.vertices2D[vertex_num_1], self.vertices2D[vertex_num_2]
        x1, y1 = vertex1
        x2, y2 = vertex2

        distance = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
        return round(distance, 3)

    def read_entity_pline_from_path(self, file_path, Input_Variables):
        parser = PlineEntityParser(file_path, self.ent_num, self.log_start_line, self.log_end_line)
        self.vertices2D, self.is_arc, self.len_varible_name, self.ang_varible_name, self.num_vertices, self.closed = parser.parse_pline()
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
                lines.append(f"(setq ip_x {self.ip[0]} )" )
                lines.append(f"(setq ip_y {self.ip[1]} )" )
            else:
                lines.append(f"(setq ip_x (getreal \"Input x offset from the insertion point <{self.ip[0]}>: \") )" )
                lines.append(f"(setq ip_y (getreal \"Input y offset from the insertion point <{self.ip[1]}>: \") )" )
            lines.append(f"(setq ip_o (rpoint ip ip_x ip_y))")
        if(self.Input_Variables == 0):
            for i in range(len(self.len_varible_name)):
                lines.append(f"( setq {self.len_varible_name[i]} {self.get_vertices_distance(i, i+1)})")
            for i in range(len(self.ang_varible_name)):
                lines.append(f"( setq {self.ang_varible_name[i]} {self.determine_angle(i, i+1)})")
        else:
            for i in range(len(self.len_varible_name)):
                lines.append(f"( setq {self.len_varible_name[i]} (getreal \"Input Ent{self.ent_num} {self.len_varible_name[i]} <{self.get_vertices_distance(i, i+1)}>: \") )")
            for i in range(len(self.ang_varible_name)):
                lines.append(f"( setq {self.ang_varible_name[i]} (getreal \"Input Ent{self.ent_num} {self.ang_varible_name[i]} <{self.determine_angle(i, i+1)}>: \") )")
                # lines.append(f"( setq {self.ang_varible_name[i]} {self.determine_angle(i, i+1)})")
        return lines
    
    def lisp_set_points(self):
        lines = []
        # p0 = insetion point
        if (self.ip == (0.0, 0.0)):
            lines.append("(setq p0 ip)")
        else:
            lines.append("(setq p0 ip_o)")
        # p0 ~ pi-1
        for i in range(len(self.vertices2D)-1):
            angle_btw_in_rad = self.determine_angle(i, i+1)
            # lines.append( f"( setq p{i+1} (polar p{i} {self.ang_varible_name[i]} {self.len_varible_name[i]}) )" )
            lines.append( f"( setq p{i+1} (polar p{i} {angle_btw_in_rad} {self.len_varible_name[i]}) )" )
            if(self.is_arc[i] != 0.0):
                lines.append(f"(setq th{i} (* (atan {self.is_arc[i]} 1.0) 4))")
                lines.append(f"(setq An{i} (rtd th{i}))")
                lines.append(f"(setq AB (distance p{i} p{i+1}))")
                lines.append(f"(setq R{i} (/ (/ AB 2.0) (sin (/ (abs th{i}) 2.0))))")
        return lines

    def lisp_command_pline(self):
        points = ""
        
        for i in range(self.num_vertices):
            points+= f" p{i}"
            # consider arc
            if(i==0):
                if(self.is_arc[i] != 0.0 ):
                    points += (f" \"arc\" \"R\" R{i} \"Angle\" An{i}")
                    # points += (f" \"arc\" \"CE\" O{i}")
            elif(i != self.num_vertices-1):
                if(self.is_arc[i] != 0.0):
                    points += (f" \"arc\" \"R\" R{i} \"Angle\" An{i}")
                    # points += (f" \"arc\" \"CE\" O{i}")
                elif(self.is_arc[i-1] != 0.0 and self.is_arc[i] == 0.0):
                    points += f" \"L\""
            elif(i == self.num_vertices-1 and self.closed):
                if(self.is_arc[i] != 0.0):
                    points += (f" \"arc\"")
                    # points += (f" \"arc\" \"CE\" O{i}")
                elif(self.is_arc[i-1] != 0.0 and self.is_arc[i] == 0.0):
                    points += f" \"L\""
            
                
        if(self.closed):
            points += " \"CL\""
        else:
            points+= " \"\""
        line = [f"(command \"pline\"{points})"]
        return line
    
# Example usage
if __name__ == "__main__":
    # Create a Polyline object
    polyline = Ent_Polyline(0)

    # Add points to the Polyline
    polyline.add_point(0, 0)
    polyline.add_point(1, 1)
    polyline.add_point(2, 0)

