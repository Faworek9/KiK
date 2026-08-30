# Kółko i Krzyżyk - Refaktoryzacja z Q-Learning

Program kółko i krzyżyk z implementacją Q-learning i strategicznego AI.

## Ideą

Program uczy się grać w kółko i krzyżyk używając Q-learning. Agent Q-learning gra przeciwko strategicznemu AI, co pozwala na efektywniejszą naukę - uczysz się walcząc z ekspertem, a nie z amatorami.

## Architektura

Projekt jest podzielony na moduły:

- **config.py** - Konfiguracja (stałe, parametry treningu, ścieżki plików)
- **game/** - Logika gry (plansza, zasady, silnik gry)
- **strategic/** - Algorytmy strategiczne (Minimax, Hybrid, Legacy)
- **ai/** - Sztuczna inteligencja (np. `ai/q_learning_legacy.py`)
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
- X = Strategic, O = Q-Learning - O uczy się grając przeciwko strategicznemu X
- X = Q-Learning, O = Strategic - X uczy się grając przeciwko strategicznemu O
- Obaj Strategic - testy idealnej gry (powinny być same remisy)
- Obaj Random - testy losowe

### Wybór algorytmu strategicznego

Dla strategicznego AI możesz wybrać algorytm w pliku `config.py`:

```python
# Strategic algorithm configuration
# Options: StrategicAlgorithmType.MINIMAX, StrategicAlgorithmType.HYBRID, StrategicAlgorithmType.LEGACY
STRATEGIC_ALGORITHM: Final[StrategicAlgorithmType] = StrategicAlgorithmType.LEGACY
```

**Dostępne algorytmy:**
- **MINIMAX** - Algorytm minimax z alpha-beta pruning (plik `strategic/move_finder_minimax.py`). Gwarantuje idealną grę, ale jest wolniejszy.
- **HYBRID** - Hybrydowy algorytm łączący heurystyczną hierarchię priorytetów z taktyczną analizą kilku ruchów do przodu (plik `strategic/move_finder_hybrid.py`). Jest kilkukrotnie szybszy od minimax i oferuje bardzo dobrą jakość gry.
- **LEGACY** - Czysto heurystyczny algorytm bez minmax (plik `strategic/move_finder_legacy.py`). Jest prosty, szybki i działa symetrycznie dla X oraz O.

### Wybór algorytmu Q-Learning

Dla agenta Q-learning możesz wybrać algorytm w pliku `config.py`:

```python
# Q-learning algorithm configuration
# Options: QLearningAlgorithmType.LEGACY, QLearningAlgorithmType.UPGRADED
Q_LEARNING_ALGORITHM: Final[QLearningAlgorithmType] = QLearningAlgorithmType.LEGACY
```

**Dostępne warianty:**
- **LEGACY** - Oryginalna implementacja z `kolko_legacy.py` (plik `ai/q_learning_legacy.py`).
- **UPGRADED** - Nowa wersja Q-learning przygotowana pod kolejne usprawnienia (plik `ai/q_learning_upgraded.py`).


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
