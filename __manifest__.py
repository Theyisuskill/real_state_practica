{
    'name': "Real state",
    'version': '16.0.1',
    'depends': ['base'],
    'author': "jesus mendoza",
    'category': 'Real state',
    'description': """
    model the Real State
    """,
    # data files always loaded at installation
    'data': [
        'security/ir.model.access.csv',
        'views/estate_property_views.xml',
        'views/state_property_type.xml',
        'views/estate_menu.xml',
        'views/estate_property_offer_views.xml'
    ],  
    # data files containing optionally loaded demonstration data
    'demo': [
        #'demo/demo_data.xml',
    ],
}