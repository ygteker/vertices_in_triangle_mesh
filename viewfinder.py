import json
import itertools
from os import remove
import sys

count = 0

if len(sys.argv) == 3:
    count = int(sys.argv[2])
file_name = sys.argv[1]

with open(''+file_name) as f:
    data = json.load(f)

candidates = data['elements']
eliminated = []

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

def removeElements(ids):
    temp = [rectangle for rectangle in candidates if rectangle['id'] in ids]
    for el in temp:
        candidates.remove(el)


def isVertex(triangle, neighbours):
    triangleValue = 0
    for temp in neighbours:
        if temp['id'] == triangle['id']:
            triangleValue = temp['value']
    neighbours.sort(key=lambda x: x['value'])
    if neighbours[-1]['id'] == triangle['id']:
        removeElements([item['id'] for item in neighbours])
        return {'isVertex': True, 'value': neighbours[-1]['value']}
    else:
        removeElements([item['id'] for item in neighbours[:-1] if item['value'] <= triangleValue])
        return {'isVertex': False, 'value': neighbours[-1]['value']}


def findVertices():
    res = []
    for triangle in candidates:
        if count > len(res) or count == 0:
            temp = isVertex(triangle, findValues(findNeighbours(triangle)))
            if temp['isVertex']:
                res.append({'id': triangle['id'], 'value': temp['value']})
    return res



print(findVertices())