import os
print(os.getcwd())
import unittest
from src.main import *


class Test(unittest.TestCase):

    def setUp(self) -> None:
        print(os.getcwd())
        self.data = pd.read_csv('data/prices.csv')
        self.data["TS"] = self.data["TS"].astype("datetime64[ns]")
        self.data = self.data.set_index("TS")
        self.resampled = self.data.resample(pd.Timedelta(hours=1))

    def test_file(self):
        pass

    def test_low(self):
        expected = [1871.96244476, 1875.917880859, 1875.7284596343]
        actual = resampled_last(self.resampled)['PRICE'].tolist()
        self.assertSequenceEqual(expected, actual, "Not equal!")

    def test_high(self):
        expected = [1875.979748793, 1875.917880859, 1875.7284596343]
        actual = resampled_high(self.resampled)['PRICE'].tolist()
        self.assertSequenceEqual(expected, actual, "Not equal!")


if __name__ == "__main__":
  unittest.main()