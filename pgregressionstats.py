'''
Description
To adapt Brian T's regressions stats code
to our new plotting interface, we revise
his _NeStatsHelper funcion to deliver a Table
string that we can write to a GUI object.
'''
from __future__ import division
from __future__ import print_function
#created by Brian Trethewey
#
#neGrapher is primary interface for graphing data
#neStats is primary interface for creating statistics output file for a dataset

from future import standard_library
standard_library.install_aliases()
from builtins import object
from past.utils import old_div

__filename__ = "pgregressionstats.py"
__date__ = "20171016"
__author__ = "Ted Cosart<ted.cosart@umontana.edu>"

import os

from numpy import mean, median, isnan

from Viz.LineRegress import slopeConfidence

from pgneestimationtablefilemanager import NeEstimationTableFileManager

class PGRegressionStats( object ):

	def __init__( self, 
					dltup_table=None,
					f_confidence_alpha=0.05,
					v_significant_value=0 ):

		self.__data_table=dltup_table
		self.__confidence_alpha=f_confidence_alpha
		self.__significant_value=v_significant_value
		return
	#end __init__

	def __get_source_file_name_from_file_manager_key( self, s_field_values ):
		'''
		This def assumes that the first field,
		as delimited by the concatenated field 
		values delivered by the NeEstimationTableFileManager,
		def getDictDataLinesKeyedToColnames,
		(currently double underscore, __), will be 
		the source genepop file name, full path, which we
		reduce to file name only.
		'''
	
		IDX_FILE_NAME=0

		FIELDDELIM=NeEstimationTableFileManager.DELIM_GROUPED_FIELD_NAMES

		ls_values=s_field_values.split( FIELDDELIM )
		
		s_file_with_path=ls_values[ IDX_FILE_NAME ]	

		s_file_name=os.path.basename( s_file_with_path )

		return s_file_name
	#end __get_source_file_name_from_file_manager_key

	def __data_is_sufficient_for_regression(self):
		b_return_value=False
		if self.__data_table is not None:
			if len( self.__data_table ) > 0:
				b_all_lines_have_sufficient_data=True
				for s_key in self.__data_table:
					if len( self.__data_table[ s_key ] ) < 2:
						b_all_lines_have_sufficient_data=False
						break
					#end if length under two
				#end for each key
				if b_all_lines_have_sufficient_data==True:
					b_return_value=True
				#end if all lines had enough data
			#end there is at least one line
		#end if there is a data table

		return b_return_value
	#end __data_is_sufficient_for_regression
		
	def __get_stats_as_string( self, b_use_file_name_only_for_column_1=True ):
		'''
		Most of this code is copied directly from Brian's
		def in Viz.LineRegress._neStatsHelper.
		'''
		PRECISION=3
		STATS_TABLE_DELIM="\t"
		BULLET=u'\u2022'
		BULLET_INDENTED="    " + BULLET + " "

		s_return=None

		b_data_is_sufficient=self.__data_is_sufficient_for_regression()

		if b_data_is_sufficient:
			table=self.__data_table
			#tableFormat = "{:<30}{:<30}{:<50}{:<80}\n"
			confPercent = (1.0 - self.__confidence_alpha)*100.0
			tableString="-----Table of per-line values-----\n"
			tableString+=STATS_TABLE_DELIM.join( [ "Source",
													"Slope",
													"Intercept" ,
													"CI("+str(confPercent)+"%)", 
													"\n" ] )
			slopeVctr = []
			confidenceVctr = []

			Uncountable = 0
			ls_keys_sorted=sorted( list(table.keys()) )
			for recordKey in ls_keys_sorted:

				record = table[recordKey]

				s_file_name=recordKey
				
				if b_use_file_name_only_for_column_1:
					s_file_name=self.__get_source_file_name_from_file_manager_key( recordKey )
				#end if not b_use_all_key_fields
				
				v_return_slope_conf=slopeConfidence( self.__confidence_alpha,record)
				slope=None; intercept=None; confidence=None
				ls_vals_for_table=None

				if type( v_return_slope_conf ) == tuple:
					#We assume we got numbers if a tuple was returned.
					slope, intercept, confidence  = v_return_slope_conf 
					 
					'''
					Note that the "float" cast was need (at least in py3 ), 
					else negative numbers don't get rounded.
					'''
					s_rounded_confidence=STATS_TABLE_DELIM.join( \
							[ str( round( float( v_val ) , PRECISION ) ) \
													for v_val in confidence ] )
					ls_vals_for_table=[ s_file_name,
											str( round( slope, PRECISION ) ),  
											str( round( intercept, PRECISION ) ) ,  
											s_rounded_confidence, 
											"\n" ]
					if isnan(slope):
						Uncountable +=1
					else:
						slopeVctr.append(slope) 
						confidenceVctr.append(confidence)
					#end if isnan

				else:

					ls_vals_for_table=[ s_file_name, "NA", "NA", "NA", "\n" ]
				#end if slopeConf returned a tuple or couldn't compute
				
				tableString+=STATS_TABLE_DELIM.join( ls_vals_for_table )
				
			#end for each recordKey

			maxSlope = max(slopeVctr)
			minSlope = min(slopeVctr)
			meanSlope = mean(slopeVctr)
			medSlope = median(slopeVctr)

			negativeCount=0
			zeroCount=0
			positiveCount=0

			for cI in confidenceVctr:
				if cI[0]>self.__significant_value:
					positiveCount+=1
				elif cI[1]<self.__significant_value:
					negativeCount+=1
				else:
					zeroCount+=1
			#end for each cI
			
			s_stats_string = "Max Regression Slope: "+str( round( maxSlope, PRECISION ) )+"\n"
			s_stats_string +="Min Regression Slope: "+str( round( minSlope, PRECISION ) )+"\n"
			s_stats_string +="Mean Regression Slope: " +str( round( meanSlope, PRECISION ) )+"\n"
			s_stats_string +="Median Regression Slope: "+str( round( medSlope, PRECISION ) )+"\n"
			s_stats_string +="\n"
			s_stats_string +="Comparison to a slope of "+str( round( self.__significant_value, PRECISION ) ) \
					+ " at alpha =  " \
					+ str( round( self.__confidence_alpha, PRECISION ) )+"\n"
			s_stats_string +=BULLET_INDENTED \
							+ "Positive Slopes: "+str( round( positiveCount, PRECISION ) )\
							+ "\n" +  BULLET_INDENTED \
							+ "Neutral Slopes: "+str( round( zeroCount, PRECISION ) ) \
							+ "\n" + BULLET_INDENTED \
							+ "Negative Slopes: "+str( round( negativeCount, PRECISION ) ) \
							+ "\n" + BULLET_INDENTED \
							+ "Non-Number Slopes: "+str( round( Uncountable, PRECISION ) )
			s_stats_string +="\n\n"
			s_stats_string +=tableString

			s_return=s_stats_string
		else:
			s_return= "Insufficient data."
		#end if our table has sufficient data else not 

		return s_return
	#end __get_stats_as_string

	def setTsvFileManagerDictAsTable( self, 
						dls_dict_of_xy_lists_by_line_name ):
		'''
		This def was added in order for clients to
		pass in the dictionary associated
		with the NeEstimationTableFileManager objects
		getDictDataLinesKeyedToColnames, to convert
		it to the correct format and then set the 
		table attribute, self.__data_table.
		'''

		'''
		Helper inner-def:
		'''
		DELIMITER=NeEstimationTableFileManager.DELIM_TABLE
		def convert_to_duple_numeric_pair( s_xy_val_string ):

			ls_vals=s_xy_val_string.split( DELIMITER )
			v_x=float( ls_vals[0] )
			v_y=float( ls_vals[1] )

			return ( v_x, v_y ) 

		#end convert_to_duple_numeric_pair

		dltup_data_converted_for_regression={}	

		for s_line_name in dls_dict_of_xy_lists_by_line_name:
			ls_xy_strings=dls_dict_of_xy_lists_by_line_name[ s_line_name ]
			ls_xy_tuples=[ convert_to_duple_numeric_pair( s_xy ) \
											for s_xy in ls_xy_strings ]
			dltup_data_converted_for_regression[ s_line_name ]=ls_xy_tuples
		#end for each line name
		
		self.__data_table=dltup_data_converted_for_regression
		return
	#end convertDataFromTsvDictAndRegress

	def getStatsTableAsString( self, b_use_file_name_only_for_column_1=True ):
		s_table="No data available"
		if self.__data_table is not None:
			s_table=self.__get_stats_as_string( b_use_file_name_only_for_column_1 )
		#end if we have table data
		return s_table
	#end getStatsTableAsString

#end class PGRegressionStats

if __name__ == "__main__":
	pass
#end if main

