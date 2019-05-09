// Databricks notebook source
// MAGIC %md
// MAGIC # Machine Learning in Scala
// MAGIC 
// MAGIC Two models (regression and classification) using Spark's MLlib library.

// COMMAND ----------

// MAGIC %md
// MAGIC # Model 1

// COMMAND ----------

//Models used
import org.apache.spark.ml.regression.{RandomForestRegressionModel, RandomForestRegressor}
import org.apache.spark.ml.classification.RandomForestClassifier

//Evaluators
import org.apache.spark.ml.evaluation.{RegressionEvaluator, MulticlassClassificationEvaluator}

// Feature transformers
import org.apache.spark.ml.feature.{VectorAssembler, StringIndexer}

// COMMAND ----------

// MAGIC %md
// MAGIC ## Regression
// MAGIC 
// MAGIC The dataset for this regression model will be the [Advertising.csv](http://www-bcf.usc.edu/~gareth/ISL/data.html) file from the ISLR website. 
// MAGIC 
// MAGIC Our goal is to predict `sales` using `TV`, `newspaper` and `radio` as features.

// COMMAND ----------

var df = sqlContext
  .read
  .format("csv")
  .option("header", "true")
  .option("inferSchema", "true")
  .load("/FileStore/tables/Advertising.csv")

// COMMAND ----------

// MAGIC %md
// MAGIC 
// MAGIC ## Create label column
// MAGIC 
// MAGIC To prepare our dataset, we must create two columns: `features` and `label`. We'll create the `features` column shortly, but first, let's rename `sales` to `label` in the cell below.

// COMMAND ----------

display(df)

// COMMAND ----------

// MAGIC %md
// MAGIC 
// MAGIC ## Creating the features column
// MAGIC 
// MAGIC As mentioned earlier, we'll need to create a `features` column in order for our Spark model to work. Each row in `features` will be an array of numerical features. To accomplish this, we'll instantiate a [`VectorAssembler`](https://spark.apache.org/docs/latest/ml-features.html#vectorassembler) object like so:
// MAGIC ```scala
// MAGIC var assembler = new VectorAssembler()
// MAGIC   .setInputCols(Array("col1", "col2", ...))
// MAGIC   .setOutputCol("features")```
// MAGIC   
// MAGIC Note that options in Spark are typically set with methods, as opposed to `sklearn`, which uses parameters.
// MAGIC   
// MAGIC Once our `assembler` is created, we can use it to transform our DataFrame like so:
// MAGIC ```scala
// MAGIC assembler.transform(df)```
// MAGIC 
// MAGIC This will return a new DataFrame object, which we'll need to save to a variable.

// COMMAND ----------

df  = df.withColumnRenamed("sales","label")

// COMMAND ----------

display(df)

// COMMAND ----------

var assembler = new VectorAssembler()
  .setInputCols(Array("TV", "radio", "newspaper"))
  .setOutputCol("features")

// COMMAND ----------

// MAGIC %md
// MAGIC ## Train/Test Split
// MAGIC 
// MAGIC Now that our DataFrame is ready for modeling we'll split it up into training and testing sets using the `.randomSplit()` method:
// MAGIC 
// MAGIC ```scala
// MAGIC var Array(train, test) = df.randomSplit(Array(.8, .2), 42)
// MAGIC ``` 
// MAGIC 
// MAGIC The first parameter (`Array(.8, .2)`) determines what percentage will go into `train` and `test` respectively. The second parameter (`42`) is a random seed.

// COMMAND ----------

df = assembler.transform(df)

// COMMAND ----------

display(df)

// COMMAND ----------

df.show(5)

// COMMAND ----------

// Train test split
var Array(train,test) = df.randomSplit(Array(.8,.2), 42) // 80-20 split, random state 42

// COMMAND ----------

// MAGIC %md
// MAGIC ## Model 2
// MAGIC 
// MAGIC For this project, we'll use a [Random Forest](https://spark.apache.org/docs/latest/ml-classification-regression.html#random-forest-regression). 
// MAGIC 
// MAGIC First we'll instantiate our model like so:
// MAGIC ```scala
// MAGIC var rf = new RandomForestRegressor()
// MAGIC   .setNumTrees(50)
// MAGIC   .setMaxDepth(3)```
// MAGIC   
// MAGIC Notice again that parameters are set with methods, similar to our `VectorAssembler` object. Check the [docs](https://spark.apache.org/docs/latest/api/scala/index.html#org.apache.spark.ml.regression.RandomForestRegressor) for other hyperparameters to tune.

// COMMAND ----------

var rf = new RandomForestRegressor()
  .setNumTrees(50)

// COMMAND ----------

// MAGIC %md
// MAGIC ## Model fitting
// MAGIC 
// MAGIC When we fit our model (`rf.fit(train)`), it actually returns a different object: a `RandomForestRegressionModel`:

// COMMAND ----------

var rfModel = rf.fit(train)

// COMMAND ----------

// This returns the same dataframe but now the predictions column is tacked on. 
display(predictions)

// COMMAND ----------

// MAGIC %md
// MAGIC ## Making predictions
// MAGIC 
// MAGIC Now that we have a fitted model, we're ready to make some predictions (`rfModel.transform(test)`). This will return a new DataFrame, with a `prediction` column appended to the end.

// COMMAND ----------

var predictions = rfModel.transform(test)

// COMMAND ----------

// MAGIC %md
// MAGIC 
// MAGIC ## Model evaluation
// MAGIC 
// MAGIC To evaluate our `predictions` DataFrame, we'll instantiate a `RegressionEvaluator` like so:
// MAGIC ```scala
// MAGIC var evaluator = new RegressionEvaluator()```
// MAGIC 
// MAGIC The default metric is RMSE. To change it to something else, use the `.setMetricName()` method when creating your object:
// MAGIC 
// MAGIC ```scala
// MAGIC var r2Evaluator = new RegressionEvaluator()
// MAGIC   .setMetricName("r2")```
// MAGIC   
// MAGIC Once instantiated, you can evaluate your `predictions` like so: `evaluator.evaluate(predictions)`

// COMMAND ----------

var r2Evaluator = new RegressionEvaluator()
  .setMetricName("r2")

// COMMAND ----------

r2Evaluator.evaluate(predictions)

// COMMAND ----------

// MAGIC %md
// MAGIC # Classification
// MAGIC 
// MAGIC Now we'll create a classification model. Once you've uploaded the `iris.csv` into DataBricks, create your DataFrame in the cell below.

// COMMAND ----------

var df = sqlContext
  .read
  .format("csv")
  .option("header", "true")
  .option("inferSchema", "true")
  .load("/FileStore/tables/iris.csv")

// COMMAND ----------

// MAGIC %md
// MAGIC ## Create `features` column
// MAGIC 
// MAGIC Just like in regression, we need to create our `features` column using a **brand new** `VectorAssembler` object.

// COMMAND ----------

display(df)

// COMMAND ----------

df.columns

// COMMAND ----------

var assembler = new VectorAssembler()
  .setInputCols(Array("sepal length (cm)", "sepal width (cm)","petal length (cm)", "petal width (cm)"))
  .setOutputCol("features")

// COMMAND ----------

df = assembler.transform(df)

// COMMAND ----------

df.show(5)

// COMMAND ----------

// MAGIC %md
// MAGIC 
// MAGIC ## Create `label` column
// MAGIC 
// MAGIC In order for our model to work, we'll need to transform the `species` column into numerical values. We can do this using Spark's `StringIndexer` object. Instantiation requires two parameters, an input column and an output column:
// MAGIC ```scala
// MAGIC var indexer = new StringIndexer()
// MAGIC   .setInputCol("theInputCol")
// MAGIC   .setOutputCol("theOutputCol")```
// MAGIC   
// MAGIC We can knock out two birds with one stone by setting the output column to be `label`.
// MAGIC 
// MAGIC **Note**: The `StringIndexer` needs to be fitted before transforming your DataFrame. During the fitting stage, the indexer will "learn" the exaustive list of possible strings in your column.

// COMMAND ----------

var labelIndexer = new StringIndexer()
  .setInputCol("species")
  .setOutputCol("label")

// COMMAND ----------

df = labelIndexer.fit(df) // Where it learns the set of all possible species
  .transform(df)

// COMMAND ----------

df.show(5)

// COMMAND ----------

// MAGIC %md
// MAGIC %md
// MAGIC ## Train/Test Split
// MAGIC 
// MAGIC Now that our DataFrame is ready for modeling we'll split it up into training and testing sets using the `.randomSplit()` method:
// MAGIC 
// MAGIC ```scala
// MAGIC var Array(train, test) = df.randomSplit(Array(.8, .2), 42)
// MAGIC ``` 
// MAGIC 
// MAGIC The first parameter (`Array(.8, .2)`) determines what percentage will go into `train` and `test` respectively. The second parameter (`42`) is a random seed.

// COMMAND ----------

var Array(train, test) = df.randomSplit(Array(.75, .25), 42)

// COMMAND ----------

// MAGIC %md
// MAGIC ## Model
// MAGIC 
// MAGIC Now we're ready to create our model. MLlib has [several options](https://spark.apache.org/docs/latest/ml-classification-regression.html#classification) to choose from. For our classification model, we'll go with a [Random Forest](https://spark.apache.org/docs/latest/ml-classification-regression.html#random-forest-classifier). 
// MAGIC 
// MAGIC First we'll instantiate our object like so:
// MAGIC ```scala
// MAGIC var rf = new RandomForestClassifier()
// MAGIC   .setNumTrees(50)
// MAGIC   .setMaxDepth(3)```
// MAGIC   
// MAGIC Notice that parameters are set with methods, similar to the `VectorAssembler` object. Check the [docs](https://spark.apache.org/docs/latest/api/scala/index.html#org.apache.spark.ml.classification.RandomForestClassifier) for other hyperparameters to tune.

// COMMAND ----------

var rf = new RandomForestClassifier()

// COMMAND ----------

// MAGIC %md
// MAGIC ## Model fitting
// MAGIC 
// MAGIC When we fit our model (`rf.fit(train)`), it actually returns a whole different object: a `RandomForestClassificationModel`. This is different than `sklearn`, which merely mutates our original instance. As a result, we'll need to save our newly fitted model as a variable:
// MAGIC 
// MAGIC ```scala
// MAGIC var rfModel = rf.fit(train)```
// MAGIC 
// MAGIC The convention in Spark is to use `Model` in the name when it's fitted.

// COMMAND ----------

var rfModel = rf.fit(train)

// COMMAND ----------

// MAGIC %md
// MAGIC ## Making predictions
// MAGIC 
// MAGIC Now that we have a fitted model, we're ready to make some predictions (`rfModel.transform(test)`). This will return a new DataFrame, with a `prediction` column appended to the end.

// COMMAND ----------

var predictions = rfModel.transform(test)

// COMMAND ----------

display(predictions)

// COMMAND ----------

// MAGIC %md
// MAGIC 
// MAGIC ## Model evaluation
// MAGIC 
// MAGIC To evaluate our `predictions` DataFrame, we'll instantiate a `MulticlassClassificationEvaluator` like so:
// MAGIC ```scala
// MAGIC var evaluator = new MulticlassClassificationEvaluator()```
// MAGIC 
// MAGIC The default metric is f1. To change it to something else, use the `.setMetricName()` method when creating your object:
// MAGIC 
// MAGIC ```scala
// MAGIC var accuracyEvaluator = new MulticlassClassificationEvaluator()
// MAGIC   .setMetricName("accuracy")```
// MAGIC   
// MAGIC Once instantiated, you can evaluate the results like so: `evaluator.evaluate(predictions)`

// COMMAND ----------

var accuracyEvaluator = new MulticlassClassificationEvaluator()
  .setMetricName("accuracy")

// COMMAND ----------

accuracyEvaluator.evaluate(predictions)
