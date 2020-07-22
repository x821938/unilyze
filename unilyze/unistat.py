from unilyze.unichar import Unichar


class Unistat(Unichar):
    def __init__(self):
        super().__init__()
        self.reset_stat()

    def reset_stat(self):
        """Clears whatever text that was previously added. All statistics are reset
        """
        self.__char_stat = {}

    def add_text(self, text):
        """Add text to be analysed. The provided text will just be added to the pool for statistics

        Args:
            text (str): Text to be added to statistics
        """
        for char in text:
            self.__char_stat.setdefault(char, 0)
            self.__char_stat[char] += 1

    def unistat(self):
        """Sums up the number of characters on each UCD property and property value

        Returns:
            dict: Here is part of the structure as an example:
             {
                'General_Category': {'Decimal_Number': {'chars': {'1', '3', '2'},
                                        'total-count': 47},
                                     'Lowercase_Letter': {'chars': {'a', 'e', 'h', 'i', 'l', 'm', 's', 't'},
                                        'total-count': 95
                                    },
            }
        """
        self.__uni_stat = {}
        for char, count in self.__char_stat.items():
            info = self.ucd_info(char)  # Get full unicode information of char
            for property, property_val in info.items():
                if property_val and not isinstance(property_val, list):
                    self.__uni_stat.setdefault(property, {})
                    self.__uni_stat[property].setdefault(property_val, {})

                    self.__uni_stat[property][property_val].setdefault("total-count", 0)
                    self.__uni_stat[property][property_val]["total-count"] += count

                    self.__uni_stat[property][property_val].setdefault("chars", set())
                    self.__uni_stat[property][property_val]["chars"].add(char)

        return self.__uni_stat

    def charstat(self):
        """Get occurrences of each character in the text

        Returns:
            dict: Example: {'T': 18, 'h': 178, 'i': 212, ......}
        """
        return self.__char_stat
