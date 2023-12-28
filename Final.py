from Pline import Ent_Polyline
from Circle import Ent_Circle
from Ellipse import Ent_Ellipse
from SPline import Ent_SPline
from LSPFileHandle import LSPFileHandler
from log_parser import LogParser
from Insertion_point_handler import IP_handler


def main():
    """
    The main function where the program execution begins.
    """
    print("Lisp program generator\n")
    Input_filepath = "./log/demo.log"
    Output_filepath = "./output/demo.lsp"
    function_name = "demo"
    Input_Variables = 0

    # load .log file
    log_reader = LogParser(Input_filepath)
    log_reader.parse_log_file()
    # create diff entities
    Ents_list = [] # store all entities 
    for ent_type, start_end, ent_name in zip(log_reader.entity_type, log_reader.entity_start_end, log_reader.entities_name):
        if(ent_type == "LWPOLYLINE"):
            Pline_ent = Ent_Polyline(len(Ents_list), ent_name, start_end)
            Pline_ent.read_entity_pline_from_path(Input_filepath, Input_Variables)

            Ents_list.append(Pline_ent)
        elif(ent_type == "CIRCLE"):
            Circle_ent = Ent_Circle(len(Ents_list), ent_name, start_end)
            Circle_ent.read_entity_circle_from_path(Input_filepath, Input_Variables)
            Ents_list.append(Circle_ent)
        elif(ent_type == "ELLIPSE"):
            Ellipse_ent = Ent_Ellipse(len(Ents_list), ent_name, start_end)
            Ellipse_ent.read_entity_ellipse_from_path(Input_filepath, Input_Variables)
            Ents_list.append(Ellipse_ent)
        elif(ent_type == "SPLINE"):
            Spline_ent = Ent_SPline(len(Ents_list), ent_name, start_end)
            Spline_ent.read_entity_from_path(Input_filepath, Input_Variables)
            Ents_list.append(Spline_ent)


    # for each entity, create a object 
    print(f"Ent len = {len(Ents_list)}")
    for entity in Ents_list:
        print(f" Ent name: {entity.ent_name}")
        print(f" Ent number: {entity.ent_num}")
        print(f" Ent points: {entity.vertices2D}")
    
    # calculate the offset 
    ip_hadler = IP_handler(0, Ents_list)
    ip_hadler.determine_offset()
    for entity, ip_offset in zip(Ents_list, ip_hadler.ip_list):
        entity.ip = ip_offset

    # initiate .lsp file
    lsp_writer = LSPFileHandler(Output_filepath)
    lsp_writer.initiate_file(function_name)


    # vertices --> command
    for entity in Ents_list:
        lsp_writer.write_lines(entity.lisp_get_variables() )
        lsp_writer.write_lines(entity.lisp_set_points())
        lsp_writer.write_lines(entity.lisp_command_pline())

    #end of .lsp file
    lsp_writer.end_file(function_name)
    lsp_writer.output_lines_to_lsp()

if __name__ == "__main__":
    # Call the main function if the script is run directly
    main()
