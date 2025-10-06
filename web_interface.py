#!/usr/bin/env python3
"""
VHACK Web Interface - Dynamic configuration with chatbot UI

Flask-based web interface for VHACK with real-time configuration switching.
"""

from flask import Flask, render_template, request, jsonify, session
import json
import os
import uuid
import sys
from datetime import datetime

try:
    from vulnerable_agent_tools import VulnerableAIAgentWithTools
except ImportError:
    print("❌ Error: LangChain not available")
    print("💡 Install with: poetry install")
    sys.exit(1)

from config_loader import ConfigLoader
import threading
import copy

app = Flask(__name__)
app.secret_key = os.urandom(24)

class VHACKWebInterface:
    def __init__(self):
        self.agents = {}  # Store agent instances per session
        self.base_config_path = "config.yaml"
        self.config_loader = ConfigLoader(self.base_config_path)
        self.security_levels = self._load_security_levels()
        
    def _load_security_levels(self):
        """Define security levels"""
        return {
            "low": {
                "name": "Low Security",
                "description": "All vulnerabilities enabled, maximum exploitation potential",
                "vulnerabilities": {
                    "prompt_injection": True,
                    "information_disclosure": True,
                    "command_injection": True,
                    "jailbreaking": True,
                    "social_engineering": True,
                    "privilege_escalation": True,
                    "ssrf": True
                },
                "behavior": {
                    "enable_command_execution": True,
                    "log_all_interactions": True,
                    "admin_password": "admin123",
                    "debug_mode": True,
                    "temperature": 0.9
                }
            },
            "medium": {
                "name": "Medium Security", 
                "description": "Some protections enabled, moderate exploitation difficulty",
                "vulnerabilities": {
                    "prompt_injection": True,
                    "information_disclosure": True,
                    "command_injection": False,
                    "jailbreaking": True,
                    "social_engineering": True,
                    "privilege_escalation": False,
                    "ssrf": False
                },
                "behavior": {
                    "enable_command_execution": False,
                    "log_all_interactions": True,
                    "admin_password": "complex_admin_pass_2024!",
                    "debug_mode": False,
                    "temperature": 0.7
                }
            },
            "high": {
                "name": "High Security",
                "description": "Most protections enabled, difficult exploitation",
                "vulnerabilities": {
                    "prompt_injection": False,
                    "information_disclosure": False,
                    "command_injection": False,
                    "jailbreaking": True,
                    "social_engineering": False,
                    "privilege_escalation": False,
                    "ssrf": False
                },
                "behavior": {
                    "enable_command_execution": False,
                    "log_all_interactions": False,
                    "admin_password": "ultra_secure_admin_password_2024_#$%",
                    "debug_mode": False,
                    "temperature": 0.3
                }
            },
            "impossible": {
                "name": "Impossible Security",
                "description": "All protections enabled, should be unexploitable",
                "vulnerabilities": {
                    "prompt_injection": False,
                    "information_disclosure": False,
                    "command_injection": False,
                    "jailbreaking": False,
                    "social_engineering": False,
                    "privilege_escalation": False,
                    "ssrf": False
                },
                "behavior": {
                    "enable_command_execution": False,
                    "log_all_interactions": False,
                    "admin_password": "impossible_to_guess_admin_password_2024_#$%^&*()_+",
                    "debug_mode": False,
                    "temperature": 0.1
                }
            }
        }
    
    def get_session_id(self):
        """Get or create session ID"""
        if 'session_id' not in session:
            session['session_id'] = str(uuid.uuid4())
        return session['session_id']
    
    def get_agent(self, session_id, config_updates=None):
        """Get or create agent for session"""
        if session_id not in self.agents or config_updates:
            # Create new agent with updated config
            if config_updates:
                # Create temporary config file for this session
                temp_config = copy.deepcopy(self.config_loader.config)
                
                # Apply security level
                if 'security_level' in config_updates:
                    security_level = config_updates['security_level']
                    level_config = self.security_levels[security_level]
                    
                    # Set the security level in config
                    temp_config['security_level'] = security_level
                    
                    # Apply security level settings
                    temp_config['vulnerabilities'].update(level_config['vulnerabilities'])
                    temp_config['behavior'].update(level_config['behavior'])
                
                # Apply custom vulnerability settings
                if 'vulnerabilities' in config_updates:
                    temp_config['vulnerabilities'].update(config_updates['vulnerabilities'])
                
                # Apply custom behavior settings
                if 'behavior' in config_updates:
                    temp_config['behavior'].update(config_updates['behavior'])
                
                # Save temp config and create agent
                temp_config_path = f"temp_config_{session_id}.yaml"
                with open(temp_config_path, 'w') as f:
                    import yaml
                    yaml.dump(temp_config, f)
                
                self.agents[session_id] = VulnerableAIAgentWithTools(temp_config_path)
                
                # Clean up temp file
                os.remove(temp_config_path)
            else:
                self.agents[session_id] = VulnerableAIAgentWithTools(self.base_config_path)
        
        return self.agents[session_id]

# Global interface instance
vhack_interface = VHACKWebInterface()

@app.route('/')
def index():
    """Main chatbot interface"""
    return render_template('index.html')

@app.route('/api/config')
def get_config():
    """Get current configuration"""
    session_id = vhack_interface.get_session_id()
    
    # Get current security level from session or default to 'low'
    current_level = session.get('security_level', 'low')
    
    return jsonify({
        'security_levels': vhack_interface.security_levels,
        'current_level': current_level,
        'current_config': vhack_interface.security_levels[current_level]
    })

@app.route('/api/config', methods=['POST'])
def update_config():
    """Update agent configuration"""
    session_id = vhack_interface.get_session_id()
    config_updates = request.json
    
    # Store security level in session
    if 'security_level' in config_updates:
        session['security_level'] = config_updates['security_level']
    
    # Update agent with new configuration
    vhack_interface.get_agent(session_id, config_updates)
    
    return jsonify({'status': 'success', 'message': 'Configuration updated'})

@app.route('/api/chat', methods=['POST'])
def chat():
    """Handle chat messages"""
    session_id = vhack_interface.get_session_id()
    user_message = request.json.get('message', '')
    
    if not user_message:
        return jsonify({'error': 'No message provided'}), 400
    
    try:
        # Get agent for current session
        agent = vhack_interface.get_agent(session_id)
        
        # Get response from agent
        response = agent.chat(user_message)
        
        # Log interaction (for security analysis)
        log_interaction(session_id, user_message, response)
        
        return jsonify({
            'response': response,
            'timestamp': datetime.now().isoformat(),
            'vulnerabilities_triggered': agent.last_vulnerabilities_triggered if hasattr(agent, 'last_vulnerabilities_triggered') else []
        })
        
    except Exception as e:
        return jsonify({'error': f'Chat error: {str(e)}'}), 500

@app.route('/api/reset')
def reset_session():
    """Reset current session"""
    session_id = vhack_interface.get_session_id()
    
    # Remove agent from memory
    if session_id in vhack_interface.agents:
        del vhack_interface.agents[session_id]
    
    # Clear session data
    session.clear()
    
    return jsonify({'status': 'success', 'message': 'Session reset'})

@app.route('/api/scenarios')
def get_scenarios():
    """Get available vulnerability scenarios"""
    scenarios = {
        'research': {
            'name': 'Research Assistant',
            'description': 'AI assistant for academic research with access to databases'
        },
        'finance': {
            'name': 'Financial Advisor',
            'description': 'AI assistant with access to financial data and transactions'
        },
        'medical': {
            'name': 'Medical Assistant', 
            'description': 'AI assistant with patient data and medical records'
        },
        'sysadmin': {
            'name': 'System Administrator',
            'description': 'AI assistant with server access and administrative privileges'
        },
        'creative': {
            'name': 'Creative Assistant',
            'description': 'AI assistant for creative writing and content generation'
        }
    }
    return jsonify(scenarios)

def log_interaction(session_id, user_message, agent_response):
    """Log user interactions for security analysis"""
    log_entry = {
        'timestamp': datetime.now().isoformat(),
        'session_id': session_id,
        'user_message': user_message,
        'agent_response': agent_response,
        'security_level': session.get('security_level', 'low')
    }
    
    # Append to log file
    with open('interaction_logs.jsonl', 'a') as f:
        f.write(json.dumps(log_entry) + '\n')

if __name__ == '__main__':
    print("🚨 VHACK Web Interface Starting...")
    print("⚠️  WARNING: This is a deliberately vulnerable application!")
    print("⚠️  FOR EDUCATIONAL PURPOSES ONLY!")
    print("🌐 Access at: http://localhost:5000")
    print("=" * 50)
    
    app.run(debug=True, host='0.0.0.0', port=5000)