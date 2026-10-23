# Naive consumption model for CHAP

Proof-of-concept model for the CHAP `health_supply` domain. Forecasts monthly
product consumption per location (`site|product`) as Poisson samples around the
mean of the last 6 recorded months. Missing entries are skipped; recorded zeros
count as observations.

Declares `target: consumption`, `domain: health_supply` and the required
covariate `stock_on_hand` in `MLproject`.
