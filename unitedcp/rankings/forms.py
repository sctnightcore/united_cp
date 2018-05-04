from django import forms


class JobSearchForm(forms.Form):

    CLASSES = (
        ('All', 'All'),
        (0, 'Novice'),
        (1, 'Swordsman'),
        (2, 'Magician'),
        (3, 'Archer'),
        (4, 'Acolyte'),
        (5, 'Merchant'),
        (6, 'Thief'),
        (7, 'Knight'),
        (8, 'Priest'),
        (9, 'Wizard'),
        (10, 'Blacksmith'),
        (11, 'Hunter'),
        (12, 'Assassin'),
        (14, 'Crusader'),
        (15, 'Monk'),
        (16, 'Sage'),
        (17, 'Rogue'),
        (18, 'Alchemist'),
        (19, 'Bard'),
        (20, 'Dancer'),
        (23, 'Super Novice'),
        (24, 'Gunslinger'),
        (25, 'Ninja'),
        (4046, 'Taekwon'),
        (4047, 'Star Gladiator'),
        (4049, 'Soul Linker'),
        (4008, 'Lord Knight'),
        (4009, 'High Priest'),
        (4010, 'High Wizard'),
        (4011, 'Whitesmith'),
        (4012, 'Sniper'),
        (4013, 'Assassin Cross'),
        (4015, 'Paladin'),
        (4016, 'Champion'),
        (4017, 'Professor'),
        (4018, 'Stalker'),
        (4019, 'Creator'),
        (4020, 'Clown'),
        (4021, 'Gypsy'),
    )

    class_filter = forms.CharField(
        max_length=150,
        label='Filter by class',
        widget=forms.Select(
            attrs={
                'required': True,
                'class': 'form-control class_filter pull-right',
                'name': 'class_filter'
            },
            choices=CLASSES
        ),

    )
