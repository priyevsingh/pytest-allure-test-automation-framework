import os
import subprocess
import webbrowser
import logging
import socketserver


rep_log_path = os.path.realpath(
    os.path.join(os.path.dirname(__file__), "..", "Reports", "logs", "gen_report.log")
)

logging.basicConfig(
    filename=rep_log_path,
    format="%(asctime)s - %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s",
    filemode="w",
    datefmt="%Y-%m-%d %H:%M:%S",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

free_port = []


def report():
    """
    This program is used to generate allure report and serve it,
    by performing below actions:

    1. Generate allure report
    2. Customize title of the report
    3. Serves the report at http://localhost:<port> on free available port.

    """

    try:
        # Generate allure-report
        report_path = os.path.realpath(
            os.path.join(os.path.dirname(__file__), "..", "Reports")
        )
        if os.path.exists(
            os.path.realpath(
                os.path.join(
                    os.path.dirname(__file__),
                    "..",
                    "Reports",
                    "allure-report",
                )
            )
        ):
            op = subprocess.check_output(
                ["allure", "generate", "allure-results", "--clean"],
                cwd=report_path,
                shell=True,
            )
            logger.info(
                f"Command used to generate allure report: allure generate allure-results --clean"
            )
        else:
            op = subprocess.check_output(
                ["allure", "generate", "allure-results"], cwd=report_path, shell=True
            )
            logger.info(
                f"Command used to generate allure report: allure generate allure-results"
            )
        logger.info(f"Output of allure generate command is : {op}")
        logger.info(f"Allure report is generated.")

    except:
        logging.error(f"Allure report is not generated", exc_info=True)

    # Customize allure report title after report generation. You can enter your own title.
    # Source: https://github.com/allure-framework/allure2/issues/804#issuecomment-902634865

    try:
        path = os.path.realpath(
            os.path.join(
                os.path.dirname(__file__),
                "..",
                "Reports",
                "allure-report",
                "widgets",
                "summary.json",
            )
        )
        logger.info(f"Allure report path was found at : {path}")
        title = "Test Automation Report"
        logger.info(f"Customizing report title as : {title}")
        with open(f"{path}", "r+") as report:
            contents = report.read().replace("Allure Report", title)
        with open(f"{path}", "w+") as report:
            report.write(contents)

    except:
        logger.error(f"Invalid allure report path", exc_info=True)

    # Serve the report at localhost on free available port
    try:
        root_path = os.path.realpath(
            os.path.join(
                os.path.dirname(__file__),
                "..",
                "Reports",
                "allure-report",
            )
        )

        # Check for free available port using socketserver.
        with socketserver.TCPServer(("localhost", 0), None) as sock:
            free_port.append(sock.server_address[1])
            logger.info(f"Free port was found at : {free_port[0]}")

            # Serve the report from allure-report directory.
            cmd = [
                "python",
                "-m",
                "http.server",
                "--bind=localhost",
                "{}".format(free_port[0]),
            ]
            subprocess.Popen(cmd, cwd=root_path, shell=True)
            logger.info(f"Allure report is served")
    except:
        logger.info(f"Allure report was not served", exc_info=True)


if __name__ == "__main__":
    try:
        report()
        logger.info(f"Serving report at: http://localhost:{free_port[0]}")
        webbrowser.open_new_tab(f"http://localhost:{free_port[0]}")
        logger.info(f"Allure report is successfully opened in default web browser")
    except:
        logger.info(f"Error while opening allure report", exc_info=True)
