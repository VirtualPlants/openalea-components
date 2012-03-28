
__license__ = "Cecill-C"
__revision__ = " $Id: test_property_graph.py 7865 2010-02-08 18:04:39Z cokelaer $ "

# Test node module
from openalea.container import PropertyGraph
from openalea.container import TemporalPropertyGraph
from temporal_property_graph_input import create_TemporalGraph

def test_temporalPropertyGraph():
    """create a graph"""
    g = create_TemporalGraph()

    # ~ begin tests
    
    # ~ Neighbors
    assert g.in_neighbors(13)==set([4, 9, 10, 11, 12])
    assert g.in_neighbors(13, 't')==set([4])
    assert g.in_neighbors(13, 's')==set([9, 10, 11, 12])
    assert g.out_neighbors(4)==set([5, 10, 11, 12, 13])
    assert g.out_neighbors(4, 't')==set([10, 11, 12, 13])
    assert g.out_neighbors(4, 's')==set([5])
    
    # ~ Edges
    assert g.out_edges(5)==set([4, 36, 37])
    assert g.out_edges(5, 't')==set([36, 37])
    assert g.out_edges(5, 's')==set([4])
    assert g.in_edges(5)==set([3, 5, 9])
    assert g.in_edges(5, 't')==set([9])
    assert g.in_edges(5, 's')==set([3, 5])
    
    # ~ Sibling
    assert g.sibling(1)==None
    assert g.sibling(16)==set([17, 18, 19])
    
    # ~ Neighborhood
    assert g.neighborhood(2, 2)==set([0, 1, 2, 3, 4, 5, 7, 8, 9, 10])
    assert g.neighborhood(2, 2, 't')==set([0, 2, 3, 4, 7, 8])
    assert g.neighborhood(2, 2, 's')==set([2, 3, 4, 5])

    # ~ Topologic Distance
    assert g.topo_dist(3)=={0: 1,
                            1: 2,
                            2: 1,
                            3: 0,
                            4: 1,
                            5: 1,
                            6: 2,
                            7: 2,
                            8: 2,
                            9: 1,
                            10: 2,
                            11: 2,
                            12: 2,
                            13: 2,
                            14: 2,
                            15: 2,
                            16: 3,
                            17: 3,
                            18: 3,
                            19: 3}
                          
    assert g.topo_dist(3, edge_type='t')=={0: 1,
                                           1: inf,
                                           2: 2,
                                           3: 0,
                                           4: 2,
                                           5: inf,
                                           6: inf,
                                           7: 3,
                                           8: 3,
                                           9: 1,
                                           10: 3,
                                           11: 3,
                                           12: 3,
                                           13: 3,
                                           14: inf,
                                           15: inf,
                                           16: inf,
                                           17: inf,
                                           18: inf,
                                           19: inf}
    assert g.topo_dist(3, edge_type='s')=={0: inf,
                                           1: inf,
                                           2: 1,
                                           3: 0,
                                           4: 1,
                                           5: 1,
                                           6: 2,
                                           7: inf,
                                           8: inf,
                                           9: inf,
                                           10: inf,
                                           11: inf,
                                           12: inf,
                                           13: inf,
                                           14: inf,
                                           15: inf,
                                           16: inf,
                                           17: inf,
                                           18: inf,
                                           19: inf}
    
     assert g.topo_dist(3, edge_dist=lambda x,y: 2)=={0: 2,
                                                      1: 4,
                                                      2: 2,
                                                      3: 0,
                                                      4: 2,
                                                      5: 2,
                                                      6: 4,
                                                      7: 4,
                                                      8: 4,
                                                      9: 2,
                                                      10: 4,
                                                      11: 4,
                                                      12: 4,
                                                      13: 4,
                                                      14: 4,
                                                      15: 4,
                                                      16: 6,
                                                      17: 6,
                                                      18: 6,
                                                      19: 6}
