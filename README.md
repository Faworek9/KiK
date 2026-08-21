# Kółko i Krzyżyk - Refaktoryzacja z Q-Learning

Program kółko i krzyżyk z implementacją Q-learning i strategicznego AI. Refaktoryzacja oryginalnego monolitycznego kodu w modułową architekturę.

## Ideą

Program uczy się grać w kółko i krzyżyk używając Q-learning. Agent Q-learning gra przeciwko strategicznemu AI (opartemu na minimax z alpha-beta pruning), co pozwala na efektywniejszą naukę - uczysz się walcząc z ekspertem, a nie z amatorami.

## Architektura

Projekt jest podzielony na moduły:

- **config.py** - Konfiguracja (stałe, parametry treningu, ścieżki plików)
- **game/** - Logika gry (plansza, zasady, silnik gry)
- **ai/** - Sztuczna inteligencja (strategic AI, Q-learning agent)
- **training/** - Trening (trainer, statystyki)
- **storage/** - Zapis/odczyt (Q-table w JSON)
- **main.py** - Punkt wejścia
- **Q-Learing_Reset.py** - Reset plików treningowych

## Konfiguracja

W pliku `config.py` możesz ustawić strategię dla każdego gracza:

```python
# Player strategy configuration
# Options: StrategyType.STRATEGIC, StrategyType.Q_LEARNING, StrategyType.RANDOM
PLAYER_X_STRATEGY: Final[StrategyType] = StrategyType.STRATEGIC
PLAYER_O_STRATEGY: Final[StrategyType] = StrategyType.Q_LEARNING
```

**Przykłady:**
- X = Strategic, O = Q-Learning (domyślne) - O uczy się grając przeciwko strategicznemu X
- X = Q-Learning, O = Strategic - X uczy się grając przeciwko strategicznemu O
- Obaj Strategic - testy idealnej gry (powinny być same remisy)
- Obaj Random - testy losowe

## Uruchomienie

```bash
python main.py
```

Program przeprowadza trening w dwóch etapach:
1. Test run - 100 gier
2. Full training - 10,000 gier

Wyniki są zapisywane do plików:
- `q_X.json` / `q_O.json` - Q-table dla odpowiedniego gracza
- `wyniki_X.txt` / `wyniki_O.txt` - statystyki treningu

## Parametry treningu

Wszystkie parametry są w `config.py`:
- `INITIAL_EPSILON` - początkowa eksploracja (0.7)
- `EPSILON_DECAY` - zmniejszanie eksploracji (0.02)
- `MIN_EPSILON` - minimalna eksploracja (0.2)
- `GAMMA_NEGATIVE` - dyskontowanie dla negatywnych nagród (0.5)
- `GAMMA_POSITIVE` - dyskontowanie dla pozytywnych nagród (0.8)
- `GAMES_COUNT` - liczba gier treningowych (10,000)
- `SAVE_INTERVAL` - zapis co N gier (100)
