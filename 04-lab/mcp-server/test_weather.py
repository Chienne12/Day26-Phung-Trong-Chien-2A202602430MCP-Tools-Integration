import unittest
from unittest.mock import AsyncMock, patch

import weather


class WeatherToolsTest(unittest.IsolatedAsyncioTestCase):
    async def test_blank_city_does_not_call_weatherapi(self):
        with patch.object(weather, "make_weather_request", new_callable=AsyncMock) as request:
            current = await weather.get_current_weather("  ")
            forecast = await weather.get_forecast("  ")
            self.assertIn("city name", current)
            self.assertIn("city name", forecast)
            request.assert_not_awaited()

    async def test_forecast_rejects_days_outside_free_tier(self):
        with patch.object(weather, "make_weather_request", new_callable=AsyncMock) as request:
            for days in (0, -1, 4):
                with self.subTest(days=days):
                    result = await weather.get_forecast("Hanoi", days)
                    self.assertIn("1 to 3 days", result)
            request.assert_not_awaited()

    async def test_forecast_reads_weatherapi_data(self):
        data = {
            "location": {"name": "Hanoi", "region": "", "country": "Vietnam"},
            "forecast": {"forecastday": [{
                "date": "2026-10-14",
                "day": {
                    "maxtemp_c": 30, "maxtemp_f": 86,
                    "mintemp_c": 23, "mintemp_f": 73.4,
                    "condition": {"text": "Sunny"},
                    "daily_chance_of_rain": 10, "maxwind_kph": 15, "uv": 6,
                },
            }]},
        }
        with patch.object(weather, "make_weather_request", new_callable=AsyncMock, return_value=data) as request:
            result = await weather.get_forecast("Hanoi", 1)

        request.assert_awaited_once_with("forecast.json", {
            "q": "Hanoi", "days": "1", "aqi": "no", "alerts": "no"
        })
        self.assertIn("2026-10-14", result)
        self.assertIn("High: 30°C", result)
        self.assertIn("Hanoi, Vietnam", result)
        self.assertNotIn("Hanoi, , Vietnam", result)

    async def test_unknown_city_returns_clear_error(self):
        with patch.object(weather, "make_weather_request", new_callable=AsyncMock,
                          return_value={"error": "No matching location found."}):
            result = await weather.get_current_weather("unknown-city")
        self.assertIn("Unable to find city unknown-city", result)

    async def test_current_weather_reports_missing_key(self):
        with patch.object(weather, "API_KEY", None):
            result = await weather.get_current_weather("Hanoi")
        self.assertIn("WEATHERAPI_KEY", result)


if __name__ == "__main__":
    unittest.main()
