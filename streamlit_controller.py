import streamlit as st
import subprocess
import time
import psutil
import os
from datetime import datetime

st.set_page_config(page_title="LiveKit Agent Controller", page_icon="🎙️", layout="wide")

# Initialize session state
if 'agent_process' not in st.session_state:
    st.session_state.agent_process = None

def is_agent_running():
    """Check if agent process is still running"""
    if st.session_state.agent_process:
        return st.session_state.agent_process.poll() is None
    return False

def start_agent():
    """Start the agent in dev mode for cloud deployment"""
    try:
        cmd = ["python", "agent_groq.py", "dev"]
        st.session_state.agent_process = subprocess.Popen(
            cmd, 
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE,
            text=True,
            cwd=os.getcwd()
        )
        return True
    except Exception as e:
        st.error(f"Failed to start agent: {e}")
        return False

def stop_agent():
    """Stop the running agent"""
    if st.session_state.agent_process:
        st.session_state.agent_process.terminate()
        st.session_state.agent_process = None
        return True
    return False

def get_agent_logs():
    """Get recent logs from agent"""
    if st.session_state.agent_process:
        try:
            # Read available output (non-blocking)
            output = st.session_state.agent_process.stdout.readline()
            error_output = st.session_state.agent_process.stderr.readline()
            
            if output:
                return f"OUT: {output.strip()}"
            elif error_output:
                return f"ERR: {error_output.strip()}"
        except Exception as e:
            return f"LOG ERROR: {e}"
    return None

# Main UI
st.title("🎙️ LiveKit Voice Agent Controller")
st.markdown("Control and monitor your LiveKit voice agent")

# Status section
running = is_agent_running()
if running:
    st.success("🟢 Agent Running")
else:
    st.error("🔴 Agent Stopped")

# Control section
st.header("🎮 Agent Control")

col1, col2 = st.columns(2)

with col1:
    if st.button("▶️ Start Agent", disabled=running, type="primary"):
        with st.spinner("Starting agent..."):
            if start_agent():
                st.success("Agent started!")
                time.sleep(1)
                st.rerun()
            else:
                st.error("Failed to start agent")

with col2:
    if st.button("⏹️ Stop Agent", disabled=not running, type="secondary"):
        if stop_agent():
            st.success("Agent stopped!")
            time.sleep(1)
            st.rerun()

# Usage instructions
st.header("📚 How to Use")

if running:
    st.info("""
    **Agent is Running in Development Mode:**
    - Agent is waiting for connections via LiveKit
    - Use the LiveKit Agents Playground to test
    - Connect via web interface at: https://agents.livekit.io/
    """)
    st.markdown("🌐 [Open Agents Playground](https://agents.livekit.io/)")
else:
    st.warning("**Agent Not Running**")
    st.write("Click 'Start Agent' to deploy the voice agent and make it available for connections.")

# Environment check
st.header("⚙️ Environment Status")
env_vars = {
    "GROQ_API_KEY": os.getenv("GROQ_API_KEY"),
    "CARTESIA_API_KEY": os.getenv("CARTESIA_API_KEY"),
    "LIVEKIT_URL": os.getenv("LIVEKIT_URL"),
    "LIVEKIT_API_KEY": os.getenv("LIVEKIT_API_KEY"),
    "LIVEKIT_API_SECRET": os.getenv("LIVEKIT_API_SECRET")
}

for var, value in env_vars.items():
    if value:
        st.success(f"✅ {var} configured")
    else:
        st.error(f"❌ {var} missing")

# Debug and Logs section
st.header("🔍 Debug Information")

# Show agent process status
if st.session_state.agent_process:
    poll_result = st.session_state.agent_process.poll()
    if poll_result is None:
        st.success(f"✅ Process running (PID: {st.session_state.agent_process.pid})")
    else:
        st.error(f"❌ Process exited with code: {poll_result}")
        # Show error output if process failed
        try:
            stderr_output = st.session_state.agent_process.stderr.read()
            if stderr_output:
                st.code(f"Error output: {stderr_output}", language="text")
        except:
            pass
else:
    st.info("No agent process started")

# Logs section (if running)
if running:
    st.header("📋 Agent Logs")
    log_container = st.empty()
    
    # Auto-refresh logs
    logs = get_agent_logs()
    if logs:
        log_container.code(logs)
    
    # Auto-refresh every 2 seconds
    if st.checkbox("Auto-refresh logs"):
        time.sleep(2)
        st.rerun()

# Footer
st.markdown("---")
st.markdown("💡 **Tip**: Make sure all environment variables are configured before starting the agent!") 
