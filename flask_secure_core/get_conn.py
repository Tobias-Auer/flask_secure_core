
_connection_manager = None

def get_connection_manager():
    print("\n\n\n\n\n\n\n\nDEBUGGGGGG: ", _connection_manager)
    return _connection_manager

def set_connection_manager(manager):
    global _connection_manager
    _connection_manager = manager
    print("DEBUGGGGGG set: ", _connection_manager)