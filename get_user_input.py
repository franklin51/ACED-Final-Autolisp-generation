class UserInput:
    @staticmethod
    def get_float_variables(variable):
        """
        Static method to request user input for a number.
        """
        user_input = []
        for i in range(len(variable)):
            while True:
                try:
                    user_input.append(float(input(f"Enter {variable[i]}:")))
                    break
                except ValueError:
                    print("Invalid input. Please enter a valid number.")
        return user_input
    
    def get_insertion_point():
        user_input = []
        while True:
                try:
                    user_input.append(float(input(f"\nEnter the x position of insertion point:")))
                    break
                except ValueError:
                    print("Invalid input. Please enter a valid number.")
        while True:
                try:
                    user_input.append(float(input(f"\nEnter the y position of insertion point:")))
                    break
                except ValueError:
                    print("Invalid input. Please enter a valid number.")
        # [0] is x position and [1] is y position
        return user_input

# Example usage
if __name__ == "__main__":
    # Create an instance of the UserInput class
    user_input_handler = UserInput()
    variables = ['d1', 'd2', 'd3']
    # Use the get_number method to get user input
    number = user_input_handler.get_float_variables(variables)

    print(f"You entered: {number}")
