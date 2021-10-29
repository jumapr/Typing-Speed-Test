"""The TypingTest class handles reading the text files with the test pargaphs, grading the test, and providing new tests"""

TEST_FILES = ['test_files/test1.txt', 'test_files/test2.txt', 'test_files/test3.txt', 'test_files/test4.txt']


class TypingTest:

    def __init__(self):
        """
        self._num_tests is set to the number of tests in the TEST_FILES list
        self._test_number starts at 0 and increments every time the user wants a new test. It corresponds to an index
        in the TEST_FILES list
        self.test_text is the string from the test text file
        self_score is number of sequential correctly typed words
        """
        self._num_tests = len(TEST_FILES)
        self._test_number = 0
        self._score = 0
        with open(TEST_FILES[self._test_number], 'r') as file:
            self.test_text = file.read()
        with open('high_score.txt', 'r') as hs_file:
            self.high_score = hs_file.read()

    def grade(self, input_text: str):
        """
        Takes the input_text from the user's tests and returns a grad (`score`)
        :param input_text: the string from the text widget at the end of the test
        :return: self._score
        """
        for input_word, test_word in zip(input_text.split(), self.test_text.split()):
            if input_word == test_word:
                self._score += 1
        if self._score > int(self.high_score):
            self.high_score = str(self._score)
            with open('high_score.txt', 'w') as hs_file:
                hs_file.write(self.high_score)
        return self._score

    def get_new_test(self):
        """
        Gets the next test from the list or circles back to the first test in the list
        """
        if self._test_number < self._num_tests-1:
            self._test_number += 1
        else:
            self._test_number = 0
        with open(TEST_FILES[self._test_number], 'r') as file:
            self.test_text = file.read()
