'''
Description
manages output of the PGOpSimuPop object
based on Tiago Anteo's code in sim.py
'''
__filename__ = "pgoutputsimupop.py"
__date__ = "20160327"
__author__ = "Ted Cosart<ted.cosart@umontana.edu>"


import os
import shutil
import bz2

FILE_DOES_NOT_EXIST=0
FILE_EXISTS_UNCOMPRESSED=1
FILE_EXISTS_AS_BZ2=2
FILE_EXISTS_AS_BOTH_UNCOMPRESSED_AND_BZ2=3

GENEPOP_FILE_EXTENSION="genepop"

class PGOutputSimuPop( object ):
	'''
	Object meant to fetch parameter values and prepare them for 
	use in a simuPop simulation.  

	Object to be passed to a PGOpSimuPop object, which is, in turn,
	passed to a PGGuiSimuPop object, so that the widgets can then access
	defs in this input object, in order to, for example, show or allow
	changes in parameter values for users before they run the simulation.
	'''

	def __init__( self, s_output_files_prefix ):

		self.__basename=s_output_files_prefix

		self.__set_file_names()

		self.out=None
		self.err=None
		self.megaDB=None
		self.conf=None

		return
	#end def __init__
	
	def __set_file_names( self ):

		s_output_files_prefix=self.__basename

		self.__outname=s_output_files_prefix + ".sim"
		self.__errname=s_output_files_prefix + ".gen"
		self.__megadbname=s_output_files_prefix + ".db"
		self.__confname=s_output_files_prefix + ".conf"
		self.__genfile=self.__errname
		self.__simfile=self.__outname
		self.__dbfile=self.__megadbname
		self.__conffile=self.__confname

		return
	#end __set_file_names
	
	
	def __delete_file_names( self ):

		del self.__outname
		del self.__errname
		del self.__megadbname
		del self.__confname

		return
	#end __set_file_names
	
	def __file_exists(self, s_name):

		b_uncompressed_exists=os.path.isfile( s_name )
		b_compressed_exists=os.path.isfile( s_name + ".bz2" )


		if b_uncompressed_exists:
			if b_compressed_exists:
				return FILE_EXISTS_AS_BOTH_UNCOMPRESSED_AND_BZ2
			else:
				return FILE_EXISTS_UNCOMPRESSED
			#end if compressed else not
		else:
			if b_compressed_exists:
				return FILE_EXISTS_AS_BZ2
			else:
				return FILE_DOES_NOT_EXIST
			#end if b_compressed_exists
		#end if uncompressed else no uncompressed
		return b_exists
	#end __file_exists

	def __raise_file_exists_error( self, s_name, s_message=None ):
		#the likely problem is a simupop output file contained
		#in this object already exists:
		if s_message is None:
			s_message="In " + self.__mytype() + " instance, can't open file " \
				+ " for writing.  File, or its compressed version, " \
				+ s_name + ".bz2, " + " exists." 
		#end if default message
		raise Exception ( "In  " + self.__mytype() + " instance, file, " \
					+ s_name + " already exists.  " \
					+  "Failed operation: " + s_message )
	#end __raise_file_exists_error

	def __raise_file_not_found_error( self, s_name, s_failed_op ):
		raise Exception ( "In  " + self.__mytype() + " instance, file, " \
				+ s_name + " not found: caused failed operation: " \
				+ s_failed_op )
	#end __raise_file_not_found_error

	def openOut(self):
		if self.__file_exists( self.__outname ):
			self.__raise_file_exists_error( self.__outname )
		else:
			self.out=open( self.__outname, 'w' )
		#end if file exists, else open
	#end openOut

	def openErr(self):
		if self.__file_exists( self.__errname ):
			self.__raise_file_exists_error( self.__errname )
		else:
			self.err=open( self.__errname, 'w' )
		#end if file exists, else open
	#end openErr

	def openMegaDB(self):
		if self.__file_exists( self.__megadbname ):
			self.__raise_file_exists_error( self.__megadbname )
		else:
			self.megaDB=open( self.__megadbname, 'w' )
		#end if file exists, else open
	#end openMegaDB
	
	def copyMe( self ):
		o_copy=PGOutputSimuPop( self.__basename )
		return o_copy
	#end copyMe

	def openConf(self):
		if self.__file_exists( self.__confname ):
			self.__raise_file_not_found_error( self.__confname )
		else:
			self.conf=open( self.__confname, 'w' )
		#end if file exists, else open
	#end openConf

	def bz2CompressAllFiles(self):
		'''
		used code and advice in, 
		http://stackoverflow.com/questions/9518705/big-file-compression-with-python

		Note: checked the shutil documentation at https://docs.python.org/2/library/shutil.html
		which warns of loss of meta file info (owner/group ACLs) when using shutil.copy() or shutil.copy2().  Unclear
		whether this applies to the copyfileobj, though my few tests showd all of these were retained.
		'''
		for s_myfile in [ self.__outname, self.__errname, self.__megadbname, self.__confname ]:
			if not self.__file_exists( s_myfile ):
				self.__raise_file_not_found_error( s_myfile, "compress file with bz2"  )
			else:
				with open( s_myfile, 'rb' ) as o_input:
					with bz2.BZ2File( s_myfile + '.bz2', 'wb', compresslevel=9 ) as o_output:
						#try/except overkill, but want logic to show
						#we don't remove the input file
						#if the copy op fails:
						try: 
							shutil.copyfileobj( o_input, o_output )
						except Exception,  e:
							raise e
						#end try except
						os.remove( s_myfile )	
					#end with bzfile for writing
				#end with current file for reading
			#end if file absent, else exists
		#end for each file
	#end bz2CompressAllFiles

	#derived from Tiao's code in ne2.py:
	def gen2Genepop( self, idx_allele_start, idx_allele_stop, 
			b_do_compress=True, 
			b_pop_per_gen=False ):

		'''
		reads the *.gen file from the simuPop output
		and produces a genepop file based on the gen file

		param idx_allele_start: int, one-based index giving the
		item (loci) number of the first allele entry in the line of gen-file input
		Example, if the *gen file has 10 microsates and 40 SNPs, then its first
		10 allele entries (that follow the indiv number and the gneration number)
		will be the microsats, and the final 40 allele entries will be the SNPs
		If we wanted only the Microsats to be included in the gen file, then
		this param would be "1", and the idx_allele_stop value would be 10. 
		If we want both msats and snps, we'd give 1 and 50 for these params. 
		If we want only SNPs, wed enter 11 for start allele and 50 for stop.

		param idx_allele_stop: int, one-based index giving the
		item (loci) number of the last allele entry in the line of gen-file input

		param optional b_do_compress, if true, will bzip2 the output genepop file

		param optional b_pop_per_gen, if true, will insert a "Pop" line between the
		generations, as given by the 2nd field in the gen file
		'''

		o_genfile=None
		o_genepopfile=None
		s_genepop_filename=self.__genfile + "." + GENEPOP_FILE_EXTENSION 
		i_num_loci=(idx_allele_stop-idx_allele_start) + 1

		IDX_GEN_INDIV=0
		IDX_GEN_GENERATION=1
		IDX_FIRST_ALLELE=2

		i_genepop_already_exists=self.__file_exists( s_genepop_filename )

		if i_genepop_already_exists != FILE_DOES_NOT_EXIST:

			self.__raise_file_exists_error( s_genepop_filename, 
					"create genepop file from gen file" )
		#end if genepop file already exists

		i_genfile_exists=self.__file_exists( self.__genfile )
		
		#if we have the uncompressed version available
		#we use it:
		if i_genfile_exists == FILE_EXISTS_UNCOMPRESSED \
			or i_genfile_exists == FILE_EXISTS_AS_BOTH_UNCOMPRESSED_AND_BZ2:

			o_genfile=open( self.__genfile )

		elif i_genfile_exists == FILE_EXISTS_AS_BZ2:

			o_genfile=bz2.BZ2File( self.__genfile + ".bz2" )

		else:
			self.__raise_file_not_found_error( self.__genfile, "convert gen file to genepop" )
		#end if uncompressed only or uncomp. and compressed, else compressed only, else no file
		
		if b_do_compress == True:
			o_genepopfile=bz2.BZ2File( s_genepop_filename + '.bz2', 'wb', compresslevel=9 ) 
		else:
			o_genepopfile=open( s_genepop_filename, 'w' )
		#end if compress else don't

		#write header and loci list:

		o_genepopfile.write( "genepop from simupop run data file " \
				+ self.__genfile + "\n" )

		for i_locus in range( i_num_loci ):
		    o_genepopfile.write("l" + str(i_locus) + "\n" )
		#end for each loci number

		#write indiv id and alleles, line by line:
		i_currgen=None

		for s_line in o_genfile:
		    
			ls_line = s_line.rstrip().split(" ")

			i_id = int(float(ls_line[IDX_GEN_INDIV]))
			i_gen = int(float(ls_line[IDX_GEN_GENERATION]))
			idx_first_allele_in_line=( idx_allele_start + IDX_FIRST_ALLELE ) - 1
			idx_last_allele_in_line=( idx_allele_stop  + IDX_FIRST_ALLELE ) - 1 
			ls_alleles = ls_line[ idx_first_allele_in_line : idx_last_allele_in_line + 1 ]

			if i_currgen is None or ( b_pop_per_gen == True and i_currgen != i_gen ):
				    o_genepopfile.write( "pop\n" )
				    i_currgen=i_gen
			    #end if new generation (== new population )
		    	#end if we should make a new population for each generation

			o_genepopfile.write( str( i_id ) + "," +  " ".join( ls_alleles ) + "\n"  )

		#end for each line in gen file

		o_genfile.close()
		o_genepopfile.close()

		return
	#end gen2Popgene

	@property
	def basename( self ):
		return self.__basename
	#end getter basename

	@basename.setter
	def basename( self, s_basename ):
		self.__basename=s_basename
		self.__set_file_names()
		return
	#end setter basename

	def __mytype( self ):
		return ( type( self ).__name__ )
	#end __mytype
#end class
