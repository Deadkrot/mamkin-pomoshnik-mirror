def feeds_by_age_months(m: int) -> int:
    if m <= 2:  return 7      # 0–2 мес
    if m <= 5:  return 6      # 3–5 мес
    if m <= 8:  return 5      # 6–8 мес
    return 4                  # 9–12 мес

def wake_windows_by_age_months(m: int):
    # Окна бодрствования по возрасту (часы, приблизительно)
    if m <= 2:  return [1.0, 1.0, 1.0, 1.0, 1.5]
    if m <= 4:  return [1.5, 1.75, 2.0, 1.75]
    if m <= 6:  return [2.0, 2.5, 2.75]
    if m <= 9:  return [2.5, 3.0]   # переход к 2 снам
    return [3.0, 3.5]               # стабильные 2 сна

def naps_count_by_age_months(m: int) -> int:
    # Кол-во дневных снов по возрасту
    if m <= 4:  return 4
    if m <= 6:  return 3
    return 2
