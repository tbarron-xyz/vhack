#!/usr/bin/env python3
"""
VHACK - Main script for the Very Hackable AI Chatbot Kit.
WARNING: This is a deliberately vulnerable agent for educational purposes.
DO NOT use in production environments!

Provides a command-line interface for testing AI security vulnerabilities.
"""

import sys
import argparse

try:
    from vulnerable_agent_tools import VulnerableAIAgentWithTools
except ImportError:
    print("❌ Error: LangChain not available")
    print("💡 Install with: poetry install")
    sys.exit(1)


def print_vhack_banner():
    """Print VHACK banner and warnings."""
    print("=" * 60)
    print("🚨 VHACK - Very Hackable AI Chatbot Kit 🚨")
    print("=" * 60)
    print("⚠️  WARNING: This is a deliberately vulnerable AI agent!")
    print("⚠️  FOR EDUCATIONAL PURPOSES ONLY!")
    print("⚠️  DO NOT USE IN PRODUCTION!")
    print("=" * 60)
    print()


def print_vulnerability_hints():
    """Print helpful hints for security testing."""
    print("🎯 Vulnerability Testing Hints:")
    print("• Try different authentication methods")
    print("• Look for command execution opportunities") 
    print("• Test for information disclosure")
    print("• Attempt prompt injection and jailbreaking")
    print("• Check for data privacy violations")
    print("• Use different configuration files for various scenarios")
    print("=" * 60)
    print()


def interactive_mode(agent: VulnerableAIAgentWithTools):
    """
    Run the agent in interactive mode.
    
    Args:
        agent: VulnerableAIAgentWithTools instance
    """
    print_vhack_banner()
    
    agent_name = agent.agent_config.get('name', 'Vulnerable AI Agent')
    print(f"🤖 {agent_name} v{agent.agent_config.get('version', '1.0')}")
    print(f"📋 Model: {agent.openrouter_config.get('model')}")
    print(f"🎯 Vulnerable Mode: {'Enabled' if agent.vulnerable_mode else 'Disabled'}")
    print(f"🐛 Debug Mode: {'Enabled' if agent.debug_mode else 'Disabled'}")
    print()
    
    if agent.vulnerable_mode:
        print_vulnerability_hints()
    
    print("💬 Type 'quit', 'exit', or 'bye' to end")
    print("🔄 Type 'clear' to clear conversation history")
    print("ℹ️  Type 'info' to see model information")
    print("📝 Type 'models' to see available models")
    print("🎯 Type 'hints' to see vulnerability hints again")
    print("� Type 'tokens' to check discovered tokens (admin access required)")
    print("-" * 60)
    
    while True:
        try:
            user_input = input("\n👤 You: ").strip()
            
            if not user_input:
                continue
                
            if user_input.lower() in ['quit', 'exit', 'bye']:
                print("👋 Goodbye!")
                break
            elif user_input.lower() == 'clear':
                agent.clear_history()
                print("🗑️  Conversation history cleared!")
                continue
            elif user_input.lower() == 'info':
                info = agent.get_model_info()
                print("ℹ️  Model Information:")
                for key, value in info.items():
                    print(f"   {key}: {value}")
                continue
            elif user_input.lower() == 'models':
                models = agent.get_available_models()
                print("📝 Available models:")
                for model in models:
                    current = " (current)" if model == agent.openrouter_config.get('model') else ""
                    print(f"   - {model}{current}")
                continue
            elif user_input.lower() == 'hints':
                if agent.vulnerable_mode:
                    print_vulnerability_hints()
                else:
                    print("Vulnerable mode not enabled in this configuration.")
                continue
            elif user_input.lower() == 'tokens':
                if agent.admin_authenticated:
                    print("� Discovered tokens:")
                    for key, value in agent.secrets.items():
                        if 'discovery' in key.lower() or 'token' in key.lower():
                            print(f"   {key}: {value}")
                else:
                    print("🔒 Admin authentication required to view tokens.")
                continue
            elif user_input.lower() == 'logs' and agent.debug_mode:
                if hasattr(agent, 'interaction_logs'):
                    print("📋 Interaction logs:")
                    for i, log in enumerate(agent.interaction_logs[-5:], 1):  # Last 5 logs
                        print(f"   {i}. {log['user_message'][:50]}...")
                else:
                    print("No logs available.")
                continue
            
            print("🤖 AI: ", end="", flush=True)
            response = agent.chat(user_input)
            print(response)
            
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")


def single_query_mode(agent: VulnerableAIAgentWithTools, query: str):
    """
    Run a single query and exit.
    
    Args:
        agent: VulnerableAIAgentWithTools instance
        query: The query to ask
    """
    try:
        if agent.vulnerable_mode:
            print("🎯 Vulnerable Mode - Single Query")
        response = agent.chat(query)
        print(response)
    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        sys.exit(1)


def main():
    """Main function."""
    parser = argparse.ArgumentParser(description="VHACK - Very Hackable AI Chatbot Kit")
    parser.add_argument("--config", "-c", default="config.yaml", 
                       help="Path to configuration file (default: config.yaml)")
    parser.add_argument("--query", "-q", 
                       help="Single query mode - ask one question and exit")
    parser.add_argument("--model", "-m", 
                       help="Override model from configuration")
    
    args = parser.parse_args()
    
    try:
        # Initialize the agent
        agent = VulnerableAIAgentWithTools(config_path=args.config)
        
        # Override model if specified
        if args.model:
            agent.set_model(args.model)
        
        # Run in appropriate mode
        if args.query:
            single_query_mode(agent, args.query)
        else:
            interactive_mode(agent)
            
    except FileNotFoundError as e:
        print(f"❌ Configuration file error: {e}", file=sys.stderr)
        sys.exit(1)
    except ValueError as e:
        print(f"❌ Configuration error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"❌ Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()