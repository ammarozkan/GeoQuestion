import math

easyatan = lambda theta : math.pi-math.atan(theta*-1) if theta < 0 else math.atan(theta)
    
def order_dots_by_OutAngleRule(dots,*connected_array):
    ordered = False
    while not ordered:
        for c in range(1,len(dots)):
            if dots[c].coord.y > dots[c-1].coord.y or (dots[c].coord.y == dots[c-1].coord.y and dots[c].coord.x > dots[c-1].coord.x):
                ordered = False
                ddrd = dots[c]
                dots[c] = dots[c-1]
                dots[c-1] = ddrd
                

                for i in range(0,len(connected_array)):
                    ddrd = connected_array[i][c]
                    connected_array[i][c] = connected_array[i][c-1]
                    connected_array[i][c-1] = ddrd
            else: ordered = True
    if connected_array != None: 
        result = (dots,)
        for connected in connected_array:
            result = result+(connected,)
        print("TPLE",result)
        return result
    else: return dots

def select_from_(array, condition, *connected_array): # if condition returns true, I will add the element!
    new_array = []
    result_connected_arrays = ()
    if connected_array != None: 
        for connected in connected_array: result_connected_arrays = result_connected_arrays + ([],)
    else : connected_array = []
    
    for counter in range(0,len(array)):
        if condition(array[counter]): new_array.append(array[counter])
        for connected_counter in range(0,len(connected_array)): result_connected_arrays[connected_counter].append(connected_array[connected_counter][counter])
    
    if connected_array == []: return new_array
    else : return (new_array,)+result_connected_arrays