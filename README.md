weather-forecasting-pipeline/
├── README.md
├── architecture/
│   └── solution-architecture.png   # Exported diagram
├── lambda-functions/
│   ├── weather_collector.py       # Lambda to collect weather data
│   └── weather_processor.py       # Lambda to process and store data
├── ec2-scripts/
│   └── aggregation_script.py      # EC2 script for data aggregation
├── api/
│   └── api_handler.py             # Lambda function for API handling
├── requirements.txt               # Python dependencies
└── docs/
    └── setup-guide.md             # Detailed setup instructions
