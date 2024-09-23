project_root/
│
├── src/
│   ├── domain/                         # Lógica de negocio y modelos
│   │   ├── models/                     # Modelos de dominio (Stock, Crypto, News, etc.)
│   │   └── services/                   # Lógica de negocio (casos de uso)
│   │
│   ├── application/                    # Casos de uso (coordinación)
│   │   └── use_cases/                  # Casos de uso específicos (CollectStockData, CollectCryptoData, etc.)
│   │
│   ├── infrastructure/                 # Conexiones a bases de datos y APIs externas
│   │   ├── db/                         # Implementaciones de repositorios y bases de datos
│   │   ├── api_clients/                # Clientes para interactuar con APIs externas (Yahoo Finance, Binance, etc.)
│   │   └── webhooks/                   # Integración con webhooks o servicios de notificación
│   │
│   ├── interfaces/                     # Interfaces de entrada/salida (CLI, API REST, GUI)
│   │   ├── cli/                        # Implementación de la CLI
│   │   ├── rest_api/                   # API REST para exponer servicios
│   │   └── gui/                        # Interfaz gráfica (si es necesario)
│   │
│   └── utils/                          # Utilidades generales como logging y configuración
│
├── tests/                              # Pruebas unitarias e integración
│   └── domain/                         # Pruebas para la capa de dominio
│   └── application/                    # Pruebas para la capa de aplicación
│   └── infrastructure/                 # Pruebas para la capa de infraestructura
│   └── interfaces/                     # Pruebas para la capa de interfaces
│
├── docs/                               # Documentación del proyecto
│   └── CONTRIBUTING.md                 # Guía para contribuir
│
├── config/                             # Configuración de la aplicación (config.ini)
│   └── config.ini
│
├── .github/                            # Configuración de CI/CD
│   └── workflows/
│       └── ci.yml
├── README.md                           # Descripción del proyecto
└── setup.py                            # Archivo para instalar el proyecto como 
