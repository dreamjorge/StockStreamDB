# utils

## Scripts

### check_missing_dependencies.py

Path: `/workspaces/StockStreamDB/scripts/../src/utils/check_missing_dependencies.py`

#### Functions:

- `check_missing_dependencies`

### check_requirements.py

Path: `/workspaces/StockStreamDB/scripts/../src/utils/check_requirements.py`

#### Functions:

- `get_installed_packages`
- `get_imported_modules`
- `get_requirements_from_file`
- `update_requirements_file`
- `check_and_sync_requirements`

### fix_flake8_errors.py

Path: `/workspaces/StockStreamDB/scripts/../src/utils/fix_flake8_errors.py`

#### Functions:

- `fix_long_lines`
- `fix_unused_vars`
- `remove_unused_imports`
- `resolve_redefined_vars`
- `process_flake8_errors`

### logging_config.py

Path: `/workspaces/StockStreamDB/scripts/../src/utils/logging_config.py`

#### Functions:

- `setup_logging`

### run_flake8.py

Path: `/workspaces/StockStreamDB/scripts/../src/utils/run_flake8.py`

#### Functions:

- `log_message`
- `run_flake8_and_fix`
- `parse_flake8_output`
- `fix_missing_blank_lines`
- `fix_long_lines`

### stock_plotting.py

Path: `/workspaces/StockStreamDB/scripts/../src/utils/stock_plotting.py`

#### Functions:

- `plot_stock_prices`

### update_schema_with_stock_model.py

Path: `/workspaces/StockStreamDB/scripts/../src/utils/update_schema_with_stock_model.py`

#### Functions:

- `check_if_stocks_table_exists`
- `drop_stocks_table`
- `create_stocks_table`
- `main`

### github_issue_creator.py

Path: `/workspaces/StockStreamDB/scripts/../src/utils/github_issue_creator/github_issue_creator.py`

#### Functions:

- `    __init__`
- `    get_cached_labels`
- `    create_label_if_not_exists`
- `    get_cached_milestones`
- `    create_milestone_if_not_exists`
- `    get_cached_issues`
- `    __init__`
- `    ensure_labels_exist`
- `    update_issue_if_needed`
- `    create_or_update_issue`
- `    check_rate_limit`
- `create_issues_from_yaml`

### read_issues_from_github.py

Path: `/workspaces/StockStreamDB/scripts/../src/utils/github_issue_creator/read_issues_from_github.py`

#### Functions:

- `export_issues_to_yaml`
