#pragma once
#include <string>
#include <memory>
#include <vector>
#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>
#include "common/types.hpp"

namespace trading {

class DataLoader {
public:
    DataLoader();
    ~DataLoader();

    // Load data from Python data service
    MarketData loadMarketData(const std::string& symbol);
    
    // Load historical data
    std::vector<MarketData> loadHistoricalData(
        const std::string& symbol,
        const Timestamp& start,
        const Timestamp& end
    );
    
    // Subscribe to real-time data
    void subscribeToRealTimeData(
        const std::string& symbol,
        std::function<void(const MarketData&)> callback
    );

private:
    py::module data_service_;  // Python module
    py::object fetcher_;       // Python data fetcher instance
};

} // namespace trading