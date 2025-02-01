import org.apache.spark.sql.{DataFrame}
import org.apache.spark.sql.functions.{desc, expr, round, col, sum, floor}
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

    def get_all_time_performances(df_runner : DataFrame) : DataFrame = {
        // "0.5", "1", "5", "10", "21.0975", "42,195"
        df_runner
        .filter(col("distance") =!= 0)
        .withColumn("pace", round(expr("duration / distance"), 2))
        .withColumn("pace_min", floor(col("pace")))
        .withColumn("pace_sec", round(expr("pace - pace_min"), 2))
        .filter(col("distance") >= 21.0975)
        .orderBy(col("pace").asc)
        .limit(20)
    }
}
