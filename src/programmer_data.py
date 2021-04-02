
processor_list = [
    # K42 F
    '18F24K42',
    '18F25K42',
    '18F26K42',
    '18F27K42',
    '18F45K42',
    '18F46K42',
    '18F47K42',
    '18F55K42',
    '18F56K42',
    '18F57K42',
    # K42 LF
    '18LF24K42',
    '18LF25K42',
    '18LF26K42',
    '18LF27K42',
    '18LF45K42',
    '18LF46K42',
    '18LF47K42',
    '18LF55K42',
    '18LF56K42',
    '18LF57K42',
    # Q43
    '18F24Q43',
    '18F25Q43',
    '18F26Q43',
    '18F27Q43',
    '18F45Q43',
    '18F46Q43',
    '18F47Q43',
    '18F55Q43',
    '18F56Q43',
    '18F57Q43',
]


programmer_list = {
    'PICkit4': {
        'command':'ipecmd',
        'target': '-P',
        'source': '-F',
        'flags': [
            '-TPPK4',
            '-M'
        ],
        'garbage': [
            'log.*',
            'MPLABXLog.xml',
            'MPLABXLog.xml*',
        ]
    }, 
    'ICD-U80': {
        'command':'ccsloader',
        'target': '-DEVICE=PIC',
        'source': '-WRITE=',
        'flags': [
            '-AREAS=ALL',
            '-POWER=TARGET'
        ],
        'garbage': []
    },
}