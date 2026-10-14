# TODO — Hoàn thành Lab 04: Weather Agent + MCP

## Phạm vi và trạng thái hiện tại

Luồng cần chạy được: **người dùng → ADK agent → MCP client → MCP server → WeatherAPI → câu trả lời**.

- [x] Repo đã có tại `D:\VIN_AI\week5\Day26-MCP-Tools-Integration`, `origin` trỏ đúng repo được yêu cầu và `main` khớp `origin/main` (commit `d089197`).
- [x] Mã nguồn đã có 3 MCP tools trong `mcp-server/weather.py`: `get_current_weather`, `get_forecast`, `health_check`.
- [x] `mcp-client/weather_agent/agent.py` đã khai báo `McpToolset` kết nối tới `/mcp`.
- [x] Chạy và kiểm chứng toàn bộ luồng bằng API key thật qua MCP, ADK CLI và ADK web API.

## Các bước thực hiện

### 1. Chuẩn bị môi trường

- [x] Tại `04-lab/mcp-server`, chạy `uv sync --locked` thành công.
- [x] Tại `04-lab/mcp-client`, chạy `uv sync --locked` thành công; `uv` dùng Python 3.13, đáp ứng `>=3.12`.
- [x] Cấu hình `WEATHERAPI_KEY` trong phiên chạy server và `GOOGLE_API_KEY` trong `mcp-client/.env` (Git bỏ qua `.env`).

### 2. Chạy MCP server và kiểm tra tools

- [x] Chạy `uv run python weather.py`; server lắng nghe tại `http://localhost:8085/mcp` cả khi không có terminal tương tác.
- [x] Dùng MCP client gọi `list_tools`: thấy đủ 3 tools trên.
- [x] Gọi `health_check`: thành công. Gọi hai weather tools khi chưa có key: nhận thông báo thiếu `WEATHERAPI_KEY`. `days=0` bị từ chối đúng giới hạn.
- [x] Gọi `get_current_weather(city="Hanoi")` và `get_forecast(city="Hanoi", days=3)` qua MCP: cả hai trả dữ liệu thật từ WeatherAPI.

### 3. Kết nối ADK agent

- [x] Tạo `04-lab/mcp-client/.env` với `GOOGLE_API_KEY=<key>`; URL dùng mặc định `http://localhost:8085/mcp`.
- [x] Chạy `uv run python verify_setup.py`: toàn bộ mục đạt.
- [x] Gọi `McpToolset.get_tools()` qua ADK: nhận đúng 3 MCP tools từ server.
- [x] Chạy `uv run adk web`: trang `http://localhost:8000` trả HTTP 200 và `/list-apps` có `weather_agent`.
- [x] Gọi `/run` trên ADK web: agent chọn `get_current_weather` cho câu hỏi hiện tại và `get_forecast` cho câu hỏi dự báo 3 ngày, rồi trả lời bằng dữ liệu tool. Cũng đã kiểm tra hai câu hỏi qua `adk run weather_agent`.

### 4. Hoàn thiện và kiểm chứng

- [x] Chặn thành phố trống và `days` ngoài khoảng 1–3; xác nhận thiếu WeatherAPI key trả thông báo rõ.
- [x] Gọi thành phố không tồn tại qua MCP: trả thông báo `No matching location found.`; kết quả Hanoi không còn dư dấu phẩy khi `region` trống.
- [x] Thêm 5 kiểm thử không cần mạng cho tham số, dữ liệu dự báo và lỗi thiếu key; `uv run python -m unittest -v test_weather.py` đạt 5/5.
- [x] Cập nhật `04-lab/README.md` với lệnh PowerShell và cách kiểm tra tools/agent.
- [x] Kiểm tra `git status`: `.env` không xuất hiện trong thay đổi chuẩn bị nộp. Log HTTP không còn ghi URL chứa WeatherAPI key.

## Hoàn thành khi

`list_tools` thấy đủ 3 tools, hai weather tools trả dữ liệu thật, `verify_setup.py` đạt, và ADK web trả lời được cả câu hỏi thời tiết hiện tại lẫn dự báo qua MCP.

Triển khai Cloud Run chỉ thực hiện nếu yêu cầu nộp bài cần endpoint từ xa; README hiện mô tả chạy local và có Dockerfile để mở rộng.
