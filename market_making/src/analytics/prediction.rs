

use std::collections::HashMap;
use rust_decimal::Decimal;

pub struct PricePrediction {
    pub timestamp: i64,
    pub price: Decimal,
    pub confidence: f64,
}

pub trait Predictor {
    fn predict(&self, historical_data: &HashMap<i64, Decimal>) -> PricePrediction;
}