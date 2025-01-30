import scala.io.Source

import org.apache.hadoop.conf.Configuration
import org.apache.hadoop.fs.Path
import org.apache.hadoop.io.{IntWritable, Text}
import org.apache.hadoop.mapreduce.lib.input.{FileInputFormat, KeyValueTextInputFormat, TextInputFormat}
import org.apache.hadoop.mapreduce.lib.output.{FileOutputFormat, TextOutputFormat}
import org.apache.hadoop.mapreduce.{Job, Mapper, Reducer}

import java.lang
import scala.jdk.CollectionConverters.IterableHasAsScala

import java.lang
import scala.jdk.CollectionConverters.IterableHasAsScala
import org.apache.hadoop.thirdparty.org.checkerframework.checker.units.qual.Length


object DataProcessing {
    def main(args: Array[String]): Unit = {
        println("test");
        // val lines = Source.fromFile("/home/charles-m/Projects/ASR/CSC5003/scala/peter_pan/src/main/scala/peter_pan_book.txt")("UTF-8")
    }
}
