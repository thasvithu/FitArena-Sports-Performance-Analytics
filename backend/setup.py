"""
FitArena Setup Script
Run this script to set up the project for the first time
"""
import os
import sys
from pathlib import Path
import subprocess

def print_header(text):
    """Print formatted header"""
    print("\n" + "="*80)
    print(f"  {text}")
    print("="*80 + "\n")

def create_directories():
    """Create necessary directories"""
    print_header("Creating Project Directories")
    
    directories = [
        'data/uploads',
        'data/processed',
        'logs',
        'models/saved_models',
        'reports'
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"✓ Created: {directory}")

def create_env_file():
    """Create .env file from template"""
    print_header("Setting Up Environment Variables")
    
    if not Path('.env').exists():
        if Path('.env.example').exists():
            import shutil
            shutil.copy('.env.example', '.env')
            print("✓ Created .env file from template")
            print("⚠ Please edit .env file with your configurations")
        else:
            print("⚠ .env.example not found")
    else:
        print("✓ .env file already exists")

def install_dependencies():
    """Install Python dependencies"""
    print_header("Installing Python Dependencies")
    
    print("Installing packages from requirements.txt...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✓ All dependencies installed successfully")
    except subprocess.CalledProcessError as e:
        print(f"✗ Error installing dependencies: {e}")
        return False
    return True

def initialize_database():
    """Initialize database"""
    print_header("Initializing Database")
    
    try:
        from src.database.connection import init_db
        init_db()
        print("✓ Database initialized successfully")
    except Exception as e:
        print(f"⚠ Could not initialize database: {e}")
        print("  You may need to set up PostgreSQL first")

def verify_installation():
    """Verify installation"""
    print_header("Verifying Installation")
    
    checks = [
        ("pandas", "Data processing"),
        ("numpy", "Numerical computing"),
        ("sklearn", "Machine learning"),
        ("fastapi", "API framework"),
        ("plotly", "Visualization"),
        ("sqlalchemy", "Database ORM"),
    ]
    
    all_ok = True
    for package, description in checks:
        try:
            __import__(package)
            print(f"✓ {package:15} - {description}")
        except ImportError:
            print(f"✗ {package:15} - {description} (NOT FOUND)")
            all_ok = False
    
    return all_ok

def print_next_steps():
    """Print next steps"""
    print_header("Setup Complete! 🎉")
    
    print("Next Steps:\n")
    print("1. Configure your environment:")
    print("   Edit the .env file with your settings\n")
    
    print("2. Explore the data:")
    print("   jupyter notebook notebooks/01_exploratory_data_analysis.ipynb\n")
    
    print("3. Train the models:")
    print("   python train_models.py\n")
    
    print("4. Start the API server:")
    print("   python src/api/main.py")
    print("   Then visit: http://localhost:8000/api/docs\n")
    
    print("5. Run tests:")
    print("   pytest tests/\n")
    
    print("For more information, see README_PROJECT.md")

def main():
    """Main setup function"""
    print_header("FitArena - Sports Performance Analytics Platform")
    print("Welcome to FitArena Setup! 🏃‍♂️\n")
    
    # Check Python version
    if sys.version_info < (3, 8):
        print("✗ Error: Python 3.8 or higher is required")
        print(f"  Current version: {sys.version}")
        return
    
    print(f"✓ Python version: {sys.version.split()[0]}")
    
    # Create directories
    create_directories()
    
    # Create env file
    create_env_file()
    
    # Install dependencies
    if not install_dependencies():
        print("\n⚠ Setup incomplete due to dependency installation errors")
        return
    
    # Initialize database (optional)
    initialize_database()
    
    # Verify installation
    if verify_installation():
        print_next_steps()
    else:
        print("\n⚠ Some packages are missing. Please check the errors above.")

if __name__ == "__main__":
    main()
