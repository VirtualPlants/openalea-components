# -*- python -*-
#
#       OpenAlea.Core
#
#       Copyright 2006-2009 INRIA - CIRAD - INRA
#
#       File author(s): Jerome Chopard <jerome.chopard@sophia.inria.fr>
#                       Fred Theveny <frederic.theveny@cirad.fr>
#                       Jonathan Legrand <jonathan.legrand@ens-lyon.fr>
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
#
#       OpenAlea WebSite: http://openalea.gforge.inria.fr
#
################################################################################
"""This module provide a set of concepts to add properties to graph elements"""

__license__ = "Cecill-C"
__revision__ = " $Id$ "

from interface.property_graph import IPropertyGraph, PropertyError
from graph import Graph, InvalidVertex, InvalidEdge
import numpy as np
from heapq import heappop, heappush
import warnings

VertexProperty, EdgeProperty, GraphProperty = range(3)
VertexIdType, EdgeIdType, ValueType = range(3)

class PropertyGraph(IPropertyGraph, Graph):
    """
    Simple implementation of IPropertyGraph using
    dict as properties and two dictionaries to
    maintain these properties
    """
    metavidtypepropertyname = "valueproperty_as_vid"
    metaeidtypepropertyname = "valueproperty_as_eid"
    
    def __init__(self, graph=None, **kwds):
        if graph is None:
            self._vertex_property = {}
            self._edge_property = {}
            self._graph_property = {}
            print "Constructing EMPTY PropertyGraph object"
        else:
            self._vertex_property = graph._vertex_property
            self._edge_property = graph._edge_property
            self._graph_property = graph._graph_property
        Graph.__init__(self, graph, **kwds)

    def __str__(self):
        """
        Format returned instance type informations.
        """
        print "Object PropertyGraph:"
        print "  - {} vertices".format(len(self._vertices))
        print "  - {} edges".format(len(self._edges))
        print "  - {} vertex properties".format(len(self._vertex_property))
        print "  - {} edge properties".format(len(self._edge_property))
        print "  - {} edge properties".format(len(self._graph_property))

    def vertex_property_names(self):
        """
        Return a key-iterator of vertex property names in the object.

        Returns
        -------
        iterator of self._vertex_property.keys()
        """
        return self._vertex_property.iterkeys()
    vertex_property_names.__doc__ = IPropertyGraph.vertex_property_names.__doc__

    def vertex_properties(self):
        """
        Returns all the vertex properties in the object as a dictionary
        with as keys, the property names and as values, a dictionary of corresponding
        vid values

        Returns
        -------
        a dictionary {'property_name': {vid: vid_ppty_value}}
        """
        return self._vertex_property
    # vertex_properties.__doc__ = IPropertyGraph.vertex_properties.__doc__

    def vertex_property(self, property_name, vids = None):
        """
        Return the dictionary of vid values, filtered by vids if not None.

        Parameters
        ----------
        property_name: str
            the name of an existing vertex property
        vids: list
            the list of vids to return

        Returns
        -------
        a dictionary {vid: vid_ppty_value}
        """
        try:
            if vids is not None:
                return dict([(k,v) for k,v in self._vertex_property[property_name].iteritems() if k in vids])
            else:
                return self._vertex_property[property_name]
        except KeyError:
            raise PropertyError("property %s is undefined on vertices"
                                % property_name)
    vertex_property.__doc__=IPropertyGraph.vertex_property.__doc__

    def edge_property_names(self):
        """
        Return a key-iterator of edges property names in the object.

        Returns
        -------
        iterator of self._edges_property.keys()
        """
        return self._edge_property.iterkeys()
    edge_property_names.__doc__ = IPropertyGraph.edge_property_names.__doc__

    def edge_properties(self):
        """
        Returns all the edges properties in the object as a dictionary
        with as keys, the property names and as values, a dictionary of corresponding
        eid values

        Returns
        -------
        a dictionary {'property_name': {eid: eid_ppty_value}}, for all edge properties
        """
        return self._edge_property
    #  edge_properties.__doc__ = IPropertyGraph. edge_properties.__doc__

    def edge_property(self, property_name, eids=None):
        """
        Return the dictionary of eid values, filtered by eids if not None.

        Parameters
        ----------
        property_name: str
            the name of an existing edge property
        vids: list
            the list of eids to return

        Returns
        -------
        a dictionary {eid: eid_ppty_value}
        """
        try:
            if eids is not None:
                return dict([(k,v) for k,v in self._edge_property[property_name].iteritems() if k in eids])
            else:
                return self._edge_property[property_name]
        except KeyError:
            raise PropertyError("property %s is undefined on edges"
                                % property_name)
    edge_property.__doc__ = IPropertyGraph.edge_property.__doc__

    def graph_property_names(self):
        """
        Return a key-iterator of graph property names in the object.

        Returns
        -------
        iterator of self._graph_property.keys()
        """
        return self._graph_property.iterkeys()

    def graph_properties(self):
        """
        Returns all the graph properties in the object as a dictionary
        with as keys, the graph property names and as values, a dictionary of
        corresponding graph values

        Returns
        -------
        a dictionary {'property_name': graph_property} for all graph properties
        """
        return self._graph_property

    def graph_property(self, property_name):
        """
        Return the corresponding graph property value.

        Parameters
        ----------
        property_name: str
            the name of an existing graph property

        Returns
        -------
        self._graph_property[property_name]
        """
        try:
            return self._graph_property[property_name]
        except KeyError:
            raise PropertyError("property %s is undefined on graph"
                                % property_name)
    graph_property.__doc__ = IPropertyGraph.graph_property.__doc__


    def add_vertex_property(self, property_name, values=None):
        """
        Add a new vertex property, with values if it is a vid dictionary, or leaves
        it empty if None.

        Parameters
        ----------
        property_name : str
            the name of the property to add
        values : dict | None
            a dictionary with vid as keys, None will add an empty property

        Returns
        -------
        Nothing, edit object
        """
        if property_name in self._vertex_property:
            raise PropertyError("property %s is already defined on vertices"
                                % property_name)
        if values is None:
            print "Creating EMPTY vertex property '{}'".format(property_name)
            values = {}
        else:
            try:
                assert isinstance(values, dict)
            except:
                raise AssertionError("Values must be a dictionary {vid: value}")
        self._vertex_property[property_name] = values
    add_vertex_property.__doc__ = IPropertyGraph.add_vertex_property.__doc__


    def extend_vertex_property(self, property_name, values):
        """
        Extend an existing vertex property 'property_name' with 'values', a vid dictionary.

        Parameters
        ----------
        property_name : str
            a string mathing an exiting property
        values : dict
            a dictionary {vid: vid_values}

        Returns
        -------
        Nothing, edit object

        Notes
        ----
        * 'property_name' should exist
        * 'values' cannot be an empty dictionary
        """
        if not isinstance(values, dict):
            raise TypeError("Values %s is not a type 'dict'" % values)
        else:
            try:
                assert values != {}
            except:
                raise AssertionError("Values is an EMPTY 'dict'")
        if property_name not in self._vertex_property:
            print PropertyError("Property %s is not defined on vertices"
                                % property_name)
            print "Creating vertex property %s" % property_name
            self._vertex_property[property_name] = {}

        id_duplicate = []
        for k,v in values.iteritems():
            if k in self.vertices():
                if not self._vertex_property[property_name].has_key(k):
                    self._vertex_property[property_name][k] = v
                else:
                    id_duplicate.append(k)
            else:
                print "Vertex id {} doesn't exist in the graph !!".format(k)
        if id_duplicate != []:
            print "Following vertex ids already have a value for property {}".format(
                property_name, id_duplicate)

    def remove_vertex_property(self, property_name):
        """
        Remove the vertex property 'property_name' of the object.

        Parameters
        ----------
        property_name : str
            name of the vertex property to remove

        Returns
        -------
        Nothing, edit object
        """
        try:
            del self._graph_property['units'][property_name]
        except:
            pass
        try:
            del self._vertex_property[property_name]
            print "Removed vertex property '{}' (n_vids={})".format(
                property_name, len(graph.vertex_property(property_name)))
        except KeyError:
            raise PropertyError("property %s is undefined on vertices"
                                % property_name)
    remove_vertex_property.__doc__ = IPropertyGraph.remove_vertex_property.__doc__

    def add_edge_property(self, property_name, values=None):
        """
        Add a new edge property, with values if it is an eid dictionary, or leaves
        it empty if None.

        Parameters
        ----------
        property_name : str
            the name of the property to add
        values : dict | None
            a dictionary with eid as keys, None will add an empty property

        Returns
        -------
        Nothing, edit object
        """
        if property_name in self._edge_property:
            raise PropertyError("property %s is already defined on edges"
                                % property_name)
        if values is None:
            print "Creating EMPTY egde property '{}'".format(property_name)
            values = {}
        try:
            assert isinstance(values, dict)
        except:
            raise AssertionError("Values must be a dictionary {eid: value}")
        self._edge_property[property_name] = values
    add_edge_property.__doc__ = IPropertyGraph.add_edge_property.__doc__

    def extend_edge_property(self, property_name, values):
        """
        Extend an existing egde property 'property_name' with 'values', an eid dictionary.

        Parameters
        ----------
        property_name : str
            a string mathing an exiting property
        values : dict
            a dictionary {eid: eid_values}

        Returns
        -------
        Nothing, edit object

        Notes
        ----
        * 'property_name' should exist
        * 'values' cannot be an empty dictionary
        """
        if not isinstance(values, dict):
            raise TypeError("Values %s is not a type 'dict'" % values)
        else:
            try:
                assert values != {}
            except:
                raise AssertionError("Values is an EMPTY 'dict'")
        if property_name not in self._edge_property:
            print PropertyError("Property %s is not defined on vertices"
                                % property_name)
            print "Creating vertex property %s" % property_name
            self._edge_property[property_name] = {}

        id_duplicate = []
        for k,v in values.iteritems():
            if k in self.vertices():
                if not self._edge_property[property_name].has_key(k):
                    self._edge_property[property_name][k] = v
                else:
                    id_duplicate.append(k)
            else:
                print "Edge id {} doesn't exist in the graph !!".format(k)
        if id_duplicate != []:
            print "Following edge ids already have a value for property {}".format(
                property_name, id_duplicate)

    def remove_edge_property(self, property_name):
        """
        Remove the edge property 'property_name' of the object.

        Parameters
        ----------
        property_name : str
            name of the edge property to remove

        Returns
        -------
        Nothing, edit object
        """
        try:
            del self._graph_property['units'][property_name]
        except:
            pass
        try:
            del self._edge_property[property_name]
            print "Removed edge property '{}' (n_eids={})".format(property_name, len(graph.edge_property(property_name)))
        except KeyError:
            raise PropertyError("property %s is undefined on edges"
                                % property_name)
    remove_edge_property.__doc__ = IPropertyGraph.remove_edge_property.__doc__

    def add_graph_property(self, property_name, values=None):
        """
        Add a new graph property, empty if values is None else add it to the object.

        Parameters
        ----------
        property_name : str
            the name of the property to add
        values : Any | None
            any type or object

        Returns
        -------
        Nothing, edit object
        """
        if property_name in self._graph_property:
            raise PropertyError("property %s is already defined on graph"
                                % property_name)
        if values is None:
            print "Creating EMPTY graph property '{}'".format(property_name)
        self._graph_property[property_name] = values
    
    def extend_graph_property(self, property_name, values):
        """
        Extend an existing graph property 'property_name' with 'values'.

        Parameters
        ----------
        property_name : str
            a string mathing an exiting property
        values : Any
            any type or object

        Returns
        -------
        Nothing, edit object

        Notes
        ----
        * 'property_name' should exist
        * 'values' cannot be an empty dictionary
        """
        if property_name not in self._graph_property:
            raise PropertyError("property %s is not defined on graph"
                                % property_name)

        try:
            assert values is not None
        except:
            raise AssertionError("Values is EMPTY (None)")
        if isinstance(self.graph_property(property_name), list):
            try:
                assert values != []
            except:
                raise AssertionError("Values is an EMPTY 'list'")
            self._graph_property[property_name].extend(values)
        elif isinstance(self.graph_property(property_name), dict):
            try:
                assert values != {}
            except:
                raise AssertionError("Values is an EMPTY 'dict'")
            self._graph_property[property_name].update( dict([(k,v) for k,v in values.iteritems() if k not in self.graph_property(property_name).keys()]) )
        else:
            print "Unable to extend 'graph_property' (type:{}) with this type of data: {}".format(type(self._graph_property[property_name]), type(values))

    def remove_graph_property(self, property_name):
        """
        Remove the graph property 'property_name' of the object.

        Parameters
        ----------
        property_name : str
            name of the graph property to remove

        Returns
        -------
        Nothing, edit object
        """
        try:
            del self._graph_property[property_name]
            print "Removed graph property '{}' (n_vids={})".format(property_name, len(graph.graph_property(property_name)))
        except KeyError:
            raise PropertyError("property %s is undefined on graph"
                                % property_name)
        try:
            del self._graph_property['units'][property_name]
        except KeyError:
            pass

    def remove_vertex(self, vid):
        """
        Remove vertex if 'vid' from the object.
        It is also removed from any vertex property!

        Parameters
        ----------
        vid : int
            the id of the vertex to remoce

        Returns
        -------
        Nothing, edit object
        """
        try:
            assert graph.has_vertex(vid)
        except:
            raise AssertionError("'vid' {} is not in the list of vertices".format(vid))
        for prop in self._vertex_property.itervalues():
            prop.pop(vid, None)
        Graph.remove_vertex(self, vid)
    remove_vertex.__doc__ = Graph.remove_vertex.__doc__

    def remove_edge(self, eid):
        """
        Remove the edge 'eid' from the object.

        Parameters
        ----------
        eid : int
            id of the edge to remove

        Returns
        -------
        Nothing, edit object
        """
        try:
            assert graph.has_edges(eid)
        except:
            raise AssertionError("'eid' {} is not in the list of edges".format(vid))
        for prop in self._edge_property.itervalues():
            prop.pop(eid, None)
        Graph.remove_edge(self, eid)

    remove_edge.__doc__ = Graph.remove_edge.__doc__

    def clear(self):
        """
        Clear the object of all vetex, edge and graph properties.

        Returns
        -------
        Nothing, edit object
        """
        for prop in self._vertex_property.itervalues():
            prop.clear()
        for prop in self._edge_property.itervalues():
            prop.clear()
        for prop in self._graph_property.itervalues():
            prop.clear()
        Graph.clear(self)
    clear.__doc__ = Graph.clear.__doc__

    def clear_edges(self):
        """
        Remove all edges from the object.

        Returns
        -------
        Nothing, edit object
        """
        for prop in self._edge_property.itervalues():
            prop.clear()
        Graph.clear_edges(self)
    clear_edges.__doc__ = Graph.clear_edges.__doc__

    @staticmethod
    def _translate_property(values, trans_vid, trans_eid, key_translation = ValueType, value_translation = ValueType):
        # translation function
        from copy import deepcopy
        
        id_value = lambda value: value
        
        trans_vid = deepcopy(trans_vid)
        trans_vid[None] = None
        def translate_vid(vid): 
            if isinstance(vid, list): return [trans_vid[i]  for i in vid]
            if isinstance(vid, tuple): return tuple([trans_vid[i]  for i in vid])
            return trans_vid[vid]
        
        trans_eid = deepcopy(trans_eid)
        trans_eid[None] = None
        def translate_eid(eid):
            if isinstance(eid, list): return [trans_eid[i]  for i in eid]
            if isinstance(eid, tuple): return tuple([trans_eid[i]  for i in eid])
            return trans_eid[eid]

        translator = { ValueType : id_value, VertexIdType :  translate_vid, EdgeIdType : translate_eid }

        key_translator = translator[key_translation]
        value_translator = translator[value_translation]

        # translate vid and value
        return dict([(key_translator(vid),value_translator(val)) for vid, val in values.iteritems()])


    def _relabel_and_add_vertex_edge_properties(self, graph, trans_vid, trans_eid):
        
        # update properties on vertices
        for prop_name in graph.vertex_property_names():
            if prop_name not in self._vertex_property:
                self.add_vertex_property(prop_name)
            value_translator = graph.get_property_value_type(prop_name,VertexProperty)

            # import property into self. translate vid and value
            self.vertex_property(prop_name).update(self._translate_property(graph.vertex_property(prop_name), trans_vid, trans_eid, VertexIdType, value_translator))

        # update properties on edges
        for prop_name in graph.edge_property_names():
            if prop_name not in self._edge_property:
                self.add_edge_property(prop_name)
            
            # Check what type of translation is required for value of the property
            value_translator = graph.get_property_value_type(prop_name,EdgeProperty)
            
            # import property into self. translate vid and value
            self.edge_property(prop_name).update(self._translate_property(graph.edge_property(prop_name), trans_vid, trans_eid, EdgeIdType, value_translator))

    def translate_graph_property(self, prop_name, trans_vid, trans_eid):
        """ Translate a graph property according to meta info """
        old_prop = self.graph_property(prop_name)
        print type(old_prop)
        key_translator = self.get_graph_property_key_type(prop_name)
        value_translator = self.get_property_value_type(prop_name, GraphProperty)
        print 'translate_graph_property',prop_name, key_translator, value_translator
        
        return self._translate_property(old_prop, trans_vid, trans_eid, key_translator, value_translator)
    
    
    def extend_property_graph(self, graph):
    # def extend(self, graph):
        """
        Extend the current object with another 'graph' of type Graph.

        Parameters
        ----------
        graph : Graph | PropertyGraph
            the object to use to extent the current one.

        Returns
        -------
        Nothing, edit object
        """
        # add and translate the vertex and edge ids of the second graph
        trans_vid, trans_eid = Graph.extend(self,graph)
        
        # relabel the edge and vertex property
        self._relabel_and_add_vertex_edge_properties(graph, trans_vid, trans_eid)
        
        # update properties on graph
        #gproperties = self.graph_property()
        newgproperties = {}
        for pname, prop in graph.graph_property_names():
            newgproperty = graph.translate_graph_property(pname,trans_vid, trans_eid)
            newgproperties[pname] = newgproperty

            prop.update(newgproperties)

        return trans_vid, trans_eid

    extend_property_graph.__doc__ = Graph.extend.__doc__
    # extend.__doc__ = Graph.extend.__doc__


    def set_graph_property_value_to_vid_type(self, propertyname, property_type = VertexProperty):
        """ Give meta info on property value type. Associate it to Vertex Id type """
        if not self._graph_property.has_key(self.metavidtypepropertyname):
            self.add_graph_property(self.metavidtypepropertyname,([],[],[],[]))
        prop = self.graph_property(self.metavidtypepropertyname)[property_type]
        prop.append(propertyname)

    def set_graph_property_value_to_eid_type(self, propertyname,  property_type = EdgeProperty):
        """ Give meta info on property value type. Associate it to Edge Id type """
        if not self._graph_property.has_key(self.metaeidtypepropertyname):
            self.add_graph_property(self.metaeidtypepropertyname,([],[],[],[]))
        prop = self.graph_property(self.metaeidtypepropertyname)[property_type]
        prop.append(propertyname)

    def set_graph_property_key_to_vid_type(self, propertyname):
        """ Give meta info on graph property key type. Associate it to Vertex Id type"""
        self.set_graph_property_value_to_vid_type(propertyname, 3)

    def set_graph_property_key_to_eid_type(self, propertyname):
        """ Give meta info on graph property key type. Associate it to Edge Id type """
        self.set_graph_property_value_to_eid_type(propertyname, 3)

    def get_property_value_type(self, propertyname, property_type = VertexProperty):
        """ Return meta info on property value type. """
        try:
            prop = self.graph_property(self.metavidtypepropertyname)[property_type]
            if propertyname in prop : return VertexIdType
        except:
            pass
        try:
            prop = self.graph_property(self.metaeidtypepropertyname)[property_type]
            if propertyname in prop : return EdgeIdType
        except:
            return ValueType

    def get_graph_property_key_type(self, propertyname):
        """ Return meta info on graph property key type. """
        return self.get_property_value_type(propertyname, 3)


    def __to_set(self, s):
        if not isinstance(s, set):
            if isinstance(s, list):
                s=set(s)
            else:
                s=set([s])
        return s

    def in_neighbors(self, vid, edge_type=None):
        """ Return the in vertices of the vertex vid
        
        :Parameters:
        - `vid` : a vertex id
        - `edges_type` : type of edges we want to consider (can be a set)

        :Returns:
        - `neighbors_list` : the set of parent vertices of the vertex vid
        """
        
        if vid not in self :
            raise InvalidVertex(vid)
        
        if edge_type==None:
            neighbors_list=set([self.source(eid) for eid in self._vertices[vid][0] ])
        else:
            edge_type=self.__to_set(edge_type) 
            edge_type_property = self._edge_property['edge_type']
            neighbors_list=set([self.source(eid) for eid in self._vertices[vid][0] if edge_type_property[eid] in edge_type])
        return neighbors_list

    def iter_in_neighbors(self, vid, edge_type=None):
        """ Return the in vertices of the vertex vid
        
        :Parameters:
        - `vid` : a vertex id
        - `edges_type` : type of edges we want to consider (can be a set)

        :Returns:
        - `iterator` : an iterator on the set of parent vertices of the vertex vid
        """
        return iter(self.in_neighbors(vid, edge_type))

    def out_neighbors(self, vid, edge_type=None):
        """ Return the out vertices of the vertex vid

        :Parameters:
        - `vid` : a vertex id
        - `edges_type` : type of edges we want to consider (can be a set)

        :Returns:
        - `neighbors_list` : the set of child vertices of the vertex vid
        """
        if vid not in self :
            raise InvalidVertex(vid)

        if edge_type==None:
            neighbors_list=set([self.target(eid) for eid in self._vertices[vid][1] ])
        else:
            edge_type=self.__to_set(edge_type) 
            edge_type_property = self._edge_property['edge_type']
            neighbors_list=set([self.target(eid) for eid in self._vertices[vid][1] if edge_type_property[eid] in edge_type])
        return neighbors_list


    def iter_out_neighbors(self, vid, edge_type=None):
        """ Return the out vertices of the vertex vid

        :Parameters:
        - `vid` : a vertex id
        - `edges_type` : type of edges we want to consider (can be a set)

        :Returns:
        - `iterator` : an iterator on the set of child vertices of the vertex vid
        """
        return iter(self.out_neighbors(vid, edge_type))

    def neighbors(self, vid, edge_type=None):
        """ Return the neighbors vertices of the vertex vid
        
        :Parameters:
        - `vid` : a vertex id
        - `edges_type` : type of edges we want to consider (can be a set)

        :Returns:
        - `neighbors_list` : the set of neighobrs vertices of the vertex vid
        """
        return self.in_neighbors(vid, edge_type) | self.out_neighbors(vid, edge_type)

    def iter_neighbors(self, vid, edge_type=None):
        """ Return the neighbors vertices of the vertex vid
        
        :Parameters:
        - `vid` : a vertex id
        - `edges_type` : type of edges we want to consider (can be a set)

        :Returns:
        - `iterartor` : iterator on the set of neighobrs vertices of the vertex vid
        """
        return iter(self.neighbors(vid, edge_type))
  

    def in_edges(self, vid, edge_type=None):
        """ Return in edges of the vertex vid
        
        :Parameters:
        - `vid` : a vertex id
        - `edges_type` : type of edges we want to consider (can be a set)

        :Returns:
        - `edge_list` : the set of the in edges of the vertex vid
        """
        if vid not in self :
            raise InvalidVertex(vid)

        if not edge_type:
            edge_list=set([eid for eid in self._vertices[vid][0]])
        else:
            edge_type=self.__to_set(edge_type)
            edge_type_property = self._edge_property['edge_type']
            edge_list=set([eid for eid in self._vertices[vid][0] if edge_type_property[eid] in edge_type])
        return  edge_list
        
    def iter_in_edges(self, vid, edge_type=None):
        """ Return in edges of the vertex vid
        
        :Parameters:
        - `vid` : a vertex id
        - `edges_type` : type of edges we want to consider (can be a set)

        :Returns:
        - `iterator` : an iterator on the set of the in edges of the vertex vid
        """  
        return iter(self.in_edges(vid, edge_type))


    def out_edges(self, vid, edge_type=None):
        """ Return out edges of the vertex vid
        
        :Parameters:
        - `vid` : a vertex id
        - `edges_type` : type of edges we want to consider (can be a set)

        :Returns:
        - `edge_list` : the set of the out edges of the vertex vid
        """
        if vid not in self :
            raise InvalidVertex(vid)
        
        if edge_type==None:
            edge_list=set([eid for eid in self._vertices[vid][1]])
        else:
            edge_type=self.__to_set(edge_type)
            edge_type_property = self._edge_property['edge_type']
            edge_list=set([eid for eid in self._vertices[vid][1] if edge_type_property[eid] in edge_type])
        return  edge_list

    def iter_out_edges(self, vid, edge_type=None):
        """ Return in edges of the vertex vid
        
        :Parameters:
        - `vid` : a vertex id
        - `edges_type` : type of edges we want to consider

        :Returns:
        - `iterator` : an iterator on the set of the in edges of the vertex vid
        """  
        return iter(self.out_edges(vid, edge_type))


    def edges(self, vid=None, edge_type=None):
        """ Return edges of the vertex vid
        If vid=None, return all edges of the graph
        
        :Parameters:
        - `vid` : a vertex id
        - `edges_type` : type of edges we want to consider

        :Returns:
        - `edge_list` : the set of the edges of the vertex vid
        """
        if vid==None:
            if edge_type is not None:
                return set([eid for eid in self._edges.keys() if self.edge_property('edge_type')[eid] == edge_type])
            else:
                return set([eid for eid in self._edges.keys()])
        return self.out_edges(vid, edge_type) | self.in_edges(vid, edge_type)

    def iter_edges(self, vid, edge_type=None):
        """ Return in edges of the vertex vid
        If vid=None, return all edges of the graph
        
        :Parameters:
        - `vid` : a vertex id
        - `edges_type` : type of edges we want to consider

        :Returns:
        - `iterator` : an iterator on the set of the edges of the vertex vid
        """  
        return iter(self.edges(vid, edge_type))

    def neighborhood(self, vid, max_distance=1, edge_type=None):
        """ Return the neighborhood of the vertex vid at distance max_distance (the disc, not the circle)
        
        :Parameters:
        - `vid` : vertex id

        :Returns:
        - `neighbors_list` : the set of the vertices at distance below max_distance of the vertex vid (including vid)
        """
        dist=self.topological_distance(vid, edge_type=edge_type, max_depth=max_distance, full_dict=False)
        return set(dist.keys())

    def iter_neighborhood(self, vid, n, edge_type=None):
        """ Return the neighborhood of the vertex vid at distance n (the disc, not the circle)
        
        :Parameters:
        - `vids` : a set of vertex id

        :Returns:
        - `iterator` : an iterator on the set of the vertices at distance n of the vertex vid
        """
        return iter(self.neighborhood(vid, n, edge_type))    


    def topological_distance(self, vid, edge_type = None, edge_dist = lambda x,y : 1, max_depth=float('inf'), full_dict=True, return_inf = True):
        """ Return the distances of each vertices from the vertex `vid` according a cost function
        
        :Parameters:
        - `vid` (int) - a vertex id
        - `edges_type` (str) - type of edges we want to consider e.g. 's' or 't'
        - `edge_dist` (function) - the cost function
        - `max_depth` (float) - the maximum depth that we want to reach
        - `full_dict` (bool) - if True this function will return the entire dictionary (with inf values)
        - `return_inf` (bool) - if True (default) return 'inf' values, else 'nan'.

        :Returns:
        - `dist_dict` : a dictionary of the distances, key : vid, value : distance
        """
        dist={}
        reduced_dist={}
        reduced_dist[vid]=0
        Q=[]

        infinite_distance = float('inf')
        for k in self._vertices.iterkeys():
            dist[k] = infinite_distance
            heappush(Q, (dist[k], k))

        dist[vid]=0
        heappush(Q, (dist[vid], vid))
        treated=set()
        modif=True
        n = self.nb_vertices()
        while (len(treated)!=n and modif):
            modif = False
            actualVid = heappop(Q)
            while actualVid[1] in treated and actualVid[0] == infinite_distance:
                actualVid = heappop(Q)

            if actualVid[0] != infinite_distance:
                actualVid = actualVid[1]
                treated.add(actualVid)
            
                for neighb in self.iter_neighbors(actualVid, edge_type):
                    dist_neighb = dist[neighb]
                    if (((dist_neighb == infinite_distance) or (dist_neighb > dist[actualVid] + edge_dist(neighb, actualVid)))
                          and (dist[actualVid] + edge_dist(neighb, actualVid) < max_depth+1 ) ):
                        
                        dist_neighb = dist[actualVid] + edge_dist(neighb, actualVid)
                        dist[neighb] = dist_neighb
                        reduced_dist[neighb] = dist_neighb
                        heappush(Q, (dist_neighb, neighb))
                    modif = True
        #~ return (reduced_dist, dist)[full_dict], Q
        if not return_inf:
            dist = dict( [(k,(v if v != infinite_distance else np.nan)) for k,v in dist.iteritems()] )

        return (reduced_dist, dist)[full_dict]


    def adjacency_matrix(self, edge_type = None, edge_dist = 1, no_edge_val = 0, oriented = True, reflexive = True, reflexive_value = 0):
        """ Return the adjacency matrix of the graph.
        :Parameters:
        - `edge_type` : type of edges we want to consider
        - `edge_dist` : cost ot cost function to apply between two edges, default : 1
        - `no_edge_val` : cost to put if there is no edge between two vertices, default : 0
        - `oriented` : if True, the graph is considered oriented and we always add an edge j -> i if i -> j exists
        - `reflexive` : if True, the graph is considered reflexive and we will put the cost or the cost_function `reflexive_value` on the diagonal of the adjacency_matrix, default : 0

        :Return:
        - `numpy.array` : a NxN matrix
        """
        if not isinstance(edge_dist, type(lambda m: 1)):
            val_edge_dist = edge_dist
            edge_dist = lambda g, x, y : val_edge_dist
        if not isinstance(reflexive_value, type(lambda m: 1)):
            val_reflexive_value = reflexive_value
            reflexive_value = lambda g, x, y : val_reflexive_value
        
        n = self.nb_vertices()
        adjacency_matrix = np.array(n*[n*[no_edge_val]])
        for edge in self.edges(edge_type=edge_type):
            v1, v2 = self.edge_vertices(edge)
            adjacency_matrix[v1, v2] = edge_dist(self, v1, v2)
            if not oriented:
                adjacency_matrix[v2, v1] = edge_dist(self, v2, v1)
        if reflexive:
            for i in range(n) : adjacency_matrix[i, i] = reflexive_value(self, i, i)
        return adjacency_matrix

    def floyd_warshall(self, edge_type = None, edge_dist = 1, oriented = False):
        adjacency_matrix = self.adjacency_matrix(edge_type, edge_dist, float('inf'), oriented)
        n = self.nb_vertices()
        for k in range(n):
            for i in range(n):
                for j in range(n):
                    adjacency_matrix[i, j]=min(adjacency_matrix[i, j], 
                                               adjacency_matrix[i, k] + adjacency_matrix[k, j])
        return adjacency_matrix

    def _add_vertex_to_domain(self, vids, domain_name):
        """ Add a set of vertices to a domain.
        Save it in two places: 
             - self.graph_property[domain_name] will return the list of all vertices belonging to 'domain_name';
             - self.vertex_property["domains"][vid] will return the list of all domains `vid` belong to.
        """
        if not "domains" in self._vertex_property:
            self._vertex_property["domains"] = {}
        
        for vid in vids:
            # Adding domain_name to the "domain" property of each `vid`:
            if self._vertex_property["domains"].has_key(vid):
                self._vertex_property["domains"][vid].append(domain_name)
            else:
                self._vertex_property["domains"][vid]=[domain_name]
            # Adding `vid` to the `domain_name` (graph_property) it belong to:
            self._graph_property[domain_name].append(vid)

    def _remove_vertex_from_domain(self, vids, domain_name):
        """Remove a set of vertices `vids` from a domain `domain_name`."""
        for vid in vids:
            self._vertex_property["domains"][vid].remove(domain_name)
            if self._vertex_property["domains"][vid]==[]:
                self._vertex_property["domains"].pop(vid)
                
            self._graph_property[domain_name].remove(vid)

    def add_vertex_to_domain(self, vids, domain_name):
        """ Add a set of vertices `vids` to a domain `domain_name`.
        Save it in two places: 
             - self.graph_property[domain_name] will return the list of all vertices belonging to 'domain_name';
             - self.vertex_property["domains"][vid] will return the list of all domains `vid` belong to.
        """
        if not "domains" in self._graph_property:
            self.add_graph_property("domains", [])
            print "Initialisation of the 'domains' dictionary..."
        if not domain_name in self.graph_property("domains"):
            self._graph_property["domains"].append(domain_name)
        
        if not domain_name in self._graph_property:
            #~ raise PropertyError("property %s is not defined on graph" % domain_name)
            print "Property {} is not defined for vertices on the graph, adding it...".format(domain_name)
            self._graph_property[domain_name] = vids
        
        self._add_vertex_to_domain(self.__to_set(vids), domain_name)

    def remove_vertex_from_domain(self, vids, domain_name):
        """Remove a set of vertices `vids` from a domain `domain_name`."""
        if not domain_name in self._graph_property:
            raise PropertyError("property {} is not defined on graph".format(domain_name))
        self._remove_vertex_from_domain(self.__to_set(vids), domain_name)

    def add_domain_from_func(self, func, domain_name):
        """ Create a domain `domain_name` of vertices according to a function `func`.
        
        :Parameters:
        - `func` : the function to make the domain (might return True or False)
        - `domain_name` : the name of the domain
        """
        if domain_name in self._graph_property:
            raise PropertyError("property {} is already defined on graph".format(domain_name))
        self._graph_property[domain_name]=[]
        if not "domains" in self._vertex_property.keys():
            self.add_vertex_property("domains")
        for vid in self._vertices.keys():
            if func(self, vid):
                self._add_vertex_to_domain(set([vid]), domain_name)

    def add_domains_from_dict(self, dict_domains, domain_names):
        """ If one already posses a dict indicating for a list of vertex which domain they belong to, it can be given to the graph directly.
        
        :Parameters:
        - `dict_domains` (dict) - *keys = ids (SpatialImage); *values = intergers indicating the domain(s)
        - `domain_name` (list) - a list containing the name of the domain(s)
        """
        list_domains = np.unique(dict_domains.values())
        if len(domain_names) != len(list_domains):
            warnings.warn("You didn't provided the same number of domains and domain names.")
            pass
        
        if not "domains" in self._vertex_property.keys():
            self.add_vertex_property("domains")
        
        for domain, domain_name in enumerate(domain_names):
            if domain_name in self._graph_property:
                raise PropertyError("property {} is already defined on graph".format(domain_name))
            self._graph_property[domain_name]=[]
            for vid in dict_domains:
                if dict_domains[vid] == list_domains[domain]:
                    self._add_vertex_to_domain(set([vid]), domain_name)

    def iter_domain(self, domain_name):
        if not domain_name in self._graph_property:
            raise PropertyError("property {} is not defined on graph".format(domain_name))
        return iter(self._graph_property[domain_name])

    def remove_domain(self, domain_name):
        """Remove a domain `domain_name`."""
        if not domain_name in self._graph_property:
            raise PropertyError("property {} is not defined on graph".format(domain_name))

        for vid in self.iter_domain(domain_name):
            self._vertex_property["domains"][vid].remove(domain_name)
            if self._vertex_property["domains"][vid]==[]:
                self._vertex_property["domains"].pop(vid)

        return self._graph_property.pop(domain_name)

    def is_connected_domain(self, domain_name, edge_type=None):
        """Return True if a domain is connected."""
        if not domain_name in self._graph_property:
            raise PropertyError("property %s is not defined on graph"
                                % domain_name)
        domain_sub_graph=Graph.sub_graph(self, self._graph_property[domain_name])
        distances=domain_sub_graph.topological_distance(domain_sub_graph._vertices.keys()[0], edge_type=edge_type)
        return not float('inf') in distances.values()


    def to_networkx(self):
        import networkx as nx
        """ Return a NetworkX Graph from a graph.

        :Parameters: 
         - `g` - TemporalPropertyGraph (property graphs temporaly linked)

        :Returns: 
         - A NetworkX graph.
        """

        g = self

        graph = nx.Graph()
        graph.add_nodes_from(g.vertices())
        graph.add_edges_from(( (g.source(eid), g.target(eid)) for eid in g.edges()))

        # Add graph, vertex and edge properties
        for k, v in g.graph_properties().iteritems():
            graph.graph[k] = v

        vp = g._vertex_property
        for prop in vp:
            for vid, value in vp[prop].iteritems():
                graph.node[vid][prop] = value
        
        ep = g._edge_property
        for eid in g.edges():
            graph.edge[g.source(eid)][g.target(eid)]['eid'] = eid

        for prop in ep:
            for eid, value in ep[prop].iteritems():
                graph.edge[g.source(eid)][g.target(eid)][prop] = value

        return graph 

    def from_networkx(self, graph):
        """ Return a Graph from a NetworkX Directed graph.
        :Parameters: 
            - `graph` : A NetworkX graph.

        :Returns: 
            - `g`: a :class:`~openalea.container.interface.Graph`.
        """
        self.clear()
        g = self

        if not graph.is_directed():
            graph = graph.to_directed()

        vp = self._vertex_property

        for vid in graph.nodes_iter():
            g.add_vertex(vid)
            d = graph.node[vid]
            for k, v in d.iteritems():
                vp.setdefault(k,{})[vid] = v

        ep = self._edge_property
        for source, target in graph.edges_iter():
            d = graph[source][target]
            eid = d.get('eid')
            eid = g.add_edge(source, target, eid)
            for k, v in d.iteritems():
                if k != 'eid':
                    ep.setdefault(k,{})[eid] = v

        gp = self._graph_property
        gp.update(graph.graph)

        return g

    def get_vertex_property_type(self, vtx_ppty):
        """
        Return the type (scalar|vector|tensor) of a given vertex property.
        TODO: Not really working except for scalars...
             ...should be more strict when defining variables types!!!
        """
        # Get every 'vertex_property values' `vtx_ppty` (if not None)...
        values_list = [v for v in self.vertex_property(vtx_ppty).values() if v is not None]
        # Now get their types and simplify this list to its 'unique values' using `set()`.
        types_set = set([type(v) for v in values_list])
        
        if len(types_set) != 1:
            raise warnings.warn("More than ONE type detected for vertex property '{}'! Please check it!".format(vtx_ppty))

        first_val = values_list[0]
        print first_val
        first_type = type(first_val)
        try:
            le = first_val.len
            if le != 1:
                return "vector", le
            else:
                return "scalar"
        except:
            return "scalar"
        try:
            sh = first_val.shape
            if sh != (1,1) and sh != ():
                return "tensor", sh
            else:
                return "scalar"
        except:
            pass

    def to_csv(self, PropertyGraph_id, ppty2export=None, out_fname=None, datetime2fname=True):
        """
        Export vertex properties `ppty2export` to a csv named `out_fname`.
        Cells are given by row and properties by columns.
        For lenght-D vectors properties, like barycenters, each D value will be outputed in a separate column.
        By default export all properties.
        
        Args:
          - `PropertyGraph_id` (str): name or id of the `PropertyGraph`.
          - `ppty2export` (list): list of vid associated properties to export. None, by default, export them all.
          - `out_fname` (str): the name of the csv file!
          - `datetime2fname` (bool): if True (default) add the date to the csv filename.
        
        Based on the original work of V.Mirabet.
        :TODO: move to TissueGraph? class.
        """
        # Init the CSV header with ['PropertyGraph_id'; 'vid'; 'x_bary'; 'y_bary'; 'z_bary';]:
        csv_head = "PropertyGraph_id"+";"+"vid"+";"
        # Get the possible ppty to export crossing required 'ppty_sublist' & availables ones (g.vertex_property_names):
        if ppty2export is not None:
            ppty2export = list(set(self.vertex_property_names()) & set(ppty2export))
        else:
            ppty2export = sorted(self.vertex_property_names())
        
        # Add these ppty names to export to the CSV header:
        for ppty in ppty2export:
            if ppty == "barycenter":
                csv_head += "bary_x;bary_y;bary_z;"
            elif ppty == "barycenter_voxel":
                csv_head += "bary_vox_x;bary_vox_y;bary_vox_z;"
            elif ppty == "inertia_values_3D":
                csv_head += "inertia_val_1;inertia_val_2;inertia_val_3;"
            else:
                csv_head += ppty+";"
        csv_head += "\n" # CSV header endline!
        
        ## Now loop the vids to get their feature values:
        # thus creating a line for each cell with their associated features.
        csv = csv_head
        for vid in sorted(self.vertices()):
            # Add 'flower_id':
            csv += PropertyGraph_id+";"
            # Add 'vid':
            csv += str(vid)+";"
            # Add cell feature values:
            for ppty in ppty2export:
                # In case of lenght-3 vectors:
                if ppty == "barycenter" or ppty == "barycenter_voxel" or ppty == "inertia_values_3D":
                    if self.vertex_property(ppty).has_key(vid):
                        for i in range(3):
                            csv += str(self.vertex_property(ppty)[vid][i])+";"
                    else:
                        csv += ";;;"
                else:
                    if vid in self.vertex_property(ppty):
                        pc = self.vertex_property(ppty)[vid]
                        if type(pc) == str:
                            csv += pc+";"
                        else:
                            try:
                                csv += str(float(pc))+";"
                            except Exception as e:
                                #print pc, e
                                csv += ";"
                    else:
                        csv += ";"
            # Remove the last ';' and put an endline '\n' instead:
            csv = csv[:-1]+"\n"
        
        if out_fname is None:
            out_fname = str(PropertyGraph_id)
            datetime2fname = True
        # Add date time if requested by 'date=True' argument:
        if datetime2fname:
            import time
            m = time.localtime()
            out_fname = out_fname+"_"+str(m.tm_year)+"_"+str(m.tm_mon)+"_"+str(m.tm_mday)+"_"+str(m.tm_hour)+"_"+str(m.tm_min)

        # Finally write the WHOLE 's' string 
        f=open(out_fname+".csv", "w")
        f.write(csv)
        f.close()
        print "Done writting '{}' file!".format(out_fname+".csv")

