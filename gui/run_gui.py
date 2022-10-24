import os, re, time
import platform
import PySimpleGUI as sg


path = os.path.realpath(os.path.join(os.path.dirname(__file__), ".."))


def run_gui():
    """
    Runs (upon double-clicking) GUI for Test Automation Framework.
    """

    sg.theme("Black")

    logo_path = os.path.realpath(
        os.path.join(os.path.dirname(__file__), "..", "gui", "logo.png")
    )

    layout = [
        [
            sg.Image(filename=logo_path, key="logo", size=(260, 100)),
            sg.Text(
                "Test Automation Framework",
                size=(40, 1),
                font=("Arial", 16),
                text_color="white",
                justification="center",
                key="text",
            ),
        ]
    ]

    layout = [
        [
            sg.Image(filename=logo_path, key="logo", size=(260, 100)),
            sg.Text(
                "Test Automation Framework",
                size=(40, 1),
                font=("Arial", 16),
                text_color="white",
                justification="center",
                key="text",
            ),
        ],
        [
            sg.Text(
                "",
                size=(20, 1),
                font=("Arial", 16),
                text_color="white",
                justification="center",
                key="text",
            )
        ],
        [
            sg.Text(
                "Console output....",
                size=(60, 1),
                font=("Arial", 10),
                text_color="red",
                key="-TEXT-",
            )
        ],
        [
            sg.Multiline(
                size=(88, 20),
                key="-OUTPUT-",
                font=("Arial", 12),
                background_color="white",
                text_color="black",
                reroute_stdout=True,
                reroute_stderr=True,
                autoscroll=True,
            )
        ],
        # [sg.Output(size=(88, 20), font='Arial 12', key='-OUTPUT-', background_color='white', text_color='black')],
        [
            sg.Button("SETUP"),
            sg.VerticalSeparator(pad=((0, 0), (0, 1)), color="red"),
            sg.Button("PYTHON_VERSION"),
            sg.VerticalSeparator(pad=((0, 0), (0, 1)), color="red"),
            sg.Button("CLEAR"),
            sg.VerticalSeparator(pad=((0, 0), (0, 1)), color="red"),
            sg.Button("EXIT"),
        ],
        [sg.HorizontalSeparator(pad=((0, 0), (0, 1)), color="red")],
        [
            sg.InputText(key="-FILEPATH-", size=(15, 2), font=("Arial", 16)),
            sg.FileBrowse(
                file_types=(("Python Scripts", "*.py"), ("All Files", "*.*")),
                key="-BROWSE-",
            ),
            #  sg.VerticalSeparator(pad=((0, 0), (0, 1)), color='red'),
            #  sg.Spin(values=('chrome', 'firefox', 'edge'), initial_value='chrome', key='-BROWSER-', size=(10, 1), font=('Arial', 10)),
            sg.VerticalSeparator(pad=((0, 0), (0, 1)), color="red"),
            sg.Button("RUN TEST CASE"),
            sg.VerticalSeparator(pad=((0, 0), (0, 1)), color="red"),
            sg.Button("RUN TEST SUITE"),
        ],
        [
            sg.Text("Manual Command", size=(14, 1), font=("Arial", 16)),
            sg.Input(focus=True, key="-IN-", size=(14, 1)),
            sg.VerticalSeparator(pad=((0, 0), (0, 1)), color="red"),
            sg.Button("Run", bind_return_key=True),
            sg.VerticalSeparator(pad=((0, 0), (0, 1)), color="red"),
            sg.Button(
                "ABOUT",
                key="-ABOUT-",
                mouseover_colors=("white", "red"),
                enable_events=True,
            ),
        ],
        [sg.HorizontalSeparator(pad=((0, 0), (0, 1)), color="red")],
        [
            sg.Text(
                "Made with " + "\U0001F493" + " at <your-org-name>",
                size=(20, 1),
                font=("Arial", 12),
                text_color="red",
                justification="left",
                auto_size_text=True,
            )
        ],
    ]

    window = sg.Window("Test Automation Framework", layout, finalize=True)

    window["-OUTPUT-"].update(
        "Hello! {}".format(os.getlogin()) + "\n" + "\n"
        "This is the GUI utility for Test Automation Framework - .\n\n"
        'Run a test case by selecting the test case file and clicking on "RUN TEST CASE".\n'
        'Run a test suite by clicking on "RUN TEST SUITE".\n'
        'You can also run a manual command by typing the command and clicking on "Run".\n\n'
        'Clear the console output by clicking on "CLEAR".' + "\n" + "\n"
        'Exit the GUI by clicking on "EXIT".\n\n'
        "For more information, please refer to the documentation.\n\n"
        "Made with \U0001F493 @ <your-org-name>\n\n"
        "System Information -\n {}".format(
            platform.system()
            + " "
            + platform.release()
            + "\n "
            + platform.version()
            + "\n "
            + platform.machine()
            + "\n "
            + platform.processor()
            + "\n "
            + "Python version"
            + " "
            + platform.python_version()
            + " "
        )
    )

    window.refresh()

    while True:
        event, values = window.read()
        if event == "EXIT" or event == sg.WIN_CLOSED:
            break  # exit button clicked

        if event == "SETUP":
            print("\n")
            print("-" * 100, "\n")
            sp = sg.execute_command_subprocess(
                "pip3",
                "install",
                "-r",
                "requirements.txt",
                "--extra-index-url https://test.pypi.org/simple",
                wait=False,
                pipe_output=True,
                cwd=path,
            )
            print(sg.execute_get_results(sp)[0], "\n")
            print("-" * 100, "\n")

        elif event == "PYTHON_VERSION":
            print(f"Running python --version")
            # For this one we need to wait for the subprocess to complete to get the results
            sp = sg.execute_command_subprocess(
                "python", "--version", wait=False, pipe_output=True
            )
            print(sg.execute_get_results(sp)[0])

        elif event == "Run":
            args = values["-IN-"].split(" ")
            print(f'Running {values["-IN-"]} args={args}', "\n\n")
            sp = sg.execute_command_subprocess(args[0], *args[1:], pipe_output=True)
            # This will cause the program to wait for the subprocess to finish
            print(sg.execute_get_results(sp)[0], "\n\n")
            window["-IN-"].update("")

        elif event == "CLEAR":
            window["-OUTPUT-"].update("")

        # elif event == '-BROWSER-':
        #     browser = values['-BROWSER-']
        #     browser = '--'+ browser.lower()

        elif event == "RUN TEST CASE":
            address = values["-FILEPATH-"]
            robj = re.compile(r"T.*")
            mo = robj.search(address)
            rel_path = mo.group()
            pathobj = re.compile(r"[/]")
            testcasepath = pathobj.sub(r"\\", rel_path)
            window["-OUTPUT-"].update("\nRunning test case: " + testcasepath + "\n")
            window.perform_long_operation(
                lambda: run_testcase(testcasepath), "EXECUTION DONE"
            )

        elif event == "RUN TEST SUITE":
            window.perform_long_operation(run_testsuite, "EXECUTION DONE")

        elif event == "EXECUTION DONE":
            window["-OUTPUT-"].update(values["-OUTPUT-"] + "\nExecution Done!\n")

        elif event == "-ABOUT-":
            sg.popup(
                "Test Automation Framework - GUI Utility\n\n"
                "Version: 1.0.0\n"
                "Made with "
                + "\U0001F493"
                + " @ <your-org-name> by <individual-or-team-name>\n\n <your-org-name> - All Rights Reserved \u00A9 {}".format(
                    time.strftime("%Y")
                ),
                font=("Arial", 9),
                text_color="red",
                relative_location=(0, 0),
                title="About",
            )

    window.close()


def run_testcase(testcasepath):
    sp = sg.execute_command_subprocess(
        "pytest",
        "--alluredir=.\\Reports\\allure-results",
        testcasepath,
        wait=True,
        pipe_output=True,
        cwd=path,
    )
    return sp


def run_testsuite():
    sp = sg.execute_command_subprocess(
        "pytest",
        "--alluredir=.\\Reports\\allure-results",
        wait=True,
        pipe_output=True,
        cwd=path,
    )
    return sp


if __name__ == "__main__":
    run_gui()
