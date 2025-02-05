import org.apache.spark.sql.Row
import org.apache.spark.sql.SparkSession
import org.apache.spark.sql.functions.col

object Main {
    def main(args: Array[String]) : Unit = {
        val year = "2019"
        val spark = SparkSessionBuilder.spark
        val df = DataReader.readCSV(spark, "/home/charles-m/Projects/ASR/CSC5003/project/data/running/run_ww_"+year+"_d.csv")
        val df_pop = DataReader.readCSV(spark, "/home/charles-m/Projects/ASR/CSC5003/project/data/population/population_processed.csv")

        val df_wr = DataReader.readCSV(spark, "/home/charles-m/Projects/ASR/CSC5003/project/data/wr/running_wr.csv")
        val saveTo = "/home/charles-m/Projects/ASR/CSC5003/project/data/processed_data/"


        // Define processing functions with their corresponding output file names
        val processingSteps = Seq(
            ("runner_prop_per_country_"+year, DataProcessor.get_runner_proportion_per_country(df, df_pop.filter(col("year") === year))),
            ("runner_nb_per_country_"+year, DataProcessor.get_runner_nb_per_country(df)),
            ("runner_prop_per_age_category_"+year, DataProcessor.get_runner_prop_per_age_category(df)),
            ("all_time_performances_"+year, DataProcessor.get_all_time_performances(df, df_wr, 20)),
            ("per_runner_data_"+year, DataProcessor.get_per_runner_data(df)),
            ("running_frequency_per_country_"+year, DataProcessor.get_running_frequency_per_country(df))
        )

        // Process and save each DataFrame
        processingSteps.foreach { case (fileName, dfProcessed) =>
            DataWriter.saveAsCSV(dfProcessed, saveTo + fileName)
        }

    }
    
}