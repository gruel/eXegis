"""Module which contains the class which create the XML part related to
the introduction (if present) in the hyppocratic aphorysm document.

note: pylint analysis 10

Authors: Jonathan Boyle, Nicolas Gruel
Copyright: IT Services, The University of Manchester
"""

import logging.config

try:
    from hyppocratic.analysis import references, footnotes
    from hyppocratic.conf import LOGGING
    from hyppocratic.baseclass import Hyppocratic
except ImportError:
    from analysis import references, footnotes
    from conf import LOGGING
    from baseclass import Hyppocratic

# Read logging configuration and create logger
logging.config.dictConfig(LOGGING)
# pylint: disable=locally-disabled, invalid-name
logger = logging.getLogger('hyppocratic.CommentaryToEpidoc')


# Define an Exception
class IntroductionException(Exception):
    """Class for exception
    """
    pass


class Introduction(Hyppocratic):
    """Class Introduction which will create the introduction XML part

    Attributes
    ----------

    self.introduction: str
        string which contain the introduction of the hyppocratic aphorysms
        document.

    self.next_footnote: int
        integer which contains the footnote reference number which
        can be present.

    self.xml: list
        list of string which contains the XML related to the introduction
        to be include in the main XML part of the document.


    """

    def __init__(self, introduction, next_footnote):
        Hyppocratic.__init__(self)
        self.introduction = introduction
        self.next_footnote = next_footnote

    def xml_main(self):
        """Method to treat the optional part of the introduction.
        """
        introduction = self.introduction.splitlines()

        # Generate the opening XML for the intro
        self.xml.append(self.xml_oss * self.xml_n_offset + '<div type="intro">')
        self.xml.append(self.xml_oss * (self.xml_n_offset + 1) + '<p>')

        for line in introduction:
            if line == '':
                continue

            # Process any witnesses in this line. If this fails with a
            # IntroductionException print an error and return
            try:
                line_ref = references(line)
            except IntroductionException:
                error = ('Unable to process _references in the introduction'
                         ' (line: {})'.format(line))
                logger.error(error)
                raise IntroductionException

            # Process any footnotes in line_ref. If this fails with a
            # IntroductionException print an error and return
            try:
                self.xml_n_offset += 2
                xml_main_to_add, self.next_footnote = \
                    footnotes(line_ref, self.next_footnote)
                self.xml_n_offset -= 2
            except IntroductionException:
                error = ('Unable to process _references in the introduction'
                         ' (line: {})'.format(line))
                logger.error(error)
                raise IntroductionException

            # Add to the XML
            self.xml.extend(xml_main_to_add)

        # Add XML to close the intro section
        self.xml.append(self.xml_oss * (self.xml_n_offset + 1) + '</p>')
        self.xml.append(self.xml_oss * self.xml_n_offset + '</div>')