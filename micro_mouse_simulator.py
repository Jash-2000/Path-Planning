import numpy as np  # For arrays

def encode(ori):
    '''
        Function to encode the orientations into direction.
    '''

    if ori == 0:
        return "Right"
    elif ori == 1:
        return "Up"
    elif ori == 2:
        return "Left"
    elif ori == 3:
        return "Down"
    else:
        return "error"
    
def decode(ori):
    '''
        Function to decode the direction for the bot.
    '''
    
    if ori_encoded == 'R':
        return 0
    elif ori == "U":
        return 1
    elif ori == "L":
        return 2
    elif ori == "D":
        return 3
    else:
        return ("error")

def addWalls(our_array):    
    '''
        Function to add walls to the maze.
        
        Technically coded a do-while loop for asking the user to add wall 
        and if yes, enter the co-ordnates.
    '''
    x_w = int(input("Enter the x - co-ordinates of the wall")) - 1
    y_w = int(input("Enter the y - co-ordinates of the wall")) - 1
    our_array[x_w][y_w] = n*n +1
    
    while (input("Do you want to add more walls ? ") == "Yes"):
        x_w = int(input("Enter the x - co-ordinates of the wall")) - 1
        y_w = int(input("Enter the y - co-ordinates of the wall")) - 1
        our_array[x_w][y_w] = n*n +1
    
    return our_array


def update_step(x,y,orientation):
    '''
        The function that updates the next step of the maze 
        according to the given set of rules. 
    '''
    return x,y,orientation



def bot(x,y,orientation):
    '''
       A kind of buffer function to save the current location and orientation of the bot.  
    '''
    print("Bot's current location is", x,y,"\n And the orientation is", encode(orientation))
    x_new,y_new,orientation_new = update_step(x,y,orientation)
    return x_new,y_new,orientation_new



def floodfill(our_array):
    '''
        The most important function of the script. 
        It undergoes the flood fill algorithm with a recursive loop.
    
    '''    
    return updated_array


# Main script strating now

n = int(input("Enter the odd size of the maze"))
our_array = np.random.randint(low = 1,high = n*n, size = (2*n-1,2*n-1))


print("\n\n\nThis is our current array(random)\n", our_array)

x_s = int(input("Enter the location of starting point(x)")) - 1
y_s = int(input("Enter the location of starting point(y)")) - 1
ori_encoded = input("Enter the orientation of the bot (R/L/U/D) ")

x_d = int(input("Enter the coordinates of the destination(x)")) - 1  
y_d = int(input("Enter the location of destination point(y)")) - 1

ori = decode(ori_encoded)
our_array[x_d][y_d] = 0
our_array[x_s][y_s] = (n*n) - 1

print("\n\n\n Before we start our game, this is the array available to you\n",our_array)

print("\n Do you want to add walls?")
print(" The walls will be displayed by the number", n*n + 1 )
if input() == 'Yes':
    our_array = addWalls(our_array)
else:
    pass
print("\n\n Final array after adding the walls\n",our_array)

print("\n\n\n\n==================================================================================")
print("\n\n\n So here we start our processing, the bot will traverse randomly and each iteration will be visible to you")