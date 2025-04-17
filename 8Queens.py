import tkinter as tk
from tkinter import ttk, font, Scale
import random
import time
import threading
import queue

class EightQueens:
    def __init__(self, root):
        self.root = root
        self.root.title("8-Queens Problem Visualizer")
        self.root.geometry("800x700")
        
        # Define theme colors
        self.CREAM = "#F5F0E1"
        self.LIGHT_BROWN = "#E1C699"
        self.MEDIUM_BROWN = "#C19A6B"
        self.DARK_BROWN = "#5C4033"
        self.HIGHLIGHT_COLOR = "#4C8BF5"  # Blue highlight
        
        # Configure the root window background
        self.root.configure(bg=self.CREAM)
        
        # Create a style for ttk widgets
        self.style = ttk.Style()
        self.style.theme_use('default')
        self.style.configure('TFrame', background=self.CREAM)
        self.style.configure('TButton', background=self.MEDIUM_BROWN, foreground=self.DARK_BROWN, font=('Arial', 10, 'bold'))
        self.style.configure('TLabel', background=self.CREAM, foreground=self.DARK_BROWN, font=('Arial', 10))
        self.style.configure('Header.TLabel', background=self.CREAM, foreground=self.DARK_BROWN, font=('Arial', 16, 'bold'))
        self.style.configure('Status.TLabel', background=self.CREAM, foreground=self.DARK_BROWN, font=('Arial', 12))
        self.style.configure('Counter.TLabel', background=self.CREAM, foreground=self.DARK_BROWN, font=('Arial', 14, 'bold'))
        
        self.BOARD_SIZE = 8
        self.is_processing = False
        self.backtracking_solution = None
        self.constrained_solution = None
        self.backtracking_steps = 0
        self.constrained_attempts = 0
        
        # Animation speed (delay in seconds)
        self.animation_speed = 0.1
        
        # Queue for thread-safe UI updates
        self.update_queue = queue.Queue()
        
        # Store queen labels for efficient updates
        self.queen_widgets = [[None for _ in range(self.BOARD_SIZE)] for _ in range(self.BOARD_SIZE)]
        self.board_squares = [[None for _ in range(self.BOARD_SIZE)] for _ in range(self.BOARD_SIZE)]
        
        # Keep track of previous solution state for incremental updates
        self.previous_solution = []
        
        self.create_widgets()
        self.create_fixed_board()
        
        # Start the update checker
        self.check_queue()
    
    def check_queue(self):
        """Process any pending UI updates from the queue"""
        try:
            while True:
                # Get all available updates (non-blocking)
                func = self.update_queue.get_nowait()
                func()
                self.update_queue.task_done()
        except queue.Empty:
            pass
        # Schedule the next check
        self.root.after(50, self.check_queue)
    
    def create_widgets(self):
        # Main frame
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Title
        self.title_label = ttk.Label(self.main_frame, text="Eight Queens Visualization", style='Header.TLabel')
        self.title_label.pack(pady=(0, 15))
        
        # Container for board and controls
        self.content_frame = ttk.Frame(self.main_frame)
        self.content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Left panel for chess board
        self.left_panel = ttk.Frame(self.content_frame)
        self.left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Chess board with decorative frame
        self.board_frame = ttk.Frame(self.left_panel, borderwidth=2, relief=tk.RIDGE)
        self.board_frame.pack(padx=10, pady=10)
        
        self.chess_board = tk.Frame(self.board_frame, bg=self.DARK_BROWN, padx=5, pady=5)
        self.chess_board.pack(padx=5, pady=5)
        
        # Right panel for controls
        self.right_panel = ttk.Frame(self.content_frame, width=200)
        self.right_panel.pack(side=tk.RIGHT, fill=tk.Y, padx=(10, 0))
        
        # Algorithm selection frame
        self.algo_frame = ttk.LabelFrame(self.right_panel, text="Algorithms", padding=10)
        self.algo_frame.pack(fill=tk.X, pady=5)
        
        self.solve_backtracking_btn = ttk.Button(
            self.algo_frame, text="Backtracking", 
            command=lambda: self.start_processing("Backtracking", self.solve_with_backtracking)
        )
        self.solve_backtracking_btn.pack(fill=tk.X, pady=(0, 5))
        
        self.solve_constrained_btn = ttk.Button(
            self.algo_frame, text="Las Vegas", 
            command=lambda: self.start_processing("Las Vegas", self.solve_with_constrained)
        )
        self.solve_constrained_btn.pack(fill=tk.X, pady=(0, 5))
        
        self.reset_btn = ttk.Button(self.algo_frame, text="Reset Board", command=self.reset_board)
        self.reset_btn.pack(fill=tk.X)
        
        # Speed control frame
        self.speed_frame = ttk.LabelFrame(self.right_panel, text="Animation Speed", padding=10)
        self.speed_frame.pack(fill=tk.X, pady=10)
        
        self.speed_scale = Scale(
            self.speed_frame,
            from_=1,
            to=10,
            orient=tk.HORIZONTAL,
            label="",
            showvalue=False,
            command=self.update_speed,
            bg=self.CREAM,
            highlightthickness=0,
            troughcolor=self.LIGHT_BROWN,
            activebackground=self.MEDIUM_BROWN
        )
        self.speed_scale.set(5)  # Default speed
        self.speed_scale.pack(fill=tk.X)
        
        self.speed_label = ttk.Label(self.speed_frame, text="Normal", anchor=tk.CENTER)
        self.speed_label.pack(fill=tk.X)
        
        # Statistics frame
        self.stats_frame = ttk.LabelFrame(self.right_panel, text="Statistics", padding=10)
        self.stats_frame.pack(fill=tk.X, pady=10)
        
        # Step counter
        self.step_counter_frame = ttk.Frame(self.stats_frame)
        self.step_counter_frame.pack(fill=tk.X, pady=5)
        
        self.step_counter_label = ttk.Label(self.step_counter_frame, text="Steps:", anchor=tk.W)
        self.step_counter_label.pack(side=tk.LEFT)
        
        self.step_counter_value = ttk.Label(self.step_counter_frame, text="0", style="Counter.TLabel", anchor=tk.E)
        self.step_counter_value.pack(side=tk.RIGHT)
        
        # Attempts counter (for Las Vegas)
        self.attempts_frame = ttk.Frame(self.stats_frame)
        self.attempts_frame.pack(fill=tk.X, pady=5)
        
        self.attempts_label = ttk.Label(self.attempts_frame, text="Attempts:", anchor=tk.W)
        self.attempts_label.pack(side=tk.LEFT)
        
        self.attempts_value = ttk.Label(self.attempts_frame, text="0", style="Counter.TLabel", anchor=tk.E)
        self.attempts_value.pack(side=tk.RIGHT)
        
        # Status frame
        self.status_frame = ttk.Frame(self.main_frame)
        self.status_frame.pack(fill=tk.X, pady=(10, 0))
        
        self.status_label = ttk.Label(
            self.status_frame, 
            text="Ready", 
            anchor=tk.CENTER, 
            style="Status.TLabel"
        )
        self.status_label.pack(fill=tk.X)
        
        # Animation timer
        self.animation_timer = None
    
    def update_speed(self, value):
        """Update animation speed based on slider value"""
        speed_value = int(value)
        self.animation_speed = 0.2 * (11 - speed_value) / 10  # Map 1-10 to slower-faster
        
        # Update speed label text
        if speed_value <= 3:
            self.speed_label.config(text="Slow")
        elif speed_value <= 7:
            self.speed_label.config(text="Normal")
        else:
            self.speed_label.config(text="Fast")
    
    def create_fixed_board(self):
        """Create a fixed chess board that won't be recreated for each update"""
        # Clear any existing board
        for widget in self.chess_board.winfo_children():
            widget.destroy()
        
        # Reset queen widgets
        self.queen_widgets = [[None for _ in range(self.BOARD_SIZE)] for _ in range(self.BOARD_SIZE)]
        
        # Create a grid layout
        for row in range(self.BOARD_SIZE):
            self.chess_board.rowconfigure(row, weight=1)
            for col in range(self.BOARD_SIZE):
                self.chess_board.columnconfigure(col, weight=1)
                square = tk.Frame(
                    self.chess_board,
                    width=60,
                    height=60,
                    bg=self.LIGHT_BROWN if (row + col) % 2 == 0 else self.MEDIUM_BROWN,
                    highlightthickness=1,
                    highlightbackground=self.DARK_BROWN
                )
                square.grid(row=row, column=col, sticky='nsew')
                
                # Add row/column labels
                if row == self.BOARD_SIZE - 1:
                    col_label = tk.Label(
                        square, 
                        text=chr(97 + col),  # a, b, c, ...
                        font=('Arial', 8),
                        fg=self.DARK_BROWN,
                        bg=square.cget('bg')
                    )
                    col_label.place(relx=0.85, rely=0.85, anchor='se')
                
                if col == 0:
                    row_label = tk.Label(
                        square, 
                        text=str(8 - row),  # 8, 7, 6, ...
                        font=('Arial', 8),
                        fg=self.DARK_BROWN,
                        bg=square.cget('bg')
                    )
                    row_label.place(relx=0.15, rely=0.15, anchor='nw')
                
                self.board_squares[row][col] = square
    
    def start_processing(self, algorithm, solver_func):
        if not self.is_processing:
            self.is_processing = True
            self.solve_backtracking_btn.config(state=tk.DISABLED)
            self.solve_constrained_btn.config(state=tk.DISABLED)
            self.reset_btn.config(state=tk.DISABLED)
            self.status_label.config(text=f"{algorithm} running...")
            self.start_animation()
            
            # Reset previous solution for animation purposes
            self.previous_solution = []
            
            # Reset counters
            if algorithm == "Backtracking":
                self.backtracking_steps = 0
                self.update_step_counter(0)
                self.attempts_value.config(text="0")
            else:  # Las Vegas
                self.constrained_attempts = 0
                self.step_counter_value.config(text="0")
                self.update_attempts_counter(0)
            
            # Run solver in separate thread
            threading.Thread(target=solver_func, daemon=True).start()
    
    def start_animation(self):
        self.stop_animation()
        self.animate_status()
    
    def animate_status(self):
        if self.is_processing:
            text = self.status_label.cget("text")
            base_text = text.rstrip('.')
            dots = text[len(base_text):]
            
            if len(dots) >= 3:
                self.status_label.config(text=base_text)
            else:
                self.status_label.config(text=base_text + dots + '.')
                
            self.animation_timer = self.root.after(500, self.animate_status)
    
    def stop_animation(self):
        if self.animation_timer:
            self.root.after_cancel(self.animation_timer)
            self.animation_timer = None
    
    def end_processing(self):
        # Use update_queue to ensure thread-safety
        self.update_queue.put(lambda: self._end_processing())
    
    def _end_processing(self):
        """Actual implementation of end_processing, run on the main thread"""
        self.is_processing = False
        self.solve_backtracking_btn.config(state=tk.NORMAL)
        self.solve_constrained_btn.config(state=tk.NORMAL)
        self.reset_btn.config(state=tk.NORMAL)
        self.stop_animation()
    
    def reset_board(self):
        if not self.is_processing:
            self.backtracking_solution = None
            self.constrained_solution = None
            self.backtracking_steps = 0
            self.constrained_attempts = 0
            self.status_label.config(text="Ready")
            self.update_step_counter(0)
            self.update_attempts_counter(0)
            self.clear_queens()
            self.previous_solution = []
    
    def clear_queens(self):
        """Remove all queens from the board without recreating the board itself"""
        self.update_queue.put(self._clear_queens)
    
    def _clear_queens(self):
        """Remove all queens from the board (run on main thread)"""
        for row in range(self.BOARD_SIZE):
            for col in range(self.BOARD_SIZE):
                if self.queen_widgets[row][col]:
                    self.queen_widgets[row][col].destroy()
                    self.queen_widgets[row][col] = None
    
    def update_status(self, text):
        """Thread-safe status update"""
        self.update_queue.put(lambda text=text: self.status_label.config(text=text))
    
    def update_step_counter(self, steps):
        """Thread-safe step counter update"""
        self.update_queue.put(lambda s=steps: self.step_counter_value.config(text=str(s)))
    
    def update_attempts_counter(self, attempts):
        """Thread-safe attempts counter update"""
        self.update_queue.put(lambda a=attempts: self.attempts_value.config(text=str(a)))
    
    def update_queen_positions(self, solution, algorithm, active_col=None):
        """Thread-safe update for queen positions"""
        # Make a copy to avoid race conditions
        solution_copy = solution.copy() if solution else []
        self.update_queue.put(lambda soln=solution_copy, alg=algorithm, col=active_col: 
                              self._update_queen_positions_incremental(soln, alg, col))
        
        # Update status if a specific column is being worked on
        if active_col is not None:
            status_text = f"{algorithm}: Placing queen {active_col+1}/{self.BOARD_SIZE}"
            self.update_queue.put(lambda text=status_text: self.status_label.config(text=text))
    
    def _update_queen_positions_incremental(self, new_solution, algorithm, active_col=None):
        """Update queen positions incrementally, only changing what's necessary"""
        # Convert solutions to list format for comparison
        current_board = [-1] * self.BOARD_SIZE
        for col, row in enumerate(new_solution):
            if col < self.BOARD_SIZE:
                current_board[col] = row

        prev_board = [-1] * self.BOARD_SIZE
        for col, row in enumerate(self.previous_solution):
            if col < self.BOARD_SIZE:
                prev_board[col] = row
        
        # Find differences and update only those positions
        for col in range(self.BOARD_SIZE):
            prev_row = prev_board[col]
            curr_row = current_board[col]
            
            # Remove queen from old position if it changed
            if prev_row != -1 and (prev_row != curr_row or curr_row == -1):
                if self.queen_widgets[prev_row][col]:
                    self.queen_widgets[prev_row][col].destroy()
                    self.queen_widgets[prev_row][col] = None
            
            # Add queen to new position
            if curr_row != -1 and curr_row != prev_row:
                queen_color = "#8B0000" if algorithm == "Backtracking" else "#006400"  # Dark red vs dark green
                
                # Highlight the active column
                if active_col is not None and col == active_col:
                    queen_color = self.HIGHLIGHT_COLOR
                
                square = self.board_squares[curr_row][col]
                
                # If there's already a queen at this position (shouldn't happen), remove it first
                if self.queen_widgets[curr_row][col]:
                    self.queen_widgets[curr_row][col].destroy()
                
                queen_label = tk.Label(
                    square,
                    text="♛",
                    font=font.Font(family="Arial", size=30),
                    fg=queen_color,
                    bg=square.cget('bg')
                )
                queen_label.place(relx=0.5, rely=0.5, anchor='center')
                self.queen_widgets[curr_row][col] = queen_label
        
        # Update any existing queens that need color change (e.g., when active column changes)
        for col in range(self.BOARD_SIZE):
            row = current_board[col]
            if row != -1 and self.queen_widgets[row][col]:
                queen_color = "#8B0000" if algorithm == "Backtracking" else "#006400"
                if active_col is not None and col == active_col:
                    queen_color = self.HIGHLIGHT_COLOR
                
                # Only update color if needed
                current_color = self.queen_widgets[row][col].cget('fg')
                if current_color != queen_color:
                    self.queen_widgets[row][col].config(fg=queen_color)
        
        # Save the current solution for the next update
        self.previous_solution = new_solution.copy()
    
    def solve_with_backtracking(self):
        start_time = time.time()
        self.backtracking_solution = [0] * self.BOARD_SIZE
        self.backtracking_steps = 0
        
        solved = self.solve_backtracking(0)
        duration = int((time.time() - start_time) * 1000)
        
        if solved:
            status_text = f"Backtracking: {self.backtracking_steps} steps in {duration} ms"
            self.update_status(status_text)
            self.update_queen_positions(self.backtracking_solution, "Backtracking")
        else:
            self.update_status("Backtracking failed (should never happen)")
        
        self.end_processing()
    
    def solve_backtracking(self, col):
        self.backtracking_steps += 1
        self.update_step_counter(self.backtracking_steps)
        
        if col >= self.BOARD_SIZE:
            return True

        for row in range(self.BOARD_SIZE):
            if self.is_safe(row, col, self.backtracking_solution):
                self.backtracking_solution[col] = row
                
                # Update UI with current solution (thread-safe)
                partial_solution = self.backtracking_solution[:col+1]  # Only include filled columns
                self.update_queen_positions(partial_solution, "Backtracking", col)
                
                time.sleep(self.animation_speed)  # Dynamic delay for visualization
                
                if self.solve_backtracking(col + 1):
                    return True
                
                # Backtrack - visualize this by updating the active column
                self.backtracking_solution[col] = 0
                partial_solution = self.backtracking_solution[:col]  # Remove this column's queen
                self.update_queen_positions(partial_solution, "Backtracking", col)
                time.sleep(self.animation_speed * 0.5)  # Shorter delay for backtracking
        
        return False
    
    def solve_with_constrained(self):
        start_time = time.time()
        self.constrained_attempts += 1
        self.update_attempts_counter(self.constrained_attempts)
        
        solution = self.constrained_las_vegas()
        duration = int((time.time() - start_time) * 1000)
        
        if solution:
            status_text = f"Las Vegas: Solved in {self.constrained_attempts} attempts ({duration} ms)"
            self.update_status(status_text)
            self.constrained_solution = solution
            self.update_queen_positions(self.constrained_solution, "Las Vegas")
            self.end_processing()
        else:
            status_text = f"Las Vegas: Failed attempt {self.constrained_attempts}, retrying..."
            self.update_status(status_text)
            self.root.after(100, self.solve_with_constrained)
    
    def is_safe(self, row, col, solution):
        for i in range(col):
            if solution[i] == row or abs(solution[i] - row) == abs(i - col):
                return False
        return True
    
    def constrained_las_vegas(self):
        queens = []  # Start with empty list to only show queens as they're placed
        steps = 0
        
        for col in range(self.BOARD_SIZE):
            steps += 1
            self.update_step_counter(steps)
            
            # Create a temporary list with the correct length for safe_rows check
            temp_queens = queens + [0] * (self.BOARD_SIZE - len(queens))
            safe_rows = self.get_safe_rows(col, temp_queens)
            
            if not safe_rows:
                return None
            
            row = random.choice(safe_rows)
            queens.append(row)
            
            # Update UI (thread-safe)
            self.update_queen_positions(queens, "Las Vegas", col)
            
            time.sleep(self.animation_speed)  # Dynamic delay for visualization
        
        return queens
    
    def get_safe_rows(self, col, queens):
        safe_rows = []
        for row in range(self.BOARD_SIZE):
            safe = True
            for i in range(col):
                if queens[i] == row or abs(queens[i] - row) == abs(i - col):
                    safe = False
                    break
            if safe:
                safe_rows.append(row)
        return safe_rows

if __name__ == "__main__":
    root = tk.Tk()
    app = EightQueens(root)
    root.mainloop()