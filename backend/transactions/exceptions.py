class TransactionError(Exception):
    ''' Basic transaction related exception '''


class NotEnoughMoneyError(TransactionError):
    ''' Throws if wallet money is not enough for requested transaction '''
    message = 'You have not enough money'


class NotYourWalletError(TransactionError):
    ''' Throws if wallet is not yours '''
    message = 'You are not the owner of wallet'


class MissingSystemWalletError(TransactionError):
    ''' Throws if system wallet is not defined '''
    message = 'System (fee) wallet was not found!'


class MissingReceiverWalletError(TransactionError):
    ''' Throws if target wallet is not found '''
    message = 'Target wallet was not found!'
