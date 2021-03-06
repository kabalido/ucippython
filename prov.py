import argparse
import ucipclient
import sys


parser = argparse.ArgumentParser()
# Add the arguments to the parser
parser.add_argument("-m", "--method_id", type=int, required=False,
   help="method id")
parser.add_argument("-p", "--parameters", required=False,
   help="list parameters separated by comma")
parser.add_argument("-l", action='store_true', help="List methods")
args = vars (parser.parse_args())

if len(sys.argv) <= 1:
     parser.error("No parameter provided")

elif  (not args['method_id'] and args['parameters']) or (args['method_id'] and not args['parameters']):
     parser.error('The - [method_id] and [parameters] should be provided')

if (args['l'] == True):
     print("Methods:")
     print("1 - Get_User_Details(subno)    ==> prov.py -m 1 -p subno")
     print("2 - Get_Offers                 ==> prov.py -m 2 -p subno")
     print("3 - Get_Balance_Date           ==> prov.py -m 3 -p subno,da_id")
     print("4 - Update_Balance_date        ==> prov.py -m 4 -p subno,amount")
     print("5 - Update_Balance_DA          ==> prov.py -m 5 -p subno,da_id,da_amount")
     print("6 - Set_Offer                  ==> prov.py -m 6 -p subno,offer_id")
     print("                                   prov.py -m 6 -p subno,offer_id,expirydate")
     print("                                   expirydate format is YYYYMMDDThh:mm:ss (e.g 20191215T23:59:59)")
     print("7 - Install_number_SDP         ==> prov.py -m 7 -p subno,serv_class,flag_temp_block")
     print("8 - Delete_number_SDP          ==> prov.py -m 8 -p subno")
     print("9 - Update_temp_block          ==> prov.py -m 9 -p subno,flag")
     print("10 - Delete Offer              ==> prov.py -m 10 -p subno,offerId")
     sys.exit(0)
ucip = ucipclient.UcipClient('10.100.2.179:83', 'gprs_bundle', 'gprs+2012')
ucip.connect()
method_id = args['method_id']
params = args['parameters'].split(",")
len_args = len(params)
if method_id == 1:
    res = ucip.get_user_details(params[0])
    if res['response'] == 0:
        print("\nsubno: " + res['subno'])
        print(f"{'Subno':<10}{'Service Class':<15}{'Language':<10}{'Status':<14}{'ActivationDate':<23}{'TempBlock':<10}")
        print("-"*82)
        activation_date = res['activationDate'] if 'activationDate' in res else "None"
        tempblock = "Yes" if 'tempBlock' in res and res['tempBlock']  else "No"
        print(f"{res['subno']:<10}{res['sc']:<15}{res['languageId']:<10}{res['status']:<14}{activation_date:<23}{tempblock:<10}")
elif method_id == 2:
    result = ucip.get_offers(params[0])
    if result['response'] == 0:
        print("\nSubno: ", result['subno'])
        print(f"{'offerId':<7} {'offerType':<9} {'startDate':<22} {'expiryDate':<22}")
        print('-'*63)
        for offer in result['offers']:
            print(f"{offer['offerId']:<7} {offer['offerType']:<9} {offer['startDate']:<22} {offer['expiryDate']:<22}")
    else:
        print("Error. Response code:",result['response'])
elif method_id == 3:
    ded_account_id = int(params[1])
    res =ucip.get_balance_date(params[0], ded_account_id)
    if res['response'] == 0:
        print("\nSubno:" + res['subno'])
        print("DedAccountID: " + str(ded_account_id))
        print(f"{'MainAccount':<12}{'DedAccount':<10}")
        print("-"*34)
        print(f"{res['ma']:<12}{res['da']:<10}")
elif method_id == 4:
    print(ucip.update_balance_date(params[0], int(params[1])))
elif method_id == 5:
    print(ucip.update_da_balance(params[0], int(params[1]), int(params[2])))
elif method_id == 6:
    if len_args == 2:
        print(ucip.set_offer(params[0], int(params[1])))
    elif len_args == 3:
        expiry_date = params[2]
        if not expiry_date:
            expiry_date = '99991231T12:00:00'
        print(ucip.set_offer(params[0], int(params[1]), 0, expiry_date))
    else:
        print('Parameter syntax error: <subno,offer_id,expiry_date> expected')
elif method_id == 7:
    if len_args == 3:
        flag = True if params[2] == 'true' else False
        print(ucip.install_subscriber_sdp(params[0], int(params[1]), flag ))
    else:
        print('Parameter syntax error : <subno,serv_class,flag_temp_block> expected')
elif method_id == 8:
     print(ucip.delete_subscriber_sdp(params[0]))
elif method_id == 9:
    if len_args == 2:
        flag = True if params[1] == 'true' else False
        print(ucip.update_tempblock(params[0], flag))
    else:
        print('Parameter syntax error : <subno,flag> expected')
elif method_id == 10:
    if len_args == 2:
        print(ucip.delete_offer(params[0], int(params[1])))
    else:
        print('Parameter syntax error : <subno,flag> expected')
else:
     print('Unknown method id: ', method_id)
