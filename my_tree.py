'''Строим граф с древовидно структрой  на вход подаеться json фаил со следующими значениями
[{'Id': 1, 'Time': 1.0, 'Parent': None, 'Children': [{'Id': 2, 'Distance': 1.0}]
Где Id-номер узла, Time - время появления узла, Parent Id родителя, Children Id детей, Distance - растояние между узлами
. Необходимо отбразить граф в следуюшем виде:
 1. Структрура расширяющиегося (вниз) дерева
 2. Отображение номеов Id на узлах
 3. Отображение Distance на ребрах
 4. Упорядочииь отображенеи относительно параметра Time'''

import json
import networkx as nx
import random
import matplotlib.pyplot as plt
import easygui


def hierarchy_pos(G, root=None, width=1., vert_gap=0.2, vert_loc=0, xcenter=0.5):
    '''
    From Joel's answer at https://stackoverflow.com/a/29597209/2966723
    Licensed under Creative Commons Attribution-Share Alike

    If the graph is a tree this will return the positions to plot this in a
    hierarchical layout.

    G: the graph (must be a tree)

    root: the root node of current branch
    - if the tree is directed and this is not given,
      the root will be found and used
    - if the tree is directed and this is given, then
      the positions will be just for the descendants of this node.
    - if the tree is undirected and not given,
      then a random choice will be used.

    width: horizontal space allocated for this branch - avoids overlap with other branches

    vert_gap: gap between levels of hierarchy

    vert_loc: vertical location of root

    xcenter: horizontal location of root
    '''
    if not nx.is_tree(G):
        raise TypeError('cannot use hierarchy_pos on a graph that is not a tree')

    if root is None:
        if isinstance(G, nx.DiGraph):
            root = next(iter(nx.topological_sort(G)))  # allows back compatibility with nx version 1.11
        else:
            root = random.choice(list(G.nodes))

    def _hierarchy_pos(G, root, width=1., vert_gap=0.2, vert_loc=0, xcenter=0.5, pos=None, parent=None):
        '''
        see hierarchy_pos docstring for most arguments

        pos: a dict saying where all nodes go if they have been assigned
        parent: parent of this branch. - only affects it if non-directed

        '''

        if pos is None:
            pos = {root: (xcenter, vert_loc)}
        else:
            pos[root] = (xcenter, vert_loc)
        children = list(G.neighbors(root))
        if not isinstance(G, nx.DiGraph) and parent is not None:
            children.remove(parent)
        if len(children) != 0:
            dx = width / len(children)
            nextx = xcenter - width / 2 - dx / 2
            for child in children:
                nextx += dx
                pos = _hierarchy_pos(G, child, width=dx, vert_gap=vert_gap,
                                     vert_loc=vert_loc - vert_gap, xcenter=nextx,
                                     pos=pos, parent=root)
        return pos

    return _hierarchy_pos(G, root, width, vert_gap, vert_loc, xcenter)


if __name__ == '__main__':
    titri = " Выбери фаил в разрешении .json "
    try:
        with open(easygui.fileopenbox(msg=r'{0}'.format(titri), filetypes=["*.json"]), newline='') as f:
            file_json = json.load(f)
    except  NameError:
        print("Выбери фаил в разрешение josn")
    except TypeError:
        print('"Выбери фаил в разрешение josn"')


    list_id, list_time, list_edges, dict_dist = [], [], [], {}
    # Парсим json
    for i in file_json:
        list_id.append(i['Id'])
        list_time.append(f"{i['Id']}, t= {i['Time']}")
        if i['Children'] is not None:
            for j in i['Children']:
                list_edges.append((i['Id'], j['Id']))
                dict_dist[(i['Id'], j['Id'])] = str(j['Distance'])

    # ---directed graph---
    G = nx.DiGraph(directed=True)

    # add nodes
    G.add_nodes_from(list_id)
    # add edges
    G.add_edges_from(list_edges)

    # set layout
    pos = hierarchy_pos(G, 1)
    # draw graph
    options = {
        'node_color': 'whitesmoke',
        'node_size': 2700,
        'width': 1,
        'arrowstyle': '-|>',
        'arrowsize': 18,
    }
    plt.figure(figsize=(8, 8))
    # рисуем граф
    nx.draw(G, pos, with_labels=False, arrows=True, **options)

    # draw edge labels
    nx.draw_networkx_edge_labels(
        G, pos,
        edge_labels=dict_dist,
        font_color='red'
    )
    labels = dict(zip(list_id, list_time))

    # рисуем метки
    nx.draw_networkx_labels(G, pos=pos, labels=labels, font_size=10, font_color='k')

    # отображаем
    ax = plt.gca()
    ax.collections[0].set_edgecolor("#000000")
    plt.show()


