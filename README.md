# A helper to prettify commands
---------------------------------------------------------------
dispatched via subprocess.Popen, especially useful for tools/externals<br> with many arguments. 
---------------------------------------------------------------

<br>


Example usage: Dict[str: List[Tuple] 
    
    
    process = PrettyPopen(args={"python3 run_file.py": [
        ("--arg1", 1),
        ("--arg2", 2),
        ("--arg3", 3),
        ("--arg4", 4),
            * * * 
        ("--arg_clean",)]}, **kwargs)
    stderr, stdout = process.communicate()
<br>
That's it.<br>
---------------------------------------------------------------<br>
To install simply run:

    pip install git+https://github.com/tevops/pretty-popen.git
