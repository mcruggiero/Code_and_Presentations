// Databricks notebook source
// MAGIC %md
// MAGIC # Pipelines and Cross Validation

// COMMAND ----------

import org.apache.spark.ml.classification.LogisticRegression
import org.apache.spark.ml.evaluation.MulticlassClassificationEvaluator

// Features
import org.apache.spark.ml.feature.{VectorAssembler, StringIndexer, Tokenizer, StopWordsRemover, CountVectorizer}

import org.apache.spark.ml.Pipeline
import org.apache.spark.ml.tuning.{CrossValidator, ParamGridBuilder}

// COMMAND ----------

// MAGIC %md
// MAGIC ## Loading the DataFrame
// MAGIC 
// MAGIC The csv for our classification model will be the [SMSSpamCollection](https://archive.ics.uci.edu/ml/datasets/sms+spam+collection) dataset from the UCI repository. After you've uploaded the csv into DataBricks, use the cell below to load it into a Spark DataFrame. 
// MAGIC 
// MAGIC Our goal is to predict whether or not a given text message is spam or ham.
// MAGIC 
// MAGIC NOTE: `SMSSpamCollection` is a tab separated file. There's a delimiter option we'll need to set.

// COMMAND ----------

var df = sqlContext
  .read
  .format("csv")
  .option("inferSchema", "true")
  .option("delimiter", "\t")
  .load("/FileStore/tables/SMSSpamCollection")

// COMMAND ----------

// MAGIC %md 
// MAGIC # Creating the `label` column.
// MAGIC 
// MAGIC We'll need to use `StringIndexer` to encode our labels (`_c0`).
// MAGIC 
// MAGIC Recall from the previous lecture how we instantiate a `StringIndexer`:
// MAGIC ```scala
// MAGIC var indexer = new StringIndexer()
// MAGIC   .setInputCol("theInputCol")
// MAGIC   .setOutputCol("theOutputCol")```
// MAGIC   
// MAGIC The key difference for this lecture is **we won't transform our DataFrame**...yet. That will happen in the `Pipeline`.
// MAGIC 
// MAGIC In the cell below, create the indexer.

// COMMAND ----------

var labelIndexer = new StringIndexer()
  .setInputCol("_c0")
  .setOutputCol("label")

// COMMAND ----------

// MAGIC %md
// MAGIC 
// MAGIC # NLP transformers
// MAGIC 
// MAGIC The `CountVectorizer` in `sklearn` included everything but the kitchen sink. In Spark, you have to use several classes to accomplish the same job. We'll create instances of the following transformers:
// MAGIC 
// MAGIC 
// MAGIC - `Tokenizer`: Splits our SMS messages into tokens
// MAGIC - `StopWordsRemover`: Removes all stopwords from the tokens column (created by the `Tokenizer`)
// MAGIC - `CountVectorizer`: Creates our document-term matrix. The output from `StopWordsRemover` will be fed into the vectorizer.

// COMMAND ----------

// Tokenizer
var tokenizer = new Tokenizer()
  .setInputCol("_c1")
  .setOutputCol("tokens")

// COMMAND ----------

// StopWordsRemover
var remover = new StopWordsRemover()
  .setInputCol(tokenizer.getOutputCol)
  .setOutputCol("tokensWithoutStopWords")

// COMMAND ----------

// CountVectorizer
var vectorizer = new CountVectorizer()
  .setInputCol(remover.getOutputCol)
  .set
  .setOutputCol("DTM")

// COMMAND ----------

// MAGIC %md
// MAGIC 
// MAGIC ## Creating the features column
// MAGIC 
// MAGIC As always, we'll need to create our features column using the [`VectorAssembler`](https://spark.apache.org/docs/latest/ml-features.html#vectorassembler) object like so:
// MAGIC ```scala
// MAGIC var assembler = new VectorAssembler()
// MAGIC   .setInputCols(Array("col1", "col2", ...))
// MAGIC   .setOutputCol("features")```
// MAGIC   
// MAGIC Unlike the previous lecture, **we won't transform our DataFrame**...yet. That will happen in the `Pipeline`.

// COMMAND ----------

var assembler = new VectorAssembler()
  .setInputCols(Array(vectorizer.getOutputCol))
  .setOutputCol("features")

// COMMAND ----------

// MAGIC %md
// MAGIC ## Train/Test Split
// MAGIC 
// MAGIC Split your DataFrame up into training and testing sets using the `.randomSplit()` method:
// MAGIC 
// MAGIC ```scala
// MAGIC var Array(train, test) = df.randomSplit(Array(.8, .2), 42)
// MAGIC ``` 
// MAGIC 
// MAGIC The first parameter (`Array(.8, .2)`) determines what percentage will go into `train` and `test` respectively. The second parameter (`42`) is a random seed.

// COMMAND ----------

df.show(5)

// COMMAND ----------

var Array(train, test) = df.randomSplit(Array(.8,.2), 42)

// COMMAND ----------



// COMMAND ----------

// MAGIC %md
// MAGIC ## Model
// MAGIC 
// MAGIC Now we're ready to create our model. MLlib has [several options](https://spark.apache.org/docs/latest/ml-classification-regression.html#classification) to choose from. For this project, we'll use [LogisticRegression](https://spark.apache.org/docs/latest/api/scala/index.html#org.apache.spark.ml.classification.LogisticRegression). 
// MAGIC 
// MAGIC We'll instantiate our model like so:
// MAGIC ```scala
// MAGIC var lr = new LogisticRegression()```

// COMMAND ----------

var lr = new LogisticRegression()

// COMMAND ----------

// MAGIC %md
// MAGIC # Pipeline
// MAGIC 
// MAGIC Now we're ready to create our pipeline using the `Pipeline` object like so:
// MAGIC ```scala
// MAGIC var pipeline = new Pipeline()
// MAGIC   .setStages(Array(transformer1, transformer2, ..., assembler, model))
// MAGIC ```
// MAGIC 
// MAGIC The pipeline object behaves exactly like Spark's models. It had a `.fit()` method which returns a **fitted model** instance, which can be used to make predictions with `.transform()`.
// MAGIC 
// MAGIC **Note**: The order in which you place your objects is the order in which they'll run.

// COMMAND ----------

var pipeline = new Pipeline()
  .setStages(Array(tokenizer, remover, vectorizer, assembler, labelIndexer, lr))

// COMMAND ----------

// MAGIC %md
// MAGIC 
// MAGIC ## Model evaluation
// MAGIC 
// MAGIC Our `CrossValidator` we'll need an instance of `MulticlassClassificationEvaluator`:
// MAGIC ```scala
// MAGIC var evaluator = new MulticlassClassificationEvaluator()```
// MAGIC 
// MAGIC The default metric is F1. To change it to something else, use the `.setMetricName()` method when creating your evaluator:
// MAGIC 
// MAGIC ```scala
// MAGIC var accuracyEvaluator = new MulticlassClassificationEvaluator()
// MAGIC   .setMetricName("accuracy")```
// MAGIC   
// MAGIC   
// MAGIC Create an evaluator the cell below, using accuracy as the metric.

// COMMAND ----------

var evaluator = new MulticlassClassificationEvaluator()
  .setMetricName("accuracy")

// COMMAND ----------

// MAGIC %md 
// MAGIC # Hypertuning parameters
// MAGIC 
// MAGIC In `sklearn` we were able to Grid Search using a simple dictionary of parameters to tune over:
// MAGIC ```python
// MAGIC params = {
// MAGIC   'foo': ['option1', 'option2', 'option3'],
// MAGIC   'bar': ['option1', 'option2', 'option3']
// MAGIC }```
// MAGIC 
// MAGIC In Spark, we have to use `ParamGridBuilder` to accomplish the same task:
// MAGIC ```scala
// MAGIC var paramGrid = new ParamGridBuilder()
// MAGIC   .addGrid(vectorizer.vocabSize, Array(3000, 4000))
// MAGIC   .addGrid(vectorizer.binary, Array(true, false))
// MAGIC   .build()
// MAGIC ```
// MAGIC 
// MAGIC Each option is set with `.addGrid()`, which takes the parameter to be tuned over, along with the `Array` of options. You'll then call `.build()` once you're done adding params.

// COMMAND ----------

var params = new ParamGridBuilder()
  .addGrid(vectorizer.binary, Array(true, false))
  .addGrid(vectorizer.vocabSize, Array(2000,3000,10000))
  .build()

// COMMAND ----------

// MAGIC %md
// MAGIC # Cross Validation
// MAGIC 
// MAGIC Now we're ready to create our `CrossValidator` (Spark's equivalent of `GridSearchCV`). Your cv will require three params:
// MAGIC 1. The model (in our case it's the `pipeline`)
// MAGIC 2. The param grid
// MAGIC 3. The evaluator
// MAGIC 
// MAGIC ```scala
// MAGIC var cv = new CrossValidator()
// MAGIC   .setEstimator(pipeline)
// MAGIC   .setEstimatorParamMaps(paramGrid)
// MAGIC   .setEvaluator(evaluator)```

// COMMAND ----------

var cv = new CrossValidator() // Same as GridSearchCV
  .setEstimator(pipeline)
  .setEvaluator(evaluator)
  .setEstimatorParamMaps(params)

// COMMAND ----------

// MAGIC %md
// MAGIC ## Model fitting
// MAGIC 
// MAGIC When we fit our `CrossValidator` (`cv.fit(train)`), it actually returns a whole different object: a `CrossValidatorModel`. This is different than `sklearn`, which merely mutates our original instance. As a result, we'll need to save our newly fitted model as a variable:
// MAGIC 
// MAGIC ```scala
// MAGIC var cvModel = cv.fit(train)```
// MAGIC 
// MAGIC The convention in Spark is to use `Model` in the name when it's fitted.

// COMMAND ----------

var cvModel = cv.fit(train)

// COMMAND ----------

// MAGIC %md
// MAGIC ## Making predictions
// MAGIC 
// MAGIC Now that we have a fitted model, we're ready to make some predictions (`cvModel.transform(test)`). This will return a new DataFrame, with a `prediction` column appended to the end.

// COMMAND ----------

var predictions = cvModel.transform(test)

// COMMAND ----------

// MAGIC %md
// MAGIC 
// MAGIC ## Model evaluation
// MAGIC 
// MAGIC Use your evaluator to score the test set below

// COMMAND ----------

evaluator.evaluate(predictions)

// COMMAND ----------

cvModel.avgMetrics

// COMMAND ----------

var bestScore = cvModel.avgMetrics.max
var i = cvModel.avgMetrics.indexOf(bestScore)

// COMMAND ----------

cvModel.getEstimatorParamMaps(i)

// COMMAND ----------

cvModel.getEstimator.
