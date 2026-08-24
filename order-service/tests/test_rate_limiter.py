from app.rate_limiter import RateLimiter


def test_rate_limiter_accepts_positive_rate():

    limiter = RateLimiter(50)

    assert limiter.interval == 0.02