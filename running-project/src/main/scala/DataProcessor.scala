import org.apache.spark.sql.{DataFrame}
import org.apache.spark.sql.functions.{desc, expr, round, col, sum, floor, lit}
import org.apache.spark.sql.functions.expr

object DataProcessor {
    def get_runner_proportion_per_country(df_runner : DataFrame, df_pop : DataFrame) : DataFrame = {
        // need to handle the cases when same country have different name in the 2 df
        val df_runner_processed = get_runner_nb_per_country(df_runner)
        val df_pop_processed = df_pop.withColumnRenamed("country_name", "country").drop("country_code", "year")
        df_runner_processed
        .join(df_pop_processed, "country", "left")
        .withColumn("runner_proportion", expr("count / population"))
        .withColumn("runner_proportion", round(col("runner_proportion"), 6))
        .sort(desc("runner_proportion"))
        .drop("count", "population")
    }

    def get_runner_nb_per_country(df_runner : DataFrame) : DataFrame = {
        df_runner
        .groupBy("country", "athlete").count()
        .groupBy("country").count()
        .na.drop().sort(desc("count"))
    }

    def get_runner_prop_per_age_category(df_runner : DataFrame) : DataFrame = {
        df_runner
        .groupBy("age_group", "athlete").count()
        .groupBy("age_group").count()
        .withColumn("fraction", round(col("count") /  sum("count").over(), 2))
    }

    def get_fastest_runners_for_distance(df_runner : DataFrame, distance_threshold : Double, pace_threshold : Double, gender : String) : DataFrame = {
        df_runner.filter(col("distance") >= distance_threshold && col("distance") < 1.2*distance_threshold  && col("pace") > pace_threshold && col("gender") === gender)
        .orderBy(col("pace").asc)
        .limit(3)
        .withColumn("best distance", lit(distance_threshold))
    }

    def get_all_time_performances(df_runner : DataFrame, df_wr : DataFrame) : DataFrame = {
        val distances = Seq(0.1, 0.2, 0.4, 0.8, 1, 1.5, 2, 3, 5, 10, 21.0975, 42.195, 50, 100)
        val genders = Seq("M", "F")
        val temp_df = df_runner
            .filter(col("distance") =!= 0)
            .withColumn("pace", round(expr("duration / distance"), 2))
            .withColumn("pace_min", floor(col("pace")))
            .withColumn("pace_sec", round(expr("pace - pace_min")*60, 0))
        val df_selected = distances
        .flatMap(distance => genders.map(gender => {
            val wr = df_wr.filter(col("gender") === gender)
            .withColumn("pace", round(expr("duration / distance"), 2))
            .filter(col("distance") === distance)
            .select("pace")
            .first()(0)

            get_fastest_runners_for_distance(temp_df, distance, wr.asInstanceOf[Double], gender)
        }))      
        .reduce(_ union _)
        df_selected
    }



}
