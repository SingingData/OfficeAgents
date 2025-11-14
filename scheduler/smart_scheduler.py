"""
Smart Virtual Environment Weekly Scheduler
Simple architecture with robust virtual environment support
"""

import schedule
import time
import subprocess
import sys
import os
import logging
from datetime import datetime, timedelta
from pathlib import Path
import json

# ============================================================================
# CONFIGURATION - EDIT THESE VALUES
# ============================================================================

# Your multi-task agent script to run weekly
SCRIPT_PATH = r"C:\path\to\your\multi_task_agent.py"

# Virtual environment path (REQUIRED for reliable execution)
VENV_PATH = r"C:\path\to\your\venv"

# Schedule settings - Multi-task agent runs once weekly
SCHEDULE_DAY = "tuesday"   # tuesday at 7am
SCHEDULE_TIME = "07:00"    # 7:00 AM

# ============================================================================
# SMART SCHEDULER - VIRTUAL ENVIRONMENT FOCUSED
# ============================================================================

class SmartVenvScheduler:
    def __init__(self):
        self.setup_logging()
        self.validate_config()
        self.python_exe = self.get_venv_python()
        self.execution_log_file = "last_execution.json"
        
    def setup_logging(self):
        """Setup logging with rotation"""
        os.makedirs("logs", exist_ok=True)
        log_file = f"logs/scheduler_{datetime.now().strftime('%Y%m%d')}.log"
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler()
            ]
        )
        
    def validate_config(self):
        """Validate configuration before starting"""
        errors = []
        
        # Check script path
        if not SCRIPT_PATH or SCRIPT_PATH == r"C:\path\to\your\weekly_script.py":
            errors.append("❌ SCRIPT_PATH not configured")
        elif not os.path.exists(SCRIPT_PATH):
            errors.append(f"❌ Script not found: {SCRIPT_PATH}")
            
        # Check virtual environment
        if not VENV_PATH or VENV_PATH == r"C:\path\to\your\venv":
            errors.append("❌ VENV_PATH not configured")
        elif not os.path.exists(VENV_PATH):
            errors.append(f"❌ Virtual environment not found: {VENV_PATH}")
        else:
            # Check for Python executable in venv
            venv_python = Path(VENV_PATH) / "Scripts" / "python.exe"
            if not venv_python.exists():
                errors.append(f"❌ Python executable not found in venv: {venv_python}")
        
        if errors:
            print("Configuration Errors:")
            for error in errors:
                print(f"  {error}")
            print("\nPlease edit the configuration at the top of this file.")
            input("Press Enter to exit...")
            sys.exit(1)
    
    def get_venv_python(self):
        """Get the Python executable from the virtual environment"""
        venv_python = Path(VENV_PATH) / "Scripts" / "python.exe"
        
        if venv_python.exists():
            logging.info(f"✓ Using virtual environment Python: {venv_python}")
            return str(venv_python)
        else:
            logging.error(f"❌ Python not found in virtual environment: {venv_python}")
            raise FileNotFoundError(f"Virtual environment Python not found: {venv_python}")
    
    def prepare_venv_environment(self):
        """Prepare environment variables for virtual environment execution"""
        env = os.environ.copy()
        
        # Set virtual environment variables
        env["VIRTUAL_ENV"] = VENV_PATH
        env["PYTHONHOME"] = ""  # Clear PYTHONHOME to avoid conflicts
        
        # Update PATH to include venv Scripts directory
        venv_scripts = str(Path(VENV_PATH) / "Scripts")
        current_path = env.get("PATH", "")
        env["PATH"] = f"{venv_scripts};{current_path}"
        
        # Set Python path
        env["PYTHONPATH"] = str(Path(VENV_PATH) / "Lib" / "site-packages")
        
        logging.info(f"✓ Environment prepared for virtual environment: {VENV_PATH}")
        return env
    
    def get_last_execution_date(self):
        """Get the date of the last successful execution"""
        try:
            if os.path.exists(self.execution_log_file):
                with open(self.execution_log_file, 'r') as f:
                    data = json.load(f)
                    last_execution = datetime.fromisoformat(data['last_execution'])
                    return last_execution
        except Exception as e:
            logging.warning(f"Could not read last execution date: {e}")
        return None
    
    def record_execution_date(self):
        """Record the current execution date"""
        try:
            data = {
                'last_execution': datetime.now().isoformat(),
                'script_path': SCRIPT_PATH,
                'schedule': f"{SCHEDULE_DAY} at {SCHEDULE_TIME}"
            }
            with open(self.execution_log_file, 'w') as f:
                json.dump(data, f, indent=2)
            logging.info(f"✓ Execution date recorded: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        except Exception as e:
            logging.error(f"Failed to record execution date: {e}")
    
    def should_run_this_week(self):
        """Check if the task should run this week (hasn't run in the last 7 days)"""
        last_execution = self.get_last_execution_date()
        
        if last_execution is None:
            logging.info("📅 No previous execution found - task will run")
            return True
        
        # Calculate days since last execution
        days_since_last = (datetime.now() - last_execution).days
        
        if days_since_last >= 7:
            logging.info(f"📅 Last execution was {days_since_last} days ago - task will run")
            return True
        else:
            logging.info(f"📅 Last execution was {days_since_last} days ago - skipping (less than 7 days)")
            return False
    
    def get_last_scheduled_time(self):
        """Get the most recent Tuesday 7 AM that should have occurred"""
        now = datetime.now()
        
        # Find the most recent Tuesday
        days_since_tuesday = (now.weekday() - 1) % 7  # Tuesday is 1 (Monday=0)
        if days_since_tuesday == 0 and now.hour >= 7:
            # It's Tuesday and past 7 AM
            last_tuesday = now.date()
        else:
            # Go back to the most recent Tuesday
            last_tuesday = (now - timedelta(days=days_since_tuesday)).date()
        
        # Create datetime for Tuesday at 7 AM
        scheduled_time = datetime.combine(last_tuesday, datetime.strptime(SCHEDULE_TIME, "%H:%M").time())
        
        return scheduled_time
    
    def check_for_missed_execution(self):
        """Check if we missed a scheduled execution and should run now"""
        last_execution = self.get_last_execution_date()
        last_scheduled = self.get_last_scheduled_time()
        now = datetime.now()
        
        logging.info(f"🔍 Checking for missed execution...")
        logging.info(f"   Last scheduled time: {last_scheduled.strftime('%Y-%m-%d %H:%M:%S')}")
        logging.info(f"   Current time: {now.strftime('%Y-%m-%d %H:%M:%S')}")
        
        # If the scheduled time has passed
        if now >= last_scheduled:
            if last_execution is None:
                logging.info("📅 No previous execution found and scheduled time has passed - will run immediately")
                return True
            elif last_execution < last_scheduled:
                logging.info(f"📅 Last execution ({last_execution.strftime('%Y-%m-%d %H:%M:%S')}) was before scheduled time - will run immediately")
                return True
            else:
                logging.info(f"📅 Already executed after scheduled time - no missed execution")
                return False
        else:
            logging.info(f"📅 Scheduled time hasn't arrived yet - no missed execution")
            return False
    
    def run_weekly_task(self):
        """Execute the weekly task in the virtual environment (with weekly frequency protection)"""
        logging.info("=" * 50)
        logging.info("🚀 Weekly task execution check")
        logging.info(f"📄 Multi-task agent: {SCRIPT_PATH}")
        logging.info(f"🐍 Python: {self.python_exe}")
        logging.info(f"📁 Virtual env: {VENV_PATH}")
        logging.info(f"⏰ Current time: {datetime.now()}")
        
        # Check if we should run this week
        if not self.should_run_this_week():
            logging.info("⏭️  Skipping execution - already ran this week")
            logging.info("=" * 50)
            return
        
        logging.info("✅ Proceeding with weekly execution")
        
        try:
            # Prepare virtual environment
            env = self.prepare_venv_environment()
            
            # Change to script directory for relative imports/paths
            script_dir = os.path.dirname(SCRIPT_PATH) or os.getcwd()
            
            # Execute the multi-task agent
            logging.info("🤖 Starting multi-task agent execution...")
            result = subprocess.run([
                self.python_exe,
                SCRIPT_PATH
            ], 
            capture_output=True, 
            text=True, 
            timeout=3600,  # 1 hour timeout
            cwd=script_dir,
            env=env
            )
            
            # Log results
            if result.returncode == 0:
                logging.info("✅ Multi-task agent completed successfully")
                if result.stdout.strip():
                    logging.info("📤 Agent output:")
                    for line in result.stdout.strip().split('\n'):
                        logging.info(f"   {line}")
                
                # Record successful execution
                self.record_execution_date()
                
            else:
                logging.error(f"❌ Multi-task agent failed with return code: {result.returncode}")
                if result.stderr.strip():
                    logging.error("📤 Error output:")
                    for line in result.stderr.strip().split('\n'):
                        logging.error(f"   {line}")
                
                # Don't record execution date on failure - allow retry next time
                logging.info("⚠️  Execution date not recorded due to failure - will retry next scheduled time")
                        
        except subprocess.TimeoutExpired:
            logging.error("⏰ Multi-task agent timed out after 1 hour")
            logging.info("⚠️  Execution date not recorded due to timeout - will retry next scheduled time")
        except Exception as e:
            logging.error(f"💥 Unexpected error executing multi-task agent: {e}")
            logging.info("⚠️  Execution date not recorded due to error - will retry next scheduled time")
        
        logging.info("🏁 Weekly task execution finished")
        logging.info("=" * 50)
    
    def test_venv_setup(self):
        """Test the virtual environment setup"""
        print("🧪 Testing virtual environment setup...")
        
        try:
            env = self.prepare_venv_environment()
            
            # Test Python version in venv
            result = subprocess.run([
                self.python_exe, "-c", 
                "import sys; print(f'Python {sys.version}'); print(f'Executable: {sys.executable}'); print(f'Virtual env: {sys.prefix}')"
            ], capture_output=True, text=True, env=env, timeout=30)
            
            if result.returncode == 0:
                print("✅ Virtual environment test passed")
                print("📋 Environment details:")
                for line in result.stdout.strip().split('\n'):
                    print(f"   {line}")
                return True
            else:
                print("❌ Virtual environment test failed")
                if result.stderr:
                    print(f"Error: {result.stderr}")
                return False
                
        except Exception as e:
            print(f"❌ Error testing virtual environment: {e}")
            return False
    
    def start(self):
        """Start the smart scheduler"""
        print("🤖 Smart Multi-Task Agent Scheduler")
        print("=" * 50)
        print(f"📄 Multi-task agent: {SCRIPT_PATH}")
        print(f"🐍 Python: {self.python_exe}")
        print(f"📁 Virtual env: {VENV_PATH}")
        print(f"📅 Schedule: Every {SCHEDULE_DAY.title()} at {SCHEDULE_TIME}")
        print(f"📝 Logs: logs/scheduler_{datetime.now().strftime('%Y%m%d')}.log")
        print(f"🔒 Frequency protection: Once per week maximum")
        print(f"🔄 Catch-up: Runs immediately if missed due to computer being off")
        
        # Show last execution info
        last_execution = self.get_last_execution_date()
        if last_execution:
            days_ago = (datetime.now() - last_execution).days
            print(f"📊 Last execution: {last_execution.strftime('%Y-%m-%d %H:%M:%S')} ({days_ago} days ago)")
        else:
            print(f"📊 Last execution: Never")
        
        print("=" * 50)
        
        # Test virtual environment setup
        if not self.test_venv_setup():
            print("\n❌ Virtual environment test failed. Please check your configuration.")
            input("Press Enter to exit...")
            return
        
        # Check for missed execution on startup
        print("\n🔍 Checking for missed executions...")
        if self.check_for_missed_execution():
            print("⚡ Missed execution detected - running multi-task agent immediately!")
            logging.info("⚡ Missed execution detected on startup - running immediately")
            self.run_weekly_task()
        else:
            print("✅ No missed executions - waiting for next scheduled time")
        
        # Schedule the task for future runs
        day_method = getattr(schedule.every(), SCHEDULE_DAY.lower(), None)
        if not day_method:
            print(f"❌ Invalid day: {SCHEDULE_DAY}")
            input("Press Enter to exit...")
            return
            
        day_method.at(SCHEDULE_TIME).do(self.run_weekly_task)
        
        # Show next run time
        next_run = schedule.next_run()
        print(f"\n⏰ Next scheduled execution: {next_run.strftime('%Y-%m-%d %H:%M:%S')}")
        print("\nScheduler is running... Press Ctrl+C to stop")
        print("-" * 50)
        
        logging.info("🚀 Smart scheduler started")
        logging.info(f"📅 Next scheduled execution: {next_run}")
        
        # Main scheduling loop
        try:
            while True:
                schedule.run_pending()
                time.sleep(60)  # Check every minute
        except KeyboardInterrupt:
            print("\n🛑 Scheduler stopped by user")
            logging.info("🛑 Scheduler stopped by user")

def main():
    """Main function"""
    # Check if schedule library is installed
    try:
        import schedule
    except ImportError:
        print("❌ Missing required library!")
        print("Install with: pip install schedule")
        print("Or in your virtual environment: path/to/venv/Scripts/pip install schedule")
        input("Press Enter to exit...")
        return
    
    # Create and start scheduler
    try:
        scheduler = SmartVenvScheduler()
        scheduler.start()
    except Exception as e:
        print(f"❌ Failed to start scheduler: {e}")
        input("Press Enter to exit...")

if __name__ == "__main__":
    main()