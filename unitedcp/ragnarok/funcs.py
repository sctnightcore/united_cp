from .models import (Login, Char)
from unitedcp.accounts.models import UserProfile


def get_game_accounts(master_id):
    game_accounts = Login.objects.values('account_id', 'userid', 'lastlogin', 'last_ip', 'logincount', 'sex', 'state', 'unban_time').filter(master_account=master_id).all()
    game_accounts_count = Login.objects.filter(master_account=master_id).count()
    return {'game': game_accounts, 'count': game_accounts_count} or None


def get_account_characters(master_id):
    main_character = None
    characters = Char.objects.values().filter(account_id__master_account=master_id).all()
    characters_count = len(characters)
    ro_character = UserProfile.objects.values('ro_character').filter(user=master_id).first()
    if ro_character:
        for char in characters:
            if char['char_id'] == ro_character['ro_character']:
                main_character = char
                break

    return {'characters': characters, 'main_character': main_character, 'count': characters_count} or None
