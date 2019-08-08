from pyspark.sql.types import *
from optimus import Optimus
from optimus.helpers.json import json_enconding 
from pyspark.ml.linalg import Vectors, VectorUDT, DenseVector
import numpy as np
nan = np.nan
import datetime
from pyspark.sql import functions as F
from optimus.ml import feature as fe
op = Optimus(master='local')
source_df=op.create.df([('id', LongType(), True),('hour', LongType(), True),('mobile', DoubleType(), True),('user_features', VectorUDT(), True),('clicked', DoubleType(), True)], [(0, 18, 1.0, DenseVector([0.0, 10.0, 0.5]), 1.0)])
class Testdf_ml_2(object):
	@staticmethod
	def test_normalizer():
		actual_df =fe.normalizer(source_df,input_cols=['features'],p=2.0)
		expected_df = op.create.df([('id', LongType(), True),('x', LongType(), True),('y', LongType(), True),('features', VectorUDT(), True),('features***NORMALIZED', VectorUDT(), True)], [(0, 1, 2, DenseVector([1.0, 0.5, -1.0]), DenseVector([0.6667, 0.3333, -0.6667])), (1, 2, 3, DenseVector([2.0, 1.0, 1.0]), DenseVector([0.8165, 0.4082, 0.4082])), (2, 3, 4, DenseVector([4.0, 10.0, 2.0]), DenseVector([0.3651, 0.9129, 0.1826]))])
		assert (expected_df.collect() == actual_df.collect())
	@staticmethod
	def test_one_hot_encoder():
		actual_df =fe.one_hot_encoder(source_df,input_cols=['id'])
		expected_df = op.create.df([('id', LongType(), True),('x', LongType(), True),('y', LongType(), True),('features', VectorUDT(), True),('id***ONE_HOT_ENCODER', VectorUDT(), True)], [(0, 1, 2, DenseVector([1.0, 0.5, -1.0]), SparseVector(2, {0: 1.0})), (1, 2, 3, DenseVector([2.0, 1.0, 1.0]), SparseVector(2, {1: 1.0})), (2, 3, 4, DenseVector([4.0, 10.0, 2.0]), SparseVector(2, {}))])
		assert (expected_df.collect() == actual_df.collect())
	@staticmethod
	def test_vector_assembler():
		actual_df =fe.vector_assembler(source_df,input_cols=['id', 'x', 'y'])
		expected_df = op.create.df([('id', LongType(), True),('x', LongType(), True),('y', LongType(), True),('features', VectorUDT(), True),('id_x_y***_VECTOR_ASSEMBLER', VectorUDT(), True)], [(0, 1, 2, DenseVector([1.0, 0.5, -1.0]), DenseVector([0.0, 1.0, 2.0])), (1, 2, 3, DenseVector([2.0, 1.0, 1.0]), DenseVector([1.0, 2.0, 3.0])), (2, 3, 4, DenseVector([4.0, 10.0, 2.0]), DenseVector([2.0, 3.0, 4.0]))])
		assert (expected_df.collect() == actual_df.collect())