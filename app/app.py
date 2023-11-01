from PySide6 import QtWidgets
import currency_converter


class App(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.c = currency_converter.CurrencyConverter()
        self.setWindowTitle('Convertisseur de devices')
        self.setup_ui()
        self.set_default_values()
        self.setup_connections()
        self.setup_css()

    def setup_ui(self):
        self.layout = QtWidgets.QHBoxLayout(self)  # type: ignore
        self.cbb_currenciesFrom = QtWidgets.QComboBox()
        self.spn_amount = QtWidgets.QSpinBox()
        self.cbb_currenciesTo = QtWidgets.QComboBox()
        self.spn_convertedAmount = QtWidgets.QSpinBox()
        self.btn_inversed = QtWidgets.QPushButton('Inverser devises')

        self.layout.addWidget(self.cbb_currenciesFrom)
        self.layout.addWidget(self.spn_amount)
        self.layout.addWidget(self.cbb_currenciesTo)
        self.layout.addWidget(self.spn_convertedAmount)
        self.layout.addWidget(self.btn_inversed)

    def set_default_values(self):
        self.cbb_currenciesFrom.addItems(sorted(list(self.c.currencies)))  # type: ignore
        self.cbb_currenciesTo.addItems(sorted(list(self.c.currencies)))  # type: ignore
        self.cbb_currenciesFrom.setCurrentText('EUR')
        self.cbb_currenciesTo.setCurrentText('EUR')

        self.spn_amount.setRange(1, 1000000)
        self.spn_amount.setValue(100)
        self.spn_convertedAmount.setRange(1, 1000000)
        self.spn_convertedAmount.setValue(100)

    def setup_connections(self):
        self.cbb_currenciesFrom.activated.connect(self.compute)
        self.cbb_currenciesTo.activated.connect(self.compute)
        self.spn_amount.valueChanged.connect(self.compute)
        self.btn_inversed.clicked.connect(self.inversed_devises)

    def setup_css(self):
        self.setStyleSheet("""
            background-color: rgb(30, 30, 30);
            color: rgb(240, 240, 240);
            width: 110;
            border: none;
        """)

    def compute(self):
        amount = self.spn_amount.value()
        currency_from = self.cbb_currenciesFrom.currentText()
        currency_to = self.cbb_currenciesTo.currentText()
        try:
            result = self.c.convert(amount, currency_from, currency_to)
        except currency_converter.currency_converter.RateNotFoundError:
            print('La conversion n\'a pas fonctionné.')
        else:
            self.spn_convertedAmount.setValue(result)

    def inversed_devises(self):
        currency_from = self.cbb_currenciesFrom.currentText()
        currency_to = self.cbb_currenciesTo.currentText()
        self.cbb_currenciesFrom.setCurrentText(currency_to)
        self.cbb_currenciesTo.setCurrentText(currency_from)
        self.compute()


app = QtWidgets.QApplication([])
win = App()
win.show()

app.exec()
