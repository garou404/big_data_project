import org.apache.spark.sql.Row
import org.apache.spark.sql.SparkSession


object Main {
    def main(args: Array[String]) : Unit = {
        val spark = SparkSessionBuilder.spark
        val df = DataReader.readCSV(spark, "/home/charles-m/Projects/ASR/CSC5003/project/data/running/run_ww_2019_d.csv")
        val df_pop = DataReader.readCSV(spark, "/home/charles-m/Projects/ASR/CSC5003/project/data/population/population_processed.csv")
        val df_wr = DataReader.readCSV(spark, "/home/charles-m/Projects/ASR/CSC5003/project/data/wr/running_wr.csv")
        val saveTo = "/home/charles-m/Projects/ASR/CSC5003/project/data/processed_data/"

        // DataProcessor.get_runner_prop_per_age_category(df)
        // Define processing functions with their corresponding output file names
        val processingSteps = Seq(
            // ("runner_prop_per_country", DataProcessor.get_runner_proportion_per_country(df, df_pop)),
            ("runner_nb_per_country", DataProcessor.get_runner_nb_per_country(df)),
            ("runner_prop_per_age_category", DataProcessor.get_runner_prop_per_age_category(df)),
            ("all_time_performances", DataProcessor.get_all_time_performances(df, df_wr)),
            ("per_runner_data", DataProcessor.get_per_runner_data(df)),
            ("running_frequency_per_country", DataProcessor.get_running_frequency_per_country(df))
        )

        // Process and save each DataFrame
        processingSteps.foreach { case (fileName, dfProcessed) =>
            DataWriter.saveAsCSV(dfProcessed, saveTo + fileName)
        }

    }
    
}