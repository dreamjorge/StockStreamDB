# infrastructure

## Scripts

### __init__.py

Path: `/workspaces/StockStreamDB/scripts/../src/infrastructure/__init__.py`

#### Functions:


### clean_db.py

Path: `/workspaces/StockStreamDB/scripts/../src/infrastructure/db/clean_db.py`

#### Functions:


### concrete_stocks_repository.py

Path: `/workspaces/StockStreamDB/scripts/../src/infrastructure/db/concrete_stocks_repository.py`

#### Functions:

- `    __init__`
- `    create_stock`
- `    get_stock_by_ticker`
- `    update_stock`
- `    get_stock_data`
- `    get`
- `    delete_stock`
- `    save`
- `    update`

### db.py

Path: `/workspaces/StockStreamDB/scripts/../src/infrastructure/db/db.py`

#### Functions:

- `init_db`

### db_setup.py

Path: `/workspaces/StockStreamDB/scripts/../src/infrastructure/db/db_setup.py`

#### Functions:

- `init_db`
- `get_session`

### models.py

Path: `/workspaces/StockStreamDB/scripts/../src/infrastructure/db/models.py`

#### Functions:


### stock_repository.py

Path: `/workspaces/StockStreamDB/scripts/../src/infrastructure/db/stock_repository.py`

#### Functions:

- `    get_stock_data`

### stock_repository_impl.py

Path: `/workspaces/StockStreamDB/scripts/../src/infrastructure/db/stock_repository_impl.py`

#### Functions:

- `    __init__`
- `    get`
- `    create_stock`
- `    save`
- `    update`
- `    delete_stock`
- `    get_stock_data`
- `    get_by_ticker`
- `    stock_exists`
- `    get_date_range_for_period`
- `    get_sample_stock_data`
- `    add_stock`
- `    commit`

### news_api_client.py

Path: `/workspaces/StockStreamDB/scripts/../src/infrastructure/db/api_clients/news_api_client.py`

#### Functions:

- `    __init__`
- `    get_news`

### env.py

Path: `/workspaces/StockStreamDB/scripts/../src/infrastructure/db/migrations/env.py`

#### Functions:

- `run_migrations_offline`
- `run_migrations_online`

### 061d83894fa5_add_id_column_to_stocks_table.py

Path: `/workspaces/StockStreamDB/scripts/../src/infrastructure/db/migrations/versions/061d83894fa5_add_id_column_to_stocks_table.py`

#### Functions:

- `upgrade`
- `downgrade`

### 14f96da0ec16_add_id_column_to_stocks_table.py

Path: `/workspaces/StockStreamDB/scripts/../src/infrastructure/db/migrations/versions/14f96da0ec16_add_id_column_to_stocks_table.py`

#### Functions:

- `upgrade`
- `downgrade`

### 184a1c26dc16_add_open_high_low_close_and_volume_.py

Path: `/workspaces/StockStreamDB/scripts/../src/infrastructure/db/migrations/versions/184a1c26dc16_add_open_high_low_close_and_volume_.py`

#### Functions:

- `upgrade`
- `downgrade`

### 1b5cda74336c_add_missing_date_column_to_stocks.py

Path: `/workspaces/StockStreamDB/scripts/../src/infrastructure/db/migrations/versions/1b5cda74336c_add_missing_date_column_to_stocks.py`

#### Functions:

- `upgrade`
- `downgrade`

### 20324a418dfd_your_migration_message.py

Path: `/workspaces/StockStreamDB/scripts/../src/infrastructure/db/migrations/versions/20324a418dfd_your_migration_message.py`

#### Functions:

- `upgrade`
- `downgrade`

### 3e4084e1e245_initial_migration.py

Path: `/workspaces/StockStreamDB/scripts/../src/infrastructure/db/migrations/versions/3e4084e1e245_initial_migration.py`

#### Functions:

- `upgrade`
- `downgrade`

### 41fe3993e8e6_add_id_column_to_stocks_table.py

Path: `/workspaces/StockStreamDB/scripts/../src/infrastructure/db/migrations/versions/41fe3993e8e6_add_id_column_to_stocks_table.py`

#### Functions:

- `upgrade`
- `downgrade`

### 6525cfe33cae_fix_stocks_id_auto_increment.py

Path: `/workspaces/StockStreamDB/scripts/../src/infrastructure/db/migrations/versions/6525cfe33cae_fix_stocks_id_auto_increment.py`

#### Functions:

- `create_stocks_table`
- `manage_table_operations`
- `upgrade`
- `downgrade`

### 8136cc14f577_added_missing_columns.py

Path: `/workspaces/StockStreamDB/scripts/../src/infrastructure/db/migrations/versions/8136cc14f577_added_missing_columns.py`

#### Functions:

- `upgrade`
- `downgrade`

### 9e8e2e43aeb3_manually_create_stocks_table.py

Path: `/workspaces/StockStreamDB/scripts/../src/infrastructure/db/migrations/versions/9e8e2e43aeb3_manually_create_stocks_table.py`

#### Functions:

- `upgrade`
- `downgrade`

### a56f4298ff14_initial_schema.py

Path: `/workspaces/StockStreamDB/scripts/../src/infrastructure/db/migrations/versions/a56f4298ff14_initial_schema.py`

#### Functions:

- `upgrade`
- `downgrade`

### bf17a92c72f8_add_autoincrement_to_stocks_id.py

Path: `/workspaces/StockStreamDB/scripts/../src/infrastructure/db/migrations/versions/bf17a92c72f8_add_autoincrement_to_stocks_id.py`

#### Functions:

- `stock_columns`
- `create_stocks_table`
- `copy_table_data`
- `drop_and_rename_table`
- `upgrade`
- `downgrade`

### d74fcf8c0b1e_add_new_fields_to_stock.py

Path: `/workspaces/StockStreamDB/scripts/../src/infrastructure/db/migrations/versions/d74fcf8c0b1e_add_new_fields_to_stock.py`

#### Functions:

- `upgrade`
- `downgrade`

### dc35511c4a5f_recreate_stocks_table_with_correct_.py

Path: `/workspaces/StockStreamDB/scripts/../src/infrastructure/db/migrations/versions/dc35511c4a5f_recreate_stocks_table_with_correct_.py`

#### Functions:

- `upgrade`
- `downgrade`

### e3cab1a2d06b_add_id_column_to_stocks_table.py

Path: `/workspaces/StockStreamDB/scripts/../src/infrastructure/db/migrations/versions/e3cab1a2d06b_add_id_column_to_stocks_table.py`

#### Functions:

- `upgrade`
- `downgrade`

### eea40ed64440_add_missing_columns.py

Path: `/workspaces/StockStreamDB/scripts/../src/infrastructure/db/migrations/versions/eea40ed64440_add_missing_columns.py`

#### Functions:

- `upgrade`
- `downgrade`

### fb225cc14cd2_add_missing_id_column_to_stocks.py

Path: `/workspaces/StockStreamDB/scripts/../src/infrastructure/db/migrations/versions/fb225cc14cd2_add_missing_id_column_to_stocks.py`

#### Functions:

- `upgrade`
- `downgrade`

### stock_fetcher.py

Path: `/workspaces/StockStreamDB/scripts/../src/infrastructure/fetchers/stock_fetcher.py`

#### Functions:

- `    fetch`

### yahoo_finance_fetcher.py

Path: `/workspaces/StockStreamDB/scripts/../src/infrastructure/fetchers/yahoo_finance_fetcher.py`

#### Functions:

- `    fetch`
