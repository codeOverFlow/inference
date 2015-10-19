/**
 * Author: adrien 
 * Date: 19/10/15
 */

import helpers._

object Main extends App {
  val rawData = Reader("112_initial.fsa.res")
  println(rawData)
  val structuredData = StructureMaker.fromRawToStructure(rawData)
  println(structuredData)
  val toLearn = StructureMaker.prepareForLearning(structuredData)
  println(toLearn)

}
