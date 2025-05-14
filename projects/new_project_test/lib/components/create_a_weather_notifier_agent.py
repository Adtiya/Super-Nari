Sure, for the purpose of such an agent, we will use the OpenWeatherMap API for getting weather data, Node Fetch for making HTTP requests, and Node Schedule for scheduling the weather updates. 

Here is the basic implementation of this weather notifier using Node.js.

```javascript
const fetch = require('node-fetch');
const schedule = require('node-schedule');

const API_KEY = 'your-open-weather-map-api-key';
const CITY = 'name-of-your-city';
const URL = `http://api.openweathermap.org/data/2.5/weather?q=${CITY}&appid=${API_KEY}`;

const getWeatherData = async () => {
    let weatherData;
    try {
        const response = await fetch(URL);
        weatherData = await response.json();
    } catch (error) {
        console.error('Error:', error);
        return;
    }
    return weatherData;
};

const getReadableWeather = async () => {
    const data = await getWeatherData();
    if (!data) return;
    
    // Convert temperature from Kelvin to Celsius
    const temperature = (data.main.temp - 273.15).toFixed(2); 
    const weatherDescription = data.weather[0].description;
    const weatherInfo = `Current temperature in ${CITY}: ${temperature}°C. Weather: ${weatherDescription}.`;
    return weatherInfo;
}

const weatherNotifier = schedule.scheduleJob('0 * * * *', async function () {
    const weatherInfo = await getReadableWeather();
    if (!weatherInfo) return;
    console.log(weatherInfo);
});

console.log('Weather notifier has been started. It will notify you about the weather every hour.');
```

This code schedules a job that runs every hour (at minute 0). This job gets the current weather data of a specific city and logs it. The temperature is converted from Kelvin (which is the default scale of the OpenWeatherMap) to Celsius.

Don't forget to replace `'your-open-weather-map-api-key'` with your actual API key from OpenWeatherMap, and `'name-of-your-city'` with the actual city name.

Also remember to install the needed npm packages by running:
`npm install node-fetch node-schedule`

Before running the code, ensure you're abiding by free tier usage policy of OpenWeatherMap API, because making requests too frequently may result in suspending your API key.