package helpers

/**
 * Author: adrien 
 * Date: 19/10/15
 */
object StructureMaker {
  /**
   * Get a list of string from a reading file to make a better structure
   * @param lines A list of String extracted from *.res data files
   * @return A list of (inputString, outputString)
   */
  def fromRawToStructure(lines: List[String]): List[(String, String)] =
    lines.map { s =>
      val splited = s.split(",")
      (splited(1), splited(2))
    }

  /**
   * Make a better structure for learning the automaton
   * @param stringCouple The structure returned by StructureMaker.fromRawToStructure -> a List[String, String]
   * @return A pretty structure to learn automaton
   */
  def prepareForLearning(stringCouple: List[(String, String)]): List[List[((String, String), Int)]] =
    stringCouple.map { case (s0, s1) =>
      s0.zipWithIndex.filter(_._2 % 2 == 0).map { case (_, i) =>
        s0.substring(i, i + 2)
      }.zip(s1.zipWithIndex.filter(_._2 % 2 == 0).map { case (_, i) =>
        s1.substring(i, i + 2)
      }).zipWithIndex.toList
    }
}
