
# Weather Notification Service

This project is a weather notification service that uses the WeatherAPI and Twilio messaging service to send a daily text message with the weather forecast for a specific city. The message includes information about the hours during the day when rain is expected, filtering the relevant hours of the day.

## Table of Contents

1. [Project Description](#project-description)
2. [How It Works](#how-it-works)
3. [Configuration](#configuration)
4. [Installation](#installation)
5. [Usage](#usage)
6. [Automated Execution](#automated-execution)
7. [Contributions](#contributions)
8. [License](#license)

## Project Description

This project is designed to send a daily text message to your mobile phone with the weather forecast for your city using an AWS EC2 instance and automated cron tasks. The message is sent at a specific hour each day, providing information about the hours of the day when rain is expected. The service fetches weather data from the WeatherAPI, processes it to extract hourly forecasts, filters to highlight rainy hours during the day, and sends this information via SMS using Twilio.

## How It Works

1. **Fetch Weather Data**: The script fetches weather data from the WeatherAPI for a specific city.
2. **Process Data**: It processes the data to extract the forecast for each hour of the day.
3. **Filter Important Information**: The script filters the forecast to highlight the hours during the day when rain is expected.
4. **Send SMS**: It sends a text message to your mobile phone using the Twilio API with the filtered forecast information.

## Configuration

1. Clone this repository.
2. Create a virtual environment and install the dependencies listed in `requirements.txt`.
3. Set up your credentials in `twilio_config.py`.
4. Set up an AWS EC2 instance and schedule a cron job to run `main.py` daily.

## Installation

1. **Clone the repository**:

    ```bash
    git clone https://github.com/rruisan/DailyWeatherForecast.git
    cd DailyWeatherForecast/
    ```

2. **Create a virtual environment**:

    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3. **Install dependencies**:

    ```bash
    pip install -r requirements.txt
    ```

4. **Configure Twilio and WeatherAPI**:

    - Edit the `twilio_config.py` file with your Twilio and WeatherAPI credentials.

## Usage

To manually run the script, use the following command:

```bash
python main.py
```

## Automated Execution

Set up a cron job on an AWS EC2 instance to run the script daily at a specific time and save the output to a log file in the same directory. For example, to run the script every day at 6 AM and log the output, add the following line to your crontab (edit crontab with `crontab -e`):

```cron
0 6 * * * /path/to/venv/bin/python /path/to/project_directory/main.py >> /path/to/project_directory/cron_log.txt 2>&1
```

## Contributions

If you would like to contribute to this project, please open an issue or create a pull request.

## License

This project is licensed under the MIT License.
