class NotEnoughMoneyError(Exception):
    ''' Throws if wallet money is not enough for requested transaction '''
    message = 'You have not enough money'
