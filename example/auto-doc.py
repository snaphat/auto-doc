import sys, os

#Append to the path.
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from autodoc import *

##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
'''~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'''
'''--------------------------------------------------------------------------'''
'''~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'''
##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def user_task():
#{
    # Some example user task
    print("Running user task...")
#}

def before_arguments_run_check_for_resources():
#{
    # example use of checking for an existing resources under "tools" or "bundled" directory.
    print(os.getcwd())
    autodoc.example_resource = autodoc.find_resource("example_resource.txt");

    #Make sure all resources exist.
    # Note this can be set by the user manually to signal an error has occurred.
    if (autodoc.error):
    #{
        display.separator();
        display.warning("Missing resources, aborting...\n");
        autodoc.exit();
    #}
    display.separator();
#}

def after_arguments_run():
#{
    # some example task
    print ("After arguments...")
#}

def before_binary_patch(binary):
#{
    # Some binary operation.
    print ("Before binary patch...")
#}

def after_binary_patch(binary):
#{
    # Some binary operation.
    print ("After binary patch...")
#}

def before_error_checks():
#{
    # Some binary operation.
    print ("Before error checks...")
#}

def after_error_checks():
#{
    print ("After error checks...")
#}

# Adds an new argument and the specified function for it
# Useful for implementing new switches into autodoc to extend functionality
autodoc.add_argument("do_user_task", user_task);

# Adds a help message to be displayed when the help switch is called
autodoc.add_helpInfo("To do a user task use --do_user_task.");

# Adds a function to be run before arguments are handled
# Useful for adding code and checks that needs to be done before anything else
autodoc.add_preSetupCode(before_arguments_run_check_for_resources);

# Adds a function to be run after arguments are handle
# Useful for adding code that needs to be done after program arguments are processed
autodoc.add_postSetupCode(after_arguments_run);

# Adds a function to run just before teardown check (before checking if an error occurred during patching)
# Useful for adding code that needs to occur after all modifications are done on the target software
# but before error checks should occur
autodoc.add_preTeardownCode(before_error_checks);

# Adds a function to run just before exit (after checking if an error occurred during patching)
# Useful for adding code that can occur at the end of a program
autodoc.add_postTeardownCode(after_error_checks);


# enableService: specifies to run auto-doc as a service on system startup
# enableSilence: specifies auto-doc to be silent when running
# enableSimulation: run a simulation without modifying any files on disk
autodoc.setup(enableService=False, enableSilence=False, enableSimulation=False);

##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
'''~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'''
'''--------------------------------------------------------------------------'''
'''~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'''
##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Below is the general structure used for patching binaries.
list = ["a.exe"];
for item in list:
#{
    #The binary to modify
    hack = binary(item);

    # Adds a function to run prior to modifying a binary
    # Useful if unpacking or some other task needs to be run on a binary before patching.
    binary.add_prologueCode(before_binary_patch);

    # Adds a function to run after modifying a binary
    binary.add_epilogueCode(after_binary_patch);

    if (hack.prologue()):
    #{
        #Modification 1:
        # The following are the tuple arguments:
        #     regex:  The compiled regex to match with.
        #     offset: The offset into the matched text to start replacal at.
        #     bytes:  The bytes to replace the match[offset] with.
        tuple     = [
                        "\x83...\x75.", # CMP followed by JNZ
                        4,
                        "\x74",
                    ];

        # additional alternative patterns can be specified by adding to the tuple.
        tuple    += [
                        "\x0F\x95.\x88...\x48", # doesn't match within the example executable.
                        0,
                        "\x90\x90\x90",
                    ];
        # Instruct auto-doc to attempt to patch the binary.
        # allowedDuplicateCount: indicates the number of times a pattern is allowed to be in the binary for replacal.
        # ignoredDuplicates: used to specify that a specific duplicate be ignored (e.g. [1,4] would indicate match 1 and 4 be ignored).
        # memset: ?
        # offsetRange: set a specific offset range be searched (e.g. [20, 100] would indicate byte 20 to 100 be searched).
        hack.modify(tuple, allowedDuplicateCount=1, ignoredDuplicates=None, memset=None, offsetRange=None);

        # Modification 2
        tuple     = [
                        "R..ning",
                        7,
                        " Modded!",
                    ];
        tuple    += [
                        "\x85.\x74.\x83..\x77.", # Non-matching random patch.
                        2,
                        "\x90\x90",
                    ];
        hack.modify(tuple);

        # error checks for binary modification done here.
        hack.epilogue();
    #}
#}

##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
'''~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'''
'''--------------------------------------------------------------------------'''
'''~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'''
##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# More error checks done here. For example, if multiple binaries were patched
# And some post-binary modification process failed.
autodoc.teardown();
