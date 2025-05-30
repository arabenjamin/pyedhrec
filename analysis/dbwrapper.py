import duckdb




def conn(source:str=None):
    
    with duckdb.connect(source) as conn:

        yield conn