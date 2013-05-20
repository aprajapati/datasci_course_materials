import MapReduce
import json
import sys

mr = MapReduce.MapReduce()
rows=5
cols=5
# Map function
# mr - MapReduce object
# data - json object formatted as a string
def mapper(data):
    matrix = data[0]
    i = data[1]    
    j = data[2]
    value = data[3]
    if matrix == 'a':
        for n in range(cols):
            mr.emit_intermediate((i,n), ['a',i,j,value])
    else:
        for n in range(rows):
            mr.emit_intermediate((n,j), ['b',i,j,value])

# Reduce function
# mr - MapReduce object
# key - key generated from map phse, associated to list_of_values
# list_of_values - values generated from map phase, associated to key
def reducer(key, list_of_values):
    # output item (only for reducer)
    # for each item in list_of_values, reconstruct a and b matrix
    a =  [0 for i in range(rows)]
    b =  [0 for i in range(cols)]
    for line in list_of_values:
        if line[0] == 'a':
            a[line[2]] = line[3]
        else:
            b[line[1]] = line[3]
            
    value = 0
    for k in range(rows):
        value += a[k] * b[k]
    
    mr.emit((key[0],key[1],value))
    
    

def main():
    # Assumes first argument is a file of json objects formatted as strings, 
    #one per line.    
    mr.execute(open(sys.argv[1]), mapper, reducer)

if __name__ == '__main__':
    main()
