# supabase_init.py
from supabase import create_client, Client

def init_supabase():
    """
    Initializes and returns a Supabase client.
    Returns:
        supabase (Client) - The initialized Supabase client object.
    """

    # Required credentials
    url = "https://koqyhknkbtaddcdvltwl.supabase.co"
    key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImtvcXloa25rYnRhZGRjZHZsdHdsIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDQxNzU1MDcsImV4cCI6MjA1OTc1MTUwN30.bJuzz1W-p1oAz9FAa8CTvJgKUSmIIC3D6plcUlM5XIo"

    supabase: Client = create_client(url, key)
    return supabase
