import json

class Node:
    ID = 0 
    
    def __init__(self, time) -> None:
        Node.ID += 1
        self.Id = Node.ID
        self.Time = time
        self.Parent = None
        self.Children = None
    
    def set_parent(self, parent, distance):
        self.Parent = {
            'Id': parent.Id,
            'Distance': distance
        }
        if (parent.Children == None):
            parent.Children = []
        parent.Children.append({
            'Id' : self.Id,
            'Distance' : distance
        })
 
def Connect(parent, child, distance):
    child.set_parent(parent, distance)

root = Node(1.0)
child1 = Node(2.0)
child2 = Node(2.1)

Connect(root, child1, 1.0)
Connect(root, child2, 50.0)

msg_json = json.dumps([vars(root), vars(child1), vars(child2)])

with open("tree.json", "w") as json_file:
    json_file.write(msg_json)

print(msg_json)








