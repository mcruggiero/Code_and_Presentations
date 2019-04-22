import numpy as np
import pandas as pd
import networkx as nx
import osmnx as ox
import geopandas as gpd
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.colors as colors
import webcolors

def random_point(lower = -180, higher = 180):
    return (np.random.uniform(low=lower, high=higher),
            np.random.uniform(low=lower, high=higher))

    print(random_point())

def colorer(color):
    answer = []
    for i in color:
        answer.append(int(255 *i))

    return answer

def closest_color(color):
    min_colors = {}
    for key, name in webcolors.css3_hex_to_names.items():
        red, green, blue = webcolors.hex_to_rgb(key)
        rd = (red - color[0]) ** 2
        gd = (green - color[1]) ** 2
        bd = (blue - color[2]) ** 2
        min_colors[(rd + gd + bd)] = name
    return min_colors[min(min_colors.keys())]

def random_color_matrix(dictionary):
    """generates a random RBG dictionary from three linspaces"""

    keys = list(dictionary.keys())
    size = len(keys)

    #These are three three random linspaces
    A = np.linspace(.2,.8, size)
    np.random.shuffle(A)

    B = np.linspace(.2,.8, size)
    np.random.shuffle(B)

    C = np.linspace(.2,.8, size)
    np.random.shuffle(C)

    color_dictionary = {"minor" : 'whitesmoke'}

    for i in range(len(keys)):
        color_dictionary[keys[i]] = closest_color(colorer((A[i],
                                                           B[i],
                                                           C[i])))
    color_dictionary["minor"] = 'whitesmoke'

    return color_dictionary

def node_labeler(node, color_dictionary, dictionary, paint_mode = 0):
    """
    labeles nodes based on dictionary entries
    paint_mode = 0, produces a name
    otherwise, produces RGB color
    """
    answer = []
    for key in dictionary:
        if node in dictionary[key]:
            answer.append(key)

    if paint_mode == 0:
        if len(answer) == 0 or answer[0] == "minor":
            return "minor"
        elif len(answer) == 1:
            return answer[0]
        else: return " ".join(answer)

    else:
        if len(answer) == 0:
            return color_dictionary["minor"]
        elif len(answer) == 1:
            return color_dictionary[answer[0]]
        else:
            return "black"

def intersection(graph):
    """Produces a dictionary for all of the nodes based on degree from a graph"""
    inter_dict = {}
    degree_list = nx.degree_histogram(graph)

    for i in range(len(degree_list)):
        node_list = []
        for j in graph.nodes():
            if nx.degree(graph,j) == i:
                node_list.append(j)

        inter_dict[i] = node_list

    return inter_dict

def major_map(nodes_df,edges_df):

    m_nodes_df = nodes_df[nodes_df.major != "minor"].copy()
    m_edges_df = edges_df[edges_df.ref != "minor"].copy()

    minor_nodes = nodes_df[nodes_df.major == "minor"]

    kill = np.asarray(minor_nodes.osmid.values)

    major_roads = ox.gdfs_to_graph(nodes_df,
                                   m_edges_df)

    for i in kill:
        major_roads.remove_node(i)

    ox.plot_graph(major_roads);

    return [intersection(major_roads), major_roads]

def node_roader(graph):
    """
    edges_df is the edge projection, nodes_df is the node projection
    returns major_road dictionary
    """

    nodes_df, edges_df = ox.graph_to_gdfs(graph, nodes=True, edges=True)

    major_roads = set(edges_df[edges_df.ref.notna()].ref.values)
    major_roads = dict.fromkeys(major_roads, set())
    color_dict = random_color_matrix(major_roads)

    #Return printout to terminal and build major_road dict
    for road in major_roads:
        print("{:<5} \t nodes in {:>18} \t colored \t {}".format(len(edges_df[edges_df.ref == road]),
                                                 road,
                                                 color_dict[road]))

        major_roads[road] = set(edges_df[edges_df.ref == road].u) | set(edges_df[edges_df.ref == road].v)

    #Make Colored Columns for edges
    edges_df.ref.fillna("minor", inplace = True) # Remove all NaN
    edges_df["color"] = edges_df.ref.apply(lambda a: color_dict[a])

    #Make Colored columns for nodes
    nodes_df["major"] = nodes_df.osmid.apply(lambda a: node_labeler(a,
                                                                    color_dict,
                                                                    major_roads,0))
    nodes_df["color"] = nodes_df.osmid.apply(lambda a: node_labeler(a,
                                                                    color_dict,
                                                                    major_roads,1))

    nodes_df["major_inter"] = nodes_df.major.apply(lambda a: a.count(" "))

    #Build coloring lines
    edge_color = [edges_df[(edges_df.u == i[0]) & (edges_df.v == i[1])].color.values[0] for i in graph.edges()]
    node_color = [nodes_df.loc[i].color for i in graph.nodes()]

    print("\nmajor road map for region")
    major_intersections = major_map(nodes_df, edges_df)
    
    ox.plot_graph(graph,
                  node_size=10,
                  node_color = node_color,
                  edge_color = edge_color,
                  annotate=False,
                  dpi = 600,
                  edge_alpha = .5
                );


    data_dictionary = {"graph":graph,
                       "edges":edges_df,
                       "nodes":nodes_df,
                       "major_roads":major_roads,
                       "major_intersections":major_intersections,
                       "color_dictionary":color_dict,
                       "edge_color":edge_color,
                       "node_color":node_color}

    return data_dictionary

def disaster_generator(ndf, location_point = 0, distance = 0):
    """Returns a graph of a disaster object"""
    # define a point at the corner of a box
    if location_point == 0:
        location_point = ndf[["y","x"]].sample(1).values[0]

    if distance == 0:
        distance=2000*np.random.uniform()
    # create network from point, inside bounding box of N, S, E, W each 1750m from point
    disaster = ox.graph_from_point(location_point,
                             distance=distance,
                             distance_type='network',
                             network_type='drive')
    fig, ax = ox.plot_graph(disaster, node_size=30, node_color='red')

    return disaster

def road_kill(dis, ndf, edf):
    """
    Removes edges from city and returns graph object of remaining city roads
    """
    city = ox.gdfs_to_graph(ndf, edf)

    #This below code is a little sloppy, but I am going to live with it for now
    live = []
    for i in city.edges():
        if i not in dis.edges():
            live.append(i[0])

    live = edf[edf["u"].isin(live)]
    #This above code is a little sloppy, but I am going to live with it for now

    print("{} roads remain of {} total roads".format(live.size, edf.size))

    city_live = ox.gdfs_to_graph(ndf, live)

    nc = ['red' if i in dis.nodes() else 'blue' for i in city.nodes()]

    ox.plot_graph(city_live, node_size=15, node_color = nc ,edge_color="g");

    return city_live

def zone_picker(df, times = 1, start = -1, end = -1):
    """from a list of random zones, returns start and end"""

    #Build data dictionary for each zone
    zone = {}
    zone[0] = df[(df.x < df.x.quantile(q = .25)) &
                        (df.y < df.y.quantile(q = .25))].copy()

    zone[1] =df[(df.x > df.x.quantile(q = .75)) &
                       (df.y > df.y.quantile(q = .75))].copy()

    zone[2] = df[(df.x > df.x.quantile(q = .75)) &
                        (df.y < df.y.quantile(q = .25))].copy()

    zone[3] = df[(df.x < df.x.quantile(q = .25)) &
                        (df.y > df.y.quantile(q = .75))].copy()

    #Build choice list
    choices = np.random.choice(range(3),2,replace=False)
    choices = {"start":choices[0], "end":choices[1]}

    #Test for valid Start/End options
    if start in range(3):
        choices["start"] = start

    if end in range(3) and end != start and start != -1:
        choices["end"] = end

    #Build answer dic
    start_dic = zone[choices["start"]].sample(1)[["osmid","x","y"]].to_dict()
    start_dic = pd.DataFrame({k+'_start': v for k, v in start_dic.items()})
    start_dic["start_zone"] = choices["start"]

    #Build temporary end dic
    end_dic = zone[choices["end"]].sample(1)[["osmid","x","y"]].to_dict()
    end_dic = pd.DataFrame({k+'_end': v for k, v in end_dic.items()})
    end_dic["end_zone"] = choices["end"]

    #rename index of end_dic dataframe
    end_dic.rename(index={end_dic.index[0]:start_dic.index[0]}, inplace=True)

    #join Dataframes
    start_dic = start_dic.join(end_dic).reset_index(drop=True)

    times = ["15:30", "17:30"]

    start_dic["Time"] = "8:30"
    for i in range(1,3): start_dic.loc[i] = start_dic.loc[0]
    for i in range(1,3): start_dic.loc[i,"Time"] = times[i - 1]

    answer = start_dic.copy()
    return answer

def random_zone_picker(df,times):
    main = zone_picker(df)
    for i in range(times - 1):
        iterate = zone_picker(df)
        main = pd.concat([main,iterate],
                         keys = ["x","y"]).reset_index(drop=True)

        if i % 500 == 0: print(i)

    return main
