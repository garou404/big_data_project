import org.apache.spark.sql.SparkSession
object SparkSessionBuilder {
    lazy val spark : SparkSession = SparkSession.builder()
    .appName("spark-lab")
    .master("local[*]")
    .getOrCreate()
}
