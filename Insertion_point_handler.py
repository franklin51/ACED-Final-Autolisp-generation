# polyline.py


class IP_handler:
    def __init__(self, main_ip_num = 0, Ent_list= []):
        """
        Constructor method to initialize the Polyline object with a list of points.
        """
        self.ent_list = Ent_list
        self.ip_list = []
        self.main_ip_num = main_ip_num
        self.main_ip = (0, 0)
        
    def get_main_ip(self):
        """
        Method to add a point to the Polyline.
        """
        self.main_ip = self.ent_list[self.main_ip_num].vertices2D[0]
    
    def determine_offset(self):
        """
        Method to determine how many parameters are needed based on the x and y coordinates of two vertices.
        """
        self.get_main_ip()
        for entity in self.ent_list:
            offset = self.tuple_sub(entity.vertices2D[0], self.ent_list[self.main_ip_num].vertices2D[0])
            self.ip_list.append(offset)

    def tuple_sub(self, tuple1, tuple2):
        result_tuple = tuple1[0] - tuple2[0], tuple1[1] - tuple2[1]
        return result_tuple

    # ========================================================
    # =========== Under are for output .lsp file =============
    # ========================================================
    
    
    
# Example usage
if __name__ == "__main__":
    # Create a Polyline object
    polyline = IP_handler(0)

    # Add points to the Polyline
    polyline.add_point(0, 0)
    polyline.add_point(1, 1)
    polyline.add_point(2, 0)

