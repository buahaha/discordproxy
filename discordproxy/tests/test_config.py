from pathlib import Path
import unittest
from unittest.mock import patch

from discordproxy import config
from discordproxy import constants


MODULE_PATH = "discordproxy.config"


@patch(MODULE_PATH + ".logging.config.dictConfig", lambda x: None)
class TestSetupServer(unittest.TestCase):
    def test_should_return_token_when_provided_in_args(self):
        # when
        token, my_args = config.setup_server(["--token", "abc"])
        # then
        self.assertEqual(token, "abc")

    @patch(MODULE_PATH + ".os.environ")
    def test_should_return_token_when_provided_as_environ_var(self, mock_environ):
        # given
        mock_environ.get.return_value = "abc"
        # when
        token, my_args = config.setup_server([])
        # then
        self.assertEqual(token, "abc")

    def test_should_have_all_defaults(self):
        # when
        token, my_args = config.setup_server(["--token", "abc"])
        # then
        self.assertEqual(my_args.token, "abc")
        self.assertEqual(my_args.host, constants.DEFAULT_HOST)
        self.assertEqual(my_args.port, constants.DEFAULT_PORT)
        self.assertEqual(my_args.log_level, "INFO")
        self.assertIsNone(my_args.log_file_path)

    def test_should_set_log_file_path_to_cwd(self):
        # given
        my_args = config._parse_args([])
        # when
        logger_dict = config._logging_config(my_args)
        # then
        self.assertEqual(
            logger_dict["handlers"]["file"]["filename"],
            str(Path.cwd() / config._LOG_FILE_NAME),
        )

    def test_should_set_log_file_path_to_given_path(self):
        # given
        my_path = Path(__file__).parent
        my_args = config._parse_args(["--log-file-path", str(my_path)])
        # when
        logger_dict = config._logging_config(my_args)
        # then
        self.assertEqual(
            logger_dict["handlers"]["file"]["filename"],
            str(my_path / config._LOG_FILE_NAME),
        )
