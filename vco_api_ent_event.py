from vco_api_main import vco_api_main

class pccwg_vco(vco_api_main):
    def __init__(self):
        super().__init__()

if __name__ == '__main__':
    '''
    Create the VCO client object, and read and write
    the event by calling the respective functions.
    '''
    conn = pccwg_vco()
    # 900 seconds i.e. 15 minutes interval for API calls
    ent_events = conn.get_ent_events(900)
    conn.write_ent_events(ent_events)
