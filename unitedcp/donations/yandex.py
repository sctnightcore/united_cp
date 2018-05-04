import hashlib

from .models import *
from unitedcp.funcs import *
from unitedcp.ragnarok.funcs import *


def yandex_donate(request):
    values = request.POST
    error__code = None
    error__message = None
    account = False

    if not values['operation_id']:
        # No operation ID
        error__code = 1
        error__message = 'Invalid operation_id {}'.format(values['operation_id'])

    if not values['label']:
        # No info about account?
        error__code = 2
        error__message = 'No information about account ({})'.format(values['label'])

    if values['codepro'] is True or values['codepro'] != 'false':
        # Payment with protection code o.O
        error__code = 3
        error__message = 'Payment {} is protected {}'.format(values['operation_id'], values['codepro'])

    if int(values['currency']) != 643:
        # Invalid currency
        error__code = 4
        error__message = 'Invalid currency {}'.format(values['currency'])

    if not float(values['withdraw_amount']):
        # No money or No money for at least one coin
        error__code = 6
        error__message = 'Payment {} has no money, or no money for at least one coin ({})'.format(values['operation_id'], values['withdraw_amount'])

    coins = float(values['withdraw_amount']) / float(settings.DONATION_RATE)

    if not coins or coins < 1:
        # No coins?
        error__code = 6
        error__message = 'Payment {} has no money, or no money for at least one coin ({})'.format(values['operation_id']
                                                                                                  , values['withdraw_amount'])

    try:
        account = User.objects.get(id=int(values['label']))
    except User.DoesNotExist:
        # Account does not exist
        error__code = 7
        error__message = 'Account {} does not exist'.format(values['label'])

    check_hash = str(values['notification_type'] + '&' + values['operation_id'] + '&' + values['amount'] + '&' + values[
        'currency'] + '&' + values['datetime'] + '&' + values['sender'] + '&' + values['codepro'] + '&' + settings.YANDEX_MONEY_KEY + '&' + values['label']).encode('utf-8')

    if hashlib.sha1(check_hash).hexdigest() != values['sha1_hash']:
        error__code = 8
        error__message = 'Sha check failed, must be: {}, get: {}'.format(values['sha1_hash'],
                                                                         hashlib.sha1(check_hash).hexdigest())

    # Add into log:
    DonationsLog.objects.create(
        payment_id=values['operation_id'],
        finished=False,
        log=error__message or 'Waiting for info...',
        error_code=error__code or 0,
        payment_system='Yandex.Money',
        donate_value=values['withdraw_amount'],
        points_value=float(coins),
        user=account.id
    )

    """
        if we have this type of error codes:
        1 - invalid payment id
        2 - no info about account
        7 - no account
        8 - sha check failed

        return status 200 and cancel payment
    """
    if error__code == 1 or error__code == 2 or error__code == 7 or error__code == 8:
        return

    if account:
        donate = UserProfile.objects.get(user=account)
        # Update coins
        if coins >= 1:
            donate.donation_points += int(round(coins*1.25))
        donate.save()

        log = 'Payment {} success'.format(values['operation_id'])
    else:
        log = 'User not found'

    # Update donation log:
    donate_log = DonationsLog.objects.last()
    DonationsLog.objects.filter(id=donate_log.id).update(finished=True, log=log)
    return
