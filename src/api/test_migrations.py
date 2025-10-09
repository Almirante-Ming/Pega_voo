#!/usr/bin/env python3
"""
Migration safety testing script.
Run this script to safely test migrations without affecting production data.
"""
import os
import sys
from pathlib import Path

# Add the app directory to Python path
sys.path.append(str(Path(__file__).parent))

from app.config.settings import settings
from sqlalchemy import create_engine, text
from alembic.config import Config
from alembic import command
import tempfile
import shutil


def test_migrations_safely():
    """Test migrations against a temporary database."""
    
    print("🔍 Testing migrations safely...")
    
    # Create a temporary database for testing
    original_db_url = settings.database_url
    
    # Parse the original URL to create a test database
    if "postgresql://" in original_db_url:
        base_url = original_db_url.rsplit('/', 1)[0]
        test_db_name = "task_fly_test_migration"
        test_db_url = f"{base_url}/{test_db_name}"
        
        # Create test database
        print(f"📦 Creating test database: {test_db_name}")
        admin_engine = create_engine(f"{base_url}/postgres")
        
        with admin_engine.connect() as conn:
            conn.execute(text("COMMIT"))  # End any existing transaction
            # Drop if exists and create fresh
            conn.execute(text(f"DROP DATABASE IF EXISTS {test_db_name}"))
            conn.execute(text(f"CREATE DATABASE {test_db_name}"))
        
        admin_engine.dispose()
        
        # Test the migrations
        print("🧪 Testing schema migration...")
        test_engine = create_engine(test_db_url)
        
        try:
            # Configure Alembic for test database
            alembic_cfg = Config("alembic.ini")
            alembic_cfg.set_main_option("sqlalchemy.url", test_db_url)
            
            # Run migrations
            print("⬆️  Running upgrade to head...")
            command.upgrade(alembic_cfg, "head")
            
            # Test downgrade
            print("⬇️  Testing downgrade...")
            command.downgrade(alembic_cfg, "base")
            
            # Run upgrade again to test population
            print("⬆️  Running upgrade again with data...")
            command.upgrade(alembic_cfg, "head")
            
            # Verify data exists
            with test_engine.connect() as conn:
                users_count = conn.execute(text("SELECT COUNT(*) FROM usuarios")).scalar()
                flights_count = conn.execute(text("SELECT COUNT(*) FROM voos")).scalar()
                reservations_count = conn.execute(text("SELECT COUNT(*) FROM reservas")).scalar()
                
                print(f"✅ Sample data created successfully:")
                print(f"   Users: {users_count}")
                print(f"   Flights: {flights_count}")
                print(f"   Reservations: {reservations_count}")
            
            print("✅ All migration tests passed!")
            
        except Exception as e:
            print(f"❌ Migration test failed: {e}")
            return False
        
        finally:
            test_engine.dispose()
            
            # Cleanup test database
            print(f"🧹 Cleaning up test database...")
            admin_engine = create_engine(f"{base_url}/postgres")
            with admin_engine.connect() as conn:
                conn.execute(text("COMMIT"))
                conn.execute(text(f"DROP DATABASE IF EXISTS {test_db_name}"))
            admin_engine.dispose()
        
        return True
    
    else:
        print("❌ Only PostgreSQL databases are supported for testing")
        return False


def check_migration_safety():
    """Check for common migration safety issues."""
    
    print("🔍 Checking migration safety...")
    
    issues = []
    
    # Check if .env file exists
    if not Path(".env").exists():
        issues.append("❌ .env file not found - database connection may fail")
    
    # Check if models are importable
    try:
        from app.models.models import Base, Usuario, Voo, Reserva
        print("✅ Models importable")
    except ImportError as e:
        issues.append(f"❌ Cannot import models: {e}")
    
    # Check if settings are loadable
    try:
        db_url = settings.database_url
        if "driver://user:pass@localhost/dbname" in db_url:
            issues.append("❌ Database URL not configured (still using default)")
        else:
            print("✅ Database URL configured")
    except Exception as e:
        issues.append(f"❌ Cannot load settings: {e}")
    
    # Check migration files
    migration_dir = Path("migration/versions")
    if not migration_dir.exists():
        issues.append("❌ Migration directory not found")
    else:
        migration_files = list(migration_dir.glob("*.py"))
        if len(migration_files) < 2:
            issues.append("❌ Expected at least 2 migration files (schema + data)")
        else:
            print(f"✅ Found {len(migration_files)} migration files")
    
    return issues


def main():
    """Main function to run all safety checks."""
    
    print("🚀 Migration Safety Checker")
    print("=" * 50)
    
    # Step 1: Basic safety checks
    issues = check_migration_safety()
    
    if issues:
        print("\n⚠️  Safety Issues Found:")
        for issue in issues:
            print(f"   {issue}")
        print("\n❌ Please fix the issues above before running migrations")
        return False
    
    print("\n✅ Basic safety checks passed!")
    
    # Step 2: Test migrations
    if not test_migrations_safely():
        print("\n❌ Migration testing failed")
        return False
    
    print("\n🎉 All tests passed! Migrations are safe to run.")
    print("\nTo apply migrations to your actual database:")
    print("   alembic upgrade head")
    
    return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)