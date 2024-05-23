import os
import sys
import django

from django.core.management.commands import flush
from django.core.management import call_command



def assertEqual(a, b):
    if a==b:
        print(" + OK +")
    else:
        print(" - Failure -")
    
    return a==b

def assertBoleanEqual(a, b):
    return a==b

def create_test(func):
    def inner1():
        Error = None
        
        print("// TEST //")
        try:
            func()
        except Exception as E:
            Error = E
        print("// END TEST")
        
        print("\nFlushing DB...")
        flush_cmd = flush.Command()
        call_command(flush_cmd, verbosity=0, interactive=False)
        print("FLUSHED!\n")
        
        if Error:
            import traceback
            print(f"Got Exception: \n{Error}")
            traceback.print_exception(Error)
    return inner1


def main():

    sys.path.append('/home/technopy/Documents/Proyecto-Marraqueta/ProyectoMarraqueta')
    #from django_project import *
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ProyectoMarraqueta.settings')
    django.setup()


    from picow_api_tests import integrity_tests, stress_tests


    """for test in integrity_tests.ALLOWED_TESTS:
        execute_test = create_test(test)
        execute_test()"""

    for test in stress_tests.ALLOWED_TESTS:
        execute_test = create_test(test)
        execute_test()



if __name__ == "__main__":
    confirmation = input("!! THIS TOOLS INTERACTS WITH PRODUCTION DATABASE !!,\nwrite 'YES' to confirm execution: ")

    if confirmation=="YES":
        main()
    else:
        print("Confirmation Failure.")
        exit()