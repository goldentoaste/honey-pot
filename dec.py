class BasePrinter:
    
    def doPrint(self, text):
        raise NotImplementedError()
        

class Printer(BasePrinter):
    
    def doPrint(self, text):
        print(text)


class PrinterDecorator(BasePrinter):
    
    def __init__(self, printer)  -> None:
        super().__init__()
        self.printer = printer
        


class FancyPrinterDecorator(PrinterDecorator):
    
    def doPrint(self, text):
        print("*fancy*")
        self.printer.doPrint(text)
        print("*facny*")
        
class DoublePrinterDecorator(PrinterDecorator):
    
    def doPrint(self, text):
        
        self.printer.doPrint(text)
        self.printer.doPrint(text)
        
p = Printer()

