# Developed by Nahidul Islam

import json
import urllib.request
from tkinter import *


class CurrencyLoader:
    """
        Load Currency Data
    """

    # Load currency data from fixer api or from a json file.
    @staticmethod
    def get_currency_rate():
        try:
            with urllib.request.urlopen(
                    "http://data.fixer.io/api/latest?access_key=1078ea87c02e6b91e80aa54a76e5a4b5") as url:
                data = json.loads(url.read().decode())
                # update the currency.json file
                with open('currency.json', 'w') as outfile:
                    json.dump(data, outfile)
                return True, data['rates']
        except Exception:
            return False, json.load(open('currency.json'))['rates']


"""
    Convert currencies
"""


class CurrencyConverter:
    # Return the converted currency amount
    @staticmethod
    def convert(amount, converted_from, converted_to):
        _, currencies = CurrencyLoader.get_currency_rate()
        converted_amount = currencies[converted_to] * amount
        return converted_amount / currencies[converted_from]


"""
    Main GUI class for this application.
"""


class CurrencyConverterApp:
    def __init__(self):
        self.__window = Tk()
        self.__window.title("Currency Converter")
        self.__window.columnconfigure(0, weight=1)
        self.__window.columnconfigure(2, weight=1)
        self.__amount = StringVar(value="1.00")
        self.__amount.trace("w", lambda name, index, mode,
                                        amount=self.__amount: self.on_change(
            amount))
        self.__is_updated, self.__currencies = CurrencyLoader.get_currency_rate()
        self.__changeable_currency = StringVar(value="EUR")
        self.__changed_currency = StringVar(value="USD")
        self.__changeable_currency.trace("w", lambda name, index, mode,
                                                     amount=self.__amount: self.on_change(
            amount))
        self.__changed_currency.trace("w", lambda name, index, mode,
                                                  amount=self.__amount: self.on_change(
            amount))
        if not self.__is_updated:
            amount_label = Label(self.__window,
                                 text="Enable internet\n to get updated conversion rate!",
                                 fg='red')
            amount_label.grid(row=0, column=0, columnspan=3, pady=(20, 0),
                              sticky=W + E + N + S)
        # Input Currency Drop Down Menu
        input_currency_menu = OptionMenu(self.__window,
                                         self.__changeable_currency,
                                         *self.__currencies.keys())
        input_currency_menu.grid(row=1, column=0, padx=(20, 20), pady=(20, 0),
                                 sticky=W + E)
        # Output Currency Drop Down Menu
        output_currency_menu = OptionMenu(self.__window,
                                          self.__changed_currency,
                                          *self.__currencies.keys())
        output_currency_menu.grid(row=1, column=2, padx=(20, 20), pady=(20, 0),
                                  sticky=W + E)
        # Currency Switch Button
        switch_currency_button = Button(self.__window, text="<=>",
                                        command=lambda
                                            amount=self.__amount: self.toggle_currencies(
                                            amount))
        switch_currency_button.grid(row=1, column=1, pady=(20, 0), )
        amount_label = Label(self.__window, text="Amount")
        amount_label.grid(row=2, column=0, columnspan=3, pady=(20, 0),
                          sticky=W + E + N + S)
        # Amount Input Box
        input_amount_entry = Entry(self.__window, textvariable=self.__amount)
        input_amount_entry.grid(row=3, column=0, columnspan=3,
                                padx=(20, 20),
                                sticky=W + E + N + S)
        # Conversion Result Label
        self.__conversion_result_label_text = StringVar()
        conversion_result_label = Label(self.__window,
                                        textvariable=self.__conversion_result_label_text)
        conversion_result_label.grid(row=4, column=0, columnspan=3,
                                     pady=(20, 20),
                                     sticky=W + E)

    # Call update_currency method on currency amount or input or output
    # currency change.
    def on_change(self, amount):
        try:
            self.update_currency(float(amount.get()))

        except ValueError:
            self.__conversion_result_label_text.set('Invalid Amount')

    # Get converted result and update the result output
    def update_currency(self, amount):
        result = CurrencyConverter.convert(amount,
                                           self.__changeable_currency.get(),
                                           self.__changed_currency.get())
        self.__conversion_result_label_text.set(
            '{:,.2f} {converted_from} = '
            '{:,.2f} {converted_to}'.format(
                amount, result,
                converted_from=self.__changeable_currency.get(),
                converted_to=self.__changed_currency.get()))

    # Toggle input and output currency
    def toggle_currencies(self, amount):
        input_currency, output_currency = self.__changeable_currency.get(), self.__changed_currency.get()
        self.__changeable_currency.set(output_currency)
        self.__changed_currency.set(input_currency)
        return self.on_change(amount)

    # Starts the application
    def start(self):
        self.on_change(self.__amount)
        self.__window.mainloop()


def main():
    ui = CurrencyConverterApp()
    ui.start()


main()
