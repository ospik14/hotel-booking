from datetime import date, timedelta


def auth_header(token: str) -> dict:
    return {'Authorization': f'Bearer {token}'}


def future_dates(start_offset: int = 1, nights: int = 2) -> tuple[str, str]:
    check_in = date.today() + timedelta(days=start_offset)
    check_out = check_in + timedelta(days=nights)
    return check_in.isoformat(), check_out.isoformat()
