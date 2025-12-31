#!/usr/bin/env python3
"""
System Test Script for SilentVoice Application
Tests both frontend and backend functionality
"""

import asyncio
import json
import time
import requests
import websockets
from typing import Dict, Any, List

# Configuration
BACKEND_URL = "http://localhost:8000"
WS_URL = "ws://localhost:8000/api/v1/ws/sign"
FRONTEND_URL = "http://localhost:3000"

# Test data - sample hand landmarks for "HELLO" gesture
SAMPLE_HAND_LANDMARKS = [
    {"x": 0.5, "y": 0.3, "z": 0.0} for _ in range(21)
]

# Colors for output
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    END = '\033[0m'

def print_test(name: str, passed: bool, details: str = ""):
    """Print test result with color coding"""
    status = f"{Colors.GREEN}✓ PASSED{Colors.END}" if passed else f"{Colors.RED}✗ FAILED{Colors.END}"
    print(f"  {status} - {name}")
    if details and not passed:
        print(f"    {Colors.YELLOW}Details: {details}{Colors.END}")

def test_backend_health():
    """Test backend health endpoint"""
    try:
        response = requests.get(f"{BACKEND_URL}/api/v1/health", timeout=5)
        passed = response.status_code == 200
        print_test("Backend Health Check", passed, str(response.status_code))
        return passed
    except Exception as e:
        print_test("Backend Health Check", False, str(e))
        return False

def test_training_stats():
    """Test training stats endpoint"""
    try:
        response = requests.get(f"{BACKEND_URL}/api/v1/training/stats", timeout=5)
        passed = response.status_code == 200
        data = response.json()
        print_test("Training Stats API", passed)
        if passed:
            print(f"    Total samples: {data.get('total_samples', 0)}")
            print(f"    Gestures: {list(data.get('gestures', {}).keys())}")
        return passed
    except Exception as e:
        print_test("Training Stats API", False, str(e))
        return False

async def test_websocket_connection():
    """Test WebSocket connection and sign recognition"""
    try:
        async with websockets.connect(WS_URL) as websocket:
            # Test connection
            print_test("WebSocket Connection", True)
            
            # Send test hand landmarks
            test_data = {
                "type": "holistic",
                "data": {
                    "rightHandLandmarks": SAMPLE_HAND_LANDMARKS,
                    "leftHandLandmarks": None,
                    "poseLandmarks": None,
                    "faceLandmarks": None
                },
                "timestamp": int(time.time() * 1000)
            }
            
            await websocket.send(json.dumps(test_data))
            
            # Wait for response
            response = await asyncio.wait_for(websocket.recv(), timeout=5.0)
            response_data = json.loads(response)
            
            # Check if we got a prediction
            if response_data.get("type") == "prediction":
                sign = response_data.get("sign", "UNKNOWN")
                confidence = response_data.get("confidence", 0)
                print_test("Sign Recognition", True)
                print(f"    Recognized: {sign} (confidence: {confidence:.2%})")
                return True
            else:
                print_test("Sign Recognition", False, "No prediction received")
                return False
                
    except asyncio.TimeoutError:
        print_test("WebSocket Response", False, "Timeout waiting for response")
        return False
    except Exception as e:
        print_test("WebSocket Connection", False, str(e))
        return False

async def test_speech_to_sign():
    """Test speech to sign conversion"""
    try:
        async with websockets.connect(WS_URL) as websocket:
            # Send test speech
            test_data = {
                "type": "speech",
                "text": "hello thank you",
                "timestamp": int(time.time() * 1000)
            }
            
            await websocket.send(json.dumps(test_data))
            
            # Wait for response
            response = await asyncio.wait_for(websocket.recv(), timeout=5.0)
            response_data = json.loads(response)
            
            # Check if we got signs
            if response_data.get("type") == "signs":
                signs = response_data.get("signs", [])
                print_test("Speech to Sign", True)
                print(f"    Signs: {' → '.join(signs)}")
                return True
            else:
                print_test("Speech to Sign", False, "No signs received")
                return False
                
    except Exception as e:
        print_test("Speech to Sign", False, str(e))
        return False

def test_upload_training_data():
    """Test training data upload"""
    try:
        # Create sample training data
        training_data = {
            "gesture": "TEST_HELLO",
            "frames": [
                {
                    "leftHandLandmarks": None,
                    "rightHandLandmarks": SAMPLE_HAND_LANDMARKS,
                    "timestamp": int(time.time() * 1000)
                }
                for _ in range(10)
            ],
            "duration": 3.0,
            "timestamp": int(time.time())
        }
        
        response = requests.post(
            f"{BACKEND_URL}/api/v1/training/upload",
            json=training_data,
            timeout=5
        )
        
        passed = response.status_code == 200
        print_test("Training Data Upload", passed, str(response.status_code))
        return passed
        
    except Exception as e:
        print_test("Training Data Upload", False, str(e))
        return False

def test_frontend_availability():
    """Check if frontend is accessible"""
    try:
        response = requests.get(FRONTEND_URL, timeout=5)
        passed = response.status_code == 200
        print_test("Frontend Availability", passed, str(response.status_code))
        return passed
    except Exception as e:
        print_test("Frontend Availability", False, str(e))
        return False

async def run_all_tests():
    """Run all system tests"""
    print(f"\n{Colors.BLUE}{'='*50}")
    print("   SilentVoice System Test Suite")
    print(f"{'='*50}{Colors.END}\n")
    
    print(f"{Colors.BLUE}Backend Tests:{Colors.END}")
    backend_tests = [
        test_backend_health(),
        test_training_stats(),
        test_upload_training_data()
    ]
    
    print(f"\n{Colors.BLUE}WebSocket Tests:{Colors.END}")
    ws_tests = [
        await test_websocket_connection(),
        await test_speech_to_sign()
    ]
    
    print(f"\n{Colors.BLUE}Frontend Tests:{Colors.END}")
    frontend_tests = [
        test_frontend_availability()
    ]
    
    # Calculate results
    all_tests = backend_tests + ws_tests + frontend_tests
    passed = sum(all_tests)
    total = len(all_tests)
    
    print(f"\n{Colors.BLUE}{'='*50}{Colors.END}")
    if passed == total:
        print(f"{Colors.GREEN}✓ All tests passed! ({passed}/{total}){Colors.END}")
    else:
        print(f"{Colors.YELLOW}⚠ {passed}/{total} tests passed{Colors.END}")
    print(f"{Colors.BLUE}{'='*50}{Colors.END}\n")
    
    # Recommendations
    if passed < total:
        print(f"{Colors.YELLOW}Recommendations:{Colors.END}")
        if not backend_tests[0]:
            print("  • Start the backend server: cd backend && uvicorn main:app --reload")
        if not frontend_tests[0]:
            print("  • Start the frontend server: cd frontend && npm run dev")
        if not ws_tests[0]:
            print("  • Check WebSocket configuration and CORS settings")
        print()

if __name__ == "__main__":
    print(f"{Colors.BLUE}Starting SilentVoice System Tests...{Colors.END}")
    print(f"Backend URL: {BACKEND_URL}")
    print(f"Frontend URL: {FRONTEND_URL}")
    print(f"WebSocket URL: {WS_URL}")
    
    # Run tests
    asyncio.run(run_all_tests())
    
    print(f"{Colors.BLUE}Test Instructions:{Colors.END}")
    print("1. Make sure both servers are running:")
    print("   • Backend: cd backend && uvicorn main:app --reload")
    print("   • Frontend: cd frontend && npm run dev")
    print("2. Or use the run script: ./run_app.sh")
    print("3. Open browser to http://localhost:3000/translate")
    print("4. Test sign recognition with your webcam")
    print("5. Test speech recognition with your microphone\n")
