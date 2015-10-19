package helpers

import java.io.File

import scala.io.Source

/**
 * Author: adrien 
 * Date: 19/10/15
 */
object Reader {
  /**
   * Read a File
   * @param filename The name of the file to read
   * @param dir The directory where the file is
   * @return The list of all lines in the file
   */
  def apply(filename: String, dir: String = "resources/"): List[String] =
    Source.fromFile(new File(dir + filename)).getLines().toList
}
