class InsufficientFundsError(Exception):
    def __init__(self, amount, balance):
        self.message = f"No hay fondos suficientes para retirar {amount}. Saldo actual: {balance}"
        super().__init__(self.message)

class InvalidTransactionType(Exception):
    def __init__(self, transaction_type):
        self.message = f"Tipo de transacción no válido '{transaction_type}'. Tipos aceptados: depósito, retiro, view_transaction_history"
        super().__init__(self.message)

class Transaction:
    def __init__(self, amount, transaction_type, balance):
        self.transaction_type = transaction_type
        self.amount = amount
        self.balance = balance

    def __str__(self):
        return f"Type: {self.transaction_type}, Amount: {self.amount}, Balance: {self.balance}"

class BankAccount:
    def __init__(self, initial_balance=1500.0):
        self.balance = initial_balance
        self.transaction_history = []

    def process_transaction(self, transaction_amount, transaction_type):
        # Si el tipo de transacción es 'view_transaction_history', no necesitamos el monto
        if transaction_type == "view_transaction_history":
            if not self.transaction_history:
                return "No transactions available."
            # Unir transacciones en una sola cadena sin caracteres extra
            return "; ".join(str(trans) for trans in self.transaction_history)

        # Para otros tipos de transacción, asegurarse de que el monto es válido
        try:
            transaction_amount = float(transaction_amount)
        except (TypeError, ValueError):
            raise ValueError(f"El monto '{transaction_amount}' no es válido. Debe ser un número.")

        # Procesar el depósito
        if transaction_type == "deposit":
            self.balance += transaction_amount
            transaction = Transaction(transaction_amount, transaction_type, self.balance)
            self.transaction_history.append(transaction)
            return f"Transaction successful! Updated account balance: {self.balance}"

        # Procesar el retiro
        elif transaction_type == "withdraw":
            if transaction_amount > self.balance:
                raise InsufficientFundsError(transaction_amount, self.balance)
            self.balance -= transaction_amount
            transaction = Transaction(transaction_amount, transaction_type, self.balance)
            self.transaction_history.append(transaction)
            return f"Transaction successful! Updated account balance: {self.balance}"

        # Tipo de transacción no válido
        else:
            raise InvalidTransactionType(transaction_type)

# Ejemplo de uso
if __name__ == "__main__":
    bank_account = BankAccount()
    try:
        # Depósito
        amount = 500.0
        transaction_type = "deposit"
        result = bank_account.process_transaction(amount, transaction_type)
        print(result)

        # Retiro
        amount = 200.0
        transaction_type = "withdraw"
        result = bank_account.process_transaction(amount, transaction_type)
        print(result)

        # Ver historial de transacciones
        transaction_type = "view_transaction_history"
        result = bank_account.process_transaction(None, transaction_type)
        print(result)

    except Exception as e:
        print(f"An unexpected error occurred: {e}")
