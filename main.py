"""Main entry point for tic-tac-toe training."""

from training.trainer import Trainer
import config


def main():
    """Main function to run training."""
    print("Starting tic-tac-toe Q-learning training...")
    print(f"Games: {config.GAMES_COUNT}")
    print(f"Initial epsilon: {config.INITIAL_EPSILON}")
    print(f"Player X strategy: {config.PLAYER_X_STRATEGY.value}")
    print(f"Player O strategy: {config.PLAYER_O_STRATEGY.value}")
    print(f"Q-learning algorithm: {config.Q_LEARNING_ALGORITHM.value}")
    
    trainer = Trainer()
    
    # Test with smaller number first
    print("Test run with 100 games...")
    trainer.train(number_of_games=100)
    
    print("Test run completed successfully!")
    print("Starting full training...")
    
    # Reset for full training
    trainer = Trainer()
    trainer.train(number_of_games=config.GAMES_COUNT)
    
    print("Training completed!")


if __name__ == "__main__":
    main()
