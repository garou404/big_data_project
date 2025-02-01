import org.apache.spark.sql.{DataFrame, SparkSession}

object DataReader {
    def readCSV(spark: SparkSession, path: String) : DataFrame = {
        spark.read.option("header", "true").csv(path)
    }
}
