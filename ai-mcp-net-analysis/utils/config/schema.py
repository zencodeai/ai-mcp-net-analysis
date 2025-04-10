from schema import Schema, And, Use, Optional

config_schema = Schema({
    'mcp': {
        'name': str,
        'version': str,
        'description': str,
    },
    'logging': {
        'name': str,
        'level': And(str, lambda s: s in ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']),
        "type": And(str, lambda s: s in ['file']),
        Optional('console'): {
            'enabled': bool,
            Optional('format'): And(str, len),
        },
        'file': {
            'enabled': bool,
            Optional('path'): And(str, len),
            Optional('max_size_mb'): And(Use(int), lambda n: n > 0),
            Optional('backup_count'): And(Use(int), lambda n: n >= 0),
            Optional('format'):  And(str, len),
        }
    }
})
