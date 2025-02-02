import org.apache.spark.sql.{DataFrame}
import org.apache.spark.sql.functions._
import org.apache.spark.sql.functions.expr
import org.apache.spark.sql.expressions.Window


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
        .groupBy("country").count().withColumnRenamed("count", "runner_nb_per_country")
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

    def get_per_runner_metrics(df_runner : DataFrame) : DataFrame = {
        val nb_of_weeks = df_runner.select("datetime").distinct().count() / 7.0
        df_runner
        .filter(col("distance") =!= 0)
        .groupBy("athlete")
        .agg(
            count("*").as("nb_of_run"),
            round(sum("distance"), 2).as("total_dist"),
            round(sum("distance") / lit(nb_of_weeks), 2).as("avg_dist_per_week"),
            round(avg("distance"), 2).as("avg_run_dist")
        )
    }

    def get_longest_running_streak_per_athlete(df_runner : DataFrame) : DataFrame = {
        // This window specification groups rows by athlete and orders them by date
        val windowSpec = Window.partitionBy("athlete").orderBy("datetime")
        

        // Identify gaps: If previous day's distance > 0, continue the streak, else reset
        val df_streak = df_runner
            .withColumn("prev_distance", lag("distance", 1).over(windowSpec)) // Get previous day’s distance
            .withColumn("streak_reset", when(col("prev_distance").isNull || col("prev_distance") === 0, 1).otherwise(0)) // Mark start of streaks
            .withColumn("streak_id", sum("streak_reset").over(windowSpec)) // Create streak groups
            .withColumn("running_streak", count("*").over(Window.partitionBy("athlete", "streak_id"))) // Count streak length
            .drop("prev_distance", "streak_reset", "streak_id") // Clean up columns

        // Get max streak per athlete
        val df_max_streak = df_streak
            .groupBy("athlete")
            .agg(max("running_streak").alias("longest_streak"))

        df_max_streak.orderBy(desc("longest_streak"))
    }

    def get_best_performances_per_athlete(df_runner : DataFrame) : DataFrame = {
        val windowSpec = Window.partitionBy("athlete").orderBy("datetime")
        val temp_df = df_runner
            .filter(col("distance") =!= 0)
            .withColumn("pace", round(expr("duration / distance"), 2))
            .withColumn("pace_min", floor(col("pace")))
            .withColumn("pace_sec", round(expr("pace - pace_min")*60, 0))
        val distances = Seq(5.0, 10.0, 21.0975, 42.195, 50.0, 100.0)   
        distances
        .map((dist : Double) => temp_df
            .filter(col("distance") >= dist)
            .withColumn("rank", rank().over(windowSpec))
            .filter(col("rank") === 1)
            .drop("rank")
            .withColumn("best_for_dist", lit(dist))
        ).reduce(_ union _)
        .withColumn("dist/dur", concat(col("distance"), lit("/"), col("duration")))
        .groupBy("athlete")
        .pivot("best_for_dist")
        .agg(first("dist/dur"))
    }

    def get_per_runner_data(df_runner : DataFrame) : DataFrame = {
        val df_metrics = get_per_runner_metrics(df_runner)
        val df_running_streak = get_longest_running_streak_per_athlete(df_runner)
        val df_best_perf = get_best_performances_per_athlete(df_runner)
        df_metrics.join(df_running_streak, "athlete", "outer").join(df_best_perf, "athlete", "outer")
    }

    def get_running_frequency_per_country(df_runner : DataFrame) : DataFrame = {
        val nb_of_weeks = df_runner.select("datetime").distinct().count() / 7.0
        df_runner
        .filter(col("distance") =!= 0)
        .groupBy("country")
        .agg(

            count("*").as("nb_of_run"),
            round(sum("distance") / lit(nb_of_weeks), 2).as("avg_dist_per_week"),
            round(avg("distance"), 2).as("avg_run_dist")
        ).withColumn("avg_run_per_week", col("nb_of_run") / lit(nb_of_weeks))


        df_runner
        .filter(col("distance") =!= 0) // Filter out rows where distance is 0
        .groupBy("country") // Group by country
        .agg(
            count("*").as("nb_of_run"),
            round(sum("distance") / lit(nb_of_weeks), 2).as("avg_dist_per_week"),
            round(avg("distance"), 2).as("avg_run_dist_per_run_per_athlete"),
            countDistinct("athlete").as("distinct_athletes")
        )
        .withColumn("avg_nb_of_run_per_athlete_per_week", round(col("nb_of_run") / lit(nb_of_weeks) / col("distinct_athletes"), 0)) // Calculate average runs per week
        .withColumn("avg_dist_per_athlete_per_week", round(col("avg_dist_per_week") / col("distinct_athletes"), 2))
    }
}
