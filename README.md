# 8-Queens Problem Visualizer

## Overview
A Python-based GUI application that visually demonstrates two different algorithms for solving the classic 8-Queens problem:
1. **Backtracking Algorithm** - A systematic approach that explores all possible configurations
2. **Las Vegas Algorithm** - A probabilistic approach that makes random choices constrained by the problem rules

The application features an interactive chessboard with real-time visualization of the algorithms' progress, adjustable animation speed, and performance statistics.

**Backtracking Algorithm**
![8-Queens **Backtracking Algorithm**](./assets/Screenshot%20from%202025-04-22%2018-59-02.png)

**Las Vegas Algorithm**
![8-Queens **Las Vegas Algorithm**](./assets/Screenshot%20from%202025-04-22%2018-59-14.png)

## Table of Contents
- [Installation](#installation)
- [Usage](#usage)
- [Features](#features)
- [Configuration](#configuration)
- [Algorithm Details](#algorithm-details)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## Installation
1. Ensure you have Python 3.x installed
2. Clone the repository:
   ```bash
   git clone https://github.com/MadhavSinha007/N-8-QueenProblem_Visualization.git
   cd N-8-QueenProblem_Visualization
   ```
3. The application uses only standard Python libraries (tkinter), so no additional packages are required.

## Usage
Run the application with:
```bash
python eight_queens.py
```

**Interface Controls:**
* **Backtracking Button**: Runs the systematic backtracking algorithm
* **Las Vegas Button**: Runs the probabilistic constrained algorithm
* **Reset Button**: Clears the board and resets statistics
* **Speed Slider**: Adjusts the animation speed (Slow to Fast)

## Features
* **Interactive Chessboard**: Visually displays queen placements and conflicts
* **Real-time Animation**: Shows the algorithm's progress step-by-step
* **Algorithm Comparison**: Demonstrates two fundamentally different approaches
* **Performance Metrics**: Tracks number of attempts/steps for each algorithm
* **Adjustable Speed**: Control the visualization speed to suit your preference
* **Responsive UI**: Clean, intuitive interface with status updates

## Configuration
The application can be customized by modifying these constants in the code:
```python
# Theme colors
CREAM = "#F5F0E1"
LIGHT_BROWN = "#E1C699"
MEDIUM_BROWN = "#C19A6B"
DARK_BROWN = "#5C4033"
HIGHLIGHT_COLOR = "#4C8BF5"

# Board size (change to make it N-Queens)
BOARD_SIZE = 8
```

## Algorithm Details

### Backtracking Algorithm
* Systematically places queens column by column
* Backtracks when a conflict is detected
* Guaranteed to find a solution but may take longer
* Visualized with red queens and highlighted active column

### Las Vegas Algorithm
* Places queens randomly but with constraints
* May fail and need to restart
* Often finds solutions faster on average
* Visualized with green queens and highlighted active column

## Contributing
Contributions are welcome! Please follow these steps:
1. Fork the repository
2. Create a new branch (`git checkout -b feature/improvement`)
3. Make your changes
4. Commit your changes (`git commit -m 'Add some feature'`)
5. Push to the branch (`git push origin feature/improvement`)
6. Open a Pull Request

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact
* Madhav Sinha - madhavsinha.prg@gmail.com
* Project Link: https://github.com/MadhavSinha007/N-8-QueenProblem_Visualization