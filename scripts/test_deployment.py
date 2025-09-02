#!/usr/bin/env python3
"""
Test script for Financial Analysis Assistant deployment.

This script tests both local and deployed versions of the application
to ensure everything is working correctly.
"""
import argparse
import json
import os
import sys
import time
from typing import Any, Dict, Optional

# Add project root to Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

import requests


def test_health_endpoint(base_url: str) -> bool:
    """Test the health endpoint."""
    try:
        print(f"🔍 Testing health endpoint: {base_url}/health")
        response = requests.get(f"{base_url}/health", timeout=10)

        if response.status_code == 200:
            health_data = response.json()
            print(f"✅ Health check passed")
            print(f"   Status: {health_data.get('status')}")
            print(f"   Version: {health_data.get('version')}")

            services = health_data.get("services", {})
            for service, status in services.items():
                emoji = "✅" if status == "connected" else "⚠️"
                print(f"   {emoji} {service}: {status}")

            return True
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False

    except Exception as e:
        print(f"❌ Health check error: {e}")
        return False


def test_chat_endpoint(base_url: str, message: str = "Analyze Apple") -> bool:
    """Test the chat API endpoint."""
    try:
        print(f"🔍 Testing chat endpoint with message: '{message}'")

        payload = {"message": message, "session_id": f"test_session_{int(time.time())}"}

        response = requests.post(
            f"{base_url}/api/chat",
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=30,
        )

        if response.status_code == 200:
            chat_data = response.json()
            print(f"✅ Chat API test passed")
            print(f"   Response length: {len(chat_data.get('response', ''))}")
            print(f"   Session ID: {chat_data.get('session_id')}")
            print(f"   Companies: {chat_data.get('companies', [])}")
            print(f"   Analysis type: {chat_data.get('analysis_type')}")

            # Print first 200 characters of response
            response_text = chat_data.get("response", "")
            if response_text:
                preview = (
                    response_text[:200] + "..."
                    if len(response_text) > 200
                    else response_text
                )
                print(f"   Response preview: {preview}")

            return True
        else:
            print(f"❌ Chat API test failed: {response.status_code}")
            try:
                error_data = response.json()
                print(f"   Error: {error_data.get('detail', 'Unknown error')}")
            except Exception:
                print(f"   Error: {response.text}")
            return False

    except Exception as e:
        print(f"❌ Chat API test error: {e}")
        return False


def test_web_interface(base_url: str) -> bool:
    """Test the web interface."""
    try:
        print(f"🔍 Testing web interface: {base_url}/")
        response = requests.get(f"{base_url}/", timeout=10)

        if response.status_code == 200:
            content = response.text
            if (
                "Financial Analysis Assistant" in content
                and "chat-container" in content
            ):
                print(f"✅ Web interface test passed")
                print(f"   Content length: {len(content)} characters")
                return True
            else:
                print(f"❌ Web interface content invalid")
                return False
        else:
            print(f"❌ Web interface test failed: {response.status_code}")
            return False

    except Exception as e:
        print(f"❌ Web interface test error: {e}")
        return False


def test_local_imports() -> bool:
    """Test that all required modules can be imported."""
    try:
        print("🔍 Testing local imports...")

        # Project root should already be in path from module import

        # Test core imports one by one for better error reporting
        try:
            from agents.state import create_initial_state
            print("  ✅ agents.state imported")
        except ImportError as e:
            print(f"  ❌ agents.state import failed: {e}")
            raise

        try:
            from agents.graph import financial_orchestrator
            print("  ✅ agents.graph imported")
        except ImportError as e:
            print(f"  ❌ agents.graph import failed: {e}")
            raise

        try:
            from config.settings import configure_pandas
            print("  ✅ config.settings imported")
        except ImportError as e:
            print(f"  ❌ config.settings import failed: {e}")
            raise

        try:
            from utils.error_handling import setup_logging
            print("  ✅ utils.error_handling imported")
        except ImportError as e:
            print(f"  ❌ utils.error_handling import failed: {e}")
            raise

        print("✅ Core imports successful")

        # Test web app imports
        try:
            from web_app import app

            print("✅ Web app imports successful")
        except ImportError as e:
            print(f"⚠️  Web app imports failed: {e}")
            return False

        # Test GCP imports (optional)
        try:
            from config.gcp_config import get_gcp_config, is_gcp_available

            print("✅ GCP config imports successful")
        except ImportError as e:
            print(f"⚠️  GCP config imports failed: {e}")

        return True

    except Exception as e:
        print(f"❌ Import test error: {e}")
        return False


def test_langgraph_functionality() -> bool:
    """Test basic LangGraph functionality."""
    try:
        print("🔍 Testing LangGraph functionality...")

        # Project root should already be in path from module import

        from agents.graph import financial_orchestrator
        from agents.state import create_initial_state

        # Test conversation start
        state = financial_orchestrator.start_conversation()
        if state and state.get("agent_response"):
            print("✅ LangGraph conversation start successful")

            # Test simple request processing
            test_state = financial_orchestrator.process_user_request("Hello", state)
            if test_state and test_state.get("agent_response"):
                print("✅ LangGraph request processing successful")
                return True
            else:
                print("❌ LangGraph request processing failed")
                return False
        else:
            print("❌ LangGraph conversation start failed")
            return False

    except Exception as e:
        print(f"❌ LangGraph test error: {e}")
        return False


def run_comprehensive_test(base_url: Optional[str] = None) -> Dict[str, bool]:
    """Run comprehensive tests."""
    results = {}

    print("🚀 Starting comprehensive test suite...")
    print("=" * 60)

    # Test local functionality
    print("\n📦 Testing Local Functionality")
    print("-" * 30)
    results["imports"] = test_local_imports()
    results["langgraph"] = test_langgraph_functionality()

    # Test web service if URL provided
    if base_url:
        print(f"\n🌐 Testing Web Service: {base_url}")
        print("-" * 30)
        results["health"] = test_health_endpoint(base_url)
        results["web_interface"] = test_web_interface(base_url)
        results["chat_api"] = test_chat_endpoint(base_url)

        # Additional chat tests
        if results["chat_api"]:
            print("\n🔄 Running additional chat tests...")
            results["chat_comparison"] = test_chat_endpoint(
                base_url, "Compare Apple and Microsoft"
            )
            results["chat_metrics"] = test_chat_endpoint(
                base_url, "Show me Tesla's financial metrics"
            )

    # Summary
    print("\n📊 Test Results Summary")
    print("=" * 60)

    passed = sum(1 for result in results.values() if result)
    total = len(results)

    for test_name, result in results.items():
        emoji = "✅" if result else "❌"
        print(f"{emoji} {test_name.replace('_', ' ').title()}")

    print(f"\nOverall: {passed}/{total} tests passed")

    if passed == total:
        print("🎉 All tests passed! Deployment is working correctly.")
    else:
        print("⚠️  Some tests failed. Check the output above for details.")

    return results


def main():
    """Main test function."""
    parser = argparse.ArgumentParser(
        description="Test Financial Analysis Assistant deployment"
    )
    parser.add_argument(
        "--url", help="Base URL to test (e.g., https://your-service-url)"
    )
    parser.add_argument(
        "--local-only", action="store_true", help="Test only local functionality"
    )
    parser.add_argument(
        "--message", default="Analyze Apple", help="Test message for chat API"
    )

    args = parser.parse_args()

    # Debug information
    print(f"🔍 Debug info:")
    print(f"   Current working directory: {os.getcwd()}")
    print(f"   Project root: {project_root}")
    print(f"   Python path (first 3): {sys.path[:3]}")
    print()

    if args.local_only:
        print("🏠 Running local tests only...")
        results = {
            "imports": test_local_imports(),
            "langgraph": test_langgraph_functionality(),
        }

        passed = sum(1 for result in results.values() if result)
        total = len(results)
        print(f"\nLocal tests: {passed}/{total} passed")

    elif args.url:
        results = run_comprehensive_test(args.url)
    else:
        # Try to detect local server
        local_url = "http://localhost:8080"
        print(f"🔍 No URL provided, trying local server: {local_url}")

        try:
            response = requests.get(f"{local_url}/health", timeout=5)
            if response.status_code == 200:
                print("✅ Local server detected")
                results = run_comprehensive_test(local_url)
            else:
                print("❌ Local server not responding, running local tests only")
                results = run_comprehensive_test()
        except Exception:
            print("❌ Local server not available, running local tests only")
            results = run_comprehensive_test()

    # Exit with appropriate code
    if all(results.values()):
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
