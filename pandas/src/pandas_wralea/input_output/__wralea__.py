
# This file has been generated at Tue Mar 11 11:47:03 2014

from openalea.core import *


__name__ = 'openalea.pandas.io'

__editable__ = True
__description__ = 'Pandas wrapping.'
__license__ = 'CECILL-C'
__url__ = 'http://openalea.gforge.inria.fr'
__alias__ = []
__version__ = '1.0.0'
__authors__ = 'OpenAlea Consortium'
__institutes__ = 'INRIA/CIRAD/INRA'
__icon__ = ''


__all__ = ['data2PandasDataframe', 'pandasDataframe2data', 'io_utils_to_csv', 'io_utils_read_csv']



data2PandasDataframe = CompositeNodeFactory(name='data2PandasDataframe',
                             description='Composite node made by grouping openalea.data file.get_data and openalea.pandas.io.read_csv',
                             category='data i/o',
                             doc='',
                             inputs=[  {  'desc': '', 'interface': IStr, 'name': 'package(get_data)', 'value': None},
   {  'desc': '', 'interface': IStr, 'name': 'glob(get_data)', 'value': '*'},
   {  'desc': '',
      'interface': IStr,
      'name': 'filename(get_data)',
      'value': None}],
                             outputs=[  {  'desc': 'A pandas.DataFrame instance which represents the csv file.',
      'interface': None,
      'name': 'dataframe(csv2pandasDataframe)'}],
                             elt_factory={  18: ('openalea.pandas.io', 'read_csv'),
   19: ('openalea.data file', 'get_data')},
                             elt_connections={  34139312: (18, 0, '__out__', 0),
   34139336: ('__in__', 0, 19, 0),
   34139360: (19, 0, 18, 0),
   34139384: ('__in__', 1, 19, 1),
   34139408: ('__in__', 2, 19, 2)},
                             elt_data={  18: {  'block': False,
          'caption': 'read_csv',
          'delay': 0,
          'hide': True,
          'id': 18,
          'lazy': True,
          'port_hide_changed': set(),
          'posx': 517.8162138584012,
          'posy': 21.302565759997524,
          'priority': 0,
          'use_user_color': False,
          'user_application': None,
          'user_color': None},
   19: {  'block': False,
          'caption': 'get_data',
          'delay': 0,
          'factory': '<openalea.core.node.NodeFactory object at 0x3dc71d0> : "get_data"',
          'hide': True,
          'id': 19,
          'lazy': True,
          'port_hide_changed': set(),
          'posx': 509.64542300600647,
          'posy': -31.791839043245815,
          'priority': 0,
          'use_user_color': False,
          'user_application': None,
          'user_color': None},
   '__in__': {  'block': False,
                'caption': 'In',
                'delay': 0,
                'hide': True,
                'id': 0,
                'lazy': True,
                'port_hide_changed': set(),
                'posx': 562.8488883496688,
                'posy': -184.5714957876693,
                'priority': 0,
                'use_user_color': False,
                'user_application': None,
                'user_color': None},
   '__out__': {  'block': False,
                 'caption': 'Out',
                 'delay': 0,
                 'hide': True,
                 'id': 1,
                 'lazy': True,
                 'port_hide_changed': set(),
                 'posx': 564.128380578765,
                 'posy': 132.82221022550735,
                 'priority': 0,
                 'use_user_color': False,
                 'user_application': None,
                 'user_color': None}},
                             elt_value={  18: [  (1, "','"),
          (2, '0'),
          (3, 'None'),
          (4, 'None'),
          (5, 'None'),
          (6, 'None'),
          (7, 'False'),
          (8, 'None'),
          (9, 'None'),
          (10, 'False'),
          (11, 'None'),
          (12, '0'),
          (13, 'None'),
          (14, 'False'),
          (15, 'None'),
          (16, 'None')],
   19: [],
   '__in__': [],
   '__out__': []},
                             elt_ad_hoc={  18: {'useUserColor': False, 'position': [517.8162138584012, 21.302565759997524], 'userColor': None},
   19: {'useUserColor': False, 'position': [509.64542300600647, -31.791839043245815], 'userColor': None},
   '__in__': {'useUserColor': False, 'position': [562.8488883496688, -184.5714957876693], 'userColor': None},
   '__out__': {'useUserColor': False, 'position': [564.128380578765, 132.82221022550735], 'userColor': None}},
                             lazy=True,
                             eval_algo='LambdaEvaluation',
                             )




pandasDataframe2data = CompositeNodeFactory(name='pandasDataframe2data',
                             description='Composite node made by grouping openalea.data file.get_data and openalea.pandas.io.to_csv',
                             category='data i/o',
                             doc='',
                             inputs=[  {  'desc': 'The DataFrame to write.',
      'interface': None,
      'name': 'dataframe(pandasDataframe2csv)',
      'value': None},
   {  'desc': '', 'interface': IStr, 'name': 'package(get_data)', 'value': None},
   {  'desc': '', 'interface': IStr, 'name': 'glob(get_data)', 'value': '*'},
   {  'desc': '',
      'interface': IStr,
      'name': 'filename(get_data)',
      'value': None}],
                             outputs=[  {  'desc': 'The file path where the Dataframe is written.',
      'interface': IFileStr,
      'name': 'csv_filepath(pandasDataframe2csv)'}],
                             elt_factory={  8: ('openalea.data file', 'get_data'), 13: ('openalea.pandas.io', 'to_csv')},
                             elt_connections={  34139288: ('__in__', 1, 8, 0),
   34139312: ('__in__', 3, 8, 2),
   34139336: (13, 0, '__out__', 0),
   34139360: (8, 0, 13, 1),
   34139384: ('__in__', 0, 13, 0),
   34139408: ('__in__', 2, 8, 1)},
                             elt_data={  8: {  'block': False,
         'caption': 'get_data',
         'delay': 0,
         'factory': '<openalea.core.node.NodeFactory object at 0x30c8d50> : "get_data"',
         'hide': True,
         'id': 8,
         'lazy': True,
         'port_hide_changed': set(),
         'posx': 371.164776354299,
         'posy': -25.54821877276729,
         'priority': 0,
         'use_user_color': False,
         'user_application': None,
         'user_color': None},
   13: {  'block': False,
          'caption': 'to_csv',
          'delay': 0,
          'hide': True,
          'id': 13,
          'lazy': True,
          'port_hide_changed': set(),
          'posx': 340.56859759893075,
          'posy': 45.5374207712318,
          'priority': 0,
          'use_user_color': False,
          'user_application': None,
          'user_color': None},
   '__in__': {  'block': False,
                'caption': 'In',
                'delay': 0,
                'hide': True,
                'id': 0,
                'lazy': True,
                'port_hide_changed': set(),
                'posx': 423.64033370419804,
                'posy': -300.7760830037442,
                'priority': 0,
                'use_user_color': False,
                'user_application': None,
                'user_color': None},
   '__out__': {  'block': False,
                 'caption': 'Out',
                 'delay': 0,
                 'hide': True,
                 'id': 1,
                 'lazy': True,
                 'port_hide_changed': set(),
                 'posx': 423.64033370419804,
                 'posy': 222.44012208426494,
                 'priority': 0,
                 'use_user_color': False,
                 'user_application': None,
                 'user_color': None}},
                             elt_value={  8: [],
   13: [  (2, "','"),
          (3, "'NA'"),
          (4, 'None'),
          (5, 'True'),
          (6, 'False'),
          (7, 'None'),
          (8, "'w'"),
          (9, 'None'),
          (10, 'None')],
   '__in__': [],
   '__out__': []},
                             elt_ad_hoc={  8: {'useUserColor': False, 'position': [371.164776354299, -25.54821877276729], 'userColor': None},
   13: {'useUserColor': False, 'position': [340.56859759893075, 45.5374207712318], 'userColor': None},
   '__in__': {'useUserColor': False, 'position': [423.64033370419804, -300.7760830037442], 'userColor': None},
   '__out__': {'useUserColor': False, 'position': [423.64033370419804, 222.44012208426494], 'userColor': None}},
                             lazy=True,
                             eval_algo='LambdaEvaluation',
                             )




io_utils_to_csv = Factory(name='to_csv',
                authors='C. Chambon',
                description='Write a pandas.DataFrame into a comma-separated-values (CSV) file. Wrapping of pandas.DataFrame.to_csv.',
                category='data i/o',
                nodemodule='io_utils',
                nodeclass='to_csv',
                inputs=[{'interface': None, 'hide': False, 'name': 'dataframe', 'value': None, 'desc': 'The dataframe to write.'}, {'hide': False, 'name': 'path_or_buf', 'value': None, 'label': 'filepath', 'interface': IFileStr, 'desc': 'File path.'}, {'interface': IStr, 'hide': True, 'name': 'sep', 'value': ',', 'desc': 'Field delimiter for the output file.'}, {'interface': IStr, 'hide': False, 'name': 'na_rep', 'value': '', 'desc': 'Missing data representation.'}, {'interface': ISequence, 'hide': True, 'name': 'cols', 'value': None, 'desc': 'Columns to write.'}, {'interface': IBool, 'hide': True, 'name': 'header', 'value': True, 'desc': 'Write out column names.'}, {'interface': IBool, 'hide': False, 'name': 'index', 'value': True, 'desc': 'Write row names (index).'}, {'interface': IInterface, 'hide': True, 'name': 'index_label', 'value': None, 'desc': 'Can be either a string or a sequence of strings. If a string is given, then the string is the column label for index column(s) if desired. If None is given, and `header` and `index` are True, then the index names are used. A sequence should be given if the DataFrame uses MultiIndex.'}, {'interface': IStr, 'hide': True, 'name': 'mode', 'value': 'w', 'desc': 'Python write mode.'}, {'interface': IStr, 'hide': True, 'name': 'nanRep', 'value': None, 'desc': 'A string representation of a missing value.'}, {'interface': IStr, 'hide': True, 'name': 'encoding', 'value': None, 'desc': 'A string representing the encoding to use if the contents are non-ascii, for python versions prior to 3.'}],
                outputs=[{'interface': IFileStr, 'name': 'filepath', 'desc': 'The path of the CSV file.'}],
                widgetmodule=None,
                widgetclass=None,
               )




io_utils_read_csv = Factory(name='read_csv',
                authors='C. Chambon',
                description='Read a CSV (comma-separated-values) file into a pandas.DataFrame. Wrapping of pandas.read_csv.',
                category='data i/o',
                nodemodule='io_utils',
                nodeclass='read_csv',
                inputs=[{'hide': False, 'name': 'filepath_or_buffer', 'value': None, 'label': 'filepath', 'interface': IFileStr, 'desc': 'The path of the CSV file to read.'}, {'interface': IStr, 'hide': True, 'name': 'sep', 'value': ',', 'desc': 'Delimiter to use. If sep is None, will try to automatically determine this.'}, {'interface': IInt, 'hide': True, 'name': 'header', 'value': 0, 'desc': 'Row to use for the column labels of the parsed DataFrame.'}, {'interface': IInterface, 'hide': True, 'name': 'index_col', 'value': None, 'desc': 'Can be either an integer or a sequence. If an integer is given, then it represents the index of the column to use as the row labels of the DataFrame. If a sequence is given, then a MultiIndex is used.'}, {'interface': ISequence, 'hide': True, 'name': 'names', 'value': None, 'desc': ' List of column names.'}, {'interface': IInterface, 'hide': True, 'name': 'skiprows', 'value': None, 'desc': 'Can be either an integer or a sequence of integers. If an integer is given, then it represents the number of rows to skip. If a sequence is given, then it represents the row numbers to skip (0-indexed).'}, {'interface': IInterface, 'hide': True, 'name': 'na_values', 'value': None, 'desc': 'Additional strings to recognize as NA/NaN. Can be either a sequence or a dict. If dict passed, specific per-column NA values.'}, {'interface': IBool, 'hide': True, 'name': 'parse_dates', 'value': False, 'desc': 'Attempt to parse dates in the index column(s).'}, {'interface': IInterface, 'hide': True, 'name': 'date_parser', 'value': None, 'desc': 'Function to use for converting dates to strings. If None, defaults to dateutil.parser.'}, {'interface': IInt, 'hide': True, 'name': 'nrows', 'value': None, 'desc': 'Number of rows of file to read. Useful for reading pieces of large files.'}, {'interface': IBool, 'hide': True, 'name': 'iterator', 'value': False, 'desc': 'Return TextParser object.'}, {'interface': IInt, 'hide': True, 'name': 'chunksize', 'value': None, 'desc': 'Return TextParser object for iteration.'}, {'interface': IInt, 'hide': True, 'name': 'skip_footer', 'value': 0, 'desc': 'Number of line at bottom of file to skip.'}, {'interface': IDict, 'hide': True, 'name': 'converters', 'value': None, 'desc': 'Dict of functions for converting values in certain columns. Keys can either be integers or column labels.'}, {'interface': IBool, 'hide': True, 'name': 'verbose', 'value': False, 'desc': 'Indicate number of NA values placed in non-numeric columns.'}, {'interface': IStr, 'hide': True, 'name': 'delimiter', 'value': None, 'desc': 'Alternative argument name for sep.'}, {'interface': IStr, 'hide': True, 'name': 'encoding', 'value': None, 'desc': 'Encoding to use for UTF when reading/writing (ex. "utf-8").'}],
                outputs=[{'interface': IInterface, 'name': 'dataframe', 'desc': 'The dataframe created from the CSV file.'}],
                widgetmodule=None,
                widgetclass=None,
               )



