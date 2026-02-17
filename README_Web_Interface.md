# Trading System Web Interface

A modern management interface providing a user-friendly way to interact with the trading system.

## 🚀 Technology Stack

### Backend
- **FastAPI** - High-performance Python web framework
- **Uvicorn** - ASGI server
- **Pydantic** - Data validation and serialization

### Frontend
- **HTML5** - Semantic markup
- **CSS3** - Modern styling
- **JavaScript (ES6+)** - Interactive logic
- **Bootstrap 5** - Responsive UI framework
- **Chart.js** - Charting library
- **Boxicons** - Icon library

## 📦 Installation

### 1. Install Dependencies

```bash
# Install all dependencies (including web interface)
pip install -e .[web,ai,visualization]

# Or install web dependencies separately
pip install fastapi uvicorn jinja2 aiofiles
```

### 2. Start Web Interface

```bash
# Method 1: Using the startup script
python run_web_interface.py

# Method 2: Directly starting the FastAPI server
uvicorn data_service.web.api_server:APIServer().app --host 0.0.0.0 --port 8000 --reload
```

### 3. Access the Interface

Open your browser and navigate to: http://localhost:8000

## 🎯 Features

### 📊 Dashboard
- **System Status Monitoring** - Real-time display of system operational status
- **Performance Metrics** - Total Return, Sharpe Ratio, Max Drawdown, etc.
- **Risk Metrics** - Risk indicators such as VaR, CVaR, Beta, etc.
- **Equity Curve** - Interactive yield curve charts
- **Portfolio Allocation** - Pie charts showing asset allocation
- **Recent Activity** - Real-time activity logs
- **Recent Trades** - Transaction record tables

### 🎮 Strategy Management
- **Strategy List** - Displays all available strategies
- **Strategy Details** - View strategy configuration and performance
- **Create Strategy** - Create new strategies via forms
- **Start/Stop** - Control operational status of strategies
- **Strategy Backtesting** - Run strategy backtests and view results

### 📈 Backtesting System
- **Backtest Configuration** - Set backtest parameters
- **Strategy Selection** - Choose the strategy to backtest
- **Time Range** - Set the time frame for backtesting
- **Results Display** - Show backtest results and charts

### 💼 Portfolio Management
- **Position Information** - Display current holdings
- **Portfolio Summary** - Total value, cash, and invested amounts
- **PnL Analysis** - Daily and total Profit/Loss
- **Weight Allocation** - Weighting of each asset

### 🤖 AI Analysis
- **Sentiment Analysis** - Analyze text sentiment
- **Market Analysis** - AI-driven market insights
- **Real-time Results** - Instant display of analysis results

## 🔧 API Endpoints

### System Status
```http
GET /api/system/status
```

### Strategy Management
```http
GET /api/strategies
POST /api/strategies
PUT /api/strategies/{id}
DELETE /api/strategies/{id}
POST /api/strategies/{id}/start
POST /api/strategies/{id}/stop
```

### Backtesting
```http
POST /api/backtest/run
```

### AI Analysis
```http
POST /api/ai/analyze
```

### Market Data
```http
GET /api/market/data/{symbol}
```

### Portfolio
```http
GET /api/portfolio/status
```

### Transaction History
```http
GET /api/trades/recent
```

## 🎨 Interface Screenshots

### Main Dashboard
- System Status Overview
- Performance Metric Cards
- Real-time Charts
- Activity Logs

### Strategy Management
- Strategy Card Grid
- Strategy Detail Modals
- Start/Stop Controls

### Backtesting Interface
- Configuration Forms
- Results Display
- Performance Charts

## 🔒 Security Features

- **CORS Support** - Cross-origin request handling
- **Input Validation** - Data validation via Pydantic
- **Error Handling** - Unified error response format
- **Logging** - Comprehensive operation logs

## 📱 Responsive Design

- **Mobile Friendly** - Support for phones and tablets
- **Desktop Optimized** - Optimization for large screen displays
- **Touch Friendly** - Support for touch operations

## 🚀 Deployment

### Development Environment
```bash
python run_web_interface.py
```

### Production Environment
```bash
# Using Gunicorn
gunicorn data_service.web.api_server:APIServer().app -w 4 -k uvicorn.workers.UvicornWorker

# Using Docker
docker build -t trading-system .
docker run -p 8000:8000 trading-system
```

### Reverse Proxy (Nginx)
```nginx
server {
    listen 80;
    server_name your-domain.com;
    
    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

## 🔧 Configuration

### Environment Variables
```bash
export TRADING_SYSTEM_HOST=0.0.0.0
export TRADING_SYSTEM_PORT=8000
export TRADING_SYSTEM_DEBUG=true
```

### Configuration File
Create `config.json`:
```json
{
    "web": {
        "host": "0.0.0.0",
        "port": 8000,
        "debug": false,
        "cors_origins": ["*"]
    },
    "trading": {
        "initial_capital": 100000,
        "commission_rate": 0.001
    }
}
```

## 🐛 Troubleshooting

### Common Issues

1. **Port Occupied**
   ```bash
   # Check port usage
   netstat -tulpn | grep 8000
   
   # Kill process
   kill -9 <PID>
   ```

2. **Missing Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Permission Issues**
   ```bash
   # Linux/Mac
   chmod +x run_web_interface.py
   
   # Windows
   python run_web_interface.py
   ```

### Log Viewing
```bash
# View application logs
tail -f logs/trading_system.log

# View error logs
tail -f logs/error.log
```

## 📈 Performance Optimization

### Frontend Optimization
- Lazy loading for charts
- Data caching
- Compression of static assets

### Backend Optimization
- Database connection pooling
- Redis caching
- Asynchronous processing

## 🔮 Future Plans

- [ ] Real-time data push (WebSocket)
- [ ] User authentication and authorization
- [ ] Multi-language support
- [ ] Mobile App
- [ ] Advanced charting features
- [ ] Backtest comparison
- [ ] Risk management panel
- [ ] Report generator

## 📞 Support

For questions or suggestions, please:
1. Refer to the documentation
2. Check the logs
3. Submit an Issue
4. Contact the development team

---

**Trading System Web Interface** - Making trading system management simple and efficient! 🚀