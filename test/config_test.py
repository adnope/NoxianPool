from config import get_supabase_client

def test_connection():
    try:
        supabase = get_supabase_client()

        response = supabase.table("your_table_name").select("*").limit(1).execute()
        print("Connection successful!")
        print("Sample response:", response.data)

        return True

    except Exception as e:
        print("Connection failed!")
        print("Error:", str(e))
        return False

if __name__ == "__main__":
    test_connection()
