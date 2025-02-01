import org.apache.spark.sql.{DataFrame, SparkSession}

object DataWriter {
  def saveAsCSV(df: DataFrame, path: String) : Unit = {
        df.write.mode("overwrite").option("header", "true").csv(path)
    }
}
