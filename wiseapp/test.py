# import Cryptopayments
# # Create your views here.
# from Wise import settings
#
# publicKey = settings.COINPAYMENTS_API_KEY
# privateKey = settings.COINPAYMENTS_API_SECRET
# IPN_URL = ''
#
#
# create_transaction_params = {
#     'amount' : 1,
#     'currency1' : 'USD',
#     'currency2' : 'LTCT',
#     'buyer_email' : 'omoleoreoluwa@gmail.com'
# }
# x = Cryptopayments
# #Client instance
# client = x.CryptoPayments(publicKey, privateKey, IPN_URL)
#
# # #make the call to createTransaction crypto payments API
# transaction = client.createTransaction(create_transaction_params)
#
#
# print(transaction)
#
# if transaction['error'] == 'ok':  #check error status 'ok' means the API returned with desired result
#     print (transaction['amount']) #print some values from the result
#     print (transaction['address'])
# else:
#     print (transaction['error'])
#
# print(transaction['txn_id'])
# #Use previous tx Id returned from the previous createTransaction method to test the getTransactionInfo call
# # post_params1 = {
# #     'txid' : transaction['txn_id'],
# # }
# post_params1 = {
#     'txid' : 'CPGD00QBHI0QYA9C0X4WD2OL2E',
# }
#
#
# transactionInfo = client.getTransactionInfo(post_params1) #call coinpayments API using instance
# print(transactionInfo)
# if transactionInfo['error'] == 'ok': #check error status 'ok' means the API returned with desired result
#     print (transactionInfo['amountf'])
#     print (transactionInfo['payment_address'])
#     print (transactionInfo['status'])
#     print (transactionInfo['status_text'])
#     # receivedf >= amountf
#     # for awaiting payments
#     #     status is 0
#     # for successful
#     # status_text should be 'complete'
#     # status should be 100
#     # for expired
#     # status is -1
#     # status_text is 'Cancelled / Timed Out'
# else:
#     print (transactionInfo['error'])

import rncryptor
# from Wise.settings import BINANCE_API_SECRET
BINANCE_API_SECRET = 'qwert'
encrypted_api_secret = rncryptor.encrypt('API_SECRET', BINANCE_API_SECRET)
print(encrypted_api_secret)
encrypted_api_secret = str(encrypted_api_secret)
# encrypted_api_secret = encrypted_api_secret.decode("utf-8")
encrypted_api_secret = bytes(encrypted_api_secret, 'ascii')
print(encrypted_api_secret)
decrypt_api_secret = rncryptor.decrypt(encrypted_api_secret, BINANCE_API_SECRET)
print(decrypt_api_secret)