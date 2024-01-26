import json
import logging
from os import path, makedirs,  getcwd, listdir, remove, walk
import shutil
from pkgutil import iter_modules

import yaml
import allure

from shared.logger.logger import get_logger, log_config_path
from shared.logger.handlers import TestDependentRotatingFileHandler
from shared.config.config import shared_config
from shared import fixtures
from shared.client import SharedClient


log = get_logger()


class SharedRunnerPlugin(object):
    enabled = False

    @classmethod
    def pytest_addoption(cls, parser):
        # parser.addoption('--base-url', action='store', help='Base URL', default='https://4sync.com')
        # parser.addoption('--device', action='store', default='iPhone 13')
        parser.addoption('--shared', dest='shared_enabled', default=False,
                         action='store_true',
                         help='Enables Shared testing framework.')
        parser.addoption('--shared-config-yaml', dest='shared_config_yaml',
                         default=None, action='store',
                         help='Overrides default Shared config with given.')

    @classmethod
    def pytest_load_initial_conftests(cls, early_config, parser, args):
        config = parser.parse(args)
        cls.enabled = config.shared_enabled
        if cls.enabled:
            # region config reading
            if config.shared_config_yaml:
                with open(config.shared_config_yaml, 'r') as new_config:
                    config_ = yaml.safe_load(new_config)
                shared_config.update(config_)
            # endregion

    @classmethod
    def pytest_cmdline_main(cls, config):
        if cls.enabled:
            # region logger configuration
            with open(log_config_path, 'r') as logger_config_file:
                log_config = json.load(logger_config_file)
                logging.config.dictConfig(log_config)
            # endregion

            # region clean results folderr
            delete_folder_path = path.join(getcwd(), '../..', shared_config['test-results-folder'])
            if path.exists(delete_folder_path) and path.isdir(delete_folder_path):
                for file_or_dir in listdir(delete_folder_path):
                    full_path = path.join(delete_folder_path, file_or_dir)
                    if path.isfile(full_path):
                        # Remove file
                        remove(full_path)
                    elif path.isdir(full_path):
                        # Remove directory and its contents
                        shutil.rmtree(full_path)
                    # endregion

            # region enable allure logging
            # config.option.allure_report_dir = path.join(getcwd(), '../..', shared_config['test-results-folder'], 'allure-results')
            config.option.allure_report_dir = path.join(getcwd(), 'allure-results')
            makedirs(config.option.allure_report_dir, exist_ok=True)
            print('!!!!!!!!!!!!!!______________!!!!!!!!!!!!!!!!')
            print(config.option.allure_report_dir)
            # endregion
            # Generate environment.properties file
            environment_file_path = path.join(config.option.allure_report_dir, 'environment.properties')
            with open(environment_file_path, 'w') as environment_file:
                environment_file.write(f'staging_name={shared_config["base-url"]}\n')
            # endregion

    @classmethod
    def pytest_configure(cls, config):
        if cls.enabled:
            # set native traceback style
            config.option.tbstyle = 'native'

            # region load fixtures
            fixtures_dir = path.dirname(fixtures.__file__)
            for importer, package_name, _ in iter_modules([fixtures_dir]):
                package = importer.find_module(package_name).load_module(package_name)
                config.pluginmanager.register(package, package_name)
            # endregion

            # clear log filename for test dependent logging handler
            TestDependentRotatingFileHandler.log_filename = None

    @classmethod
    def pytest_runtest_setup(cls, item):
        if cls.enabled:
            TestDependentRotatingFileHandler.log_filename = cls._get_full_test_log_filename(item)

    @classmethod
    def pytest_exception_interact(cls, node):
        if cls.enabled:
            node._was_failed = True

    @classmethod
    def pytest_runtest_teardown(cls, item):
        if cls.enabled:
            log.debug('Collecting logs.')

            def attach_html(path_):
                if path.isfile(path_):
                    name = path.basename(path_)
                    with open(path_) as html_file:
                        html_file_content = html_file.read()
                    allure.attach(html_file_content, name, allure.attachment_type.HTML)

            if TestDependentRotatingFileHandler.log_filename and \
                    path.isfile(TestDependentRotatingFileHandler.log_filename):
                with open(TestDependentRotatingFileHandler.log_filename) as \
                        log_file:
                    log_file_content = log_file.read()
                allure.attach(log_file_content, 'Debug log', allure.attachment_type.TEXT)

            failed = getattr(item, '_was_failed', False)
            if failed:
                attach_html(path.join(shared_config['temp-folder'], '500.html'))
                attach_html(path.join(shared_config['temp-folder'], '404.html'))
                client = SharedClient()
                screenshot_content = client.take_screenshot()
                if screenshot_content:
                    allure.attach(screenshot_content, 'screenshot', allure.attachment_type.PNG)

                def find_file_by_extension(directory, extension):
                    for root, dirs, files in walk(directory):
                        for file in files:
                            if file.endswith("." + extension):
                                return path.join(root, file)
                    return None

                def attach_webm_to_allure(directory_path):
                    file_extension = "webm"

                    # Find a WebM file in the "result" directory
                    found_file = find_file_by_extension(directory_path, file_extension)

                    if found_file:
                        # Read the binary content of the WebM file
                        webm_content = open(found_file, "rb").read()

                        # Attach the WebM file to Allure report with a dynamic title
                        webm_title = path.basename(found_file)
                        allure.attach(webm_content, webm_title, allure.attachment_type.WEBM)
                        print(f"WebM file found and attached to Allure: {found_file}")
                    else:
                        print(f"No WebM file found in the 'result' directory.")

                # Example usage
                directory_path = getcwd(), 'allure-results'
                print('!!directory_path', directory_path)
                attach_webm_to_allure(directory_path)
            # client.close_browser()

    @classmethod
    def _get_full_test_log_filename(cls, test_item):
        full_test_name = f'{test_item.module.__name__}.' \
                         f'{test_item.cls.__name__ if test_item.cls else test_item.module.__name__}.' \
                         f'{test_item.name}'
        full_test_name = full_test_name.split('[')
        test_results_path = full_test_name[0].split('.')
        if len(full_test_name) > 1:
            test_results_path[-1] = '['.join([test_results_path[-1], full_test_name[1]])
        test_results_path.insert(0, shared_config['test-results-folder'])
        test_log_filename = '%s.txt' % path.join(*test_results_path)
        test_log_filename = test_log_filename.replace('"', '')
        test_log_filename = path.join(getcwd(), test_log_filename)
        return test_log_filename
