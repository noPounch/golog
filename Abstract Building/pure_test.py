import os, json
print(json.dumps({'hello': 'world'}))

with open(os.path.join( os.path.dirname( os.path.abspath(__file__) ) , 'test/test.json' ),'w') as file:
    print(json.dumps({'hello': 'world'}))
