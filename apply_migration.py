#!/usr/bin/env python3
"""
Test Supabase connection and check existing database schema
"""
import os
import sys
from supabase import create_client, Client

# Supabase credentials
SUPABASE_URL = "https://rbsswyljndnvrjnfexya.supabase.co"
SUPABASE_SERVICE_ROLE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InJic3N3eWxqbmRudnJqbmZleHlhIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc1MzU2OTcyMywiZXhwIjoyMDY5MTQ1NzIzfQ.jCwUfAcgOV3R2XjWp9CpKOqf1_NE8JBRmYJ7RhQTq8o"

def test_database():
    """Test database connection and check existing schema"""
    try:
        # Create Supabase client with service role key
        supabase: Client = create_client(SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY)
        
        print("🔗 Testing Supabase connection...")
        print(f"🌐 URL: {SUPABASE_URL}")
        
        # Test basic connection by trying to access a system table
        try:
            # Check if properties table exists
            result = supabase.table('properties').select('id').limit(1).execute()
            print("✅ Properties table already exists!")
            print(f"📊 Found {len(result.data)} records")
            return True
        except Exception as e:
            if "relation \"public.properties\" does not exist" in str(e):
                print("❌ Properties table does not exist - migration needed")
                
                # Try to check what tables do exist by accessing a known system table
                try:
                    # Check if we can access auth.users (should always exist)
                    auth_result = supabase.table('auth.users').select('id').limit(1).execute()  
                    print("✅ Database connection is working")
                    print("📋 Rental platform migration is required")
                    return False
                except Exception as auth_e:
                    print(f"⚠️  Cannot access auth.users: {str(auth_e)}")
                    # Try a different approach - check basejump tables
                    try:
                        basejump_result = supabase.table('basejump.accounts').select('id').limit(1).execute()
                        print("✅ Database connection is working (basejump accessible)")
                        print("📋 Rental platform migration is required")
                        return False
                    except Exception as basejump_e:
                        print(f"⚠️  Cannot access basejump.accounts: {str(basejump_e)}")
                        print("✅ Basic connection works, but need to apply schema")
                        return False
            else:
                print(f"❌ Unexpected error accessing properties: {str(e)}")
                return False
            
    except Exception as e:
        print(f"❌ Failed to connect to database: {str(e)}")
        return False

def print_migration_instructions():
    """Print instructions for manually applying the migration"""
    print("\n" + "="*60)
    print("📋 MANUAL MIGRATION INSTRUCTIONS")
    print("="*60)
    print("1. Go to: https://supabase.com/dashboard/project/rbsswyljndnvrjnfexya/sql")
    print("2. Open: backend/supabase/migrations/20250127000000_rental_platform_schema.sql")
    print("3. Copy the entire SQL content and paste it into the SQL Editor")
    print("4. Click 'Run' to execute the migration")
    print("5. Verify tables are created: properties, booking_requests, rental_applications, etc.")
    print("="*60)
    
    # Also print the file path for easy access
    migration_file = "backend/supabase/migrations/20250127000000_rental_platform_schema.sql"
    print(f"📄 Migration file location: {migration_file}")

if __name__ == "__main__":
    print("🏠 Krib AI Rental Platform - Database Setup")
    print("="*50)
    
    success = test_database()
    
    if not success:
        print_migration_instructions()
    else:
        print("\n🎉 Database schema is already set up!")
        print("✅ Ready to test rental platform endpoints")
    
    sys.exit(0 if success else 1) 