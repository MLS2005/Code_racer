"""
Code Racer - A racing-themed code reading quiz game
Enhanced version with better UI, timing system, and expanded question bank
"""

from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Static, Input, Button, Label
from textual.containers import Container, Vertical, Horizontal, Center, ScrollableContainer
from textual.binding import Binding
from textual.screen import Screen
from textual import events
import random
import time


# Expanded code challenges organized by difficulty
CODE_CHALLENGES = {
    "beginner": [
        {
            "code": '''total = 0
for i in range(5):
    total += i
print(total)''',
            "questions": [
                {"question": "Where is total initialized?", "answer": 1},
                {"question": "Which line starts the loop?", "answer": 2},
                {"question": "Where does the addition happen?", "answer": 3},
                {"question": "Which line outputs the result?", "answer": 4},
            ]
        },
        {
            "code": '''name = "Python"
length = len(name)
print(length)''',
            "questions": [
                {"question": "Where is the variable 'name' created?", "answer": 1},
                {"question": "Which line calculates the length?", "answer": 2},
                {"question": "Where is the output statement?", "answer": 3},
            ]
        },
        {
            "code": '''x = 10
y = 20
result = x + y
print(result)''',
            "questions": [
                {"question": "Where is x assigned?", "answer": 1},
                {"question": "Which line adds x and y?", "answer": 3},
                {"question": "Where is y defined?", "answer": 2},
            ]
        },
        {
            "code": '''numbers = [1, 2, 3, 4, 5]
first = numbers[0]
last = numbers[-1]
print(first, last)''',
            "questions": [
                {"question": "Where is the list created?", "answer": 1},
                {"question": "Which line gets the first element?", "answer": 2},
                {"question": "Where is the last element accessed?", "answer": 3},
            ]
        },
        {
            "code": '''age = 25
if age >= 18:
    print("Adult")
else:
    print("Minor")''',
            "questions": [
                {"question": "Where is the condition check?", "answer": 2},
                {"question": "Which line prints 'Adult'?", "answer": 3},
                {"question": "Where is the else clause?", "answer": 4},
            ]
        },
    ],
    "intermediate": [
        {
            "code": '''lower_str = ""
for letter in my_str:
    if "A" <= letter <= "Z":
        lower_str += chr(ord(letter) + 32)
    else:
        lower_str += letter
return lower_str''',
            "questions": [
                {"question": "Where does the loop start?", "answer": 2},
                {"question": "Which line initializes the empty string?", "answer": 1},
                {"question": "Where is the uppercase check condition?", "answer": 3},
                {"question": "Which line converts uppercase to lowercase?", "answer": 4},
                {"question": "Where is the result returned?", "answer": 7},
            ]
        },
        {
            "code": '''total = 0
for num in numbers:
    if num % 2 == 0:
        total += num
return total''',
            "questions": [
                {"question": "Where is the total initialized?", "answer": 1},
                {"question": "Which line checks if a number is even?", "answer": 3},
                {"question": "Where does the loop begin?", "answer": 2},
                {"question": "Which line adds to the total?", "answer": 4},
                {"question": "Where is the result returned?", "answer": 5},
            ]
        },
        {
            "code": '''def find_max(lst):
    max_val = lst[0]
    for num in lst:
        if num > max_val:
            max_val = num
    return max_val''',
            "questions": [
                {"question": "Where is the function defined?", "answer": 1},
                {"question": "Which line initializes max_val?", "answer": 2},
                {"question": "Where is the comparison?", "answer": 4},
                {"question": "Which line updates max_val?", "answer": 5},
            ]
        },
        {
            "code": '''words = ["hello", "world", "python"]
result = []
for word in words:
    result.append(word.upper())
print(result)''',
            "questions": [
                {"question": "Where is the result list initialized?", "answer": 2},
                {"question": "Which line converts to uppercase?", "answer": 4},
                {"question": "Where does the loop start?", "answer": 3},
                {"question": "Which line prints the output?", "answer": 5},
            ]
        },
        {
            "code": '''count = 0
while count < 10:
    if count % 3 == 0:
        print(count)
    count += 1''',
            "questions": [
                {"question": "Where is the while loop condition?", "answer": 2},
                {"question": "Which line checks divisibility by 3?", "answer": 3},
                {"question": "Where is count incremented?", "answer": 5},
                {"question": "Which line prints the count?", "answer": 4},
            ]
        },
    ],
    "advanced": [
        {
            "code": '''result = []
for i in range(len(data)):
    if data[i] > 0:
        result.append(data[i] * 2)
    else:
        result.append(0)
return result''',
            "questions": [
                {"question": "Where is the result list created?", "answer": 1},
                {"question": "Which line checks if a value is positive?", "answer": 3},
                {"question": "Where does the multiplication happen?", "answer": 4},
                {"question": "Which line appends zero for negative values?", "answer": 6},
                {"question": "Where is the result returned?", "answer": 7},
            ]
        },
        {
            "code": '''def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

result = fibonacci(5)''',
            "questions": [
                {"question": "Where does the function definition start?", "answer": 1},
                {"question": "Which line contains the base case check?", "answer": 2},
                {"question": "Where is the recursive call?", "answer": 4},
                {"question": "Which line calls the function?", "answer": 6},
                {"question": "Where is the base case return?", "answer": 3},
            ]
        },
        {
            "code": '''matrix = [[1, 2], [3, 4], [5, 6]]
flat = []
for row in matrix:
    for item in row:
        flat.append(item)
print(flat)''',
            "questions": [
                {"question": "Where is the matrix defined?", "answer": 1},
                {"question": "Which line starts the outer loop?", "answer": 3},
                {"question": "Where is the inner loop?", "answer": 4},
                {"question": "Which line appends to flat?", "answer": 5},
            ]
        },
        {
            "code": '''def quick_sort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quick_sort(left) + middle + quick_sort(right)''',
            "questions": [
                {"question": "Where is the base case?", "answer": 2},
                {"question": "Which line selects the pivot?", "answer": 4},
                {"question": "Where is the left partition created?", "answer": 5},
                {"question": "Which line contains the recursive calls?", "answer": 8},
                {"question": "Where is the right partition?", "answer": 7},
            ]
        },
        {
            "code": '''class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

head = Node(1)
head.next = Node(2)''',
            "questions": [
                {"question": "Where is the class defined?", "answer": 1},
                {"question": "Which line initializes the data attribute?", "answer": 3},
                {"question": "Where is the next pointer set to None?", "answer": 4},
                {"question": "Which line creates the first node?", "answer": 6},
                {"question": "Where is the second node linked?", "answer": 7},
            ]
        },
    ]
}


class CodeDisplay(Static):
    """Widget to display code with line numbers and syntax highlighting"""
    
    CSS = """
    CodeDisplay {
        background: #1e1e1e;
        color: #d4d4d4;
        border: heavy #00ff00;
        padding: 1 2;
        height: auto;
    }
    """
    
    def __init__(self, code: str, **kwargs):
        self.code_lines = code.split('\n')
        super().__init__(**kwargs)
    
    def render(self) -> str:
        lines = []
        for i, line in enumerate(self.code_lines, 1):
            lines.append(f"[cyan]{i:2d}[/cyan] │ [white]{line}[/white]")
        return "\n".join(lines)


class RaceProgress(Static):
    """Display race progress with enhanced visuals"""
    
    CSS = """
    RaceProgress {
        background: $panel;
        border: solid #ffa500;
        padding: 1 2;
        height: auto;
    }
    """
    
    def __init__(self, total_questions: int, **kwargs):
        self.total = total_questions
        self.current = 0
        super().__init__(**kwargs)
    
    def update_progress(self, current: int):
        self.current = current
        self.refresh()
    
    def render(self) -> str:
        percentage = int((self.current / self.total) * 100) if self.total > 0 else 0
        filled = int(percentage / 5)
        bar = "[green]" + "█" * filled + "[/green][dim]" + "░" * (20 - filled) + "[/dim]"
        
        car_position = min(filled, 19)
        track = list("─" * 20)
        track[car_position] = "🏎️"
        track_display = "".join(track)
        
        return f"""[bold yellow]🏁 RACE PROGRESS[/bold yellow]
{bar} [bold]{percentage}%[/bold]
{track_display}
[bold cyan]Checkpoint:[/bold cyan] {self.current}/{self.total}"""


class Timer(Static):
    """Display race timer"""
    
    CSS = """
    Timer {
        background: $panel;
        border: solid #ff1493;
        padding: 1 2;
        height: auto;
        text-align: center;
    }
    """
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.start_time = time.time()
        self.timer_active = True
    
    def on_mount(self) -> None:
        """Start the timer when mounted"""
        self.update_timer()
    
    def update_timer(self) -> None:
        """Update the timer display"""
        if self.timer_active:
            elapsed = time.time() - self.start_time
            minutes = int(elapsed // 60)
            seconds = int(elapsed % 60)
            self.update(f"[bold magenta]⏱️  TIME: {minutes:02d}:{seconds:02d}[/bold magenta]")
            self.set_timer(0.1, self.update_timer)
    
    def stop(self) -> float:
        """Stop the timer and return elapsed time"""
        self.timer_active = False
        return time.time() - self.start_time


class HomeScreen(Screen):
    """Home screen with difficulty selection"""
    
    CSS = """
    HomeScreen {
        align: center middle;
        background: $surface;
    }
    
    #home-container {
        width: 70;
        height: auto;
        border: heavy #00ff00;
        background: $panel;
        padding: 3;
    }
    
    #title-art {
        text-align: center;
        padding: 1;
        color: #00ff00;
    }
    
    #subtitle {
        text-align: center;
        color: #ffa500;
        padding: 1;
        text-style: bold;
    }
    
    .difficulty-btn {
        width: 100%;
        height: 3;
        margin: 1;
    }
    
    #instructions {
        text-align: center;
        color: $text-muted;
        padding: 2;
        margin-top: 1;
    }
    
    #features {
        text-align: center;
        color: #00ffff;
        padding: 1;
    }
    """
    
    def compose(self) -> ComposeResult:
        with Center():
            with Vertical(id="home-container"):
                yield Static("""[bold green]
    ╔═══════════════════════════════════════╗
    ║                                       ║
   ║     🏁   C O D E   R A C E R   🏁     ║
    ║                                       ║
   ║           🏎️ ═══════════ 💨            ║
    ║                                       ║
    ╚═══════════════════════════════════════╝
[/bold green]""", id="title-art")
                
                yield Static("[bold]Master the Art of Code Reading![/bold]", id="subtitle")
                
                yield Static("""[dim]✨ Start your Engines! ✨
  
                             Get ready to test your code reading skills![/dim]""", id="features")
                
                yield Button("🟢 BEGINNER RACE - Easy Warm-Up", id="beginner", classes="difficulty-btn", variant="success")
                yield Button("🟡 INTERMEDIATE RACE - Challenge Mode", id="intermediate", classes="difficulty-btn", variant="warning")
                yield Button("🔴 ADVANCED RACE - Expert Level", id="advanced", classes="difficulty-btn", variant="error")
                
                yield Static("[dim italic]Choose your difficulty and start your engines! 🏁[/dim italic]", id="instructions")
    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle difficulty selection"""
        difficulty = event.button.id
        self.app.start_race(difficulty)


class GameScreen(Screen):
    """Main game screen with enhanced UI"""
    
    CSS = """
    GameScreen {
        background: $surface;
    }
    
    #game-header {
        dock: top;
        height: 3;
        background: #00ff00;
        color: black;
        content-align: center middle;
        text-style: bold;
    }
    
    #stats-container {
        dock: top;
        height: auto;
        layout: horizontal;
    }
    
    #code-container {
        height: auto;
        margin: 1;
    }
    
    #question-container {
        height: auto;
        border: heavy #ffa500;
        background: $panel;
        padding: 1 2;
        margin: 1;
    }
    
    #question-text {
        color: #ffa500;
        text-style: bold;
        padding: 1;
    }
    
    #input-container {
        height: auto;
        layout: horizontal;
        align: center middle;
        padding: 1;
    }
    
    #feedback {
        dock: bottom;
        height: 3;
        content-align: center middle;
        text-align: center;
        text-style: bold;
    }
    
    .success {
        background: #00ff00;
        color: black;
    }
    
    .error {
        background: #ff0000;
        color: white;
    }
    
    Input {
        width: 25;
        margin-right: 1;
    }
    
    Button {
        width: 20;
    }
    """
    
    BINDINGS = [
        Binding("escape", "back_home", "Back to Menu"),
    ]
    
    def __init__(self, difficulty: str):
        super().__init__()
        self.difficulty = difficulty
        self.current_question_idx = 0
        self.score = 0
        self.current_attempts = 0  # Local: attempts on current question
        self.max_attempts = 2  # Maximum attempts per question
        self.wrong_attempt = False # Decides to give point for question or not
        self.load_challenge()
    
    def load_challenge(self):
        """Load a random challenge for the selected difficulty"""
        self.wrong_attemps = 0
        self.challenge = random.choice(CODE_CHALLENGES[self.difficulty])
        self.total_questions = len(self.challenge["questions"])
    
    def compose(self) -> ComposeResult:
        difficulty_emoji = {"beginner": "🟢", "intermediate": "🟡", "advanced": "🔴"}
        yield Static(f"{difficulty_emoji[self.difficulty]} CODE RACER - {self.difficulty.upper()} MODE", id="game-header")
        
        with Container(id="stats-container"):
            yield Timer(id="timer")
            yield RaceProgress(self.total_questions, id="progress")
        
        with Container(id="code-container"):
            yield CodeDisplay(self.challenge["code"], id="code-display")
        
        with Container(id="question-container"):
            yield Static(self.get_current_question(), id="question-text")
            with Container(id="input-container"):
                yield Input(placeholder="Line number", id="answer-input")
                yield Button("🏁 SUBMIT", id="submit-btn", variant="primary")
        
        yield Static("", id="feedback")
    
    def get_current_question(self) -> str:
        if self.current_question_idx < len(self.challenge["questions"]):
            q = self.challenge["questions"][self.current_question_idx]
            return f"[bold]QUESTION {self.current_question_idx + 1}/{self.total_questions}[/bold]\n\n{q['question']}"
        return "🏁 Race Complete!"
    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button press"""
        if event.button.id == "submit-btn":
            self.check_answer()
    
    def on_input_submitted(self, event: Input.Submitted) -> None:
        """Handle enter key in input"""
        self.check_answer()
    
    def action_back_home(self) -> None:
        """Return to home screen"""
        self.app.pop_screen()
    
    def check_answer(self):
        """Check if the answer is correct"""
        input_widget = self.query_one("#answer-input", Input)
        feedback_widget = self.query_one("#feedback", Static)
        
        try:
            user_answer = int(input_widget.value.strip())
        except ValueError:
            feedback_widget.update("⚠️  Please enter a valid line number!")
            feedback_widget.remove_class("success", "error")
            return
        
        correct_answer = self.challenge["questions"][self.current_question_idx]["answer"]
        
        if user_answer == correct_answer:
            if self.wrong_attempt:
                self.wrong_attempt = False
            else:
                self.score += 1
            feedback_widget.update("✅ CORRECT! Checkpoint Passed! 🏁")
            feedback_widget.remove_class("error")
            feedback_widget.add_class("success")
            
            # Move to next question
            self.current_question_idx += 1
            progress = self.query_one("#progress", RaceProgress)
            progress.update_progress(self.current_question_idx)
            
            if self.current_question_idx < len(self.challenge["questions"]):
                question_widget = self.query_one("#question-text", Static)
                question_widget.update(self.get_current_question())
                input_widget.value = ""
                input_widget.focus()
            else:
                self.show_results()
        else:
            feedback_widget.update(f"❌ PIT STOP! Correct answer: Line {correct_answer}")
            feedback_widget.remove_class("success")
            feedback_widget.add_class("error")
            input_widget.value = ""
            self.wrong_attempt = True
            
    
    def show_results(self):
        """Show final results with combined speed and accuracy score"""
        timer = self.query_one("#timer", Timer)
        elapsed_time = timer.stop()
        
        question_widget = self.query_one("#question-text", Static)
        input_widget = self.query_one("#answer-input", Input)
        submit_btn = self.query_one("#submit-btn", Button)
        feedback_widget = self.query_one("#feedback", Static)
        
        # Calculate accuracy score (0-100)
        # Max possible score if all correct on first try
        max_possible_score = self.total_questions
        # Actual score (can be fractional due to half points)
        
        accuracy_score = int(((self.score)/ max_possible_score) * 100)
        
        # Calculate speed score based on time (0-100)
        # Target times by difficulty: beginner=60s, intermediate=90s, advanced=120s
        target_times = {"beginner": 10 ,"intermediate": 10, "advanced": 120}
        target_time = target_times[self.difficulty]
        
        # Speed score: 100 if under target, decreases as time increases
        if elapsed_time <= target_time:
            speed_score = 100
        else:
            # Lose 2 points per second over target (minimum 0)
            speed_score = max(0, 100 - int((elapsed_time - target_time) * 2))
        
        # Combined score: 60% accuracy, 40% speed
        final_score = int((accuracy_score * 0.6) + (speed_score * 0.4))
        
        minutes = int(elapsed_time // 60)
        seconds = int(elapsed_time % 60)
        
        result_text = f"""[bold yellow]🏁 RACE FINISHED! 🏁[/bold yellow]

[bold cyan]Difficulty:[/bold cyan] {self.difficulty.upper()}
[bold cyan]Points Earned:[/bold cyan] {self.score}/{self.total_questions}
[bold magenta]Race Time:[/bold magenta] {minutes:02d}:{seconds:02d}

[bold white]━━━━━━━━━━ RACE SCORES ━━━━━━━━━━[/bold white]
[bold cyan]📊 Accuracy Score:[/bold cyan] {accuracy_score}/100
[bold magenta]⚡ Speed Score:[/bold magenta] {speed_score}/100
[bold yellow]🏆 FINAL SCORE:[/bold yellow] [bold green]{final_score}/100[/bold green]

"""
        # Performance rating based on final score
        if final_score >= 90:
            result_text += "[bold green]🥇 LEGENDARY! You're a Code Racing Master![/bold green]"
            rating = "S-RANK"
        elif final_score >= 80:
            result_text += "[bold yellow]🥈 EXCELLENT! Outstanding Performance![/bold yellow]"
            rating = "A-RANK"
        elif final_score >= 70:
            result_text += "[bold]🥉 GREAT JOB! Strong Racing Skills![/bold]"
            rating = "B-RANK"
        elif final_score >= 60:
            result_text += "[bold cyan]💪 GOOD EFFORT! You're Improving![/bold cyan]"
            rating = "C-RANK"
        else:
            result_text += "[bold red]🔧 KEEP PRACTICING! Speed up and focus![/bold red]"
            rating = "D-RANK"
        
        result_text += f"\n[bold white]Performance Rank:[/bold white] [bold]{rating}[/bold]"
        result_text += "\n\n[dim]Press ESC to return to menu[/dim]"
        
        question_widget.update(result_text)
        input_widget.display = False
        submit_btn.display = False
        feedback_widget.update("")


class CodeRacerApp(App):
    """Main application"""
    
    TITLE = "Code Racer"
    CSS = """
    Screen {
        background: #0a0a0a;
    }
    """
    
    BINDINGS = [
        Binding("q", "quit", "Quit"),
    ]
    
    def on_mount(self) -> None:
        """Show home screen on start"""
        self.push_screen(HomeScreen())
    
    def start_race(self, difficulty: str) -> None:
        """Start a race with the selected difficulty"""
        self.push_screen(GameScreen(difficulty))


def main():
    app = CodeRacerApp()
    app.run()


if __name__ == "__main__":
    main()