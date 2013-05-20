import MapReduce
import json
import sys

mr = MapReduce.MapReduce()

# Map function
# mr - MapReduce object
# data - json object formatted as a string
def mapper(data):
    sequence_id = data[0]
    dna = data[1]    
    dna = dna[:-10]
    mr.emit_intermediate(dna, sequence_id)

# Reduce function
# mr - MapReduce object
# key - key generated from map phse, associated to list_of_values
# list_of_values - values generated from map phase, associated to key
def reducer(key, list_of_values):
    # output item (only for reducer)
    mr.emit(key)
    

def main():
    # Assumes first argument is a file of json objects formatted as strings, 
    #one per line.    
    mr.execute(open(sys.argv[1]), mapper, reducer)

if __name__ == '__main__':
    main()
