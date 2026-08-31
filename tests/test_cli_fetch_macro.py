import unittest
from unittest.mock import patch, MagicMock

from click.testing import CliRunner

from src.interfaces.cli.cli import cli


class TestCLIFetchMacro(unittest.TestCase):
    @patch("src.interfaces.cli.cli.ManageMacroUseCase")
    @patch("src.interfaces.cli.cli.FredFetcher")
    @patch("src.interfaces.cli.cli.get_session")
    def test_cli_fetch_macro_stores_observations(
        self,
        mock_get_session,
        mock_fred_fetcher_class,
        mock_manage_macro_use_case_class,
    ):
        mock_session = MagicMock()
        mock_get_session.return_value.__enter__.return_value = mock_session
        mock_use_case_instance = mock_manage_macro_use_case_class.return_value
        mock_use_case_instance.fetch_and_store_series.return_value = 5

        runner = CliRunner()
        result = runner.invoke(cli, ["fetch-macro", "FEDFUNDS"])

        self.assertEqual(result.exit_code, 0)
        self.assertIn("Stored 5 observations for FEDFUNDS", result.output)
        mock_use_case_instance.fetch_and_store_series.assert_called_once_with(
            "FEDFUNDS", start=None, end=None
        )

    @patch("src.interfaces.cli.cli.ManageMacroUseCase")
    @patch("src.interfaces.cli.cli.FredFetcher")
    @patch("src.interfaces.cli.cli.get_session")
    def test_cli_fetch_macro_reports_no_data(
        self,
        mock_get_session,
        mock_fred_fetcher_class,
        mock_manage_macro_use_case_class,
    ):
        mock_session = MagicMock()
        mock_get_session.return_value.__enter__.return_value = mock_session
        mock_use_case_instance = mock_manage_macro_use_case_class.return_value
        mock_use_case_instance.fetch_and_store_series.return_value = 0

        runner = CliRunner()
        result = runner.invoke(cli, ["fetch-macro", "UNKNOWNSERIES"])

        self.assertEqual(result.exit_code, 0)
        self.assertIn("No data returned for UNKNOWNSERIES", result.output)

    @patch("src.interfaces.cli.cli.ManageMacroUseCase")
    @patch("src.interfaces.cli.cli.FredFetcher")
    @patch("src.interfaces.cli.cli.get_session")
    def test_cli_fetch_macro_passes_start_and_end_options(
        self,
        mock_get_session,
        mock_fred_fetcher_class,
        mock_manage_macro_use_case_class,
    ):
        mock_session = MagicMock()
        mock_get_session.return_value.__enter__.return_value = mock_session
        mock_use_case_instance = mock_manage_macro_use_case_class.return_value
        mock_use_case_instance.fetch_and_store_series.return_value = 3

        runner = CliRunner()
        result = runner.invoke(
            cli,
            [
                "fetch-macro",
                "CPIAUCSL",
                "--start",
                "2020-01-01",
                "--end",
                "2020-12-31",
            ],
        )

        self.assertEqual(result.exit_code, 0)
        mock_use_case_instance.fetch_and_store_series.assert_called_once_with(
            "CPIAUCSL", start="2020-01-01", end="2020-12-31"
        )
