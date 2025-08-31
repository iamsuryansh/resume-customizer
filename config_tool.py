#!/usr/bin/env python3
"""
Configuration Utility for Resume Customizer Tool

This utility helps manage configuration settings and prompts.
"""

import argparse
import sys
from pathlib import Path

from config_manager import ConfigManager


def show_config(config: ConfigManager):
    """Display current configuration."""
    print("📋 Resume Customizer Configuration")
    print("=" * 50)
    
    summary = config.get_config_summary()
    
    print("\n🤖 AI Settings:")
    print(f"  Model: {summary['ai_model']}")
    print(f"  Max Retries: {summary['max_retries']}")
    
    print("\n📁 Paths:")
    print(f"  Templates Directory: {summary['templates_dir']}")
    print(f"  Output Directory: {summary['output_dir']}")
    
    print("\n📄 LaTeX Settings:")
    print(f"  Compiler: {summary['latex_compiler']}")
    print(f"  Compilation Passes: {summary['compilation_passes']}")
    
    print("\n🎯 Customization:")
    print(f"  Focus Areas: {', '.join(summary['focus_areas'])}")
    print(f"  Add Explanations: {summary['add_explanations']}")
    print(f"  Preserve Formatting: {summary['preserve_formatting']}")
    
    print("\n📂 Output Settings:")
    print(f"  Include Timestamp: {summary['include_timestamp']}")
    print(f"  Cleanup Aux Files: {summary['cleanup_aux_files']}")


def set_config_value(config: ConfigManager, setting: str, value: str):
    """Set a configuration value."""
    setting_parts = setting.split('.')
    if len(setting_parts) != 2:
        print("❌ Error: Setting must be in format 'section.key'")
        return False
    
    section, key = setting_parts
    
    try:
        config.update_config(section, key, value)
        print(f"✅ Updated {setting} = {value}")
        return True
    except Exception as e:
        print(f"❌ Error updating configuration: {e}")
        return False


def show_prompt_template(config: ConfigManager):
    """Show the current prompt template."""
    print("📝 Current AI Prompt Template")
    print("=" * 50)
    
    # Build a sample prompt
    sample_resume = "[Your resume content would go here]"
    sample_job = "[Job description would go here]"
    
    prompt = config.build_ai_prompt(sample_resume, sample_job)
    print(prompt)


def edit_prompt_section(config: ConfigManager, section: str, key: str, value: str):
    """Edit a prompt section."""
    try:
        config.update_prompt(section, key, value)
        print(f"✅ Updated prompt {section}.{key}")
        return True
    except Exception as e:
        print(f"❌ Error updating prompt: {e}")
        return False


def list_models():
    """List available AI models."""
    print("🤖 Available AI Models")
    print("=" * 30)
    print("  gemini-1.5-flash    (Fast, general purpose)")
    print("  gemini-1.5-pro      (More capable, slower)")
    print("  gemini-pro          (Legacy, may be deprecated)")
    print("\nNote: Model availability may vary based on your API access.")


def reset_config(config: ConfigManager):
    """Reset configuration to defaults."""
    print("⚠️  This will reset all configuration to defaults.")
    response = input("Are you sure? (y/N): ")
    
    if response.lower() in ['y', 'yes']:
        # Remove config files to force recreation
        if config.config_file.exists():
            config.config_file.unlink()
        if config.prompts_file.exists():
            config.prompts_file.unlink()
        
        # Reload with defaults
        config.load_configurations()
        print("✅ Configuration reset to defaults")
    else:
        print("❌ Reset cancelled")


def validate_config(config: ConfigManager):
    """Validate current configuration."""
    print("🔍 Validating Configuration")
    print("-" * 30)
    
    issues = []
    
    # Check if directories exist
    templates_dir = config.get_templates_dir()
    output_dir = config.get_output_dir()
    
    if not templates_dir.exists():
        issues.append(f"Templates directory not found: {templates_dir}")
    
    # Check for resume template
    resume_template = templates_dir / config.get_resume_template_name()
    if not resume_template.exists():
        issues.append(f"Resume template not found: {resume_template}")
    
    # Check LaTeX compiler
    import shutil
    compiler = config.get_latex_compiler()
    if not shutil.which(compiler):
        issues.append(f"LaTeX compiler not found: {compiler}")
    
    # Report results
    if issues:
        print("❌ Configuration Issues Found:")
        for issue in issues:
            print(f"  • {issue}")
    else:
        print("✅ Configuration is valid")
    
    return len(issues) == 0


def main():
    parser = argparse.ArgumentParser(description="Manage Resume Customizer configuration")
    parser.add_argument('--config-dir', '-d', help="Configuration directory")
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Show configuration
    subparsers.add_parser('show', help='Show current configuration')
    
    # Set configuration value
    set_parser = subparsers.add_parser('set', help='Set configuration value')
    set_parser.add_argument('setting', help='Setting in format section.key')
    set_parser.add_argument('value', help='Value to set')
    
    # Show prompt template
    subparsers.add_parser('prompt', help='Show current prompt template')
    
    # Edit prompt
    edit_parser = subparsers.add_parser('edit-prompt', help='Edit prompt section')
    edit_parser.add_argument('section', help='Prompt section')
    edit_parser.add_argument('key', help='Prompt key')
    edit_parser.add_argument('value', help='New value')
    
    # List models
    subparsers.add_parser('models', help='List available AI models')
    
    # Reset configuration
    subparsers.add_parser('reset', help='Reset configuration to defaults')
    
    # Validate configuration
    subparsers.add_parser('validate', help='Validate current configuration')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    # Initialize configuration
    config_dir = Path(args.config_dir) if args.config_dir else None
    config = ConfigManager(config_dir)
    
    # Execute command
    if args.command == 'show':
        show_config(config)
    elif args.command == 'set':
        set_config_value(config, args.setting, args.value)
    elif args.command == 'prompt':
        show_prompt_template(config)
    elif args.command == 'edit-prompt':
        edit_prompt_section(config, args.section, args.key, args.value)
    elif args.command == 'models':
        list_models()
    elif args.command == 'reset':
        reset_config(config)
    elif args.command == 'validate':
        valid = validate_config(config)
        sys.exit(0 if valid else 1)


if __name__ == "__main__":
    main()
