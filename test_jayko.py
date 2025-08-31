import subprocess
import os
# module for writing unit tests 

def test_compile_say1():
    result = subprocess.run (
        ["python3", "jayko.py", "jko_src/say1.jko"],
        capture_output=True,
        text=True
    )
    c_result = subprocess.run (
        ["./output"],
        capture_output=True,
        text=True
    )
    #print(result.stdout)
    #print(repr(c_result.stdout))
    #print(c_result.stderr)
    assert result.returncode == 0
    assert c_result.stdout == "1\n69\n-68hello\n24\n1\n"

def test_compile_bf():
    result = subprocess.run (
        ["python3", "jayko.py", "jko_src/bf.jko"],
        capture_output=True,
        text=True
    )
    c_result = subprocess.run (
        ["./output"],
        capture_output=True,
        text=True
    )
    #print(result.stdout)
    print(repr(c_result.stdout))
    #print(c_result.stderr)
    assert result.returncode == 0
    assert c_result.stdout == 'STARTING INSTRUCTION ANALYSIS H e l l o   W o r l d ! \n 0 0 72 100 87 33 10 0 0 0 0 0 0 0 0 0 0 0 0 0 COMPLETE\n '

def test_compile_fizzbuzz():
    result = subprocess.run (
        ["python3", "jayko.py", "jko_src/fizzbuzz.jko"],
        capture_output=True,
        text=True
    )
    c_result = subprocess.run (
        ["./output"],
        capture_output=True,
        text=True
    )
    #print(result.stdout)
    print(repr(c_result.stdout))
    #print(c_result.stderr)
    assert result.returncode == 0
    assert c_result.stdout == '3Fizz5Buzz6Fizz9Fizz10Buzz12Fizz15FizzBuzz18Fizz20Buzz21Fizz24Fizz25Buzz27Fizz30FizzBuzz'

def test_compile_factorial():
    result = subprocess.run (
        ["python3", "jayko.py", "jko_src/fac.jko"],
        capture_output=True,
        text=True
    )
    c_result = subprocess.run (
        ["./output"],
        capture_output=True,
        text=True
    )
    #print(result.stdout)
    print(repr(c_result.stdout))
    #print(c_result.stderr)
    assert result.returncode == 0
    assert c_result.stdout == '3628800'

def test_compile_110():
    result = subprocess.run (
        ["python3", "jayko.py", "jko_src/110.jko"],
        capture_output=True,
        text=True
    )
    c_result = subprocess.run (
        ["./output"],
        capture_output=True,
        text=True
    )
    #print(result.stdout)
    print(repr(c_result.stdout))
    #print(c_result.stderr)
    assert result.returncode == 0
    assert c_result.stdout[-10:-1] == "111100010"   # eventually we want to test the full output

def test_compile_functions():
    result = subprocess.run (
        ["python3", "jayko.py", "jko_src/functions.jko"],
        capture_output=True,
        text=True
    )
    c_result = subprocess.run (
        ["./output"],
        capture_output=True,
        text=True
    )
    #print(result.stdout)
    print(repr(c_result.stdout))
    #print(c_result.stderr)
    assert result.returncode == 0
    assert c_result.stdout == "7\n-28475\n"   # eventually we want to test the full output





