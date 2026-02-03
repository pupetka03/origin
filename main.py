import sys
from core.parser import parser
from core.executor import executor


def open_fail(fail):
    code = []
    fail_open = fail
    with open(f"{fail_open}", "r") as f:
        for line in f:
            lines = line.strip()
            if lines:
                code.append(lines)
    return code



def main(fail):
    fail_code = open_fail(fail)
    executor(fail_code)
    


    




if len(sys.argv) > 1:
    file_path = sys.argv[1]
    main(file_path)



#if __name__ == "__main__":
#    main()
