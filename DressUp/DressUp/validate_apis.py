import requests
import argparse

def fetch_temperature(api):
    if api == 'custom':
        response = requests.post('http://3.65.218.209:8000/api/temperature', json={"city": "Oslo"})
        data = response.json()
        return data['temperature']
    elif api == 'openweathermap':
        response = requests.get('https://api.openweathermap.org/data/2.5/weather?q=Oslo&appid=d2a2b4ae87b93c165c5421cee9970939&units=metric')
        data = response.json()
        return data['main']['temp']
    else:
        raise ValueError('Invalid API')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Validate API Temperatures')
    parser.add_argument('--api', choices=['custom', 'openweathermap'], required=True, help='API to fetch the temperature from')
    args = parser.parse_args()

    temperature = fetch_temperature(args.api)
    print(temperature)


