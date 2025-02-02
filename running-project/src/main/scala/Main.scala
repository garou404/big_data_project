import org.apache.spark.sql.Row
import org.apache.spark.sql.SparkSession


object Main {
    def main(args: Array[String]) : Unit = {
        val spark = SparkSessionBuilder.spark
        val df = DataReader.readCSV(spark, "/home/charles-m/Projects/ASR/CSC5003/project/data/running/run_ww_2019_d.csv")
        val df_pop = DataReader.readCSV(spark, "/home/charles-m/Projects/ASR/CSC5003/project/data/population/population_processed.csv")
        val df_wr = DataReader.readCSV(spark, "/home/charles-m/Projects/ASR/CSC5003/project/data/wr/running_wr.csv")
        
        // df.show(10)

        val df_test = DataProcessor.get_all_time_performances(df, df_wr)
        df_test.show(40)

        // val df_test2 = DataProcessor.get_runner_proportion_per_country(df, df_pop.where("year = 2019"))
        // df_test2.show()
    }
    
}