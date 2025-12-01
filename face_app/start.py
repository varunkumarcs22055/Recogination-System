"""Simple startup wrapper to avoid interruptions"""
import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import and run the main app
if __name__ == "__main__":
    try:
        import app_perfect
    except KeyboardInterrupt:
        print("\n\n⏹️ Server stopped by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
