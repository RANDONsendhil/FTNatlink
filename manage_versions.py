#!/usr/bin/env python3
"""
Package Version Manager
Manages versions for natlink packages from configuration file
Provides environment variables and installation helpers with variable substitution
"""

import yaml
import sys
import os
import subprocess
from pathlib import Path
import tempfile
import shutil


class PackageVersionManager:
    def __init__(self, config_file="package_config.yaml"):
        self.config_file = Path(config_file)
        self.config = self.load_config()

    def load_config(self):
        """Load configuration from YAML file"""
        if not self.config_file.exists():
            raise FileNotFoundError(f"Config file {self.config_file} not found")

        with open(self.config_file, "r") as f:
            return yaml.safe_load(f)

    def get_version(self, package_name):
        """Get version for a specific package"""
        return self.config["versions"].get(package_name, "1.0.0")

    def get_environment_variables(self):
        """Get environment variables for version substitution"""
        env_vars = {
            "NATLINK_VERSION": self.get_version("natlink"),
            "NATLINKCORE_VERSION": self.get_version("natlinkcore"),
            "DTACTIONS_VERSION": self.get_version("dtactions"),
        }
        return env_vars

    def create_temp_package_with_versions(self, package_path, package_name):
        """Create a temporary copy of package with versions substituted"""
        package_dir = Path(package_path)
        if not package_dir.exists():
            raise FileNotFoundError(f"Package directory {package_dir} not found")

        # Create temporary directory
        temp_dir = Path(tempfile.mkdtemp(prefix=f"{package_name}_"))

        # Copy package to temp directory
        temp_package = temp_dir / package_dir.name
        shutil.copytree(package_dir, temp_package)

        # Find and update pyproject.toml
        pyproject_file = temp_package / "pyproject.toml"
        if pyproject_file.exists():
            self.substitute_variables_in_file(pyproject_file)

        return temp_package

    def substitute_variables_in_file(self, file_path):
        """Substitute version variables in a file"""
        env_vars = self.get_environment_variables()

        with open(file_path, "r") as f:
            content = f.read()

        # Substitute all environment variables
        for var_name, var_value in env_vars.items():
            content = content.replace(f"${{{var_name}}}", var_value)

        with open(file_path, "w") as f:
            f.write(content)

    def install_package_with_versions(self, package_path, package_name, editable=True):
        """Install package with version substitution"""
        print(
            f"📦 Installing {package_name} with version {self.get_version(package_name)}"
        )

        try:
            package_dir = Path(package_path)
            if not package_dir.exists():
                raise FileNotFoundError(f"Package directory {package_dir} not found")

            # For editable installs, substitute variables in place temporarily
            pyproject_file = package_dir / "pyproject.toml"
            backup_content = None

            if pyproject_file.exists():
                # Backup original content
                with open(pyproject_file, "r") as f:
                    backup_content = f.read()

                # Substitute variables
                self.substitute_variables_in_file(pyproject_file)

            # Build pip install command
            cmd = [sys.executable, "-m", "pip", "install"]
            if editable:
                cmd.append("-e")
            cmd.append(str(package_dir))

            # Run installation
            result = subprocess.run(cmd, capture_output=True, text=True)

            # Restore original content
            if backup_content and pyproject_file.exists():
                with open(pyproject_file, "w") as f:
                    f.write(backup_content)

            if result.returncode == 0:
                print(f"✅ Successfully installed {package_name}")
                return True
            else:
                print(f"❌ Failed to install {package_name}")
                print(f"Error: {result.stderr}")
                return False

        except Exception as e:
            print(f"❌ Error installing {package_name}: {e}")
            # Restore backup if error occurred
            if (
                "backup_content" in locals()
                and backup_content
                and pyproject_file.exists()
            ):
                with open(pyproject_file, "w") as f:
                    f.write(backup_content)
            return False

    def install_all_packages(self, editable=True):
        """Install all packages with version management"""
        package_configs = [
            ("packages/dtactions", "dtactions"),
            ("packages/natlink/pythonsrc", "natlink"),
            ("packages/natlinkcore", "natlinkcore"),
        ]

        success_count = 0
        for package_path, package_name in package_configs:
            if Path(package_path).exists():
                if self.install_package_with_versions(
                    package_path, package_name, editable
                ):
                    success_count += 1
            else:
                print(f"⚠️  {package_path} not found, skipping {package_name}")

        print(
            f"\n🎯 Installation complete: {success_count}/{len(package_configs)} packages installed"
        )
        return success_count == len(package_configs)

    def install_dependencies(self, dep_type="core"):
        """Install dependencies from YAML configuration"""
        if (
            "dependencies" not in self.config
            or dep_type not in self.config["dependencies"]
        ):
            print(f"⚠️  No {dep_type} dependencies configured")
            return True

        deps = self.config["dependencies"][dep_type]
        print(f"📦 Installing {dep_type} dependencies...")

        cmd = [sys.executable, "-m", "pip", "install"] + deps
        result = subprocess.run(cmd, capture_output=True, text=True)

        if result.returncode == 0:
            print(f"✅ {dep_type.title()} dependencies installed successfully")
            return True
        else:
            print(f"❌ Failed to install {dep_type} dependencies")
            print(f"Error: {result.stderr}")
            return False

    def run_installation_script(self, script_name):
        """Run a custom installation script from YAML config"""
        if "scripts" not in self.config or script_name not in self.config["scripts"]:
            print(f"⚠️  Script '{script_name}' not found in configuration")
            return True

        script = self.config["scripts"][script_name]
        print(f"🔧 Running script: {script_name}")

        # Write script to temporary file and execute
        import tempfile

        with tempfile.NamedTemporaryFile(mode="w", suffix=".bat", delete=False) as f:
            f.write(script)
            temp_script = f.name

        try:
            result = subprocess.run(
                [temp_script], shell=True, capture_output=True, text=True
            )
            if result.returncode == 0:
                print(f"✅ Script '{script_name}' completed successfully")
                return True
            else:
                print(f"❌ Script '{script_name}' failed")
                print(f"Error: {result.stderr}")
                return False
        finally:
            Path(temp_script).unlink(missing_ok=True)

    def install_all_from_config(self):
        """Complete installation process using YAML configuration"""
        print("🚀 Starting YAML-configured installation process")
        print("=" * 60)

        success = True

        # 1. Install core dependencies first
        if not self.install_dependencies("core"):
            success = False

        # 2. Install packages in configured order
        install_config = self.config.get("installation", {})
        install_order = install_config.get(
            "order", ["dtactions", "natlink", "natlinkcore"]
        )
        editable = install_config.get("editable", True)

        print(f"\n📦 Installing packages in order: {', '.join(install_order)}")

        for package_name in install_order:
            package_config = install_config.get("packages", {}).get(package_name, {})
            package_path = package_config.get("path", f"packages/{package_name}")

            # Run pre-install commands
            pre_commands = package_config.get("pre_install_commands", [])
            for cmd in pre_commands:
                print(f"🔧 Pre-install: {cmd}")
                subprocess.run(cmd, shell=True)

            # Install the package
            if not self.install_package_with_versions(
                package_path, package_name, editable
            ):
                success = False

            # Run post-install commands
            post_commands = package_config.get("post_install_commands", [])
            for cmd in post_commands:
                print(f"🔧 Post-install: {cmd}")
                subprocess.run(cmd, shell=True)

        # 3. Install development dependencies if requested
        if success:
            print(f"\n🎯 YAML-configured installation complete!")
            print("=" * 60)

            # Run test script if available
            if "test_installation" in self.config.get("scripts", {}):
                print("🧪 Running installation tests...")
                self.run_installation_script("test_installation")

        return success

    def show_versions(self):
        """Display current version configuration"""
        print("📦 Package Versions Configuration:")
        print("=" * 50)
        for package, version in self.config["versions"].items():
            if package in ["natlink", "natlinkcore", "dtactions"]:
                print(f"🔧 {package:15} : {version}")
        print("=" * 50)

        print("\n🌍 Environment Variables:")
        print("=" * 50)
        env_vars = self.get_environment_variables()
        for var_name, var_value in env_vars.items():
            print(f"{var_name:20} = {var_value}")
        print("=" * 50)

    def export_environment(self):
        """Export environment variables for shell"""
        env_vars = self.get_environment_variables()

        print("# Environment variables for package versions")
        print("# Source this file or copy these exports:")
        for var_name, var_value in env_vars.items():
            print(f"export {var_name}={var_value}")


def main():
    """Main function"""
    manager = PackageVersionManager()

    if len(sys.argv) > 1:
        command = sys.argv[1]

        if command == "show":
            manager.show_versions()
        elif command == "install":
            editable = "--no-editable" not in sys.argv
            manager.install_all_packages(editable=editable)
        elif command == "install-yaml":
            manager.install_all_from_config()
        elif command == "install-deps":
            dep_type = sys.argv[2] if len(sys.argv) > 2 else "core"
            manager.install_dependencies(dep_type)
        elif command == "run-script" and len(sys.argv) > 2:
            script_name = sys.argv[2]
            manager.run_installation_script(script_name)
        elif command == "install-package" and len(sys.argv) > 2:
            package_name = sys.argv[2]
            package_path = f"packages/{package_name}"
            if package_name == "natlink":
                package_path = "packages/natlink/pythonsrc"
            editable = "--no-editable" not in sys.argv
            manager.install_package_with_versions(package_path, package_name, editable)
        elif command == "env":
            manager.export_environment()
        else:
            print(
                "Usage: python manage_versions.py [show|install|install-yaml|install-deps|run-script|install-package <name>|env]"
            )
            print("Options:")
            print("  --no-editable    Install in non-editable mode")
            print("\nNew YAML-based commands:")
            print("  install-yaml     - Complete installation using YAML configuration")
            print(
                "  install-deps     - Install dependencies (core|development|documentation)"
            )
            print("  run-script       - Run custom script from YAML configuration")
    else:
        print("🔧 Package Version Manager")
        print("=" * 40)
        manager.show_versions()
        print("\nCommands:")
        print("  show              - Show current versions")
        print("  install           - Install all packages with version substitution")
        print("  install-yaml      - Complete YAML-configured installation process")
        print("  install-deps      - Install specific dependency group")
        print("  install-package   - Install specific package")
        print("  run-script        - Run custom installation script")
        print("  env               - Export environment variables")
        print("\nOptions:")
        print("  --no-editable     - Install in non-editable mode")


if __name__ == "__main__":
    main()
