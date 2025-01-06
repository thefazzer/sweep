

use rust_decimal::Decimal;

pub struct ProfitMetrics {
    pub realized_pnl: Decimal,
    pub unrealized_pnl: Decimal,
    pub total_fees: Decimal,
}

pub trait ProfitCalculator {
    fn calculate_profit(&self) -> ProfitMetrics;
}