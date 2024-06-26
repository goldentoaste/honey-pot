

import re


'''
stolen from: https://stackoverflow.com/a/42789508/12471420
'''

class Trie():
    """Regex::Trie in Python. Creates a Trie out of a list of words. The trie can be exported to a Regex pattern.
    The corresponding Regex should match much faster than a simple Regex union."""

    def __init__(self):
        self.data = {}

    def add(self, word):
        ref = self.data
        for char in word:
            ref[char] = char in ref and ref[char] or {}
            ref = ref[char]
        ref[''] = 1

    def dump(self):
        return self.data

    def quote(self, char):
        return re.escape(char)

    def _pattern(self, pData):
        data = pData
        if "" in data and len(data.keys()) == 1:
            return None

        alt = []
        cc = []
        q = 0
        for char in sorted(data.keys()):
            if isinstance(data[char], dict):
                try:
                    recurse = self._pattern(data[char])
                    alt.append(self.quote(char) + recurse)
                except:
                    cc.append(self.quote(char))
            else:
                q = 1
        cconly = not len(alt) > 0

        if len(cc) > 0:
            if len(cc) == 1:
                alt.append(cc[0])
            else:
                alt.append('[' + ''.join(cc) + ']')

        if len(alt) == 1:
            result = alt[0]
        else:
            result = "(?:" + "|".join(alt) + ")"

        if q:
            if cconly:
                result += "?"
            else:
                result = "(?:%s)?" % result
        return result

    def pattern(self):
        return self._pattern(self.dump())
    
    
if __name__ == '__main__':
    pythonKeywords =  [
 "class",
    "break",
    "case",
    "module",
    "public",
    "finally",
    "in",
    "package",
    "new",
    "continue",
    "as",
    "if",
    "private",
    "for",
    "super",
    "return",
    "try",
    "do",
    "throw",
    "string",
    "instanceof",
    "enum",
    "while",
    "this",
    "static",
    "interface",
    "yield",
    "catch",
    "switch",
    "else",
    "get",
    "typeof",
    "export",
    "new",
    "function",
    "keyof",
    "import",
    "from",
    "of"

]
    t = Trie()
    
    for word in pythonKeywords:
        t.add(word)
    
    print(t.pattern())
    