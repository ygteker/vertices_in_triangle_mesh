import json
import itertools
import sys

count = 0

if len(sys.argv) == 3:
    count = int(sys.argv[2])
file_name = sys.argv[1]

print(len(sys.argv))

with open(''+file_name) as f:
    data = json.load(f)

def inTriangle(mNodeId, mTriangle):
    return mNodeId in [nodeId for nodeId in mTriangle['nodes']]

def findTriangles(node):
    return [triangle for triangle in data['elements'] if inTriangle(node, triangle)]

def findNeighbours(triangle):
    res = list(itertools.chain.from_iterable([findTriangles(node) for node in triangle['nodes']]))
    return list({item['id']: item for item in res}.values())

def findValues(neighbours):
    res = []
    for triangle in neighbours:
        res.append({'id': triangle['id'], 'value': next(valueEl['value'] for valueEl in data['values'] if valueEl['element_id'] == triangle['id'])})
    return res

def isVertex(triangle, neighbours):
    neighbours.sort(key=lambda x: x['value'])
    if neighbours[-1]['id'] == triangle['id']:
        return {'isVertex': True, 'value': neighbours[-1]['value']}
    return {'isVertex': False, 'value': neighbours[-1]['value']}

def findVertices():
    res = []
    for triangle in data['elements']:
        if count > len(res) or count == 0:
            temp = isVertex(triangle, findValues(findNeighbours(triangle)))
            if temp['isVertex']:
                res.append({'id': triangle['id'], 'value': temp['value']})
    return res

print(findVertices())