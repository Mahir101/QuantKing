#include "risk_manager.hpp"
#include <spdlog/spdlog.h>
#include <algorithm>

namespace trading {

RiskManager::RiskManager(const RiskLimits& limits) : limits_(limits) {}

bool RiskManager::checkOrderRisk(const Order& order, const Portfolio& portfolio) {
    std::lock_guard<std::mutex> lock(mutex_);
    
    try {
        // 1. Check single position size limit
        double position_value = order.getQuantity() * order.getPrice();
        double portfolio_value = portfolio.getTotalValue(current_prices_);
        
        if (position_value / portfolio_value > limits_.max_position_size) {
            spdlog::warn("Position size limit exceeded for {}", order.getSymbol());
            return false;
        }
        
        // 2. Check leverage limit
        double total_exposure = portfolio.getTotalExposure() + position_value;
        if (total_exposure / portfolio_value > limits_.max_leverage) {
            spdlog::warn("Leverage limit exceeded");
            return false;
        }
        
        // 3. Check drawdown limit
        if (portfolio.getDrawdown() > limits_.max_drawdown) {
            spdlog::warn("Drawdown limit exceeded");
            return false;
        }
        
        // 4. Check daily loss limit
        if (portfolio.getDailyPnL() < -limits_.daily_loss_limit) {
            spdlog::warn("Daily loss limit exceeded");
            return false;
        }
        
        // 5. Check concentration limit
        auto position = portfolio.getPosition(order.getSymbol());
        double new_position_size = (position ? position->getQuantity() : 0) + order.getQuantity();
        double new_concentration = new_position_size * order.getPrice() / portfolio_value;
        
        if (new_concentration > limits_.position_concentration) {
            spdlog::warn("Position concentration limit exceeded for {}", order.getSymbol());
            return false;
        }
        
        // Update risk metrics
        updateRiskMetrics(portfolio);
        return true;
        
    } catch (const std::exception& e) {
        spdlog::error("Error in risk check: {}", e.what());
        return false;
    }
}

void RiskManager::updateRiskMetrics(const Portfolio& portfolio) {
    std::lock_guard<std::mutex> lock(mutex_);
    
    try {
        // Update risk metrics
        current_metrics_["drawdown"] = portfolio.getDrawdown();
        current_metrics_["leverage"] = portfolio.getLeverage();
        current_metrics_["daily_pnl"] = portfolio.getDailyPnL();
        current_metrics_["concentration"] = portfolio.getConcentration();
        
        // Log risk metrics
        spdlog::debug("Risk metrics updated: drawdown={:.2f}%, leverage={:.2f}x, daily_pnl=${:.2f}",
            current_metrics_["drawdown"] * 100,
            current_metrics_["leverage"],
            current_metrics_["daily_pnl"]);
            
    } catch (const std::exception& e) {
        spdlog::error("Error updating risk metrics: {}", e.what());
    }
}

std::map<std::string, double> RiskManager::getRiskMetrics() const {
    std::lock_guard<std::mutex> lock(mutex_);
    return current_metrics_;
}

void RiskManager::updateCurrentPrices(const std::map<std::string, double>& prices) {
    std::lock_guard<std::mutex> lock(mutex_);
    current_prices_ = prices;
}

} // namespace trading