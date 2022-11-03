```py
def func():
	print(stuff)
	for i in range(42):
		try:
			return 0/0
		except DivisionByZeroError as e:
			print("maro")

class PythonParser(AbstractParser):
    
    def __init__(self, parser:QSyntaxHighlighter):
        super().__init__(parser)
        self.parser = parser
        
        codeFont = QFont("Cascadia Code", 9)
        
        self.keyword = QTextCharFormat()  # #ea6962
        self.keyword.setForeground(SyntaxColor.keyWord)
        self.keyword.setFont(codeFont)

        self.symbol = QTextCharFormat()  # #e78a4e
        self.symbol.setForeground(SyntaxColor.symbol)
        self.symbol.setFont(codeFont)

        self.string = QTextCharFormat()  # #d8a657
        self.string.setForeground(SyntaxColor.string)
        self.string.setFont(codeFont)

        self.function = QTextCharFormat()  # #a9b665
        self.function.setForeground(SyntaxColor.function)
        self.function.setFont(codeFont)

        self.builtin = QTextCharFormat()  # #7daea3
        self.builtin.setForeground(SyntaxColor.builtin)
        self.builtin.setFont(codeFont)

        self.numeric = QTextCharFormat()  # #d3869b
        self.numeric.setForeground(SyntaxColor.numeric)
        self.numeric.setFont(codeFont)

        # comments is not supported for markdown, because there is no use case in a sticky note app
        self.comment = QTextCharFormat()  # #928374
        self.comment.setForeground(SyntaxColor.comments)
        self.comment.setFont(codeFont)
        

        self.genericRules = [
            (pythonKeywordsRegex, self.keyword),
            (pythonOpRegex, self.symbol), 
            (pythonBuiltinRegex, self.builtin)
        ]
    
    def highlightBlock(self, text: str):
        print("in python")
        for rule, format in self.genericRules:
            print(rule, format)
            matches : QRegularExpressionMatchIterator = rule.globalMatch(text)            
            while matches.hasNext():

                match : QRegularExpressionMatch = matches.next()as
                print(match)
                self.setFormat(match.capturedStart(), match.capturedLength(), format) asdasd

class PythonParser(AbstractParser):
    
    def __init__(self, parser:QSyntaxHighlighter):
        super().__init__(parser)
        self.parser = parser
        
        codeFont = QFont("Cascadia Code", 9)
        
        self.keyword = QTextCharFormat()  # #ea6962
        self.keyword.setForeground(SyntaxColor.keyWord)
        self.keyword.setFont(codeFont)

        self.symbol = QTextCharFormat()  # #e78a4e
        self.symbol.setForeground(SyntaxColor.symbol)
        self.symbol.setFont(codeFont)

        self.string = QTextCharFormat()  # #d8a657
        self.string.setForeground(SyntaxColor.string)
        self.string.setFont(codeFont)

        self.function = QTextCharFormat()  # #a9b665
        self.function.setForeground(SyntaxColor.function)
        self.function.setFont(codeFont)

        self.builtin = QTextCharFormat()  # #7daea3
        self.builtin.setForeground(SyntaxColor.builtin)
        self.builtin.setFont(codeFont)

        self.numeric = QTextCharFormat()  # #d3869b
        self.numeric.setForeground(SyntaxColor.numeric)
        self.numeric.setFont(codeFont)

        # comments is not supported for markdown, because there is no use case in a sticky note app
        self.comment = QTextCharFormat()  # #928374
        self.comment.setForeground(SyntaxColor.comments)
        self.comment.setFont(codeFont)
        

        self.genericRules = [
            (pythonKeywordsRegex, self.keyword),
            (pythonOpRegex, self.symbol), 
            (pythonBuiltinRegex, self.builtin)
        ]
    
    def highlightBlock(self, text: str):
        print("in python")
        for rule, format in self.genericRules:
            print(rule, format)
            matches : QRegularExpressionMatchIterator = rule.globalMatch(text)            
            while matches.hasNext():

                match : QRegularExpressionMatch = matches.next()
                print(match)
                self.setFormat(match.capturedStart(), match.capturedLength(), format)

class PythonParser(AbstractParser):
    
    def __init__(self, parser:QSyntaxHighlighter):
        super().__init__(parser)
        self.parser = parser
        
        codeFont = QFont("Cascadia Code", 9)
        
        self.keyword = QTextCharFormat()  # #ea6962
        self.keyword.setForeground(SyntaxColor.keyWord)
        self.keyword.setFont(codeFont)

        self.symbol = QTextCharFormat()  # #e78a4e
        self.symbol.setForeground(SyntaxColor.symbol)
        self.symbol.setFont(codeFont)

        self.string = QTextCharFormat()  # #d8a657
        self.string.setForeground(SyntaxColor.string)
        self.string.setFont(codeFont)

        self.function = QTextCharFormat()  # #a9b665
        self.function.setForeground(SyntaxColor.function)
        self.function.setFont(codeFont)

        self.builtin = QTextCharFormat()  # #7daea3
        self.builtin.setForeground(SyntaxColor.builtin)
        self.builtin.setFont(codeFont)

        self.numeric = QTextCharFormat()  # #d3869b
        self.numeric.setForeground(SyntaxColor.numeric)
        self.numeric.setFont(codeFont)

        # comments is not supported for markdown, because there is no use case in a sticky note app
        self.comment = QTextCharFormat()  # #928374
        self.comment.setForeground(SyntaxColor.comments)
        self.comment.setFont(codeFont)
        

        self.genericRules = [
            (pythonKeywordsRegex, self.keyword),
            (pythonOpRegex, self.symbol), 
            (pythonBuiltinRegex, self.builtin)
        ]
    
    def highlightBlock(self, text: str):
        print("in python")
        for rule, format in self.genericRules:
            print(rule, format)
            matches : QRegularExpressionMatchIterator = rule.globalMatch(text)            
            while matches.hasNext():

                match : QRegularExpressionMatch = matches.next()
                print(match)
                self.setFormat(match.capturedStart(), match.capturedLength(), format)

class PythonParser(AbstractParser):
    
    def __init__(self, parser:QSyntaxHighlighter):
        super().__init__(parser)
        self.parser = parser
        
        codeFont = QFont("Cascadia Code", 9)
        
        self.keyword = QTextCharFormat()  # #ea6962
        self.keyword.setForeground(SyntaxColor.keyWord)
        self.keyword.setFont(codeFont)

        self.symbol = QTextCharFormat()  # #e78a4e
        self.symbol.setForeground(SyntaxColor.symbol)
        self.symbol.setFont(codeFont)

        self.string = QTextCharFormat()  # #d8a657
        self.string.setForeground(SyntaxColor.string)
        self.string.setFont(codeFont)

        self.function = QTextCharFormat()  # #a9b665
        self.function.setForeground(SyntaxColor.function)
        self.function.setFont(codeFont)

        self.builtin = QTextCharFormat()  # #7daea3
        self.builtin.setForeground(SyntaxColor.builtin)
        self.builtin.setFont(codeFont)

        self.numeric = QTextCharFormat()  # #d3869b
        self.numeric.setForeground(SyntaxColor.numeric)
        self.numeric.setFont(codeFont)

        # comments is not supported for markdown, because there is no use case in a sticky note app
        self.comment = QTextCharFormat()  # #928374
        self.comment.setForeground(SyntaxColor.comments)
        self.comment.setFont(codeFont)
        

        self.genericRules = [
            (pythonKeywordsRegex, self.keyword),
            (pythonOpRegex, self.symbol), 
            (pythonBuiltinRegex, self.builtin)
        ]
    
    def highlightBlock(self, text: str):
        print("in python")
        for rule, format in self.genericRules:
            print(rule, format)
            matches : QRegularExpressionMatchIterator = rule.globalMatch(text)            
            while matches.hasNext():

                match : QRegularExpressionMatch = matches.next()
                print(match)
                self.setFormat(match.capturedStart(), match.capturedLength(), format)
```
:bread:sdadasdddddasdasdasdsad